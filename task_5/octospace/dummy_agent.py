from typing import Tuple
class Ship:
    def __init__(self, ship_id: int, side: int, self_base_coords: Tuple[int, int], enemy_base_coords: Tuple[int, int]):
        self.ship_id = ship_id
        self.side = side
        self.self_base_coords = self_base_coords
        self.enemy_base_coords = enemy_base_coords

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

    def get_self_ship_coords(self, obs: dict):
        ship = self.get_self_ship(obs)
        return (ship[1], ship[2])
    
    def get_self_ship_health(self, obs: dict):
        ship = self.get_self_ship(obs)
        return ship[4]
    
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
        return list(filter(lambda planet: planet[2] == -1, planets))
    
    def get_allied_planets(self, obs: dict):
        if self.side == 0:
            return self.get_player_1_planets(obs)
        return self.get_player_2_planets(obs)

    def get_enemy_planets(self, obs: dict):
        if self.side == 0:
            return self.get_player_2_planets(obs)
        return self.get_player_1_planets(obs)
    
    def get_player_1_planets(self, obs: dict):
        planets = self.get_planets(obs)
        return list(filter(lambda planet: planet[2] < 50, planets))
    
    def get_player_2_planets(self, obs: dict):
        planets = self.get_planets(obs)
        return list(filter(lambda planet: planet[2] >= 50, planets))
    
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
    
    def is_enemy_in_range(self, obs: dict, distance: int = 8):
        x_self, y_self = self.get_self_ship_coords(obs)
        enemy_ships = self.get_enemy_ships(obs)

        result = [0, 0, 0, 0]  # [N, S, W, E]

        for enemy in enemy_ships:
            x, y = enemy[1], enemy[2]

            if x_self == x and 0 < y_self - y <= distance:
                result[0] = 1
            if x_self == x and 0 < y - y_self <= distance:
                result[1] = 1
            if y_self == y and 0 < x_self - x <= distance:
                result[2] = 1
            if y_self == y and 0 < x - x_self <= distance:
                result[3] = 1

            if all(result):
                break

        return result
    
    def get_self_base_planet(self, obs: dict):
        allied_planets = self.get_allied_planets(obs)
        return next((planet for planet in allied_planets if (planet[0], planet[1]) == self.self_base_coords), None)
    
    def get_enemy_base_planet(self, obs: dict):
        enemy_planets = self.get_enemy_planets(obs)
        return next((planet for planet in enemy_planets if (planet[0], planet[1]) == self.enemy_base_coords), None)
    
    def get_self_base_planet_health(self, obs: dict):
        self_base_planet = self.get_self_base_planet(obs)
        return self_base_planet[2]
    
    def get_self_base_planet_coords(self, obs: dict):
        self_base_planet = self.get_self_base_planet(obs)
        return (self_base_planet[0], self_base_planet[1])

    def get_enemy_base_planet_health(self, obs: dict):
        self_enemy_planet = self.get_enemy_base_planet(obs)
        return self_enemy_planet[2]
    
    def get_enemy_base_planet_coords(self, obs: dict):
        self_enemy_planet = self.get_enemy_base_planet(obs)
        return (self_enemy_planet[0], self_enemy_planet[1])

class Agent:
    def __init__(self, side: int):
        """
        :param side: Indicates whether the player is on left side (0) or right side (1)
        """
        self.side = side

        self.enemy_base_coords = None
        self.self_base_coords = None

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

        if self.self_base_coords is None:
            if self.side == 0:
                self.self_base_coords = next(((planet[0], planet[1]) for planet in obs["planets_occupation"] if planet[2] < 50), None)
            else:
                self.self_base_coords = next(((planet[0], planet[1]) for planet in obs["planets_occupation"] if planet[2] >= 50), None)

        if self.enemy_base_coords is None:
            if self.side == 0:
                self.enemy_base_coords = next(((planet[0], planet[1]) for planet in obs["planets_occupation"] if planet[2] >= 50), None)
            else:
                self.enemy_base_coords = next(((planet[0], planet[1]) for planet in obs["planets_occupation"] if planet[2] < 50), None)

        ship = Ship(0, self.side, self.self_base_coords, self.enemy_base_coords)

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