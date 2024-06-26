def discover_maze_hand_on_wall():
    directions = [East, North, West, South]
    current_pos = (get_pos_x(), get_pos_y())
    discovered = {}
    visited = set()
    pdir = 0
    size = get_world_size() ** 2

    while True:
        visited.add(current_pos)
        if get_entity_type() == Entities.Treasure:
            treasure_pos = current_pos
        if len(visited) == size:
            break
        for i in range(4):
            d_idx = (pdir + 3 + i) % 4
            d = directions[d_idx]
            if move(d):
                new_pos = (get_pos_x(), get_pos_y())
                if current_pos not in discovered:
                    discovered[current_pos] = set()
                discovered[current_pos].add(new_pos)
                if new_pos not in discovered:
                    discovered[new_pos] = set()
                discovered[new_pos].add(current_pos)
                current_pos = new_pos
                pdir = d_idx
                break
    return prepare_grid(discovered), treasure_pos
