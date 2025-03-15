from typing import Tuple

def get_self_ship(obs: dict, ship_id: int):
    return next((ship for ship in obs["allied_ships"] if ship[0] == ship_id), None)

def get_allied_ships(obs: dict, ship_id: int):
    allied_ships = obs["allied_ships"]
    return list(filter(lambda ship: ship[0] != ship_id, allied_ships))

def get_enemy_ships(obs: dict):
    enemy_ships = obs["enemy_ships"]
    return enemy_ships

def get_nearest_allied_ship(obs: dict, ship_id: int):
    allied_ships = get_allied_ships(obs, ship_id)
    return get_nearest_ship_from_collection(obs, allied_ships)

def get_nearest_enemy_ship(obs: dict):
    enemy_ships = get_enemy_ships(obs)
    return get_nearest_ship_from_collection(enemy_ships)

def get_nearest_ship_from_collection(obs: dict, ships: list, ship_id: int):
    self_ship = get_self_ship(obs, ship_id)
    return min(ships, key=lambda ship: get_distance((self_ship[1], self_ship[2]), (ship[1], ship[2])), default=None)

def get_distance(coords_1, coords_2):
    x_1, y_1 = coords_1
    x_2, y_2 = coords_2

    return (x_2 - x_1) ** 2 - (y_2 - y_1) ** 2

def get_self_ship_coords(obs: dict, ship_id: int):
    ship = get_self_ship(obs, ship_id)
    return (ship[1], ship[2])

def get_self_ship_health(obs: dict, ship_id: int):
    ship = get_self_ship(obs, ship_id)
    return ship[4]

def get_allied_ships_count(obs: dict, ship_id: int):
    allied_ships = get_allied_ships(obs, ship_id)
    return len(allied_ships)

def get_enemy_ships_count(obs: dict):
    enemy_ships = get_enemy_ships(obs)
    return len(enemy_ships)

def get_planets(obs: dict):
    return obs["planets_occupation"]

def get_unoccupied_planets(obs: dict):
    planets = get_planets(obs)
    return list(filter(lambda planet: planet[2] == -1, planets))

def get_allied_planets(obs: dict, side: int):
    if side == 0:
        return get_player_1_planets(obs)
    return get_player_2_planets(obs)

def get_enemy_planets(obs: dict, side: int):
    if side == 0:
        return get_player_2_planets(obs)
    return get_player_1_planets(obs)

def get_player_1_planets(obs: dict):
    planets = get_planets(obs)
    return list(filter(lambda planet: planet[2] < 50, planets))

def get_player_2_planets(obs: dict):
    planets = get_planets(obs)
    return list(filter(lambda planet: planet[2] >= 50, planets))

def get_allied_planets_count(obs: dict, side: int):
    allied_planets = get_allied_planets(obs, side)
    return len(allied_planets)

def get_enemy_planets_count(obs: dict, side: int):
    enemy_planets = get_enemy_planets(obs, side)
    return len(enemy_planets)

def get_nearest_planet_from_collection(obs: dict, planets: list, ship_id: int):
    self_ship = get_self_ship(obs, ship_id)
    print(self_ship)

    return min(planets, key=lambda planet: get_distance((self_ship[1], self_ship[2]), (planet[0], planet[1])), default=None)

def get_nearest_unoccupied_planet(obs: dict, ship_id: int):
    unoccupied_planets = get_unoccupied_planets(obs)
    return get_nearest_planet_from_collection(obs, unoccupied_planets, ship_id)

def get_nearest_allied_planet(obs: dict, side: int, ship_id: int):
    allied_planets = get_allied_planets(obs, side)
    return get_nearest_planet_from_collection(obs, allied_planets, ship_id)

def get_nearest_enemy_planet(obs: dict, side: int, ship_id: int):
    enemy_planets = get_enemy_planets(obs, side)
    return get_nearest_planet_from_collection(obs, enemy_planets, ship_id)

def is_enemy_in_range(obs: dict, ship_id: int, distance: int = 8):
    x_self, y_self = get_self_ship_coords(obs, ship_id)
    enemy_ships = get_enemy_ships(obs)

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

def get_self_base_planet(obs: dict, side: int, self_base_coords: Tuple[int, int]):
    allied_planets = get_allied_planets(obs, side)
    return next((planet for planet in allied_planets if (planet[0], planet[1]) == self_base_coords), None)

def get_enemy_base_planet(obs: dict, side: int, enemy_base_coords: Tuple[int, int]):
    enemy_planets = get_enemy_planets(obs, side)
    return next((planet for planet in enemy_planets if (planet[0], planet[1]) == enemy_base_coords), None)

def get_self_base_planet_health(obs: dict, side: int, self_base_coords: Tuple[int, int]):
    self_base_planet = get_self_base_planet(obs, side, self_base_coords)
    return self_base_planet[2]

def get_enemy_base_planet_health(obs: dict, side: int, enemy_base_coords: Tuple[int, int]):
    self_enemy_planet = get_enemy_base_planet(obs, side, enemy_base_coords)
    return self_enemy_planet[2]
