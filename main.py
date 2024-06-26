def farm_pumpkins(pumpkin_target):
    # Farm pumpkins until we have at least pumkin_target
    #
    # Probably shouldn't spoil too much...
    # I'll leave this as an exercise for the player :P
    #
    # Return True to indicate success, or False to indicate
    # that this call should be retried
    #
    # For now just assume we have enough pumpkins
    return True


def benchmark_maze_cycle():
    gold = num_items(Items.Gold)
    power = num_items(Items.Power)
    seconds = get_time()
    ops = get_op_count()
    maze_cycle()
    seconds = get_time() - seconds
    ops = get_op_count() - ops
    power = power - num_items(Items.Power)
    gold = num_items(Items.gold) - gold
    print(seconds, "seconds,", ops, "ops,", power, "power,", gold, "gold")


benchmark_maze_cycle()
