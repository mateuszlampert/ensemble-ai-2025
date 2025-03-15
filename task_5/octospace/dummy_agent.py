# Skeleton for Agent class

import random

class Ship:
    def __init__(self, ship_id: int):
        self.ship_id = ship_id

    def get_self_ship(self, obs: dict):
        return next((ship for ship in obs["allied_ships"] if ship[0] == self.ship_id), None)

    def get_allied_ships(self, obs: dict):
        allied_ships = obs["allied_ships"]
        return list(filter(lambda ship: ship[0] != self.ship_id, allied_ships))
    
    def get_enemy_ships(self, obs: dict):
        enemy_ships = obs["enemy_ships"]
        return enemy_ships
    
    def get_nearest_allied_ship(self, obs: dict):
        allied_ships = self.get_allied_ships(obs)
        return self.get_nearest_ship_from_collection(obs, allied_ships)
    
    def get_nearest_enemy_ship(self, obs: dict):
        enemy_ships = self.get_enemy_ships(self, obs)
        return self.get_nearest_ship_from_collection(enemy_ships)
    
    def get_nearest_ship_from_collection(self, obs: dict, ships: list):
        self_ship = self.get_self_ship(obs)
        return min(ships, key=lambda ship: self.get_distance((self_ship[1], self_ship[2]), (ship[1], ship[2])), default=None)

    def get_distance(self, coords_1, coords_2):
        x_1, y_1 = coords_1
        x_2, y_2 = coords_2

        return (x_2 - x_1) ** 2 - (y_2 - y_1) ** 2

    def get_ship_coords(self, obs: dict):
        ship = self.get_self_ship(obs)
        return (ship[1], ship[2])
    
    def get_self_ship_health(self, obs: dict):
        ship = self.get_self_ship(obs)
        return ship["health"]
    
    def get_allied_ships_count(self, obs: dict):
        allied_ships = self.get_allied_ships(obs)
        return len(allied_ships)

    def get_enemy_ships_count(self, obs: dict):
        enemy_ships = self.get_enemy_ships(obs)
        return len(enemy_ships)
    
    def get_planets(self, obs: dict):
        return obs["planets_occupation"]
    
    def get_unoccupied_planets(self, obs: dict):
        planets = self.get_planets(obs)
        return list(filter(lambda planet: planet["occupation_progress"] == -1, planets))
    
    def get_allied_planets(self, obs: dict):
        planets = self.get_planets(obs)
        return list(filter(lambda planet: planet["occupation_progress"] < 50, planets))

    def get_enemy_planets(self, obs: dict):
        planets = self.get_planets(obs)
        return list(filter(lambda planet: planet["occupation_progress"] >= 50, planets))
    
    def get_allied_planets_count(self, obs: dict):
        allied_planets = self.get_allied_planets(obs)
        return len(allied_planets)

    def get_enemy_planets_count(self, obs: dict):
        enemy_planets = self.get_enemy_planets(obs)
        return len(enemy_planets)

    def get_nearest_planet_from_collection(self, obs: dict, planets: list):
        self_ship = self.get_self_ship(obs)
        return min(planets, key=lambda planet: self.get_distance((self_ship[1], self_ship[2]), (planet[0], planet[1])), default=None)

    def get_nearest_unoccupied_planet(self, obs: dict):
        unoccupied_planets = self.get_unoccupied_planets(obs)
        return self.get_nearest_ship_from_collection(obs, unoccupied_planets)

    def get_nearest_allied_planet(self, obs: dict):
        allied_planets = self.get_allied_planets(obs)
        return self.get_nearest_planet_from_collection(obs, allied_planets)

    def get_nearest_enemy_planet(self, obs: dict):
        enemy_planets = self.get_enemy_planets(obs)
        return self.get_nearest_planet_from_collection(obs, enemy_planets)

class Agent:
    def __init__(self, side: int):
        """
        :param side: Indicates whether the player is on left side (0) or right side (1)
        """
        self.side = side

    def get_action(self, obs: dict) -> dict:
        """
        Main function, which gets called during step() of the environment.

        Observation space:
            map: whole grid of board_size, which already has applied visibility mask on it
            allied_ships: an array of all currently available ships for the player. The ships are represented as a list:
                (ship id, position x, y, current health points, firing_cooldown, move_cooldown)
                - ship id: int [0, 1000]
                - position x: int [0, 100]
                - position y: int [0, 100]
                - health points: int [1, 100]
                - firing_cooldown: int [0, 10]
                - move_cooldown: int [0, 3]
            enemy_ships: same, but for the opposing player ships
            planets_occupation: for each visible planet, it shows the occupation progress:
                - planet_x: int [0, 100]
                - planet_y: int [0, 100]
                - occupation_progress: int [-1, 100]:
                    -1: planet is unoccupied
                    0: planet occupied by the 1st player
                    100: planet occupied by the 2nd player
                    Values between indicate an ongoing conflict for the ownership of the planet
            resources: current resources available for building

        Action space:
            ships_actions: player can provide an action to be executed by every of his ships.
                The command looks as follows:
                - ship_id: int [0, 1000]
                - action_type: int [0, 1]
                    0 - move
                    1 - fire
                - direction: int [0, 3] - direction of movement or firing
                    0 - right
                    1 - down
                    2 - left
                    3 - up
                - speed (not applicable when firing): int [0, 3] - a number of fields to move
            construction: int [0, 10] - a number of ships to be constructed

        :param obs:
        :return:
        """

        return {
            "ships_actions": [[ship[0], 0, 0, 3] for i, ship in enumerate(obs["allied_ships"])],
            "construction": 1
        }

    def load(self, abs_path: str):
        """
        Function for loading all necessary weights for the agent. The abs_path is a path pointing to the directory,
        where the weights for the agent are stored, so remember to join it to any path while loading.

        :param abs_path:
        :return:
        """
        pass

    def eval(self):
        """
        With this function you should switch the agent to inference mode.

        :return:
        """
        pass

    def to(self, device):
        """
        This function allows you to move the agent to a GPU. Please keep that in mind,
        because it can significantly speed up the computations and let you meet the time requirements.

        :param device:
        :return:
        """
        pass