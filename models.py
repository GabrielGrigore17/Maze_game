import turtle
import config
import random # For Enemy class's initial direction and move method
import math # For Player.is_collision and Enemy.is_close

class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape(config.PLAYER_RIGHT_GIF)
        self.penup()
        self.speed(config.PLAYER_SPEED)
        self.gold = config.INITIAL_PLAYER_GOLD
        self.key = config.INITIAL_PLAYER_HAS_KEY
        self.arrow = config.INITIAL_PLAYER_ARROWS

    def go_up(self, walls_list, doors_locs, friends_locs):
        move_to_x = self.xcor()
        move_to_y = self.ycor() + config.BLOCK_SIZE
        if (move_to_x, move_to_y) not in walls_list and \
           (move_to_x, move_to_y) not in doors_locs and \
           (move_to_x, move_to_y) not in friends_locs:
            self.goto(move_to_x, move_to_y)

    def go_down(self, walls_list, doors_locs, friends_locs):
        move_to_x = self.xcor()
        move_to_y = self.ycor() - config.BLOCK_SIZE
        if (move_to_x, move_to_y) not in walls_list and \
           (move_to_x, move_to_y) not in doors_locs and \
           (move_to_x, move_to_y) not in friends_locs:
            self.goto(move_to_x, move_to_y)

    def go_left(self, walls_list, doors_locs, friends_locs):
        move_to_x = self.xcor() - config.BLOCK_SIZE
        move_to_y = self.ycor()
        self.shape(config.PLAYER_LEFT_GIF)
        if (move_to_x, move_to_y) not in walls_list and \
           (move_to_x, move_to_y) not in doors_locs and \
           (move_to_x, move_to_y) not in friends_locs:
            self.goto(move_to_x, move_to_y)

    def go_right(self, walls_list, doors_locs, friends_locs):
        move_to_x = self.xcor() + config.BLOCK_SIZE
        move_to_y = self.ycor()
        self.shape(config.PLAYER_RIGHT_GIF)
        if (move_to_x, move_to_y) not in walls_list and \
           (move_to_x, move_to_y) not in doors_locs and \
           (move_to_x, move_to_y) not in friends_locs:
            self.goto(move_to_x, move_to_y)

    def is_collision(self, other_turtle_object):
        a = self.xcor() - other_turtle_object.xcor()
        b = self.ycor() - other_turtle_object.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))
        return distance < config.PLAYER_COLLISION_DISTANCE


class Enemy(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape(config.ENEMY_LEFT_GIF)
        self.penup()
        self.speed(config.ENEMY_SPEED)
        self.goto(x, y)
        self.direction = random.choice(["down", "up", "left", "right"])
        # Dependencies to be injected after instantiation
        self.walls_list = None
        self.doors_locs = None
        self.friends_locs = None
        self.player_obj = None

    def set_dependencies(self, walls_list, doors_locs, friends_locs, player_obj):
        self.walls_list = walls_list
        self.doors_locs = doors_locs
        self.friends_locs = friends_locs
        self.player_obj = player_obj

    def move(self):
        if not all([self.walls_list is not None, self.doors_locs is not None, self.friends_locs is not None, self.player_obj is not None]):
            # Dependencies not set, reschedule and skip logic
            turtle.ontimer(self.move, random.randint(config.ENEMY_MOVE_MIN_DELAY, config.ENEMY_MOVE_MAX_DELAY))
            return

        dx = 0
        dy = 0
        if self.direction == "up":
            dy = config.BLOCK_SIZE
        elif self.direction == "down":
            dy = -config.BLOCK_SIZE
        elif self.direction == "left":
            dx = -config.BLOCK_SIZE
            self.shape(config.ENEMY_LEFT_GIF)
        elif self.direction == "right":
            dx = config.BLOCK_SIZE
            self.shape(config.ENEMY_RIGHT_GIF)

        if self.is_close(self.player_obj):
            if self.player_obj.xcor() < self.xcor(): self.direction = "left"
            elif self.player_obj.xcor() > self.xcor(): self.direction = "right"
            elif self.player_obj.ycor() < self.ycor(): self.direction = "down"
            elif self.player_obj.ycor() > self.ycor(): self.direction = "up"
            
            # Update dx/dy based on new direction toward player
            if self.direction == "up": dx, dy = 0, config.BLOCK_SIZE
            elif self.direction == "down": dx, dy = 0, -config.BLOCK_SIZE
            elif self.direction == "left": dx, dy = -config.BLOCK_SIZE, 0
            elif self.direction == "right": dx, dy = config.BLOCK_SIZE, 0
        
        move_to_x = self.xcor() + dx
        move_to_y = self.ycor() + dy

        if (move_to_x, move_to_y) not in self.walls_list and \
           (move_to_x, move_to_y) not in self.doors_locs and \
           (move_to_x, move_to_y) not in self.friends_locs:
            self.goto(move_to_x, move_to_y)
        else:
            self.direction = random.choice(["down", "up", "left", "right"])
        
        turtle.ontimer(self.move, random.randint(config.ENEMY_MOVE_MIN_DELAY, config.ENEMY_MOVE_MAX_DELAY))

    def is_close(self, other_turtle_object):
        a = self.xcor() - other_turtle_object.xcor()
        b = self.ycor() - other_turtle_object.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))
        return distance < config.ENEMY_DETECTION_RADIUS

    def destroy(self):
        self.goto(config.OFF_SCREEN_X, config.OFF_SCREEN_Y)
        self.hideturtle()

class Friend(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape(config.FRIEND_GIF)
        self.penup()
        self.speed(config.PEN_SPEED) 
        self.key = config.INITIAL_FRIEND_HAS_KEY
        self.arrow = config.INITIAL_FRIEND_ARROWS
        self.goto(x, y)

class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape(config.WALL_GIF)
        self.penup()
        self.speed(config.PEN_SPEED)

class BlackSquare(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape(config.BLACK_SQUARE_GIF)
        self.penup()
        self.speed(config.BLACK_SQUARE_SPEED)

class Health(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape(config.HEART_GIF)
        self.penup()
        self.speed(config.HEALTH_SPEED)
        self.goto(x, y)

    def destroy(self): 
        self.goto(config.OFF_SCREEN_X, config.OFF_SCREEN_Y)
        self.hideturtle()

class Treasure(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape(config.TREASURE_GIF)
        self.penup()
        self.speed(config.TREASURE_SPEED)
        self.gold = config.TREASURE_NORMAL_GOLD
        self.goto(x, y)

    def destroy(self): 
        self.goto(config.OFF_SCREEN_X, config.OFF_SCREEN_Y)
        self.hideturtle()

class TreasureSmall(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape(config.TREASURE_SMALL_GIF)
        self.penup()
        self.speed(config.TREASURE_SPEED)
        self.gold = config.TREASURE_SMALL_GOLD
        self.goto(x, y)

    def destroy(self): 
        self.goto(config.OFF_SCREEN_X, config.OFF_SCREEN_Y)
        self.hideturtle()

class TreasureBig(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape(config.TREASURE_BIG_GIF)
        self.penup()
        self.speed(config.TREASURE_SPEED)
        self.gold = config.TREASURE_BIG_GOLD
        self.goto(x, y)

    def destroy(self): 
        self.goto(config.OFF_SCREEN_X, config.OFF_SCREEN_Y)
        self.hideturtle()

class Key(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape(config.KEY_GIF)
        self.penup()
        self.speed(config.KEY_SPEED)

class Arrow(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape(config.ARROW_GIF)
        self.penup()
        self.speed(config.ARROW_SPEED)

class ArrowNumber(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape(config.ONE_GIF) 
        self.penup()
        self.speed(config.ARROW_NUMBER_SPEED)

class Gold(turtle.Turtle): 
    def __init__(self, value, x, y, color):
        turtle.Turtle.__init__(self)
        self.color(color)
        self.penup()
        self.speed(config.PEN_SPEED) 
        self.goto(x, y)
        self.write("Gold: {}".format(value), move=False, align="right", font=config.GOLD_FONT)
        self.hideturtle()

class Score(turtle.Turtle): 
    def __init__(self, value):
        turtle.Turtle.__init__(self)
        self.color(config.SCORE_TEXT_COLOR)
        self.penup()
        self.speed(config.PEN_SPEED)
        self.write("Score: {}".format(value), move=False, align="center", font=config.SCORE_FONT)
        self.hideturtle()

class Door(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape(config.DOOR_GIF)
        self.penup()
        self.speed(config.DOOR_SPEED)
        self.goto(x, y)

    def destroy(self): 
        self.goto(config.OFF_SCREEN_X, config.OFF_SCREEN_Y)
        self.hideturtle()

class Stairs(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape(config.STAIRS_GIF)
        self.penup()
        self.speed(config.STAIRS_SPEED)
        self.goto(x, y)

class GameOver(turtle.Turtle): 
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square") 
        self.color(config.GAME_OVER_SHAPE_COLOR)
        self.penup()
        self.speed(config.GAME_OVER_SPEED)

class GameWin(turtle.Turtle): 
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape(config.EXIT_GIF)
        self.penup()
        self.speed(config.GAME_WIN_SPEED)
        self.goto(x, y)
