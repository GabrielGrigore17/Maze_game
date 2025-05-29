import unittest
from unittest.mock import patch, MagicMock, call
import sys
import os

# Adjust path to import from the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Modules to be tested or mocked
import game_logic as gl
import config
from LEVELS import game_over_screen # For testing game over in main loop logic (if applicable)

# Since game_logic imports models, and models imports turtle,
# we need to ensure turtle is mocked *before* game_logic (and thus models) is imported.
# However, game_logic is already imported above. This can be tricky.
# A common pattern is to set up mocks for modules that create side effects (like turtle)
# very early, or structure imports carefully.

# For this test, we will patch 'turtle' where it's used by 'models' and 'game_logic'
# and also patch the model classes themselves if we want to check their instantiation
# without running their full __init__ (which might try to use turtle).

@patch('models.turtle', MagicMock()) # Mock turtle within models.py
@patch('game_logic.turtle', MagicMock()) # Mock turtle within game_logic.py (if it used turtle directly)
class TestGameLogic(unittest.TestCase):

    def setUp(self):
        # Reset game state variables in game_logic before each test
        # This is important because game_logic.py defines module-level globals.
        gl.end_game = False
        gl.levels = ["", config.LEVEL_1_TEST, config.LEVEL_2_TEST, config.LEVEL_3_TEST] # Use test levels
        gl.treasures = []
        gl.treasures_small = []
        gl.treasures_big = []
        gl.current_gold = config.INITIAL_PLAYER_GOLD
        gl.gold_text_x = 0
        gl.gold_text_y = 0
        gl.doors = []
        gl.doors_locations = []
        gl.enemies = []
        gl.friends = []
        gl.friends_locations = []
        gl.walls = []
        gl.start_point = []
        gl.hearts = []
        gl.hearts_x_cor = []
        gl.current_level = config.DEFAULT_LEVEL_INDEX
        
        # Re-instantiate objects to ensure they are fresh and use mocked turtle
        # Patching the classes themselves to check instantiation calls
        with patch('models.Player', autospec=True) as self.MockPlayer, \
             patch('models.Pen', autospec=True) as self.MockPen, \
             patch('models.GameOver', autospec=True) as self.MockGameOver, \
             patch('models.Key', autospec=True) as self.MockKey, \
             patch('models.Arrow', autospec=True) as self.MockArrow, \
             patch('models.ArrowNumber', autospec=True) as self.MockArrowNumber, \
             patch('models.Stairs', autospec=True) as self.MockStairs, \
             patch('models.GameWin', autospec=True) as self.MockGameWin, \
             patch('models.Health', autospec=True) as self.MockHealth, \
             patch('models.Enemy', autospec=True) as self.MockEnemy, \
             patch('models.Friend', autospec=True) as self.MockFriend, \
             patch('models.Door', autospec=True) as self.MockDoor, \
             patch('models.Treasure', autospec=True) as self.MockTreasure, \
             patch('models.TreasureSmall', autospec=True) as self.MockTreasureSmall, \
             patch('models.TreasureBig', autospec=True) as self.MockTreasureBig, \
             patch('models.Gold', autospec=True) as self.MockGold: # For text display

            # Re-assign in game_logic to use these mocks for instantiation tests
            gl.Player_Class = self.MockPlayer # Store mock class
            gl.Pen_Class = self.MockPen
            gl.GameOver_Class = self.MockGameOver
            gl.Key_Class = self.MockKey
            gl.Arrow_Class = self.MockArrow
            gl.ArrowNumber_Class = self.MockArrowNumber
            gl.Stairs_Class = self.MockStairs
            gl.GameWin_Class = self.MockGameWin
            # Create instances of these mocks for gl state
            gl.player = self.MockPlayer()
            gl.pen = self.MockPen()
            gl.game_over = self.MockGameOver()
            gl.key = self.MockKey()
            gl.arrow = self.MockArrow()
            gl.arrow_number = self.MockArrowNumber()
            gl.stairs = self.MockStairs()
            gl.game_win = self.MockGameWin()
            
            # For lists that are populated by setup_maze, we just need to ensure
            # their respective mocked classes are used.
            gl.Health_Class = self.MockHealth
            gl.Enemy_Class = self.MockEnemy
            gl.Friend_Class = self.MockFriend
            gl.Door_Class = self.MockDoor
            gl.Treasure_Class = self.MockTreasure
            gl.TreasureSmall_Class = self.MockTreasureSmall
            gl.TreasureBig_Class = self.MockTreasureBig
            gl.Gold_Class = self.MockGold
            
            # Initial setup of hearts using mocked Health
            gl.hearts.clear()
            gl.hearts_x_cor.clear()
            for y_H in range(len(config.LEVEL_1_TEST)): # Use a test level
                for x_H in range(len(config.LEVEL_1_TEST[y_H])):
                    character_H = config.LEVEL_1_TEST[y_H][x_H]
                    if character_H == "H":
                        screen_x_H = config.MAZE_START_X + (x_H * config.BLOCK_SIZE)
                        screen_y_H = config.MAZE_START_Y - (y_H * config.BLOCK_SIZE)
                        gl.hearts_x_cor.append(screen_x_H)
                        # Use the stored mock class for instantiation
                        gl.hearts.append(gl.Health_Class(screen_x_H, screen_y_H))


    def test_initial_game_state_variables(self):
        self.assertEqual(gl.current_gold, config.INITIAL_PLAYER_GOLD)
        self.assertEqual(gl.current_level, config.DEFAULT_LEVEL_INDEX)
        self.assertIsInstance(gl.walls, list)
        self.assertIsInstance(gl.enemies, list)
        self.assertFalse(gl.end_game)
        # Check if player object is an instance of the *mocked* Player class
        self.assertIsInstance(gl.player, self.MockPlayer.__class__)


    def test_end_game_function_logic(self):
        gl.end_game = False # Ensure it's false initially
        gl.end_game_function_logic()
        self.assertTrue(gl.end_game)

    @patch('game_logic.os.execv')
    @patch('game_logic.sys.executable', 'python_mock')
    @patch('game_logic.sys.argv', ['main.py_mock'])
    def test_restart_logic(self, mock_execv):
        gl.restart_logic()
        mock_execv.assert_called_once_with('python_mock', ['python_mock'] + ['main.py_mock'])

    def test_setup_maze_logic(self):
        # Use a simple test level
        test_level_data = [
            "XPX",
            "XEX",
            "XTX"
        ]
        # Reset relevant mock instance calls from setUp
        self.MockPen_instance = gl.pen
        self.MockPlayer_instance = gl.player
        
        self.MockPen_instance.goto.reset_mock()
        self.MockPen_instance.stamp.reset_mock()
        self.MockPlayer_instance.goto.reset_mock()
        self.MockEnemy_instances = []

        # Override Enemy_Class to capture instances created by setup_maze_logic
        def mock_enemy_init_side_effect(x, y):
            instance = MagicMock(spec=gl.Enemy_Class) # Create a new mock for each instance
            instance.xcor.return_value = x # Make methods like xcor work if needed
            instance.ycor.return_value = y
            self.MockEnemy_instances.append(instance)
            return instance
        
        gl.Enemy_Class.side_effect = mock_enemy_init_side_effect # Use the factory

        # Clear lists that setup_maze_logic should populate
        gl.walls.clear()
        gl.enemies.clear()
        gl.treasures.clear()
        gl.start_point.clear()

        gl.setup_maze_logic(test_level_data)

        # Player assertions
        # P is at (1,0) -> screen_x = -288 + 24 = -264, screen_y = 288 - 0 = 288
        expected_player_x = config.MAZE_START_X + (1 * config.BLOCK_SIZE)
        expected_player_y = config.MAZE_START_Y + (0 * config.BLOCK_SIZE)
        self.MockPlayer_instance.goto.assert_called_with(expected_player_x, expected_player_y)
        self.assertEqual(gl.start_point[0], [expected_player_x, expected_player_y])

        # Wall assertions (Pen)
        # X are at (0,0), (2,0), (0,1), (2,1), (0,2), (2,2)
        self.assertEqual(len(gl.walls), 6)
        self.assertEqual(self.MockPen_instance.stamp.call_count, 6)

        # Enemy assertions
        self.assertEqual(len(gl.enemies), 1)
        self.assertEqual(len(self.MockEnemy_instances), 1)
        enemy_instance = self.MockEnemy_instances[0]
        # E is at (1,1) -> screen_x = -264, screen_y = 288 - 24 = 264
        expected_enemy_x = config.MAZE_START_X + (1 * config.BLOCK_SIZE)
        expected_enemy_y = config.MAZE_START_Y - (1 * config.BLOCK_SIZE)
        # Check that Enemy was instantiated with these coordinates (via its goto mock if constructor calls goto)
        # The Enemy mock created by @patch will have its __init__ mocked.
        # Our side_effect for gl.Enemy_Class ensures new_enemy = Enemy(x,y) results in a mock.
        # The Enemy's own goto would be called if its __init__ wasn't fully mocked out by autospec.
        # If Enemy's __init__ calls self.goto(x,y), then enemy_instance.goto would be called.
        # Assuming our MockEnemy from autospec has a mock goto:
        enemy_instance.goto.assert_called_with(expected_enemy_x, expected_enemy_y)
        enemy_instance.set_dependencies.assert_called_once_with(gl.walls, gl.doors_locations, gl.friends_locations, gl.player)
        
        # Treasure assertions
        # T is at (1,2) -> screen_x = -264, screen_y = 288 - 48 = 240
        self.assertEqual(len(gl.treasures), 1)
        # To check Treasure instantiation, we'd need to mock Treasure and check its calls
        # similar to how Enemy was handled, or check the type in gl.treasures.
        # For simplicity, we'll assume gl.Treasure_Class was used if not testing specific Treasure calls here.

        # Check that lists are populated
        self.assertTrue(len(gl.walls) > 0)
        self.assertTrue(len(gl.enemies) > 0)
        self.assertTrue(len(gl.treasures) > 0)


# Add dummy test levels to config for isolated testing if not already present
# These would ideally be in a separate test_config_override.py or similar
config.LEVEL_1_TEST = ["P"]
config.LEVEL_2_TEST = ["X"]
config.LEVEL_3_TEST = ["E"]


if __name__ == '__main__':
    unittest.main()
