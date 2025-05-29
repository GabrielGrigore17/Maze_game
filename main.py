import turtle
import time # For time.sleep
import config
from threading import Thread
from platform import system

# Import from our new modules
from sound import play_sound, PlaySoundException
from models import * # Still useful for classes like Gold, Score, BlackSquare if instantiated directly in main loop/UI updates
import game_logic as gl # Use an alias for game_logic

# System specific setup
system_name = system() # Store result of system()

# --- Turtle Screen Setup ---
wn = turtle.Screen()
wn.bgcolor(config.BACKGROUND_COLOR)
wn.title(config.SCREEN_TITLE)
wn.setup(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
wn.tracer(0) # Turn off screen updates for manual control

# --- Shape Registration (Uses config) ---
# This needs to be done once for the turtle screen instance
turtle.register_shape(config.PLAYER_RIGHT_GIF)
turtle.register_shape(config.PLAYER_LEFT_GIF)
turtle.register_shape(config.WALL_GIF)
turtle.register_shape(config.TREASURE_GIF)
turtle.register_shape(config.TREASURE_SMALL_GIF)
turtle.register_shape(config.TREASURE_BIG_GIF)
turtle.register_shape(config.ENEMY_LEFT_GIF)
turtle.register_shape(config.ENEMY_RIGHT_GIF)
turtle.register_shape(config.HEART_GIF)
turtle.register_shape(config.KEY_GIF)
turtle.register_shape(config.FRIEND_GIF)
turtle.register_shape(config.DOOR_GIF)
turtle.register_shape(config.ARROW_GIF)
turtle.register_shape(config.STAIRS_GIF)
turtle.register_shape(config.BLACK_SQUARE_GIF)
turtle.register_shape(config.DUNGEON_1_GIF)
turtle.register_shape(config.DUNGEON_2_GIF)
turtle.register_shape(config.DUNGEON_3_GIF)
turtle.register_shape(config.EXIT_GIF)
turtle.register_shape(config.BLACK_BACKGROUND_GIF)
turtle.register_shape(config.WINNER_GIF)
turtle.register_shape(config.LOSER_GIF)
turtle.register_shape(config.ONE_GIF)
turtle.register_shape(config.TWO_GIF)
turtle.register_shape(config.THREE_GIF)
turtle.register_shape(config.FOUR_GIF)
turtle.register_shape(config.FIVE_GIF)

# --- Initial Game Setup ---
# Play background music
if system_name == 'Windows':
    theme_thread = Thread(target=play_sound, args=(config.THEME_MP3,), daemon=True)
    theme_thread.start()

# Loading screen animation
for _ in range(config.LOADING_SCREEN_REPEATS): # Use _ if loop variable i is not used
    wn.bgpic(config.DUNGEON_1_GIF)
    wn.update()
    time.sleep(config.LOADING_SCREEN_DELAY)
    wn.bgpic(config.DUNGEON_2_GIF)
    wn.update()
    time.sleep(config.LOADING_SCREEN_DELAY)
    wn.bgpic(config.DUNGEON_3_GIF)
    wn.update()
    time.sleep(config.LOADING_SCREEN_DELAY)

# Set up the first level
wn.bgpic(config.BLACK_BACKGROUND_GIF) # Set default background after loading
gl.setup_maze_logic(gl.levels[gl.current_level])

# Stamp initial hearts (hearts list is populated in game_logic)
for heart_obj in gl.hearts:
    heart_obj.stamp()

# --- Key Bindings ---
turtle.listen()
# Player movement methods now expect walls, doors_locations, friends_locations
turtle.onkeypress(lambda: gl.player.go_left(gl.walls, gl.doors_locations, gl.friends_locations), "Left")
turtle.onkeypress(lambda: gl.player.go_right(gl.walls, gl.doors_locations, gl.friends_locations), "Right")
turtle.onkeypress(lambda: gl.player.go_down(gl.walls, gl.doors_locations, gl.friends_locations), "Down")
turtle.onkeypress(lambda: gl.player.go_up(gl.walls, gl.doors_locations, gl.friends_locations), "Up")
turtle.onkeypress(gl.end_game_function_logic, "q") # Use renamed function from game_logic
turtle.onkeypress(gl.restart_logic, "r")          # Use renamed function from game_logic

wn.tracer(0) # Ensure tracer is off

# Start enemy movement (enemies list is populated in game_logic.setup_maze_logic)
for enemy_obj in gl.enemies:
    # enemy_obj.move itself will handle turtle.ontimer for subsequent moves
    turtle.ontimer(enemy_obj.move, config.ENEMY_MOVE_ONTURN_TIMER)


# --- Main Game Loop ---
while not gl.end_game: # Access end_game from game_logic
    # Update UI elements based on player state
    if gl.player.key: gl.key.showturtle()
    else: gl.key.hideturtle()

    if gl.player.arrow:
        gl.arrow.showturtle()
        gl.arrow_number.showturtle()
    else:
        gl.arrow.hideturtle()
        gl.arrow_number.hideturtle()

    # Update arrow count display
    if gl.player.arrow == 1: gl.arrow_number.shape(config.ONE_GIF)
    elif gl.player.arrow == 2: gl.arrow_number.shape(config.TWO_GIF)
    elif gl.player.arrow == 3: gl.arrow_number.shape(config.THREE_GIF)
    elif gl.player.arrow == 4: gl.arrow_number.shape(config.FOUR_GIF)
    elif gl.player.arrow == config.MAX_PLAYER_ARROWS: gl.arrow_number.shape(config.FIVE_GIF)
    else: gl.arrow_number.hideturtle()

    # Check for collision with stairs (next level)
    if gl.player.is_collision(gl.stairs):
        if system_name == 'Windows': Thread(target=play_sound, args=(config.NEXT_LEVEL_MP3,)).start()
        
        wn.clear() # Clears screen, stamps, and turtle objects (except those explicitly preserved or re-created)
        wn.bgcolor(config.BACKGROUND_COLOR)
        wn.title(config.GAME_TITLE_NEXT_LEVEL)
        wn.setup(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)

        # Re-register shapes for the new screen instance after wn.clear()
        # This is crucial as clearwn also clears shape registrations for some turtle versions
        shapes_to_register = [
            config.PLAYER_RIGHT_GIF, config.PLAYER_LEFT_GIF, config.WALL_GIF, config.TREASURE_GIF,
            config.TREASURE_SMALL_GIF, config.TREASURE_BIG_GIF, config.ENEMY_LEFT_GIF, config.ENEMY_RIGHT_GIF,
            config.HEART_GIF, config.KEY_GIF, config.FRIEND_GIF, config.DOOR_GIF, config.ARROW_GIF,
            config.STAIRS_GIF, config.BLACK_SQUARE_GIF, config.DUNGEON_1_GIF, config.DUNGEON_2_GIF,
            config.DUNGEON_3_GIF, config.EXIT_GIF, config.BLACK_BACKGROUND_GIF, config.WINNER_GIF,
            config.LOSER_GIF, config.ONE_GIF, config.TWO_GIF, config.THREE_GIF, config.FOUR_GIF, config.FIVE_GIF
        ]
        for shape_file in shapes_to_register:
            turtle.register_shape(shape_file)
        
        gl.current_level += 1
        
        # Preserve player's arrows and gold (gold is already preserved via gl.current_gold)
        current_player_arrows = gl.player.arrow
        
        # Re-initialize player and other necessary game objects from game_logic
        gl.player = Player() 
        gl.player.arrow = current_player_arrows
        
        gl.pen = Pen()
        gl.key = Key() # Re-create UI elements
        gl.arrow = Arrow()
        gl.arrow_number = ArrowNumber()
        gl.game_over = GameOver()
        gl.stairs = Stairs(config.FAR_OFF_SCREEN_X, config.FAR_OFF_SCREEN_Y) 
        gl.game_win = GameWin(config.FAR_OFF_SCREEN_X, config.FAR_OFF_SCREEN_Y)

        gl.setup_maze_logic(gl.levels[gl.current_level]) # This populates walls, enemies, etc.
        
        # Re-stamp hearts (which are preserved in gl.hearts)
        for heart_obj in gl.hearts: heart_obj.stamp() 

        # Re-bind keys
        turtle.listen()
        turtle.onkeypress(lambda: gl.player.go_left(gl.walls, gl.doors_locations, gl.friends_locations), "Left")
        turtle.onkeypress(lambda: gl.player.go_right(gl.walls, gl.doors_locations, gl.friends_locations), "Right")
        turtle.onkeypress(lambda: gl.player.go_down(gl.walls, gl.doors_locations, gl.friends_locations), "Down")
        turtle.onkeypress(lambda: gl.player.go_up(gl.walls, gl.doors_locations, gl.friends_locations), "Up")
        turtle.onkeypress(gl.restart_logic, "r")
        turtle.onkeypress(gl.end_game_function_logic, "q")
        
        wn.tracer(0) 

        for enemy_obj in gl.enemies: 
            turtle.ontimer(enemy_obj.move, config.ENEMY_MOVE_ONTURN_TIMER)

    # Check for collision with game_win exit
    if gl.player.is_collision(gl.game_win):
        gl.player.goto(config.OFF_SCREEN_X, config.OFF_SCREEN_Y)
        if system_name == 'Windows': Thread(target=play_sound, args=(config.GAME_WIN_MP3,)).start()
        wn.update()
        time.sleep(config.GAME_WIN_SLEEP_DELAY)
        wn.clear()
        wn.bgcolor(config.BACKGROUND_COLOR) 
        wn.bgpic(config.WINNER_GIF)
        turtle.listen() 
        turtle.onkeypress(gl.restart_logic, "r")
        turtle.onkeypress(gl.end_game_function_logic, "q")
        Score(gl.current_gold) # Score is a model class, takes current_gold from game_logic

    # Collision with Doors
    for door_obj in gl.doors[:]: 
        if gl.player.is_collision(door_obj) and gl.player.key is True:
            if system_name == 'Windows': Thread(target=play_sound, args=(config.DOOR_MP3,)).start()
            x_coord = door_obj.xcor()
            y_coord = door_obj.ycor()
            door_obj.destroy()
            if door_obj in gl.doors: gl.doors.remove(door_obj) 
            if (x_coord, y_coord) in gl.doors_locations: gl.doors_locations.remove((x_coord, y_coord))
            gl.player.key = False

    # Collision with Treasures
    for treasure_list in [gl.treasures, gl.treasures_big, gl.treasures_small]:
        for treasure_obj in treasure_list[:]:
            if gl.player.is_collision(treasure_obj):
                if system_name == 'Windows': Thread(target=play_sound, args=(config.TREASURE_MP3,)).start()
                Gold(gl.current_gold, gl.gold_text_x, gl.gold_text_y, config.BACKGROUND_COLOR) 
                gl.player.gold += treasure_obj.gold
                gl.current_gold += treasure_obj.gold
                Gold(gl.current_gold, gl.gold_text_x, gl.gold_text_y, config.GOLD_TEXT_COLOR) 
                treasure_obj.destroy()
                if treasure_obj in treasure_list: treasure_list.remove(treasure_obj)

    # Collision with Friends
    for friend_obj in gl.friends[:]:
        if gl.player.is_collision(friend_obj):
            if system_name == 'Windows': Thread(target=play_sound, args=(config.FRIEND_MP3,)).start()
            x_coord = friend_obj.xcor()
            y_coord = friend_obj.ycor()
            gl.player.key = True
            friend_obj.key = False 
            if gl.player.arrow < config.MAX_PLAYER_ARROWS: gl.player.arrow += 1
            friend_obj.arrow = 0 
            if friend_obj in gl.friends: gl.friends.remove(friend_obj)
            if (x_coord, y_coord) in gl.friends_locations: gl.friends_locations.remove((x_coord, y_coord))
    
    # Collision with Enemies
    for enemy_obj in gl.enemies[:]:
        if gl.player.is_collision(enemy_obj):
            if gl.player.arrow > 0: 
                if system_name == 'Windows': Thread(target=play_sound, args=(config.ENEMY_MP3,)).start()
                enemy_obj.destroy()
                if enemy_obj in gl.enemies: gl.enemies.remove(enemy_obj)
                gl.player.arrow -= 1
            else: # Player takes damage
                if gl.hearts_x_cor: 
                    heart_to_remove_x = max(gl.hearts_x_cor)
                    for heart_obj in gl.hearts[:]:
                        if heart_obj.xcor() == heart_to_remove_x:
                            if system_name == 'Windows': Thread(target=play_sound, args=(config.DAMAGE_MP3,)).start()
                            temp_black_square = BlackSquare() 
                            temp_black_square.goto(heart_obj.xcor(), heart_obj.ycor())
                            temp_black_square.stamp()
                            temp_black_square.hideturtle() 
                            
                            heart_obj.destroy()
                            if heart_obj in gl.hearts: gl.hearts.remove(heart_obj)
                            gl.hearts_x_cor.remove(heart_to_remove_x)
                            
                            if gl.start_point: gl.player.goto(gl.start_point[0][0], gl.start_point[0][1])
                            break 
                
                if not gl.hearts: # No hearts left - Game Over
                    if system_name == 'Windows': Thread(target=play_sound, args=(config.GAME_LOSE_MP3,)).start()
                    gl.player.goto(config.OFF_SCREEN_X, config.OFF_SCREEN_Y) 
                    wn.clear()
                    wn.bgcolor(config.BACKGROUND_COLOR)
                    wn.bgpic(config.LOSER_GIF)
                    wn.title(config.SCREEN_TITLE)
                    wn.setup(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
                    
                    turtle.listen() 
                    turtle.onkeypress(gl.end_game_function_logic, "q")
                    turtle.onkeypress(gl.restart_logic, "r")
                    
                    gl.enemies.clear() # Clear enemies for game over screen
                    gl.setup_maze_logic(game_over_screen) # game_over_screen from LEVELS
                    # No need to restart enemy movement timers here

    wn.update()

if not gl.end_game: # If loop broken by some other means, ensure wn.bye() is called
    wn.bye()
