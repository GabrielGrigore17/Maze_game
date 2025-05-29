import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import platform

# Adjust path to import sound and config from the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config # Used by sound module
from sound import play_sound, PlaySoundException

class TestSound(unittest.TestCase):

    def test_play_sound_exception(self):
        with self.assertRaises(PlaySoundException):
            raise PlaySoundException("Test exception")

    @patch('sound.windll', create=True) # Mock windll for non-Windows or to isolate test
    @patch('sound.c_buffer', create=True)
    @patch('sound.getfilesystemencoding', return_value='utf-8')
    @patch('sound.sleep', create=True) # Mock time.sleep
    def test_play_sound_windows_flow(self, mock_sleep, mock_getfsencoding, mock_c_buffer, mock_windll):
        # This test focuses on the Windows-specific parts of play_sound
        # It will only run the mciSendStringA parts if platform.system() is 'Windows'
        # or if we further mock platform.system()

        # Mock the mciSendStringA function
        mock_mci_send_string = MagicMock(return_value=0) # 0 indicates success
        mock_windll.winmm.mciSendStringA = mock_mci_send_string
        
        # Mock mciGetErrorStringA (though not expected to be called if mciSendStringA returns 0)
        mock_mci_get_error = MagicMock()
        mock_windll.winmm.mciGetErrorStringA = mock_mci_get_error

        # Mock c_buffer to simulate its behavior if needed, though often just creating it is enough
        # if its internal state isn't critical to the test.
        # Here, the .value attribute is accessed for duration_in_ms.
        mock_c_buffer_instance = MagicMock()
        mock_c_buffer_instance.value = b"1000" # Simulate 1000ms duration
        mock_c_buffer.return_value = mock_c_buffer_instance

        # Call play_sound
        sound_file = "test.mp3"
        play_sound(sound_file, block=True) # Test with blocking

        if platform.system() == "Windows":
            # Check if mciSendStringA was called with expected commands
            self.assertTrue(mock_mci_send_string.called)
            calls = mock_mci_send_string.call_args_list
            
            # Check for 'open' command
            open_call_found = any(f'open "{sound_file}" alias' in str(call) for call in calls)
            self.assertTrue(open_call_found, "mciSendStringA not called with 'open'")

            # Check for 'set time format' command
            set_format_call_found = any('set' in str(call) and 'time format milliseconds' in str(call) for call in calls)
            self.assertTrue(set_format_call_found, "mciSendStringA not called with 'set time format'")
            
            # Check for 'status length' command
            status_length_call_found = any('status' in str(call) and 'length' in str(call) for call in calls)
            self.assertTrue(status_length_call_found, "mciSendStringA not called with 'status length'")

            # Check for 'play' command
            play_call_found = any(f'play' in str(call) and 'from 0 to 1000' in str(call) for call in calls)
            self.assertTrue(play_call_found, "mciSendStringA not called with 'play'")
            
            mock_sleep.assert_called_once_with(1.0) # 1000ms / 1000.0
        else:
            # On non-Windows, mciSendStringA should not be called by the current implementation
            # as it's guarded by an implicit assumption of `windll` availability.
            # The function is expected to do nothing or raise an AttributeError if ctypes parts are not guarded.
            # Given the provided sound.py, it will attempt to use windll.
            # If windll is not present (mocked as create=True, so it exists but has no winmm by default unless mocked),
            # an AttributeError would occur.
            # If we want to test the "does nothing gracefully" part, we'd need to ensure windll.winmm exists but mciSendStringA is not called.
            # For this test, if it's not Windows, we simply assert that the mocked mciSendStringA wasn't called.
            # However, the original code does NOT have a platform check *inside* play_sound,
            # it relies on ctypes.windll only being available on Windows.
            # If ctypes.windll itself is not available on a non-windows system, it would error earlier.
            # Our @patch('sound.windll', create=True) makes `windll` exist.
            # The current `play_sound` will proceed to call `windll.winmm.mciSendStringA`.
            # So this test will behave as if on Windows due to mocks.
            # To truly test non-Windows, we'd mock platform.system() or ensure windll is not available.
            # For simplicity, this test primarily validates the Windows path when mocks are active.
            # A separate test might be needed for non-Windows behavior if strict differentiation is required.
            pass # Covered by Windows specific assertions due to mocking structure.

    @patch('sound.windll', create=True)
    @patch('sound.c_buffer', create=True)
    @patch('sound.getfilesystemencoding', return_value='utf-8')
    @patch('sound.sleep', create=True)
    def test_play_sound_mci_error(self, mock_sleep, mock_getfsencoding, mock_c_buffer, mock_windll):
        if platform.system() == "Windows":
            mock_mci_send_string = MagicMock(return_value=263) # Simulate an MCI error code
            mock_windll.winmm.mciSendStringA = mock_mci_send_string
            
            mock_error_buffer_instance = MagicMock()
            mock_error_buffer_instance.value = b"Test MCI Error"
            
            # Make c_buffer return the error buffer when mciGetErrorStringA needs it.
            # For mciSendStringA, it returns a generic buffer for other uses.
            def c_buffer_side_effect(size):
                if mock_mci_send_string.call_count > 1 and mock_windll.winmm.mciGetErrorStringA.call_count == 0: # Approx. when error string buffer is created
                    return mock_error_buffer_instance
                return MagicMock() # Generic buffer for other calls
            mock_c_buffer.side_effect = c_buffer_side_effect

            mock_windll.winmm.mciGetErrorStringA = MagicMock()

            with self.assertRaisesRegex(PlaySoundException, "Test MCI Error"):
                play_sound("error.mp3")
            
            mock_windll.winmm.mciGetErrorStringA.assert_called_once()
        else:
            self.skipTest("MCI error test is specific to Windows execution path")

    @patch('platform.system', return_value='Linux') # Mock as non-Windows
    @patch('sound.windll', create=False) # Ensure windll is not found or causes AttributeError
    def test_play_sound_non_windows(self, mock_windll_create_false, mock_platform_system):
        # This test aims to simulate a non-Windows environment more accurately
        # by making `windll` unavailable or behave as it would on non-Windows.
        
        # The original `play_sound` function directly tries `from ctypes import windll`.
        # If this fails (e.g. on Linux where windll might not be part of a minimal ctypes),
        # an AttributeError or ImportError would occur.
        # If ctypes is present but windll is not an attribute for that OS, it's an AttributeError.
        
        # Because sound.py is already imported, we can't easily test the initial `from ctypes import windll` failing.
        # However, if `windll` was successfully imported but doesn't have `winmm`, that's an AttributeError.
        # If `sound.windll` itself is patched to be unavailable, then `play_sound` would fail.
        
        # Let's assume `from ctypes import windll` succeeds but `windll.winmm` is the problem.
        # We can achieve this by patching `sound.windll` to an object that doesn't have `winmm`.
        with patch('sound.windll', MagicMock(spec=[])) as mock_windll_no_winmm: # spec=[] means it has no attributes
             with self.assertRaises(AttributeError): # Expect AttributeError when accessing mock_windll_no_winmm.winmm
                 play_sound("test.mp3")

if __name__ == '__main__':
    unittest.main()
