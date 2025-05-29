import unittest
from unittest.mock import patch, MagicMock, call
import sys
import os

# Adjust path to import from the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
# Import all from models (or specific classes if preferred)
from models import * 

# Mock the turtle module for all tests in this file
# This way, any turtle.Turtle method calls are on a mock object.
@patch('models.turtle', MagicMock())
class TestModels(unittest.TestCase):

    def test_player_creation(self):
        player = Player()
        self.assertIsInstance(player, Player)
        player.shape.assert_called_with(config.PLAYER_RIGHT_GIF)
        player.penup.assert_called_once()
        player.speed.assert_called_with(config.PLAYER_SPEED)
        self.assertEqual(player.gold, config.INITIAL_PLAYER_GOLD)
        self.assertEqual(player.key, config.INITIAL_PLAYER_HAS_KEY)
        self.assertEqual(player.arrow, config.INITIAL_PLAYER_ARROWS)

    def test_player_movement(self):
        player = Player()
        # Reset mocks for specific call counting in this test method
        player.goto.reset_mock()
        player.shape.reset_mock()

        # Mock game state lists (empty for simple movement)
        walls = []
        doors_locs = []
        friends_locs = []

        # Go Up
        player.setposition(0, 0) # Set initial position for predictable goto
        player.go_up(walls, doors_locs, friends_locs)
        player.goto.assert_called_with(0, config.BLOCK_SIZE)
        
        # Go Down
        player.setposition(0, 0)
        player.goto.reset_mock() # Reset after previous call
        player.go_down(walls, doors_locs, friends_locs)
        player.goto.assert_called_with(0, -config.BLOCK_SIZE)

        # Go Left
        player.setposition(0, 0)
        player.goto.reset_mock()
        player.go_left(walls, doors_locs, friends_locs)
        player.shape.assert_called_with(config.PLAYER_LEFT_GIF)
        player.goto.assert_called_with(-config.BLOCK_SIZE, 0)
        
        # Go Right
        player.setposition(0, 0)
        player.goto.reset_mock()
        player.shape.reset_mock()
        player.go_right(walls, doors_locs, friends_locs)
        player.shape.assert_called_with(config.PLAYER_RIGHT_GIF)
        player.goto.assert_called_with(config.BLOCK_SIZE, 0)

    def test_player_is_collision(self):
        player = Player()
        mock_other = MagicMock(spec=turtle.Turtle) # Mock another turtle object
        
        player.setposition(0,0)
        mock_other.xcor.return_value = 0
        mock_other.ycor.return_value = 10 # distance = 10
        self.assertTrue(player.is_collision(mock_other)) # 10 < PLAYER_COLLISION_DISTANCE (26)

        mock_other.xcor.return_value = 0
        mock_other.ycor.return_value = 30 # distance = 30
        self.assertFalse(player.is_collision(mock_other)) # 30 not < PLAYER_COLLISION_DISTANCE (26)

    def test_enemy_creation(self):
        enemy = Enemy(50, 100)
        self.assertIsInstance(enemy, Enemy)
        enemy.shape.assert_called_with(config.ENEMY_LEFT_GIF)
        enemy.penup.assert_called_once()
        enemy.speed.assert_called_with(config.ENEMY_SPEED)
        enemy.goto.assert_called_with(50, 100)
        self.assertIn(enemy.direction, ["down", "up", "left", "right"])

    def test_enemy_destroy(self):
        enemy = Enemy(0,0)
        enemy.destroy()
        enemy.goto.assert_called_with(config.OFF_SCREEN_X, config.OFF_SCREEN_Y)
        enemy.hideturtle.assert_called_once()

    def test_enemy_is_close(self):
        enemy = Enemy(0,0)
        mock_player = MagicMock(spec=Player)

        enemy.setposition(0,0)
        mock_player.xcor.return_value = 50 # distance = 50
        mock_player.ycor.return_value = 0
        self.assertTrue(enemy.is_close(mock_player)) # 50 < ENEMY_DETECTION_RADIUS (100)

        mock_player.xcor.return_value = 150
        mock_player.ycor.return_value = 0 # distance = 150
        self.assertFalse(enemy.is_close(mock_player))

    @patch('models.turtle.ontimer') # Mock turtle.ontimer for Enemy.move
    def test_enemy_move_no_dependencies(self, mock_ontimer):
        enemy = Enemy(0,0)
        enemy.move() # Should just reschedule ontimer if dependencies not set
        mock_ontimer.assert_called_once_with(enemy.move, random.randint(config.ENEMY_MOVE_MIN_DELAY, config.ENEMY_MOVE_MAX_DELAY))

    @patch('models.turtle.ontimer')
    def test_enemy_move_with_dependencies(self, mock_ontimer):
        enemy = Enemy(0, 0)
        mock_player = MagicMock(spec=Player)
        mock_player.xcor.return_value = 1000 # Far away
        mock_player.ycor.return_value = 1000
        
        walls = [(-24,0)] # Wall to the left
        doors_locs = []
        friends_locs = []
        
        enemy.set_dependencies(walls, doors_locs, friends_locs, mock_player)
        enemy.goto.reset_mock() # Reset after init
        
        # Test case: Enemy tries to move into a wall
        enemy.setposition(0,0)
        enemy.direction = "left" # Try to move into wall at (-24,0)
        enemy.move()
        
        # Should not have moved, and direction should have changed
        enemy.goto.assert_not_called() # Did not move to (-24,0)
        self.assertNotEqual(enemy.direction, "left") # Direction changed
        mock_ontimer.assert_called_with(enemy.move, random.randint(config.ENEMY_MOVE_MIN_DELAY, config.ENEMY_MOVE_MAX_DELAY))

        # Test case: Enemy moves freely
        enemy.goto.reset_mock()
        enemy.direction = "right" # Assume (24,0) is free
        enemy.move()
        enemy.goto.assert_called_with(config.BLOCK_SIZE, 0) # Moved right
        # Shape should have been updated to right
        enemy.shape.assert_called_with(config.ENEMY_RIGHT_GIF)


    def test_friend_creation(self):
        friend = Friend(0,0)
        self.assertIsInstance(friend, Friend)
        friend.shape.assert_called_with(config.FRIEND_GIF)
        self.assertEqual(friend.key, config.INITIAL_FRIEND_HAS_KEY)
        self.assertEqual(friend.arrow, config.INITIAL_FRIEND_ARROWS)

    def test_pen_creation(self):
        pen = Pen()
        self.assertIsInstance(pen, Pen)
        pen.shape.assert_called_with(config.WALL_GIF)

    def test_black_square_creation(self):
        bs = BlackSquare()
        self.assertIsInstance(bs, BlackSquare)
        bs.shape.assert_called_with(config.BLACK_SQUARE_GIF)
    
    def test_health_creation_and_destroy(self):
        health = Health(0,0)
        self.assertIsInstance(health, Health)
        health.shape.assert_called_with(config.HEART_GIF)
        health.destroy()
        health.goto.assert_called_with(config.OFF_SCREEN_X, config.OFF_SCREEN_Y)
        health.hideturtle.assert_called_once()

    def test_treasure_variants(self):
        treasure = Treasure(0,0)
        self.assertEqual(treasure.gold, config.TREASURE_NORMAL_GOLD)
        treasure.destroy()
        treasure.goto.assert_called_with(config.OFF_SCREEN_X, config.OFF_SCREEN_Y)
        
        treasure_small = TreasureSmall(0,0)
        self.assertEqual(treasure_small.gold, config.TREASURE_SMALL_GOLD)
        treasure_small.destroy()
        treasure_small.goto.assert_called_with(config.OFF_SCREEN_X, config.OFF_SCREEN_Y)

        treasure_big = TreasureBig(0,0)
        self.assertEqual(treasure_big.gold, config.TREASURE_BIG_GOLD)
        treasure_big.destroy()
        treasure_big.goto.assert_called_with(config.OFF_SCREEN_X, config.OFF_SCREEN_Y)
        
    def test_key_creation(self):
        key_obj = Key() # Renamed to avoid conflict with models.Key
        self.assertIsInstance(key_obj, Key)
        key_obj.shape.assert_called_with(config.KEY_GIF)

    def test_arrow_creation(self):
        arrow_obj = Arrow()
        self.assertIsInstance(arrow_obj, Arrow)
        arrow_obj.shape.assert_called_with(config.ARROW_GIF)

    def test_arrow_number_creation(self):
        an = ArrowNumber()
        self.assertIsInstance(an, ArrowNumber)
        an.shape.assert_called_with(config.ONE_GIF)

    def test_gold_text_creation(self):
        gold_display = Gold(100, 50, 50, "yellow")
        self.assertIsInstance(gold_display, Gold)
        gold_display.color.assert_called_with("yellow")
        gold_display.write.assert_called_with("Gold: 100", move=False, align="right", font=config.GOLD_FONT)
        gold_display.hideturtle.assert_called_once()

    def test_score_text_creation(self):
        score_display = Score(500)
        self.assertIsInstance(score_display, Score)
        score_display.color.assert_called_with(config.SCORE_TEXT_COLOR)
        score_display.write.assert_called_with("Score: 500", move=False, align="center", font=config.SCORE_FONT)
        score_display.hideturtle.assert_called_once()

    def test_door_creation_and_destroy(self):
        door = Door(0,0)
        self.assertIsInstance(door, Door)
        door.shape.assert_called_with(config.DOOR_GIF)
        door.destroy()
        door.goto.assert_called_with(config.OFF_SCREEN_X, config.OFF_SCREEN_Y)
        door.hideturtle.assert_called_once()

    def test_stairs_creation(self):
        stairs = Stairs(0,0)
        self.assertIsInstance(stairs, Stairs)
        stairs.shape.assert_called_with(config.STAIRS_GIF)

    def test_game_over_stamp_creation(self): # Renamed to reflect its use
        go_stamp = GameOver()
        self.assertIsInstance(go_stamp, GameOver)
        go_stamp.shape.assert_called_with("square")
        go_stamp.color.assert_called_with(config.GAME_OVER_SHAPE_COLOR)

    def test_game_win_exit_creation(self): # Renamed to reflect its use
        gw_exit = GameWin(0,0)
        self.assertIsInstance(gw_exit, GameWin)
        gw_exit.shape.assert_called_with(config.EXIT_GIF)

if __name__ == '__main__':
    unittest.main()
