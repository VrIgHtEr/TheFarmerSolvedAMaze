def discover_maze_tremaux():
    self_cells = []
    for y in range(get_world_size()):
        row = []
        self_cells.append(row)
        for x in range(get_world_size()):
            row.append({"x": x, "y": y, "walls": {}, "exits": {}})
    for y in range(get_world_size()):
        for x in range(get_world_size()):
            cell = self_cells[y][x]

            node = self_cells[y][(x + 1) % get_world_size()]
            wall = {"mark": 0}
            cell["walls"][East] = wall
            node["walls"][West] = wall
            cell["exits"][East] = node
            node["exits"][West] = cell

            node = self_cells[(y + 1) % get_world_size()][x]
            wall = {"mark": 0}
            cell["walls"][North] = wall
            node["walls"][South] = wall
            cell["exits"][North] = node
            node["exits"][South] = cell
    movements = {
        East: [North, West, South, East],
        North: [West, South, East, North],
        West: [South, East, North, West],
        South: [East, North, West, South],
    }
    entrance_dir = None
    treasure_pos = (0, 0)
    while True:
        cell = self_cells[get_pos_y()][get_pos_x()]
        marks = [[], [], []]
        movement_idx = entrance_dir
        if movement_idx == None:
            movement_idx = East
        for direction in movements[movement_idx]:
            if direction in cell["exits"]:
                marks[cell["walls"][direction]["mark"]].append(direction)

        if len(marks[2]) == len(cell["exits"]):
            break
        next_dir = None

        if len(marks[0]) >= len(cell["exits"]) - 1:
            if get_entity_type() == Entities.Treasure:
                treasure_pos = (get_pos_x(), get_pos_y())
            if len(marks[0]) > 0:
                next_dir = marks[0][0]

        if next_dir == None:
            if cell["walls"][entrance_dir]["mark"] < 2:
                next_dir = entrance_dir

        if next_dir == None:
            if len(marks[0]) > 0:
                next_dir = marks[0][0]
            else:
                next_dir = marks[1][0]

        if not move(next_dir):
            neighbour_dir = movements[next_dir][1]
            cell["exits"][next_dir]["exits"].pop(neighbour_dir)
            cell["exits"][next_dir]["walls"].pop(neighbour_dir)
            cell["exits"].pop(next_dir)
            cell["walls"].pop(next_dir)
        else:
            entrance_dir = movements[next_dir][1]
            cell["walls"][next_dir]["mark"] += 1

    discovered = {}
    for y in range(get_world_size()):
        for x in range(get_world_size()):
            pos = (x, y)
            cell = self_cells[y][x]

            for dir in cell["exits"]:
                other = cell["exits"][dir]
                pos2 = (other["x"], other["y"])

                if pos not in discovered:
                    discovered[pos] = set()
                discovered[pos].add(pos2)

                if pos2 not in discovered:
                    discovered[pos2] = set()
                discovered[pos2].add(pos)

    return prepare_grid(discovered), treasure_pos
