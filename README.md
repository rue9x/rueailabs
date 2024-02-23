# rueailabs
App for voice conversations with AI. 

# Features
- Simple UI
- Voice recognition with Google
- Voice responses with your favorite ElevenLabs voices
- Intelligent conversation with OpenAI's ChatGPT-3.5 model
- Customizable personality
- Remebers everything in your current conversation
  
# How to install?
Install python
pip install -r requirements.txt

# How to run?
py rueailabs.py / python rueailabs.py

# How to set up?
1. Edit config.json. Add your keys for ElevenLabs, OpenAI and AzureTTS, each encoded in base64 for protection (https://base64decode.org/)
2. In voices.json, for elevenlabs:
   - "shortname name of voice (make one up": "elevenlabs_voice_id"
3. In config.json, change "voice" to whatever shorthand name of the voices you set up in step 2.
4.  Change the initial_prompt to customize the personality of the AI.

# How to use?
1. launch 'py rueailabs.py'
2. Click 'record', talk to the ai. It will listen for up to 30 seconds or wait for you to stop talking.
3. Wait 5-15 seconds for response, depending on how OpenAI and ElevenLabs are feeling.
