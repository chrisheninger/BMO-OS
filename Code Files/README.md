Notes:

- `ssh bmo@bmo.local`
- To run a command like `vlc --loop --no-osd --fullscreen "/home/bmo/animations/BMO_Idle_loop_ColorAdjust.mp4"` over ssh, be sure to first run `export DISPLAY=:0.0`
- `sudo pip3 install python-vlc keyboard python-dotenv realtime==1.0.0`
- `scp -r . bmo@bmo.local:/home/bmo/code` - copy code from laptop to bmo

Ideas:

- Voice-to-text via microphone ("Hey Beemo")
  - Fed into ChatGPT?
  - Smarthome commands via Google Home or SmartRent directly?
  - Are there open source implementations of Google Home's voice commands?
- Motion sensor from SmartRent, when it changes to active state, have BMO say WelcomeFriends- then back into Idle_loop
  - Log in using my credentials (can hardcode in env, along with unit_id and device_id)
  - Handle fetch sessions endpoint access/refresh tokens
  - Connect to device channel via websocket
  - Listen for changes to the attribute for motion detected
  - Turn BMO's screen completely off when motion isn't detected

gpio 17 - b1 (up)
gpio 27 - b2 (right)
gpio 22 - b3 (down)
gpio 23 - b4 (left)
gpio 24 - b5 (triangle)
gpio 25 - b6 (small circle)
gpio 26 - b7 (large circle)

#63bda4 (99,189,164)
#d9ffea (217,255,234)
#62afb7 (98,175,183)
#f20553 (242,5,83)
#ffec47 (255,236,71)

#AFFCB7 (175,252,183)
