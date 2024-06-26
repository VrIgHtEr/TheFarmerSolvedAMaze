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
        if len(heap) == 1:
            cell = heap.pop()
        else:
            cell = heap[0]
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
                    and heap[child_index]["min_cost"]
                    - heap[child_index + 1]["min_cost"]
                    > 0
                ):
                    child_index += 1
                child = heap[child_index]
                if parent["min_cost"] - child["min_cost"] <= 0:
                    break
                heap[parent_index], heap[child_index] = child, parent
                parent["heap_index"], child["heap_index"] = child_index, parent_index
                parent_index = child_index
        closed_set[cell["pos"]] = open_set.pop(cell["pos"])
        for neighbour in cell["exits"]:
            ncell = cell["neighbours"][neighbour]
            npos = ncell["pos"]
            if npos not in closed_set:
                if npos not in open_set:
                    ncell["parent"] = cell
                    if npos == drone_pos:
                        return ncell
                    ncell["cost"] = cell["cost"] + 1
                    ncell["heuristic"] = abs(drone_pos[0] - npos[0]) + abs(
                        drone_pos[1] - npos[1]
                    )
                    ncell["min_cost"] = ncell["cost"] + ncell["heuristic"]
                    child_index = len(heap)
                    ncell["heap_index"] = child_index
                    open_set[npos] = ncell
                    heap.append(ncell)
                    while child_index > 0:
                        parent_index = (child_index - 1) // 2
                        parent, child = heap[parent_index], heap[child_index]
                        d = parent["min_cost"] - child["min_cost"]
                        if d < 0 or (
                            d == 0 and parent["heuristic"] <= child["heuristic"]
                        ):
                            break
                        heap[parent_index], heap[child_index] = child, parent
                        parent["heap_index"], child["heap_index"] = (
                            child_index,
                            parent_index,
                        )
                        child_index = parent_index
                else:
                    new_score = cell["cost"] + 1
                    if new_score < ncell["cost"]:
                        ncell["parent"] = cell
                        ncell["cost"] = new_score
                        ncell["min_cost"] = new_score + ncell["heuristic"]
                        child_index = ncell["heap_index"]
                        while child_index > 0:
                            parent_index = (child_index - 1) // 2
                            parent, child = heap[parent_index], heap[child_index]
                            d = parent["min_cost"] - child["min_cost"]
                            if d < 0 or (
                                d == 0 and parent["heuristic"] <= child["heuristic"]
                            ):
                                break
                            heap[parent_index], heap[child_index] = child, parent
                            parent["heap_index"], child["heap_index"] = (
                                child_index,
                                parent_index,
                            )
                            child_index = parent_index
