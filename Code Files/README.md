Notes:

- `ssh bmo@bmo.local`
- To run a command like `vlc --loop --no-osd --fullscreen "/home/bmo/animations/BMO_Idle_loop_ColorAdjust.mp4"` over ssh, be sure to first run `export DISPLAY=:0.0`
- `sudo pip3 install python-vlc keyboard`

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
