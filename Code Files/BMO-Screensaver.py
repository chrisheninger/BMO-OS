import vlc
import time
import RPi.GPIO as GPIO

# Create a new instance of VLC and a new media player object
instance = vlc.Instance()
player = instance.media_player_new()

# Enable fullscreen
player.set_fullscreen(True)

# Define file paths
idle_path = "/home/bmo/animations/BMO_IdleLoop.mp4"
file_paths = {
    "b1 (up)": "/home/bmo/animations/BMO_DontSayThings.mp4",
    "b2 (right)": "/home/bmo/animations/BMO_WelcomeFriends.mp4",
    "b3 (down)": "/home/bmo/animations/BMO_WorryBaby.mp4",
    "b4 (left)": "/home/bmo/animations/BMO_YourHand.mp4",
}

# Define a global so we can recursively play idle loop
animation_playing = False


def play_idle_loop():
    global animation_playing
    while not animation_playing:
        player.set_media(instance.media_new(idle_path))
        player.play()
        time.sleep(1)  # Wait for media to start playing
        while player.is_playing():
            time.sleep(1)  # Wait until the animation has finished playing


def play_animation(file_path):
    global animation_playing
    animation_playing = True
    player.set_media(instance.media_new(file_path))
    player.play()
    time.sleep(1)  # Wait for media to start playing
    while player.is_playing():
        time.sleep(1)  # Wait until the animation has finished playing
    animation_playing = False


def stop_and_exit(pin):
    player.stop()
    exit(0)


# GPIO Setup
GPIO.setmode(GPIO.BCM)

# Define the pin numbers
buttons = {
    17: "b1 (up)",
    27: "b2 (right)",
    22: "b3 (down)",
    23: "b4 (left)",
    24: "b5 (triangle)",
    25: "b6 (small circle)",
    26: "b7 (large circle)"
}

# Function to generate callback functions


def make_callback(name):
    if name in file_paths:
        return lambda pin: play_animation(file_paths[name])
    elif name == "b7 (large circle)":
        return stop_and_exit
    else:
        return lambda pin: None


# Setup the pins and attach handlers
for pin, name in buttons.items():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(
        pin, GPIO.FALLING, callback=make_callback(name), bouncetime=100)

# Start the idle loop
play_idle_loop()

# Loop forever
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
