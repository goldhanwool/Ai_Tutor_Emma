from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
import uvicorn
from api.router import router
from function.text_to_speech import convert_text_to_speech
from function.speech_to_text import convert_speech_to_text

app = FastAPI()
origins = [
    "http://localhost:3000",  
    "http://localhost:8000",  
]

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

'''
    FastAPI 앱의 루트 경로(/)를 socket_app으로 마운트되어 루트 URL에 대한 모든 요청이 
    socket_app으로 라우팅되기 때문에,FastAPI 라우트 @app.get("/")는 호출안됨.

'''
# app.mount("/", socket_app)
app.include_router(router)

@app.get("/")
async def root():
    import requests
    url = "https://randomuser.me/api/"
    response = requests.get(url)
    print(response.json())

    return {"message": "Hello World"}


# 세션 데이터 저장을 위한 변수 선언
'''
sessions = {
  "ea1b1a14-2892-4e37-8388-81b0986a619f": [
      {
          id: '134f6911-9805-40b5-ae68-b6a6d2a946de',
          messages: [
              { content: 'hi', id: 'bf35a5e5-85ba-4ea5-b3f4-15e448f09de6', aiMessage: true/false, animate: false },
              { content: 'Hello! How can I assist you today?', id: 'f6b8c5bd-1521-475a-b680-7d47c0afe0fc' aiMessage: true/false },
              // ... 기타 메시지들
          ]
      },
      {
          id: "대화ID2",
        .
        .
        }
    ]  
  "3d8b97ef-f782-4e28-a062-0906b6d71059": [
    .
    .
  ]
}
'''
sessions = {}

import uuid
import json
import openai

from starlette.config import Config

config = Config('.env')

openai.organization = config("OPEN_AI_ORG")
openai.api_key = config("OPEN_AI_KEY")


# Socket.IO 연결
@sio.on("connect")
async def client_connect(sid, env): #env는 인증용으로
    """
    socket.io 클라이언트가 연결될 때 connect는 미리 정의된 이벤트, param -> sid, environ, auth python-socketio 패키지에서 미리 정해놓은 것들.
        - environ: http 헤더를 포함한 http 리퀘스트 데이터를 담는 WSGI 표준 딕셔너리
        - auth: 인증 데이터
        - sid: 클라이언트의 고유 식별자, socket.io Id
        - raise HttpException 대신 -> raise ConnectionRefusedError를 사용
    
    """
    print("New Client Connected to This id :"+" "+str(sid))


@sio.on("session-history")
async def get_session_id(sid, data):
    print(f"\n[get_session_id] > session-history: data['sessionId']", data['sessionId'])
    # if len(sessions) > 3:
    #     sessions.clear()

    '''
    *[data]
        {
            'sessionId': 'b62b264c-6d25-4ec6-aa58-6f158ae6a68c'
        }

    *process ->
        기존에 있던 session이면 'sessionId', 'conversations'를 키로 객체 리턴
        없으면 새로운 session을 생성하고, 'sessionId', 'conversations'를 키로 객체 리턴

    '''
    print(f"\n[get_session_id] > session-history: sessions", sessions)
    if data['sessionId'] in sessions:
        print(f"\n[get_session_id] > sessions[data['sessionId']]", sessions[data['sessionId']])
        
        session_obj = { 
            'sessionId': data['sessionId'],
            'conversations': sessions[data['sessionId']]
        }
        
        await sio.emit("session-details", json.dumps(session_obj))

    else :
        new_session_id = str(uuid.uuid4())
        '''
            새로운 세션 객체에 값을 할당한다 
            sessions = { 'ea1b1a14-2892-4e37-8388-81b0986a619f' : [] }
        '''
        sessions[str(new_session_id)] = []
        print(f"\n[get_session_id] > session-history: sessions", sessions)
        
        session_obj = { 
            'sessionId': new_session_id,
            'conversations': []
        }
        print(f"\n[get_session_id] > session-history: session_obj", session_obj)
        
        await sio.emit("session-details", json.dumps(session_obj))
        #await get_session_id_handler(sid, data)

#대화처리
@sio.on("client-message")
async def conversation_message(sid, data): #sid: socket id
    '''
    *[data] <class 'dict'> 
        {
            'sessionId': '2194c5d1-296c-42ce-9005-e0c36b5e45c4',
            'message': {'id': '17fc1aeb-367e-49cc-88e4-a6eb0ea68b91','content': 'hello', 'aiMessage': False, 'animate': False}, 
            'conversationId': 'b62b264c-6d25-4ec6-aa58-6f158ae6a68c'
        }
    '''
    print(f"\n[conversation_message] > accept > conversation-message: ", type(data), data)
    
    await conversation_message_handler(sid, data)


async def conversation_message_handler(sid, data):
    print(f"\n[conversation_message_handler] > sessions: ", sessions)
    print(f"\n[CMH] > conversation-message: ", type(data), data)
    
    # Using OpenAI call
    # messages=[{
    #             "role":"system", "content" : "You are an experienced English tutor who graduated from Harvard University in Boston.You are talking to a student who wants to practice speaking English. Help them practice speaking English by talking to your student and While talking to your student, help your student how to say what they would like to say."
    #         },
    #         {
    #             "role":"user", "content" : message['content']
    #         }]
    #response = await asyncio.to_thread(openai.ChatCompletion.create, 'gpt-4', messages)
    async def get_openai(content):
        return openai.ChatCompletion.create(
            model='gpt-4',
            messages=[
                # GPT 역할 정의
                {"role":"system", "content" : "You are an experienced English tutor who graduated from Harvard University in Boston.You are talking to a student who wants to practice speaking English. Help them practice speaking English by talking to your student and While talking to your student, help your student how to say what they would like to say. "},
                # 질문
                {"role":"user", "content" : content} 
                    
            ]
        )
    
    # openai 객체가 async를 지원하지 않음 -> 비동기 함수에 동기를 넣기 위해 사용
    '''
    **[response.get('choices')[0].get('message').get('content')] : str 
            
            Hello! It's great to see you're ready to practice your English. How can I assist you today?
    
    '''
    response = await get_openai(data['message']['content']) 
    openai_message = response.get('choices')[0].get('message').get('content') if response else "Error occurred from AI"
    print("[conversation_message_handler] > ai_message_content: ", response.get('choices')[0].get('message').get('content'))

    
    # 세션 아이디가 sessions에 존재하면 -> AI의 응답 메세지를 생성 후 세션에 추가하고 클라이언트에 전송하고.
    if data['sessionId'] in sessions:
        print(f"\n[CMH] > data['sessionId']: ", data['sessionId'])
        aiMessage = {
            'content': openai_message,
            'id': str(uuid.uuid4()),
            'aiMessage': True,
            'animate': True
        }
        print("\n---------before for session in sessions[data['sessionId']]", sessions[data['sessionId']])
        print("****Sessions Length: ", len(sessions[data['sessionId']]))
        #sessions = {'d78b323a-f0f7-455e-94e7-06f51ca9dd1d': []}
        if not sessions[data['sessionId']]:
            print("\n---------신규 데이터 session에 메세지 넣기:")
            con_dict = {
                'id': data['conversationId'],
                'messages': [data['message'], aiMessage]
            }
            sessions[data['sessionId']].append(con_dict)
            print(f"\n[CMH] > 신규 데이터 반영 후 sessions[data['sessionId']] ", sessions[data['sessionId']])
        else:
            '''
            sessions:  
                {
                    '6134e4de-d30c-469f-b99f-65550afb9827': [], 
                    'bf1143e0-65cd-4d66-a281-fe62ea49ba91': [
                        {
                            'id': 'fa2ec32f-4e15-4188-829a-bb8f4c999385', 
                            'messages': [
                                    {
                                        'id': 'ca18fccc-82b6-4248-bf8d-1ac089727e31', 
                                        'content': 'hello', 
                                        'aiMessage': False, 
                                        'animate': False
                                    }, 
                                    {
                                        'content': 'Hello, I am AI', 
                                        'id': '92d0be30-2af0-44eb-ac86-1eceab8fee99', 
                                        'aiMessage': True, 
                                        'animate': True
                                    }
                            ]
                        }
                    ]
                }

            '''
            for session in sessions[data['sessionId']]:
                print("\n---------기존 데이터가 있는 session에 메세지 넣기: session['id'] == data['conversationId']", session['id'], data['conversationId'])
                session['messages'].append(data['message'])
                session['messages'].append(aiMessage)
                print(f"\n[CMH] > 기존 데이터가 반영 후 -> sessions[data['sessionId']]: ", sessions[data['sessionId']])

        response_data = sessions[data['sessionId']]
        print(f"\n[CMH] > response_data: ", response_data[0])
        await sio.emit("server-message", json.dumps(response_data[0]))



#세션 초기화
@sio.on("session-remove")
async def remove_session(sid, data): #sid: socket id
    print(f"\n[remove_session] > target_session_id: ", target_session_id)
    target_session_id = data['sessionId']
    
    if target_session_id in sessions:
        del sessions[target_session_id]


#소리를 텍스트로 변환한다. 
@sio.on("upload-file")
async def upload_file(sid, file): #sid: socket id
    file_name = uuid.uuid4()
    file_path = f"upload/{file_name}.mp3"
    print(f"\n[upload_file] > getFile...file_name: ", file_name)

    audio_data = file['data']
    
    #텍스트 저장 플로우 짜기
     
    try:
        #Save audio file
        with open(file_path, 'wb') as file:
            file.write(audio_data)
        #Open audio file
        audio_input = open(file_path, "rb") 

        async def convert_audio_to_text(audio_file):
            try:
                return openai.Audio.transcribe("whisper-1", audio_file)
            except Exception as e:
                print(e)
                return None

        message_decoded = await convert_audio_to_text(audio_input)
            #Check data value
        if not message_decoded:
            raise ConnectionRefusedError("Error occurred from Convert_Audio_To_Text")
        print(f"\n[upload_file] > message_decoded: ", message_decoded['text'])
   
        async def get_openai(content):
            return openai.ChatCompletion.create(
                model='gpt-4',
                messages=[
                    # GPT 역할 정의
                    {"role":"system", "content" : "You are an experienced English tutor who graduated from Harvard University in Boston.You are talking to a student who wants to practice speaking English. Help them practice speaking English by talking to your student and While talking to your student, help your student how to say what they would like to say. "},
                    # 질문
                    {"role":"user", "content" : content} 
                        
                ],
                max_tokens=30
            )
    
        # openai 객체가 async를 지원하지 않음 -> 비동기 함수에 동기를 넣기 위해 사용
        '''
        **[response.get('choices')[0].get('message').get('content')] : str 
                
                Hello! It's great to see you're ready to practice your English. How can I assist you today?
        
        '''
        text_to_openai = message_decoded['text']
        openai_response = await get_openai(text_to_openai) 
        print(f"\n[upload_file] > openai_response: ", openai_response["choices"][0]["message"]["content"])
        text = openai_response["choices"][0]["message"]["content"]
        
        audio_output = await convert_text_to_speech(text)

        if not audio_output:
            raise ConnectionRefusedError("Error occurred from Convert_Text_To_Audio")

        file_name = 'a.mp3'
        with open(file_name, 'wb') as file:
            file.write(audio_output)
        #Create a generator that yields chunks of data
        def iterfile():
            yield audio_output
        print(f"\n[upload_file] > audio_output: ", type(audio_output))
        await sio.emit("response-upload-file", audio_output)

    except Exception as e:
        print(f"\n[upload_file] > Exception: ", e)
        await sio.emit("response-upload-file", json.dumps(e))


'''
reload 옵션이나 workers 옵션을 사용할 때 필요한 Uvicorn의 요구사항
    -애플리케이션을 직접적으로 전달하는 대신에, 애플리케이션을 문자열 형태로 가져와야 함
    -애플리케이션을 가져오는 방법은 "패키지명:객체명" 형태로 가져오는 것

'''
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)