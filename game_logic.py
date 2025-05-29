import turtle 
import math
import random 
import config
from LEVELS import level_1, level_2, level_3, game_over_screen 
from models import (Player, Pen, GameOver, Key, Arrow, ArrowNumber, 
                    Stairs, GameWin, Health, Treasure, TreasureSmall, 
                    TreasureBig, Enemy, Friend, Door, Gold)

# --- Global Game State Variables ---
end_game = False

levels = ["", level_1, level_2, level_3] 
treasures = []
treasures_small = []
treasures_big = []
current_gold = config.INITIAL_PLAYER_GOLD
gold_text_x = 0 
gold_text_y = 0 
doors = []
doors_locations = []
enemies = [] 
friends = []
friends_locations = []
walls = [] 
start_point = [] 
hearts = []      
hearts_x_cor = [] 
current_level = config.DEFAULT_LEVEL_INDEX

# Instantiate game objects 
player = Player()
pen = Pen() 
game_over = GameOver() 
key = Key() 
arrow = Arrow() 
arrow_number = ArrowNumber() 
stairs = Stairs(config.FAR_OFF_SCREEN_X, config.FAR_OFF_SCREEN_Y) 
game_win = GameWin(config.FAR_OFF_SCREEN_X, config.FAR_OFF_SCREEN_Y) 

# --- Core Game Functions ---

def end_game_function_logic():
    global end_game
    end_game = True

def restart_logic():
    import sys 
    import os  
    os.execv(sys.executable, ['python'] + sys.argv)

# Initial setup of hearts 
for y_H in range(len(level_1)): 
    for x_H in range(len(level_1[y_H])):
        character_H = level_1[y_H][x_H]
        screen_x_H = config.MAZE_START_X + (x_H * config.BLOCK_SIZE)
        screen_y_H = config.MAZE_START_Y - (y_H * config.BLOCK_SIZE)
        if character_H == "H":
            hearts_x_cor.append(screen_x_H)
            hearts.append(Health(screen_x_H, screen_y_H))

def setup_maze_logic(level_data: list) -> None:
    # Explicitly declare which module-level variables we are modifying
    global gold_text_x, gold_text_y, current_gold
    global player, pen, game_over, key, arrow, arrow_number, stairs, game_win
    global levels, treasures, treasures_small, treasures_big, doors, doors_locations
    global enemies, friends, friends_locations, walls, start_point, hearts, hearts_x_cor, current_level
    
    walls.clear()
    doors.clear()
    doors_locations.clear()
    treasures.clear()
    treasures_small.clear()
    treasures_big.clear()
    enemies.clear() 
    friends.clear()
    friends_locations.clear()
    start_point.clear()

    # Reset visual state of persistent UI elements that might have been stamped
    game_over.goto(config.OFF_SCREEN_X, config.OFF_SCREEN_Y) 

    for y in range(len(level_data)):
        for x in range(len(level_data[y])):
            character = level_data[y][x]
            screen_x = config.MAZE_START_X + (x * config.BLOCK_SIZE)
            screen_y = config.MAZE_START_Y - (y * config.BLOCK_SIZE)

            if character == "X":
                pen.goto(screen_x, screen_y)
                pen.stamp()
                walls.append((screen_x, screen_y))
            elif character == "P":
                player.goto(screen_x, screen_y)
                start_point.append([screen_x, screen_y])
            elif character == "T": treasures.append(Treasure(screen_x, screen_y))
            elif character == "B": treasures_big.append(TreasureBig(screen_x, screen_y))
            elif character == "C": treasures_small.append(TreasureSmall(screen_x, screen_y))
            elif character == "E":
                new_enemy = Enemy(screen_x, screen_y)
                # Dependencies (walls, player etc.) are now module globals in game_logic
                new_enemy.set_dependencies(walls, doors_locations, friends_locations, player)
                enemies.append(new_enemy)
            elif character == "G": # Game Over stamp positions
                game_over.goto(screen_x, screen_y)
                game_over.stamp()
            elif character == "F":
                friends.append(Friend(screen_x, screen_y))
                friends_locations.append((screen_x, screen_y))
            elif character == "K": # Key's initial position (usually hidden)
                key.goto(screen_x, screen_y)
                key.hideturtle()
            elif character == "D":
                doors.append(Door(screen_x, screen_y))
                doors_locations.append((screen_x, screen_y))
            elif character == "A": # Arrow icon's initial position
                arrow.goto(screen_x, screen_y)
                arrow.hideturtle()
            elif character == "Q": # Arrow number display's initial position
                arrow_number.goto(screen_x, screen_y)
                arrow_number.hideturtle()
            elif character == "S": # Gold text display position
                gold_text_x = screen_x 
                gold_text_y = screen_y 
                # Gold class is for displaying text, not a global variable to be reassigned
                Gold(current_gold, screen_x, screen_y, config.GOLD_TEXT_COLOR) 
            elif character == "N": # Stairs to next level
                stairs = Stairs(screen_x, screen_y) 
            elif character == "W": # Game win / exit object
                game_win = GameWin(screen_x, screen_y)
