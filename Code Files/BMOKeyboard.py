import vlc
import time
import keyboard

# Create a new instance of VLC and a new media player object
instance = vlc.Instance()
player = instance.media_player_new()

# Enable fullscreen
player.set_fullscreen(True)

# Define file paths
idle_path = "/home/bmo/animations/BMO_Idle_loop_ColorAdjust.mp4"
file_paths = {
    "a": "/home/bmo/animations/BMO_DontSayThings_ColorAdjust.mp4",
    "b": "/home/bmo/animations/BMO_WelcomeFriends_ColorAdjust.mp4",
    "c": "/home/bmo/animations/BMO_WorryBaby_ColorAdjust.mp4",
    "d": "/home/bmo/animations/BMO_YourHand_ColorAdjust.mp4",
}


def play_idle_loop():
    player.set_media(instance.media_new(idle_path))
    player.play()
    time.sleep(1)  # Wait for media to start playing


def play_animation(file_path):
    player.set_media(instance.media_new(file_path))
    player.play()
    time.sleep(1)  # Wait for media to start playing
    while player.is_playing():
        time.sleep(1)  # Wait until the animation has finished playing
    play_idle_loop()  # Return to the idle loop


def stop_and_exit():
    player.stop()
    exit(0)


# Set up hotkeys
for key, file_path in file_paths.items():
    keyboard.add_hotkey(
        key, lambda file_path=file_path: play_animation(file_path))
keyboard.add_hotkey('esc', stop_and_exit)

# Start the idle loop
play_idle_loop()

# Start the keyboard event loop
keyboard.wait()
