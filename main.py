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


for i in range(10):
    power = num_items(Items.Power)
    seconds = get_time()
    ops = get_op_count()
    maze_cycle()
    ops = get_op_count() - ops
    seconds = get_time() - seconds
    power = power - num_items(Items.Power)
    print(seconds, "seconds, ", ops, "ops, ", power, "power")
