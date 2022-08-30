def jump():
    turn_left()
    move()
    turn_left()
    turn_left()
    turn_left()
    move()
    turn_left()
    turn_left()
    turn_left()
    move()
    turn_left()
    
while not at_goal():
    if front_is_clear() :
        move()
    elif wall_in_front() :
        jump()