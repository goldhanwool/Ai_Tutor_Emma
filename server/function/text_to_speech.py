import requests
from starlette.config import Config
config = Config('.env')

ELEVEN_LABS_API_KEY = config("ELEVEN_LABS_API_KEY")

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
        voice_rachel = "21m00Tcm4TlvDq8ikWAM"
        #voice_rachel = "2EiwWnXFnvU5JabPnv8n" #Clyde

        #Constructing Headers and Endpoint
        headers = {
            "xi-api-key": ELEVEN_LABS_API_KEY,
            "Content-Type": "application/json",
            "accept": "audio/mpeg"
            }

        endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_rachel}"

        # send request
        #print("\n+----------------------CALL ELEVEN_LABS API-----------------------+")
        #print('')

        response = requests.post(endpoint, json=body, headers=headers)
        
    except Exception as e:
        #print(f"ELEVEN_LABS API Error {e}")
        raise ConnectionRefusedError(f"ELEVEN_LABS API Error {e}")

    if response.status_code == 200:
        return response.content
    
    else:
        return "None"


