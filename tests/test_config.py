import unittest
import sys
import os

# Adjust path to import config from the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

class TestConfig(unittest.TestCase):

    def test_screen_dimensions(self):
        self.assertIsInstance(config.SCREEN_WIDTH, int)
        self.assertIsInstance(config.SCREEN_HEIGHT, int)
        self.assertGreater(config.SCREEN_WIDTH, 0)
        self.assertGreater(config.SCREEN_HEIGHT, 0)

    def test_screen_title(self):
        self.assertIsInstance(config.SCREEN_TITLE, str)
        self.assertTrue(len(config.SCREEN_TITLE) > 0)

    def test_background_color(self):
        self.assertIsInstance(config.BACKGROUND_COLOR, str)
        self.assertTrue(len(config.BACKGROUND_COLOR) > 0)

    def test_asset_paths_are_strings(self):
        self.assertIsInstance(config.PLAYER_RIGHT_GIF, str)
        self.assertIsInstance(config.PLAYER_LEFT_GIF, str)
        self.assertIsInstance(config.WALL_GIF, str)
        self.assertIsInstance(config.TREASURE_GIF, str)
        # Add more checks for other assets if desired
        self.assertTrue(config.PLAYER_RIGHT_GIF.startswith(r"Resources"))
        self.assertTrue(config.THEME_MP3.endswith(".mp3"))

    def test_game_settings_types(self):
        self.assertIsInstance(config.PLAYER_SPEED, int)
        self.assertIsInstance(config.ENEMY_SPEED, int)
        self.assertIsInstance(config.BLOCK_SIZE, int)
        self.assertIsInstance(config.ENEMY_DETECTION_RADIUS, int)
        self.assertIsInstance(config.INITIAL_PLAYER_GOLD, int)
        self.assertIsInstance(config.INITIAL_PLAYER_HAS_KEY, bool)
        self.assertIsInstance(config.TREASURE_NORMAL_GOLD, int)
        self.assertIsInstance(config.MAX_PLAYER_ARROWS, int)
        self.assertIsInstance(config.LOADING_SCREEN_REPEATS, int)
        self.assertIsInstance(config.LOADING_SCREEN_DELAY, float)

    def test_font_settings(self):
        self.assertIsInstance(config.GOLD_FONT, tuple)
        self.assertEqual(len(config.GOLD_FONT), 3)
        self.assertIsInstance(config.GOLD_FONT[0], str) # Font name
        self.assertIsInstance(config.GOLD_FONT[1], int) # Font size
        self.assertIsInstance(config.GOLD_FONT[2], str) # Font style

        self.assertIsInstance(config.SCORE_FONT, tuple)
        self.assertEqual(len(config.SCORE_FONT), 3)

    def test_coordinate_values(self):
        self.assertIsInstance(config.OFF_SCREEN_X, int)
        self.assertIsInstance(config.MAZE_START_Y, int)

if __name__ == '__main__':
    unittest.main()
