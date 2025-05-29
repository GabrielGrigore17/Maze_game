import config  # For SOUND_BLOCKING_MODE

class PlaySoundException(Exception):
    pass


def play_sound(sound, block=config.SOUND_BLOCKING_MODE):
    # This function only works on Windows
    # If you use Unix or something else the sounds won't work
    # but hopefully everything else works
    from ctypes import c_buffer, windll
    from random import random  # Local import
    from time import sleep  # Local import
    from sys import getfilesystemencoding  # Local import

    def win_command(*command):
        buf = c_buffer(255)
        command_str = ' '.join(command).encode(getfilesystemencoding())
        error_code = int(windll.winmm.mciSendStringA(command_str, buf, 254, 0))
        if error_code:
            error_buffer = c_buffer(255)
            windll.winmm.mciGetErrorStringA(error_code, error_buffer, 254)
            exception_message = ('\n    Error ' + str(error_code) + ' for command:'
                                 '\n        ' + command_str.decode() +
                                 '\n    ' + error_buffer.value.decode())
            raise PlaySoundException(exception_message)
        return buf.value

    alias = 'playsound_' + str(random())
    win_command('open "' + sound + '" alias', alias)
    win_command('set', alias, 'time format milliseconds')
    duration_in_ms_bytes = win_command('status', alias, 'length')
    
    # Ensure duration_in_ms_bytes is decoded before being used in win_command
    duration_in_ms_decoded = duration_in_ms_bytes.decode()
    win_command('play', alias, 'from 0 to', duration_in_ms_decoded)

    if block:
        # Ensure duration_in_ms_decoded is float for sleep
        sleep(float(duration_in_ms_decoded) / 1000.0)
