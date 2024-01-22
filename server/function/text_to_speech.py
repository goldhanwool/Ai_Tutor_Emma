import requests
from starlette.config import Config
config = Config('.env')

ELEVEN_LABS_API_KEY = config("ELEVEN_LABS_API_KEY")
VOICE_RACHEL = config("ELEVEN_LABS_VOICE")

#ELEVEN_LABS
async def convert_text_to_speech(message):
    #print("[convert_text_to_speech] > message: ", message)
    try:
        body = {
            "text": message,
            "voice_setings":{
                "stability": 0,
                "similarity_boost": 0,
                "speed": 0.7,
            }
        }

        #Define voice
        voice_rachel = VOICE_RACHEL

        #Constructing Headers and Endpoint
        headers = {
            "xi-api-key": ELEVEN_LABS_API_KEY,
            "Content-Type": "application/json",
            "accept": "audio/mpeg"
            }

        endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_rachel}"

        response = requests.post(endpoint, json=body, headers=headers)
        
    except Exception as e:
        #print(f"ELEVEN_LABS API Error {e}")
        raise ConnectionRefusedError(f"ELEVEN_LABS API Error {e}")

    if response.status_code == 200:
        return response.content
    
    else:
        return "None"


