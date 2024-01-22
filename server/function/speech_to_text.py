import openai

#whisper-1
async def convert_speech_to_text(file_path):
        #Open audio file
        audio_input = open(file_path, "rb") 

        #Check audio file
        if not audio_input:
            raise ConnectionRefusedError(f"Not audio_input")

        async def convert_audio_to_text(audio_file):
            #print("\n+----------------------CALL Whisper-1 API-----------------------+")
            try:
                return openai.Audio.transcribe("whisper-1", audio_file)
            except Exception as e:
                raise ConnectionRefusedError(f"Whisper-1 API Error {e}")

        message_decoded = await convert_audio_to_text(audio_input)
            #Check data value
        if not message_decoded:
            raise ConnectionRefusedError(f"Not message_decoded")
        
        #print(f"\n[upload_file] > message_decoded['text']: ", message_decoded['text'])
        return message_decoded['text'] # { "text": "Hello" }