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
                    "exits": {East, North, West, South},
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
                current["exits"].remove(North)
                current["blocked"].add(North)

                node["exits"].remove(South)
                node["blocked"].add(South)

            if (
                current["pos"] not in discovered
                or east["pos"] not in discovered[current["pos"]]
            ):
                node = current["neighbours"][East]

                current["exits"].remove(East)
                current["blocked"].add(East)

                node["exits"].remove(West)
                node["blocked"].add(West)
    return grid
