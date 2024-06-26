def heap_float(heap, child_index):
    while child_index > 0:
        parent_index = (child_index - 1) // 2
        parent, child = heap[parent_index], heap[child_index]
        d = parent["min_cost"] - child["min_cost"]
        if d < 0 or (d == 0 and parent["heuristic"] <= child["heuristic"]):
            break
        heap[parent_index], heap[child_index] = child, parent
        parent["heap_index"], child["heap_index"] = child_index, parent_index
        child_index = parent_index


def heap_pop(heap):
    if len(heap) == 1:
        return heap.pop()
    else:
        ret = heap[0]
        heap[0] = heap.pop()
        heap[0]["heap_index"] = 0
    max = len(heap) // 2
    parent_index = 0
    mchild = len(heap) - 1
    while parent_index < max:
        parent = heap[parent_index]
        child_index = parent_index * 2 + 1
        if (
            child_index < mchild
            and heap[child_index]["min_cost"] - heap[child_index + 1]["min_cost"] > 0
        ):
            child_index += 1
        child = heap[child_index]
        if parent["min_cost"] - child["min_cost"] <= 0:
            break
        heap[parent_index], heap[child_index] = child, parent
        parent["heap_index"], child["heap_index"] = child_index, parent_index
        parent_index = child_index
    return ret


def find_path(grid, target):
    drone_pos = get_pos_x(), get_pos_y()
    target_node = grid[target[1]][target[0]]
    target_node["parent"] = None
    if drone_pos == target:
        return target_node
    pos = target_node["pos"]
    target_node["heap_index"] = 0
    target_node["cost"] = 0
    target_node["heuristic"] = abs(pos[0] - drone_pos[0]) + abs(pos[1] - drone_pos[1])
    target_node["min_cost"] = target_node["heuristic"]
    open_set = {target: target_node}
    closed_set = {}
    heap = [target_node]

    while True:
        cell = heap_pop(heap)
        pos = cell["pos"]
        closed_set[pos] = open_set.pop(pos)
        for neighbour in cell["exits"]:
            ncell = cell["neighbours"][neighbour]
            npos = ncell["pos"]
            if npos not in closed_set and npos in cell["connectivity"]:
                if npos not in open_set:
                    new_cell = grid[npos[1]][npos[0]]
                    new_cell["cost"] = cell["cost"] + 1
                    new_cell["heuristic"] = abs(drone_pos[0] - npos[0]) + abs(
                        drone_pos[1] - npos[1]
                    )
                    new_cell["min_cost"] = new_cell["cost"] + new_cell["heuristic"]
                    new_cell["heap_index"] = len(heap)
                    new_cell["parent"] = cell
                    open_set[npos] = new_cell
                    heap.append(new_cell)
                    heap_float(heap, len(heap) - 1)
                    if npos == drone_pos:
                        return new_cell
                else:
                    other = open_set[npos]
                    new_score = cell["cost"] + 1
                    old_score = other["cost"]
                    if new_score < old_score:
                        other["parent"] = cell
                        other["cost"] = new_score
                        other["min_cost"] = new_score + other["heuristic"]
                        heap_float(heap, other["heap_index"])
