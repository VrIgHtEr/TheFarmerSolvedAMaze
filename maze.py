def do_maze_cycle(discovery):
    grid, target = discovery
    node = None
    opposite_directions = {
        North: South,
        South: North,
        East: West,
        West: East,
    }

    while True:
        node = find_path(grid, target)
        while node != None:
            for direction in list(node["blocked"]):
                if move(direction):
                    opposite = opposite_directions[direction]
                    other_node = node["neighbours"][direction]

                    node["blocked"].remove(direction)
                    other_node["blocked"].remove(opposite)

                    node["exits"][direction] = 0
                    other_node["exits"][opposite] = 0

                    node["connectivity"].add(other_node["pos"])
                    other_node["connectivity"].add(node["pos"])
                    move(opposite)

            next = node["parent"]
            neighbours = node["neighbours"]
            if next == None:
                break
            move(node["directions"][next["pos"]])
            node = next

        next_pos = measure()
        if next_pos == None:
            harvest()
            break
        else:
            while get_entity_type() == Entities.Treasure:
                use_item(Items.Fertilizer)
        target = next_pos


def discover_maze(perfect):
    if perfect:
        return discover_maze_hand_on_wall()
    else:
        return discover_maze_tremaux()


def finish_incomplete_cycle():
    entity = get_entity_type()
    if entity == Entities.Hedge or entity == Entities.Treasure:
        do_maze_cycle(discover_maze(False))


def ensure_fertilizer(cycle_length, initial_fertilizers):
    fertilizer_owned = num_items(Items.Fertilizer)
    fertilizer_missing = cycle_length + initial_fertilizers - fertilizer_owned
    if fertilizer_missing > 0:
        fertilizer_cost_pumpkins = get_cost(Items.Fertilizer)[Items.Pumpkin]
        pumpkins_needed = fertilizer_missing * fertilizer_cost_pumpkins
        while not farm_pumpkins(pumpkins_needed):
            pass
        fertilizer_missing -= initial_fertilizers
        if fertilizer_missing > 0:
            trade(Items.Fertilizer, fertilizer_missing)


def maze_cycle():
    cycle_length = 300
    initial_fertilizers = 50
    finish_incomplete_cycle()
    while True:
        ensure_fertilizer(cycle_length, initial_fertilizers)
        if get_ground_type() != Grounds.Soil:
            till()
        if get_entity_type() != None:
            harvest()
        plant(Entities.Bush)
        while not can_harvest():
            if get_water() < 1 and num_items(Items.Water_Tank) >= 1:
                use_item(Items.Water_Tank)
        while get_entity_type() != Entities.Bush:
            if num_items(Items.Fertilizer) < cycle_length:
                if not trade(Items.Fertilizer):
                    continue
            use_item(Items.Fertilizer)
        do_maze_cycle(discover_maze(True))
        break
