from typing import Tuple

def get_self_ship(obs: dict, ship_id: int):
    return next((ship for ship in obs["allied_ships"] if ship[0] == ship_id), None)

def get_allied_ships(obs: dict, ship_id: int):
    allied_ships = obs["allied_ships"]
    return list(filter(lambda ship: ship[0] != ship_id, allied_ships))

def get_enemy_ships(obs: dict):
    enemy_ships = obs["enemy_ships"]
    return enemy_ships

def get_ship_coords(ship):
    return (ship[1], ship[2])

def get_planet_coords(planet):
    return (planet[0], planet[1])

def get_nearest_allied_ship_coords(obs: dict, ship_id: int, side: int):
    allied_ships = get_allied_ships(obs, ship_id)
    if len(allied_ships) == 0:
        if side == 0:
            return (9999, 9999)
        return (-9999, -9999)

    return get_ship_coords(get_nearest_ship_from_collection(obs, allied_ships, ship_id))

def get_nearest_enemy_ship_coords(obs: dict, ship_id: int, side: int):
    enemy_ships = get_enemy_ships(obs)
    if len(enemy_ships) == 0:
        if side == 0:
            return (9999, 9999)
        return (-9999, -9999)

    return get_ship_coords(get_nearest_ship_from_collection(obs, enemy_ships, ship_id))

def get_nearest_ship_from_collection(obs: dict, ships: list, ship_id: int):
    self_ship = get_self_ship(obs, ship_id)
    return min(ships, key=lambda ship: get_distance((self_ship[1], self_ship[2]), (ship[1], ship[2])), default=None)

def get_distance(coords_1, coords_2):
    x_1, y_1 = coords_1
    x_2, y_2 = coords_2

    return (x_2 - x_1) ** 2 - (y_2 - y_1) ** 2

def get_self_ship_coords(obs: dict, ship_id: int):
    ship = get_self_ship(obs, ship_id)
    return get_ship_coords(ship)

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

    return min(planets, key=lambda planet: get_distance((self_ship[1], self_ship[2]), (planet[0], planet[1])), default=None)

def get_nearest_unoccupied_planet_coords(obs: dict, ship_id: int, enemy_base_coords: Tuple[int, int]):
    unoccupied_planets = get_unoccupied_planets(obs)

    if len(unoccupied_planets) == 0:
        return enemy_base_coords
    
    return get_planet_coords(get_nearest_planet_from_collection(obs, unoccupied_planets, ship_id))

def get_nearest_allied_planet_coords(obs: dict, side: int, ship_id: int, self_base_coords: Tuple[int, int]):
    allied_planets = get_allied_planets(obs, side)
    if len(allied_planets) == 0:
        return self_base_coords

    return get_planet_coords(get_nearest_planet_from_collection(obs, allied_planets, ship_id))

def get_nearest_enemy_planet_coords(obs: dict, side: int, ship_id: int, enemy_base_coords: Tuple[int, int]):
    enemy_planets = get_enemy_planets(obs, side)
    if len(enemy_planets) == 0:
        return enemy_base_coords
    
    return get_planet_coords(get_nearest_planet_from_collection(obs, enemy_planets, ship_id))

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

    return next((planet for planet in allied_planets if (int(planet[0]), int(planet[1])) == self_base_coords), None)

def get_enemy_base_planet(obs: dict, side: int, enemy_base_coords: Tuple[int, int]):
    enemy_planets = get_enemy_planets(obs, side)
    return next((planet for planet in enemy_planets if (int(planet[0]), int(planet[1])) == enemy_base_coords), None)

def get_self_base_planet_health(obs: dict, side: int, self_base_coords: Tuple[int, int]):
    self_base_planet = get_self_base_planet(obs, side, self_base_coords)
    if not self_base_planet:
        return 0
    
    return self_base_planet[2]

def get_enemy_base_planet_health(obs: dict, side: int, enemy_base_coords: Tuple[int, int]):
    enemy_base_planet = get_enemy_base_planet(obs, side, enemy_base_coords)
    if not enemy_base_planet:
        return 100

    return enemy_base_planet[2]

def get_self_ship_cooldown(obs: dict, ship_id: int):
    self_ship = get_self_ship(obs, ship_id)
    return int(self_ship[5] > 0)

def obs_to_state(obs: dict, ship_id: int, side: int):
    self_base_coords = (9, 9) if side == 0 else (90, 90)
    enemy_base_coords = (90, 90) if side == 0 else (9, 9)

    # print(list(map(len, [
    #     get_self_ship_coords(obs, ship_id),
    # self_base_coords,
    # get_nearest_allied_ship_coords(obs, ship_id, side),
    # get_nearest_enemy_ship_coords(obs, ship_id, side),
    # get_nearest_unoccupied_planet_coords(obs, ship_id, enemy_base_coords),
    # get_nearest_allied_planet_coords(obs, side, ship_id, self_base_coords),
    # get_nearest_enemy_planet_coords(obs, side, ship_id, enemy_base_coords),
    # enemy_base_coords,
    # is_enemy_in_range(obs, ship_id)
    # ])))

    return [
        *get_self_ship_coords(obs, ship_id),
        *self_base_coords,
        *get_nearest_allied_ship_coords(obs, ship_id, side),
        *get_nearest_enemy_ship_coords(obs, ship_id, side),
        *get_nearest_unoccupied_planet_coords(obs, ship_id, enemy_base_coords),
        *get_nearest_allied_planet_coords(obs, side, ship_id, self_base_coords),
        *get_nearest_enemy_planet_coords(obs, side, ship_id, enemy_base_coords),
        *enemy_base_coords,
        *is_enemy_in_range(obs, ship_id),
        get_self_ship_health(obs, ship_id),
        get_self_base_planet_health(obs, side, self_base_coords),
        get_enemy_base_planet_health(obs, side, enemy_base_coords),
        get_enemy_ships_count(obs),
        get_allied_ships_count(obs, ship_id),
        get_enemy_planets_count(obs, side),
        get_allied_planets_count(obs, side),
        get_self_ship_cooldown(obs, ship_id)
    ]

def val_to_action(ship_id: int, val: int):
    if val == 0:
        return [ship_id, 0, 0, 0]
    elif val == 1:
        return [ship_id, 0, 0, 1]
    elif val == 2:
        return [ship_id, 0, 0, 2]
    elif val == 3:
        return [ship_id, 0, 0, 3]
    elif val == 4:
        return [ship_id, 0, 1, 1]
    elif val == 5:
        return [ship_id, 0, 1, 2]
    elif val == 6:
        return [ship_id, 0, 1, 3]
    elif val == 7:
        return [ship_id, 0, 2, 1]
    elif val == 8:
        return [ship_id, 0, 2, 2]
    elif val == 9:
        return [ship_id, 0, 2, 3]
    elif val == 10:
        return [ship_id, 0, 3, 1]
    elif val == 11:
        return [ship_id, 0, 3, 2]
    elif val == 12:
        return [ship_id, 0, 3, 3]
    elif val == 13:
        return [ship_id, 1, 0]
    elif val == 14:
        return [ship_id, 1, 1]
    elif val == 15:
        return [ship_id, 1, 2]
    else:
        return [ship_id, 1, 3]

def action_to_val(action: list):
    if len(action) == 4:
        _, _, direction, speed = action

        if direction == 0 and speed == 0:
            return 0
        elif direction == 0 and speed == 1:
            return 1
        elif direction == 0 and speed == 2:
            return 2
        elif direction == 0 and speed == 3:
            return 3
        elif direction == 1 and speed == 1:
            return 4
        elif direction == 1 and speed == 2:
            return 5
        elif direction == 1 and speed == 3:
            return 6
        elif direction == 2 and speed == 1:
            return 7
        elif direction == 2 and speed == 2:
            return 8
        elif direction == 2 and speed == 3:
            return 9
        elif direction == 3 and speed == 1:
            return 10
        elif direction == 3 and speed == 2:
            return 11
        elif direction == 3 and speed == 3:
            return 12

    elif len(action) == 3:
        _, _, direction = action

        if direction == 0:
            return 13
        elif direction == 1:
            return 14
        elif direction == 2:
            return 15
        else:
            return 16