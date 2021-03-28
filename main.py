import turtle
import math
import random
import time
from LEVELS import *
from threading import Thread
from platform import system
system = system()  # storing the name of the system (Windows, Unix etc.) to help avoid errors with sound playing
end_game = False  # variable used to signal the end of the game


# I got this bit of code of the internet to help me play sounds. I have no idea how it works :)
# I should also add that it only works on Windows
# If you use Unix or something else the sounds won't work but hopefully everything else works
########################################################################################################################
class PlaySoundException(Exception):
    pass


def play_sound(sound, block=True):

    from ctypes import c_buffer, windll
    from random import random
    from time import sleep
    from sys import getfilesystemencoding

    def win_command(*command):
        buf = c_buffer(255)
        command = ' '.join(command).encode(getfilesystemencoding())
        error_code = int(windll.winmm.mciSendStringA(command, buf, 254, 0))
        if error_code:
            error_buffer = c_buffer(255)
            windll.winmm.mciGetErrorStringA(error_code, error_buffer, 254)
            exception_message = ('\n    Error ' + str(error_code) + ' for command:'
                                 '\n        ' + command.decode() +
                                 '\n    ' + error_buffer.value.decode())
            raise PlaySoundException(exception_message)
        return buf.value

    alias = 'playsound_' + str(random())
    win_command('open "' + sound + '" alias', alias)
    win_command('set', alias, 'time format milliseconds')
    duration_in_ms = win_command('status', alias, 'length')
    win_command('play', alias, 'from 0 to', duration_in_ms.decode())

    if block:
        sleep(float(duration_in_ms) / 1000.0)

########################################################################################################################


def end_game_function():
    """
    Ends the game

    :return: None
    """
    global end_game
    end_game = True


def restart():
    """
    Restarts the game by ending the current script and executing it from the beginning.

    :return: None
    """
    import sys
    import os
    os.execv(sys.executable, ['python'] + sys.argv)


wn = turtle.Screen()  # declaring the screen we are going to work on
wn.bgcolor("black")  # setting the background color
wn.title("Sandi's Maze")  # setting the title of the screen
wn.setup(700, 700)  # setting the height and width in pixels
wn.tracer(0)  # turning off drawing animations

# registering all of the textures for the in-game elements
turtle.register_shape(r"Resources\player_right.gif")
turtle.register_shape(r"Resources\player_left.gif")
turtle.register_shape(r"Resources\wall.gif")
turtle.register_shape(r"Resources\treasure.gif")
turtle.register_shape(r"Resources\treasure_small.gif")
turtle.register_shape(r"Resources\treasure_big.gif")
turtle.register_shape(r"Resources\enemy_left.gif")
turtle.register_shape(r"Resources\enemy_right.gif")
turtle.register_shape(r"Resources\heart.gif")
turtle.register_shape(r"Resources\key.gif")
turtle.register_shape(r"Resources\friend.gif")
turtle.register_shape(r"Resources\door.gif")
turtle.register_shape(r"Resources\arrow.gif")
turtle.register_shape(r"Resources\stairs.gif")
turtle.register_shape(r"Resources\black_square.gif")
turtle.register_shape(r"Resources\dungeon_1.gif")
turtle.register_shape(r"Resources\dungeon_2.gif")
turtle.register_shape(r"Resources\dungeon_3.gif")
turtle.register_shape(r"Resources\exit.gif")
turtle.register_shape(r"Resources\black_background.gif")
turtle.register_shape(r"Resources\winner.gif")
turtle.register_shape(r"Resources\loser.gif")
turtle.register_shape(r"Resources\one.gif")
turtle.register_shape(r"Resources\two.gif")
turtle.register_shape(r"Resources\three.gif")
turtle.register_shape(r"Resources\four.gif")
turtle.register_shape(r"Resources\five.gif")

if system == 'Windows':  # checking to see if the system we run on is a windows system
    # creating a separate thread to play the background music (if we don't do this, the game can't continue
    # until the music is over)
    # daemon=True means that the thread will be forcefully stopped once the main program has finished
    thread = Thread(target=play_sound, args=(r"Resources\theme.mp3",), daemon=True)
    thread.start()  # starting the thread

# creating the illusion of a loading screen by iterating through three pictures four times
for i in range(4):
    wn.bgpic(r"Resources\dungeon_1.gif")  # setting the background
    wn.update()  # updating the screen
    time.sleep(0.5)  # waiting 0.5 seconds
    wn.bgpic(r"Resources\dungeon_2.gif")  # setting the background
    wn.update()  # updating the screen
    time.sleep(0.5)  # waiting 0.5 seconds
    wn.bgpic(r"Resources\dungeon_3.gif")  # setting the background
    wn.update()  # updating the screen
    time.sleep(0.5)  # waiting 0.5 seconds


class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape(r"Resources\player_right.gif")  # giving the player texture
        self.penup()  # not leaving traces on the screen when we move the player around
        self.speed(0)  # setting the animation speed to the fastest value
        self.gold = 0  # variable that stores the current score of the player
        self.key = False  # variable that stores whether or not the player has a key
        self.arrow = 0  # variable that stores the number of arrows that the player has

    def go_up(self):
        """
        Moves the player up by one block. If the upper neighbour is a wall, a friend or an unopened door
        the command is not executed.

        :return: None
        """
        move_to_x = self.xcor()
        move_to_y = self.ycor() + 24

        # testing to see if the neighbour is a wall, a friend or an unopened door
        if (move_to_x, move_to_y) not in walls and (move_to_x, move_to_y) not in doors_locations \
                and (move_to_x, move_to_y) not in friends_locations:
            self.goto(move_to_x, move_to_y)

    def go_down(self):
        """
        Moves the player down by one block. If the lower neighbour is a wall, a friend or an unopened door
        the command is not executed.

        :return: None
        """
        move_to_x = self.xcor()
        move_to_y = self.ycor() - 24

        # testing to see if the neighbour is a wall, a friend or an unopened door
        if (move_to_x, move_to_y) not in walls and (move_to_x, move_to_y) not in doors_locations\
                and (move_to_x, move_to_y) not in friends_locations:
            self.goto(move_to_x, move_to_y)

    def go_left(self):
        """
        Moves the player left by one block. If the left neighbour is a wall, a friend or an unopened door
        the command is not executed.

        :return: None
        """
        move_to_x = self.xcor() - 24
        move_to_y = self.ycor()
        self.shape(r"Resources\player_left.gif")  # changing the texture in order to have the player face left

        # testing to see if the neighbour is a wall, a friend or an unopened door
        if (move_to_x, move_to_y) not in walls and (move_to_x, move_to_y) not in doors_locations \
                and (move_to_x, move_to_y) not in friends_locations:
            self.goto(move_to_x, move_to_y)

    def go_right(self):
        """
        Moves the player right by one block. If the right neighbour is a wall, a friend or an unopened door
        the command is not executed.

        :return: None
        """
        move_to_x = self.xcor() + 24
        move_to_y = self.ycor()
        self.shape(r"Resources\player_right.gif")  # changing the texture in order to have the player face right

        # testing to see if the neighbour is a wall, a friend or an unopened door
        if (move_to_x, move_to_y) not in walls and (move_to_x, move_to_y) not in doors_locations \
                and (move_to_x, move_to_y) not in friends_locations:
            self.goto(move_to_x, move_to_y)

    def is_collision(self, other):
        """
        Testing to see if the player is within a block sized radius away from an map element

        :param other: any map element (has to be an object that inherits the turtle class)
        :return: boolean indicating collision state
        """
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))  # distance between self and other

        if distance < 26:
            return True
        else:
            return False


class Enemy(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape(r"Resources\enemy_left.gif")  # giving the enemy texture
        self.penup()  # not leaving traces on the screen when the enemy moves around
        self.speed(0)  # setting the animation speed to the fastest value
        self.goto(x, y)  # sending the enemy to its start location
        self.direction = random.choice(["down", "up", "left", "right"])  # randomly deciding the next possible move

    def move(self):
        """
        Moves the enemy by one block in a random direction. If the neighbour is a wall,
        a friend or an unopened door the command is not executed. If the player is close, the enemy
        will chase him instead of moving around randomly.

        :return: None
        """
        if self.direction == "up":
            dx = 0
            dy = 24
        elif self.direction == "down":
            dx = 0
            dy = -24
        elif self.direction == "left":
            dx = -24
            dy = 0
            self.shape(r"Resources\enemy_left.gif")  # changing the texture in order to have the enemy face left
        elif self.direction == "right":
            dx = 24
            dy = 0
            self.shape(r"Resources\enemy_right.gif")  # changing the texture in order to have the enemy face left
        else:
            dx = 0
            dy = 0

        # if the player is close the enemy will try to go in his direction
        if self.is_close(player):
            if player.xcor() < self.xcor():
                self.direction = "left"
            elif player.xcor() > self.xcor():
                self.direction = "right"
            elif player.ycor() < self.ycor():
                self.direction = "down"
            elif player.ycor() > self.ycor():
                self.direction = "up"

        move_to_x = self.xcor() + dx
        move_to_y = self.ycor() + dy

        # testing to see if the neighbour is a wall, a friend or an unopened door
        if (move_to_x, move_to_y) not in walls and (move_to_x, move_to_y) not in doors_locations \
                and (move_to_x, move_to_y) not in friends_locations:
            self.goto(move_to_x, move_to_y)
        else:
            self.direction = random.choice(["down", "up", "left", "right"])  # changing direction

        # calling the function within itself indefinitely with a random delay until the game ends
        turtle.ontimer(self.move, t=random.randint(100, 300))

    def is_close(self, other):
        """
        Testing to see if the player is within a specified radius away from the enemy

        :param other: the player
        :return: boolean indicating if the closeness conditions are met
        """
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))  # distance between self and other

        if distance < 100:
            return True
        else:
            return False

    def destroy(self):
        """
        Destroying the enemy both by moving it outside of the map and hiding it from view.
        (you can never be too sure :) )

        :return: None
        """
        self.goto(2000, 2000)  # sending the enemy outside of the map
        self.hideturtle()  # hiding the enemy from view


class Friend(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape(r"Resources\friend.gif")  # giving the friend texture
        self.penup()  # not leaving traces on the screen when we move the friend
        self.speed(0)  # setting the animation speed to the fastest value
        self.key = True  # variable that stores whether or not the friend has a key
        self.arrow = 1  # variable that stores the number of arrows that the friend has
        self.goto(x, y)  # sending the enemy to its location


class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape(r"Resources\wall.gif")  # giving the wall texture
        self.penup()  # not leaving traces on the screen when we draw the wall
        self.speed(0)  # setting the animation speed to the fastest value


class BlackSquare(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape(r"Resources\black_square.gif")  # giving the square texture
        self.penup()  # not leaving traces on the screen when we draw the square
        self.speed(0)  # setting the animation speed to the fastest value


class Health(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape(r"Resources\heart.gif")  # giving the heart texture
        self.penup()  # not leaving traces on the screen when we draw the heart
        self.speed(0)  # setting the animation speed to the fastest value
        self.goto(x, y)  # sending the heart to its location

    def destroy(self):
        """
        Destroying the heart both by moving it outside of the map and hiding it from view.
        (you can never be too sure :) )

        :return: None
        """
        self.goto(2000, 2000)  # sending the heart outside of the map
        self.hideturtle()  # hiding the heart from view


class Treasure(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape(r"Resources\treasure.gif")  # giving the treasure texture
        self.penup()  # not leaving traces on the screen when we draw the treasure
        self.speed(0)  # setting the animation speed to the fastest value
        self.gold = 100  # storing the value of this kind of treasure
        self.goto(x, y)  # sending the treasure to its location

    def destroy(self):
        """
        Destroying the treasure both by moving it outside of the map and hiding it from view.
        (you can never be too sure :) )

        :return: None
        """
        self.goto(2000, 2000)  # sending the treasure outside of the map
        self.hideturtle()  # hiding the treasure from view


class TreasureSmall(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape(r"Resources\treasure_small.gif")  # giving the treasure texture
        self.penup()  # not leaving traces on the screen when we draw the treasure
        self.speed(0)  # setting the animation speed to the fastest value
        self.gold = 25  # storing the value of this kind of treasure
        self.goto(x, y)  # sending the treasure to its location

    def destroy(self):
        """
        Destroying the treasure both by moving it outside of the map and hiding it from view.
        (you can never be too sure :) )

        :return: None
        """
        self.goto(2000, 2000)  # sending the treasure outside of the map
        self.hideturtle()  # hiding the treasure from view


class TreasureBig(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape(r"Resources\treasure_big.gif")  # giving the treasure texture
        self.penup()  # not leaving traces on the screen when we draw the treasure
        self.speed(0)  # setting the animation speed to the fastest value
        self.gold = 250  # storing the value of this kind of treasure
        self.goto(x, y)  # sending the treasure to its location

    def destroy(self):
        """
        Destroying the treasure both by moving it outside of the map and hiding it from view.
        (you can never be too sure :) )

        :return: None
        """
        self.goto(2000, 2000)  # sending the treasure outside of the map
        self.hideturtle()  # hiding the treasure from view


class Key(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape(r"Resources\key.gif")  # giving the key texture
        self.penup()  # not leaving traces on the screen when we draw the key
        self.speed(0)  # setting the animation speed to the fastest value


class Arrow(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape(r"Resources\arrow.gif")  # giving the arrow texture
        self.penup()  # not leaving traces on the screen when we draw the arrow
        self.speed(0)  # setting the animation speed to the fastest value


class ArrowNumber(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape(r"Resources\one.gif")  # giving the arrow number texture
        self.penup()  # not leaving traces on the screen when we draw the arrow number
        self.speed(0)  # setting the animation speed to the fastest value


class Gold(turtle.Turtle):
    def __init__(self, value, x, y, color):
        turtle.Turtle.__init__(self)
        self.color(color)  # setting the text color to the color received in the constructor
        self.penup()  # not leaving traces on the screen when we draw the gold
        self.speed(0)  # setting the animation speed to the fastest value
        self.goto(x, y)  # sending the text to its location
        # writing the text on the screen
        self.write("Gold: {}".format(value), move=False, align="right", font=("ocr a extended", 14, "normal"))
        self.hideturtle()  # hiding the turtle so that only the text remains


class Score(turtle.Turtle):
    def __init__(self, value):
        turtle.Turtle.__init__(self)
        self.color("black")  # setting the text color
        self.penup()  # not leaving traces on the screen when we draw the score
        self.speed(0)  # setting the animation speed to the fastest value
        # writing the text on the screen
        self.write("Score: {}".format(value), move=False, align="center", font=("impact", 50, "bold"))
        self.hideturtle()  # hiding the turtle so that only the text remains


class Door(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape(r"Resources\door.gif")  # giving the door texture
        self.penup()  # not leaving traces on the screen when we draw the door
        self.speed(0)  # setting the animation speed to the fastest value
        self.goto(x, y)  # sending the door to its location

    def destroy(self):
        """
        Destroying the door both by moving it outside of the map and hiding it from view.
        (you can never be too sure :) )

        :return: None
        """
        self.goto(2000, 2000)  # sending the door outside of the map
        self.hideturtle()  # hiding the door from view


class Stairs(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape(r"Resources\stairs.gif")  # giving the stairs texture
        self.penup()  # not leaving traces on the screen when we draw the stairs
        self.speed(0)  # setting the animation speed to the fastest value
        self.goto(x, y)  # sending the stairs to their location


class GameOver(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")  # setting the shape
        self.color("red")  # setting the color
        self.penup()  # not leaving traces on the screen when we draw GAME OVER
        self.speed(0)  # setting the animation speed to the fastest value


class GameWin(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape(r"Resources\exit.gif")  # giving the exit texture
        self.penup()  # not leaving traces on the screen when we draw the exit
        self.speed(0)  # setting the animation speed to the fastest value
        self.goto(x, y)  # sending the exit to its location


levels = [""]  # creating the levels list
treasures = []  # creating the medium treasures list
treasures_small = []  # creating the small treasures list
treasures_big = []  # creating the big treasures list
current_gold = 0  # creating the variable that stores the current score of the player
gold_text_x = 0  # x coordinate of the "Gold: ..." text
gold_text_y = 0  # y coordinate of the "Gold: ..." text
doors = []  # creating the doors list
doors_locations = []  # list that stores the locations of the doors (to help with collision)
stairs = Stairs(3000, 3000)  # instantiating the Stairs class and sending the object outside the map
game_win = GameWin(3000, 3000)  # instantiating the GameWin class and sending the object outside the map
enemies = []  # creating the enemies list
friends = []  # creating the friends list
friends_locations = []  # list that stores the locations of the friends (to help with collision)
pen = Pen()  # instantiating the Pen class
game_over = GameOver()  # instantiating the GameOver class
player = Player()  # instantiating the Player class
key = Key()  # instantiating the Key class
arrow = Arrow()  # instantiating the Arrow class
arrow_number = ArrowNumber()  # instantiating the ArrowNumber class
walls = []  # list that stores the locations of the walls (to help with collision)
start_point = []  # storing the start position for the player
hearts = []  # creating the hearts list
hearts_x_cor = []  # storing the order of the hearts (the one in the right is always the first one to go)
current_level = 1  # storing the current level


# iterating through the first level matrix to get the health
# we are doing this outside of the setup_maze function in order to avoid resetting the health on every level
for y_H in range(len(level_1)):
    for x_H in range(len(level_1[y_H])):
        character_H = level_1[y_H][x_H]  # storing the current letter of the matrix
        # setting the coordinates for the element
        screen_x_H = -288 + (x_H * 24)
        screen_y_H = 288 - (y_H * 24)
        if character_H == "H":  # if the character is a H then we've found where the hearts are supposed to be
            hearts_x_cor.append(screen_x_H)  # adding the x coordinate of the heart to the list
            hearts.append(Health(screen_x_H, screen_y_H))  # adding the heart to the hearts list


def setup_maze(level: list) -> None:
    """
    This function reads a level from a list of strings and it sets up
    the GUI based on the characters it sees.

    :param level: game level in text format
    :return: None
    """
    # sending the element outside of the map because it remains in the middle of the screen when it's not used
    game_over.goto(2000, 2000)
    # iterating through the current level matrix
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]  # storing the current letter of the matrix
            # setting the coordinates for the element that is about to be pinned to the GUI
            screen_x = -288 + (x * 24)
            screen_y = 288 - (y * 24)
            if character == "X":  # X means WALL
                pen.goto(screen_x, screen_y)
                pen.stamp()  # stamping the wall gif in every appropriate place
                walls.append((screen_x, screen_y))
            if character == "P":  # P means PLAYER
                player.goto(screen_x, screen_y)
                start_point.append([screen_x, screen_y])
            if character == "T":  # T means NORMAL TREASURE
                treasures.append(Treasure(screen_x, screen_y))
            if character == "B":  # B means BIG TREASURE
                treasures_big.append(TreasureBig(screen_x, screen_y))
            if character == "C":  # C means SMALL TREASURE
                treasures_small.append(TreasureSmall(screen_x, screen_y))
            if character == "E":  # E means ENEMY
                enemies.append(Enemy(screen_x, screen_y))
            if character == "G":  # G means GAME OVER SQUARE
                game_over.goto(screen_x, screen_y)
                game_over.stamp()
            if character == "F":  # F means FRIEND
                friends.append(Friend(screen_x, screen_y))
                friends_locations.append((screen_x, screen_y))
            if character == "K":  # K means KEY
                key.goto(screen_x, screen_y)
                key.hideturtle()
            if character == "D":  # D means DOOR
                doors.append(Door(screen_x, screen_y))
                doors_locations.append((screen_x, screen_y))
            if character == "A":  # A means ARROW
                arrow.goto(screen_x, screen_y)
                arrow.hideturtle()
            if character == "Q":  # Q means ARROW NUMBER
                arrow_number.goto(screen_x, screen_y)
                arrow_number.hideturtle()
            if character == "S":  # S means CURRENT SCORE ("Gold:...")
                global gold_text_x, gold_text_y
                gold_text_x = screen_x
                gold_text_y = screen_y
                Gold(current_gold, screen_x, screen_y, "red")
            if character == "N":  # N means STAIRS
                global stairs
                stairs = Stairs(screen_x, screen_y)
            if character == "W":  # W means EXIT
                global game_win
                game_win = GameWin(screen_x, screen_y)


# any of these lines except for the last one can be deactivated for a shorter game experience
levels.append(level_1)
levels.append(level_2)
levels.append(level_3)

wn.bgpic(r"Resources\black_background.gif")  # setting up the background image

setup_maze(levels[1])  # loading in the first level

# associating different functions with keys
turtle.listen()
turtle.onkeypress(player.go_left, "Left")
turtle.onkeypress(player.go_right, "Right")
turtle.onkeypress(player.go_down, "Down")
turtle.onkeypress(player.go_up, "Up")
turtle.onkeypress(end_game_function, "q")
turtle.onkeypress(restart, "r")

wn.tracer(0)  # avoiding animations


# kicking the enemies into motion
for enemy in enemies:
    turtle.ontimer(enemy.move, t=250)

# main loop
while True:
    if end_game:  # testing to see if the player pressed Q
        break

    if player.key:  # condition to show the key icon on screen
        key.showturtle()
    else:
        key.hideturtle()

    if player.arrow:  # condition to show the arrow icon on screen
        arrow.showturtle()
        arrow_number.showturtle()
    else:
        arrow.hideturtle()
        arrow_number.hideturtle()

    if player.arrow == 1:  # updating the number of arrows on screen
        arrow_number.shape(r"Resources\one.gif")
    elif player.arrow == 2:
        arrow_number.shape(r"Resources\two.gif")
    elif player.arrow == 3:
        arrow_number.shape(r"Resources\three.gif")
    elif player.arrow == 4:
        arrow_number.shape(r"Resources\four.gif")
    elif player.arrow == 5:
        arrow_number.shape(r"Resources\five.gif")
    else:
        arrow_number.hideturtle()

    if player.is_collision(stairs):  # condition to go to the next level
        # playing the level up sound
        if system == 'Windows':
            Thread(target=play_sound, args=(r"Resources\next_level.mp3",)).start()
        # resetting every asset ##############
        wn.clear()
        wn.bgcolor("black")
        wn.title("A Maze Game")
        wn.setup(700, 700)
        wn.tracer(0)
        current_level += 1
        treasures = []
        treasures_small = []
        treasures_big = []
        gold_text_x = 0
        gold_text_y = 0
        doors = []
        doors_locations = []
        stairs = Stairs(3000, 3000)
        game_win = GameWin(3000, 3000)
        enemies = []
        friends = []
        friends_locations = []
        pen = Pen()
        game_over = GameOver()
        arrows = player.arrow
        player = Player()
        player.arrow = arrows
        key = Key()
        arrow = Arrow()
        arrow_number = ArrowNumber()
        walls = []
        start_point = []
        ######################################
        setup_maze(levels[current_level])  # loading in the next level
        for heart in hearts:  # loading in the lives from the previous level as lives don't reset
            heart.stamp()
        # associating different functions with keys again
        # I have no idea why this is necessary but apparently it is
        turtle.listen()
        turtle.onkeypress(player.go_left, "Left")
        turtle.onkeypress(player.go_right, "Right")
        turtle.onkeypress(player.go_down, "Down")
        turtle.onkeypress(player.go_up, "Up")
        turtle.onkeypress(restart, "r")
        turtle.onkeypress(end_game_function, "q")

        wn.tracer(0)
        for enemy in enemies:  # kicking the enemies into motion
            turtle.ontimer(enemy.move, t=250)

    if player.is_collision(game_win):  # condition to win the game
        player.goto(2000, 2000)  # unloading the player from the map
        # playing the winning sound
        if system == 'Windows':
            Thread(target=play_sound, args=(r"Resources\game_win.mp3",)).start()
        wn.update()
        time.sleep(1)
        wn.clear()  # unloading every asset
        wn.bgpic(r"Resources\winner.gif")  # setting the winning background picture
        # making sure the quit and restart buttons still work
        turtle.listen()
        turtle.onkeypress(restart, "r")
        turtle.onkeypress(end_game_function, "q")
        Score(current_gold)  # loading the score on the screen

    # testing every door to see if the player both is near and has a key
    for door in doors:
        if player.is_collision(door) and player.key is True:
            # playing the door sound
            if system == 'Windows':
                Thread(target=play_sound, args=(r"Resources\door.mp3",)).start()
            x_coord = door.xcor()
            y_coord = door.ycor()
            # getting rid of the door
            door.destroy()
            doors.remove(door)
            doors_locations.remove((x_coord, y_coord))
            player.key = False  # removing the key from the player

    # testing every treasure to see if the player is near
    for treasure in treasures:
        if player.is_collision(treasure):
            # playing the treasure sound
            if system == 'Windows':
                Thread(target=play_sound, args=(r"Resources\treasure.mp3",)).start()
            # covering up the old score via writing over it with black
            # I know it's a horrible way to do things but I couldn't think of anything else
            Gold(current_gold, gold_text_x, gold_text_y, "black")
            # updating the score
            player.gold += treasure.gold
            current_gold += treasure.gold
            # showing the new score on the screen
            Gold(current_gold, gold_text_x, gold_text_y, "red")
            # removing the treasure
            treasure.destroy()
            treasures.remove(treasure)

    # same as for the normal treasure described above
    for treasure in treasures_big:
        if player.is_collision(treasure):
            if system == 'Windows':
                Thread(target=play_sound, args=(r"Resources\treasure.mp3",)).start()
            Gold(current_gold, gold_text_x, gold_text_y, "black")
            player.gold += treasure.gold
            current_gold += treasure.gold
            Gold(current_gold, gold_text_x, gold_text_y, "red")
            treasure.destroy()
            treasures_big.remove(treasure)

    # same as for the normal treasure described above
    for treasure in treasures_small:
        if player.is_collision(treasure):
            if system == 'Windows':
                Thread(target=play_sound, args=(r"Resources\treasure.mp3",)).start()
            Gold(current_gold, gold_text_x, gold_text_y, "black")
            player.gold += treasure.gold
            current_gold += treasure.gold
            Gold(current_gold, gold_text_x, gold_text_y, "red")
            treasure.destroy()
            treasures_small.remove(treasure)

    # testing every friend to see if the player is near
    for friend in friends:
        if player.is_collision(friend):
            # playing the friend sound
            if system == 'Windows':
                Thread(target=play_sound, args=(r"Resources\friend.mp3",)).start()
            x_coord = friend.xcor()
            y_coord = friend.ycor()
            # getting a key and an arrow from the friend
            player.key = True
            friend.key = False
            if player.arrow < 5:
                player.arrow += 1
            friend.arrow = 0
            # removing the friend from the checking list
            friends.remove(friend)

    # testing every enemy to see if the player is near
    for enemy in enemies:
        if player.is_collision(enemy):
            # if the player has arrows then the enemy dies and the rest of the instructions won't execute
            if player.arrow:
                # playing the enemy death sound
                if system == 'Windows':
                    Thread(target=play_sound, args=(r"Resources\enemy.mp3",)).start()
                enemy.destroy()
                enemies.remove(enemy)
                player.arrow -= 1  # decrementing the arrows number
                continue
            # if the player has no arrows then he dies and looses a life
            for heart in hearts:
                if heart.xcor() == max(hearts_x_cor):
                    # playing the player damage sound
                    if system == 'Windows':
                        Thread(target=play_sound, args=(r"Resources\damage.mp3",)).start()
                    # removing a life from the player
                    # again it's a very bad way to do it but I couldn't come up with anything else
                    black_square = BlackSquare()
                    black_square.goto(heart.xcor(), heart.ycor())
                    black_square.stamp()
                    heart.destroy()
                    hearts.remove(heart)
                    hearts_x_cor.remove(max(hearts_x_cor))
                    # player returns to the spawn point
                    player.goto(start_point[0][0], start_point[0][1])
            # if the player has no lives left then it's game over
            if not len(hearts):
                # playing the game over sound
                if system == 'Windows':
                    Thread(target=play_sound, args=(r"Resources\game_lose.mp3",)).start()
                player.goto(2000, 2000)
                wn.clear()  # unloading every asset
                wn.bgpic(r"Resources\loser.gif")  # setting up the game over background
                wn.title("Sandi's Maze")
                wn.setup(700, 700)
                # making sure the keys still work
                # I have no idea why I have to set them up every single time
                turtle.listen()
                turtle.onkeypress(player.go_left, "Left")
                turtle.onkeypress(player.go_right, "Right")
                turtle.onkeypress(player.go_down, "Down")
                turtle.onkeypress(player.go_up, "Up")
                turtle.onkeypress(end_game_function, "q")
                turtle.onkeypress(restart, "r")
                # loading a short game over animation to make things more interesting
                setup_maze(game_over_screen)

    wn.update()  # updating the screen after every change
wn.bye()  # closing the window when the player quits
