def prepare_grid(discovered):
    grid = []
    world_size = get_world_size()
    for y in range(world_size):
        row = []
        grid.append(row)
        for x in range(world_size):
            row.append(
                {
                    "pos": (x, y),
                    "neighbours": {},
                    "blocked": set(),
                    "exits": {East: 0, North: 0, West: 0, South: 0},
                    "connectivity": {
                        ((x + 1) % world_size, y),
                        ((x + world_size - 1) % world_size, y),
                        (x, (y + 1) % world_size),
                        (x, (y + world_size - 1) % world_size),
                    },
                    "heap_index": 0,
                    "parent": None,
                    "cost": 0,
                    "min_cost": 0,
                    "heuristic": 0,
                    "directions": {},
                }
            )

    for y in range(get_world_size()):
        for x in range(get_world_size()):
            current = grid[y][x]
            east = grid[y][(x + 1) % world_size]
            north = grid[(y + 1) % world_size][x]

            current["neighbours"][East] = east
            east["neighbours"][West] = current
            current["directions"][east["pos"]] = East
            east["directions"][current["pos"]] = West

            current["neighbours"][North] = north
            north["neighbours"][South] = current
            current["directions"][north["pos"]] = North
            north["directions"][current["pos"]] = South

            if (
                current["pos"] not in discovered
                or north["pos"] not in discovered[current["pos"]]
            ):
                node = current["neighbours"][North]
                current["exits"].pop(North)
                current["blocked"].add(North)
                current["connectivity"].remove(node["pos"])

                node["exits"].pop(South)
                node["blocked"].add(South)
                node["connectivity"].remove(current["pos"])

            if (
                current["pos"] not in discovered
                or east["pos"] not in discovered[current["pos"]]
            ):
                node = current["neighbours"][East]

                current["exits"].pop(East)
                current["blocked"].add(East)
                current["connectivity"].remove(node["pos"])

                node["exits"].pop(West)
                node["blocked"].add(West)
                node["connectivity"].remove(current["pos"])
    return grid
