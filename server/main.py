from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
import uvicorn
from function.text_to_speech import convert_text_to_speech
from function.speech_to_text import convert_speech_to_text
from function.message_handler import message_handler
import requests

import uuid
import json
import openai
import os
from starlette.config import Config

app = FastAPI()
origins = ['http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Socket.io 인스턴스 생성 Socket io (sio) create a Socket.IO server
sio = socketio.AsyncServer(cors_allowed_origins=[], async_mode='asgi')
#wrap with ASGI application
socket_app = socketio.ASGIApp(sio)


@app.route("/")
async def root():
    return "Health Check"

# 세션 데이터 저장을 위한 변수 선언
sessions = {}

config = Config('.env')

openai.organization = config("OPEN_AI_ORG")
openai.api_key = config("OPEN_AI_KEY")

# Socket.IO 연결
@sio.on("connect")
async def client_connect(sid, env): #env는 인증용으로
    print("\n...>> New Client Connected to This id :"+" "+str(sid)+"\n")


@sio.on("session-history")
async def get_session_id(sid, data):
    if data['sessionId'] in sessions:
        session_obj = { 
            'sessionId': data['sessionId'],
            'conversations': sessions[data['sessionId']]
        }
        await sio.emit("session-details", json.dumps(session_obj))
    else :
        new_session_id = str(uuid.uuid4())
        sessions[str(new_session_id)] = []
        
        session_obj = { 
            'sessionId': new_session_id,
            'conversations': []
        }
        await sio.emit("session-details", json.dumps(session_obj))

#대화처리
@sio.on("client-message")
async def conversation_message(sid, data): #sid: socket id
    openai_response = await message_handler(
        sid=sid, 
        data=data,
        sessions=sessions,
        type='text'
    )
    text_output, _ = openai_response
    await sio.emit("server-message", json.dumps(text_output)) 


#세션 초기화
@sio.on("remove-session")
async def remove_session(sid, data): #sid: socket id
    target_session_id = data['sessionId']
    sessions[target_session_id] = []
    await sio.emit("reponse-remove-session", 'success')

@sio.on("upload-file")
async def upload_file(sid, data): #sid: socket id
    stt_file_name = uuid.uuid4()
    audio_input_path = f"upload/{stt_file_name}.mp3"

    audio_data = data['data']
    
    with open(audio_input_path, 'wb') as file:
        file.write(audio_data)
    
    try:    
        #텍스트로 변경하기 
        message_decoded = await convert_speech_to_text(audio_input_path)
        
        #데이터 객체 만들기
        openai_data = {
            'sessionId': data['sessionId'],
            'conversationId': data['conversationId'],
            'message': {
                'id': str(uuid.uuid4()),
                'content': message_decoded,
                'aiMessage': False,
                'animate': False
            }
        }
        #openai로 답변 생성
        openai_response = await message_handler(
            sid=None, 
            data=openai_data,
            sessions=sessions,
            type='audio'
        ) 
        
        text_output, audio_output = openai_response 
        #Create a generator that yields chunks of data
        def iterfile():
            yield audio_output
        
        os.remove(f'{audio_input_path}')
        
        # Send the response 객체 만들기
        await sio.emit("server-message", json.dumps(text_output)) #대화텍스트 보내기
        await sio.emit("response-upload-file", audio_output)#오디오 음성 보내기

    
    except Exception as e:
        print("[upload_file] > Exception:", e)
        await sio.emit("response-upload-file", json.dumps(e))


@sio.on("disconnect")
async def disconnect(sid):
    print("Client Disconnected: "+" "+str(sid))


from fastapi.staticfiles import StaticFiles
app.mount("/", socket_app)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)