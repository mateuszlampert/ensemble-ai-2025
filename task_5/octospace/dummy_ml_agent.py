import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np
from collections import deque
import datetime


class DQN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, output_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)


class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)

    def add(self, experience):
        self.buffer.append(experience)

    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)

    def size(self):
        return len(self.buffer)


class Ship:
    def __init__(self, q_network, target_network, optimizer, replay_buffer):
        self.state_dim = 2
        self.action_dim = 4
        self.epsilon = 0.1  # Exploration factor
        self.gamma = 0.99  # Discount factor
        self.lr = 1e-3  # Learning rate
        self.batch_size = 64

        self.q_network = q_network
        self.target_network = target_network
        self.optimizer = optimizer
        self.replay_buffer = replay_buffer

    def predict_action(self, state):
        """
        Predict action based on current state.
        You should implement your logic here to decide the best action.
        This is typically the epsilon-greedy policy.
        """
        if random.random() < self.epsilon:
            # Exploration: Choose a random action
            return random.randint(0, self.action_dim - 1)
        else:
            # Exploitation: Choose the best action based on the current Q-values
            with torch.no_grad():
                state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
                q_values = self.q_network(state_tensor)
                return torch.argmax(q_values, dim=1).item()

    def update(self):
        """
        Perform one update of the Q-network based on experiences in the buffer.
        """
        if self.replay_buffer.size() < self.batch_size:
            return  # Not enough samples to update

        # Sample a batch from the replay buffer
        batch = self.replay_buffer.sample(self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        # Convert batch to tensors
        states = torch.tensor(states, dtype=torch.float32)
        actions = torch.tensor(actions, dtype=torch.long)
        rewards = torch.tensor(rewards, dtype=torch.float32)
        next_states = torch.tensor(next_states, dtype=torch.float32)
        dones = torch.tensor(dones, dtype=torch.float32)

        # Compute Q-values for the current states
        q_values = self.q_network(states)
        q_values = q_values.gather(1, actions.unsqueeze(1))

        # Compute target Q-values for the next states using the target network
        with torch.no_grad():
            next_q_values = self.target_network(next_states)
            next_q_values_max = next_q_values.max(1)[0]
            target_q_values = rewards + self.gamma * next_q_values_max * (1 - dones)

        # Compute loss (MSE)
        print(q_values.size(), q_values.squeeze(1).size(), target_q_values.size())
        loss = nn.MSELoss()(q_values.squeeze(1), target_q_values)

        # Perform backpropagation
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def add_to_buffer(self, state, action, reward, next_state, done):
        self.replay_buffer.add((state, action, reward, next_state, done))

    def train(self, state, action, reward, next_state, done):
        """
        After taking an action, add the experience to the replay buffer
        and periodically update the Q-network.
        """
        # Add experience to the replay buffer
        self.replay_buffer.add((state, action, reward, next_state, done))

        # Update the Q-network
        self.update()

    def update_target_network(self):
        """
        Update the target network with the current Q-network weights.
        This is done periodically to stabilize learning.
        """
        self.target_network.load_state_dict(self.q_network.state_dict())


def state_from_obs(ship_data: tuple):
    id, x, y, *_ = ship_data
    return x, y


def action_from_actions(action):
    return action[2]


class Agent:
    def __init__(self, side: int):
        """
        :param side: Indicates whether the player is on left side (0) or right side (1)
        """
        self.side = side

    def get_action(self, obs: dict, info: dict = None) -> dict:
        ship = Ship(
            self.q_network, self.target_network, self.optimizer, self.replay_buffer
        )

        if info:
            is_win = info["reward"] == 1
            is_lose = info["reward"] == -1
            is_draw = info["terminated"]
            reward = 100 if is_win else -100 if is_lose else -20

            is_end = is_win or is_lose or is_draw

            prev_actions = info["actions"]
            prev_obs = info["prev_obs"]

            for id, x, y, *_ in obs["allied_ships"]:
                if any(map(lambda x: x[0] == id, prev_obs["allied_ships"])):
                    ship.train(
                        state_from_obs(
                            list(
                                filter(lambda x: x[0] == id, prev_obs["allied_ships"])
                            )[0]
                        ),
                        action_from_actions(
                            list(filter(lambda x: x[0] == id, prev_actions["ships_actions"]))[0]
                        ),
                        reward,
                        state_from_obs(
                            list(filter(lambda x: x[0] == id, obs["allied_ships"]))[0]
                        ),
                        is_end,
                    )
            
            if random.random() < 0.001: 
                self.save_model(f"agents/{datetime.datetime.now().hour}_{datetime.datetime.now().minute}.pth")

            # next_state = np.random.rand(agent.state_dim)  # Replace with actual environment logic
            # reward = np.random.random()  # Replace with actual game logic for reward
            # done = np.random.choice([True, False])  # Replace with actual game condition

            # Train the agent with the received feedback

            # total_reward += reward

            # Periodically update target network
            # if random.random() < 0.1: ship.update_target_network()

        ship = Ship(
            self.q_network, self.target_network, self.optimizer, self.replay_buffer
        )

        ships_actions = []

        for id, x, y, *_ in obs["allied_ships"]:
            direction = ship.predict_action([x, y])
            ships_actions.append([id, 0, direction, 1])

        if random.random() < 0.1:
            ship.update_target_network()

        return {"ships_actions": ships_actions, "construction": 1}

    def load(self, abs_path: str):
        """
        Function for loading all necessary weights for the agent. The abs_path is a path pointing to the directory,
        where the weights for the agent are stored, so remember to join it to any path while loading.

        :param abs_path:
        :return:
        """
        filename = "agents/1_15.pth"

        self.state_dim = 2
        self.action_dim = 4
        self.epsilon = 0.1  # Exploration factor
        self.gamma = 0.99  # Discount factor
        self.lr = 1e-3  # Learning rate
        self.batch_size = 64
        self.buffer_size = 10000

        self.q_network = DQN(self.state_dim, self.action_dim)
        self.q_network.load_state_dict(torch.load(filename))
        print(f"Model loaded from {filename}")
        self.target_network = DQN(self.state_dim, self.action_dim)
        self.target_network.load_state_dict(self.q_network.state_dict())

        # Optimizer
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=self.lr)

        # Replay buffer
        self.replay_buffer = ReplayBuffer(self.buffer_size)

    def eval(self):
        """
        With this function you should switch the agent to inference mode.

        :return:
        """
        self.q_network.eval()

    def to(self, device):
        """
        This function allows you to move the agent to a GPU. Please keep that in mind,
        because it can significantly speed up the computations and let you meet the time requirements.

        :param device:
        :return:
        """
        self.q_network.to(device)
    
    def save_model(self, filename="dqn_model.pth"):
        torch.save(self.q_network.state_dict(), filename)
        print(f"Model saved to {filename}")
    
    def load_model(self, filename="dqn_model.pth"):
        self.q_network.load_state_dict(torch.load(filename))
        print(f"Model loaded from {filename}")