# Screen Settings
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Sandi's Maze"
BACKGROUND_COLOR = "black"

# Asset Paths (GIFs and MP3s)
PLAYER_RIGHT_GIF = r"Resources\player_right.gif"
PLAYER_LEFT_GIF = r"Resources\player_left.gif"
WALL_GIF = r"Resources\wall.gif"
TREASURE_GIF = r"Resources\treasure.gif"
TREASURE_SMALL_GIF = r"Resources\treasure_small.gif"
TREASURE_BIG_GIF = r"Resources\treasure_big.gif"
ENEMY_LEFT_GIF = r"Resources\enemy_left.gif"
ENEMY_RIGHT_GIF = r"Resources\enemy_right.gif"
HEART_GIF = r"Resources\heart.gif"
KEY_GIF = r"Resources\key.gif"
FRIEND_GIF = r"Resources\friend.gif"
DOOR_GIF = r"Resources\door.gif"
ARROW_GIF = r"Resources\arrow.gif"
STAIRS_GIF = r"Resources\stairs.gif"
BLACK_SQUARE_GIF = r"Resources\black_square.gif"
DUNGEON_1_GIF = r"Resources\dungeon_1.gif"
DUNGEON_2_GIF = r"Resources\dungeon_2.gif"
DUNGEON_3_GIF = r"Resources\dungeon_3.gif"
EXIT_GIF = r"Resources\exit.gif"
BLACK_BACKGROUND_GIF = r"Resources\black_background.gif"
WINNER_GIF = r"Resources\winner.gif"
LOSER_GIF = r"Resources\loser.gif"
ONE_GIF = r"Resources\one.gif"
TWO_GIF = r"Resources\two.gif"
THREE_GIF = r"Resources\three.gif"
FOUR_GIF = r"Resources\four.gif"
FIVE_GIF = r"Resources\five.gif"

THEME_MP3 = r"Resources\theme.mp3"
NEXT_LEVEL_MP3 = r"Resources\next_level.mp3"
GAME_WIN_MP3 = r"Resources\game_win.mp3"
DOOR_MP3 = r"Resources\door.mp3"
TREASURE_MP3 = r"Resources\treasure.mp3"
FRIEND_MP3 = r"Resources\friend.mp3"
ENEMY_MP3 = r"Resources\enemy.mp3"
DAMAGE_MP3 = r"Resources\damage.mp3"
GAME_LOSE_MP3 = r"Resources\game_lose.mp3"

# Game Settings - Speeds (mostly animation speeds, 0 is fastest)
PLAYER_SPEED = 0
ENEMY_SPEED = 0
PEN_SPEED = 0
BLACK_SQUARE_SPEED = 0
HEALTH_SPEED = 0
TREASURE_SPEED = 0
KEY_SPEED = 0
ARROW_SPEED = 0
ARROW_NUMBER_SPEED = 0
DOOR_SPEED = 0
STAIRS_SPEED = 0
GAME_OVER_SPEED = 0
GAME_WIN_SPEED = 0

# Text and Font settings
GOLD_TEXT_COLOR = "red"
GOLD_FONT_NAME = "ocr a extended"
GOLD_FONT_SIZE = 14
GOLD_FONT_STYLE = "normal"
GOLD_FONT = (GOLD_FONT_NAME, GOLD_FONT_SIZE, GOLD_FONT_STYLE)

SCORE_TEXT_COLOR = "black"
SCORE_FONT_NAME = "impact"
SCORE_FONT_SIZE = 50
SCORE_FONT_STYLE = "bold"
SCORE_FONT = (SCORE_FONT_NAME, SCORE_FONT_SIZE, SCORE_FONT_STYLE)

GAME_OVER_SHAPE_COLOR = "red" # This was a shape color not text

# Game Mechanics
BLOCK_SIZE = 24  # Size of a game block/tile in pixels
PLAYER_COLLISION_DISTANCE = 26 # Distance for player collision detection (slightly more than BLOCK_SIZE)
ENEMY_DETECTION_RADIUS = 100 # Radius for enemy to detect player

# Initial game state values
INITIAL_PLAYER_GOLD = 0
INITIAL_PLAYER_HAS_KEY = False
INITIAL_PLAYER_ARROWS = 0
INITIAL_FRIEND_HAS_KEY = True
INITIAL_FRIEND_ARROWS = 1
TREASURE_NORMAL_GOLD = 100
TREASURE_SMALL_GOLD = 25
TREASURE_BIG_GOLD = 250
MAX_PLAYER_ARROWS = 5

# Sound related
SOUND_BLOCKING_MODE = True # For play_sound function (True means the game pauses for sound)

# Loading screen
LOADING_SCREEN_REPEATS = 4
LOADING_SCREEN_DELAY = 0.5 # seconds

# Enemy movement
ENEMY_MOVE_MIN_DELAY = 100 # milliseconds for random timer
ENEMY_MOVE_MAX_DELAY = 300 # milliseconds for random timer
ENEMY_MOVE_ONTURN_TIMER = 250 # milliseconds for turtle.ontimer

# Coordinates for off-screen placement (used to "hide" objects)
OFF_SCREEN_X = 2000
OFF_SCREEN_Y = 2000
# Coordinates for far off-screen placement (used for stairs and game_win initial positions)
FAR_OFF_SCREEN_X = 3000
FAR_OFF_SCREEN_Y = 3000


# Maze setup
MAZE_START_X = -288 # X coordinate of the top-left corner of the maze grid
MAZE_START_Y = 288 # Y coordinate of the top-left corner of the maze grid

# Other constants
DEFAULT_LEVEL_INDEX = 1 # The game starts at level 1 from the levels list (as levels[0] is empty string)
GAME_WIN_SLEEP_DELAY = 1 # Seconds to wait after win condition before showing winner screen
GAME_TITLE_NEXT_LEVEL = "A Maze Game" # Title for screen on next level load (was hardcoded)
