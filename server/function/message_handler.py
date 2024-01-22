import json
import uuid
import openai
from function.text_to_speech import convert_text_to_speech

'''
*[data] <class 'dict'> 
    {
        'sessionId': '2194c5d1-296c-42ce-9005-e0c36b5e45c4',
        'message': {'id': '17fc1aeb-367e-49cc-88e4-a6eb0ea68b91','content': 'hello', 'aiMessage': False, 'animate': False}, 
        'conversationId': 'b62b264c-6d25-4ec6-aa58-6f158ae6a68c'
    }

Sessions -> 객체 내 메세지 구조    
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
'''

async def message_handler(sid, data, sessions, type):
    #print(f"\n[message_handler] > sessions: ", sessions)
    #print(f"\n[MH] > message: ", data)
    
    #기존 단어와 합쳐서 보여주기
    previousConversation = [];
    existingConversation = sessions[data['sessionId']]
    
    # for message_obj in existingConversation['message']:
    #     if message_obj['aiMessage'] == False:
    #         previousConversation.append(message_obj['content'])
    #print("\n[MH] > existingConversation: ", existingConversation)
    if existingConversation == []:
        ex_message_obj = { 
            'role': 'user',
            'content': ''
        }
        previousConversation.append(ex_message_obj)
    else:
        #previousConversation = [previousConversation.append(message_obj['content']) for message_obj in existingConversation['message'] if message_obj['aiMessage'] == False]    
        for message_obj in existingConversation[0]['messages']:
            if message_obj['aiMessage'] == False:
                ex_message_obj = { 
                    'role': 'user',
                    'content': message_obj['content']
                }
                previousConversation.append(ex_message_obj)
            else :
                ex_message_obj = { 
                    'role': 'system',
                    'content': message_obj['content']
                }
                previousConversation.append(ex_message_obj)
    
    
    language = 'English'    
    openai_role = [
        {
            "role":"system", 
            "content" : f"""
                Your name is Emma. You born Korea. 
                You are an experienced {language} tutor who graduated from Harvard University in Boston.
                You are talking to a student who wants to practice speaking {language}. 
                Help them practice speaking {language} by talking to your student and While talking to your student, 
                help your student how to say what they would like to say. 
                As an English tutor, you provide accurate and easy-to-understand answers when users ask about English grammar, vocabulary, and pronunciation.
                You correct the user's sentences and explain why such corrections are necessary. Additionally, to aid learning, you can present example sentences or practice exercises.
                Answer the questions less than 50 words.
            """
        }
    ]    
    new_user_message = [
        {
            "role":"user", 
            "content" : data['message']['content']
        }
    ]
    openai_content = openai_role + previousConversation + new_user_message 

    #print("[MH] > previousConversation: ", previousConversation)
    #print("\n[MH] > openai_content: ", openai_content)

    async def get_openai(content):
        return openai.ChatCompletion.create(
            model='gpt-4',
            messages=content,
            max_tokens=100
        )
    
    # 기존 데이터와 합쳐서 클라이언트에 전송
    response = await get_openai(openai_content) 
    openai_message = response.get('choices')[0].get('message').get('content') if response else "Error occurred from AI"
    print("\n[MH] > ai_message_content: ", response.get('choices')[0].get('message').get('content'))

    if type == 'audio':
        #오디오 파일로 만들기
        audio = await convert_text_to_speech(openai_message)

    # 세션 아이디가 sessions에 존재하면 -> AI의 응답 메세지를 생성 후 세션에 추가하고 클라이언트에 전송하고.
    if data['sessionId'] in sessions:
        #print(f"\n[MH] > data['sessionId']: ", data['sessionId'])
        aiMessage = {
            'content': openai_message,
            'id': str(uuid.uuid4()),
            'aiMessage': True,
            'animate': True
        }
        #print("\n---------before for session in sessions[data['sessionId']]", sessions[data['sessionId']])
        #print("****Sessions Length: ", len(sessions[data['sessionId']]))
        #sessions = {'d78b323a-f0f7-455e-94e7-06f51ca9dd1d': []}
        if not sessions[data['sessionId']]:
            #print("\n---------신규 데이터 session에 메세지 넣기:")
            con_dict = {
                'id': data['conversationId'],
                'messages': [data['message'], aiMessage]
            }
            sessions[data['sessionId']].append(con_dict)
            #print(f"\n[MH] > 신규 데이터 반영 후 sessions[data['sessionId']] ", sessions[data['sessionId']])
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
                #print("\n---------기존 데이터가 있는 session에 메세지 넣기: session['id'] == data['conversationId']", session['id'], data['conversationId'])
                session['messages'].append(data['message'])
                session['messages'].append(aiMessage)
                #print(f"\n[MH] > 기존 데이터가 반영 후 -> sessions[data['sessionId']]: ", sessions[data['sessionId']])

        response_data = sessions[data['sessionId']]
        #print(f"\n[MH] > return_data > len(session), len(messages): ", len(response_data), len(response_data[0]['messages']))
        
        if type == 'audio':
            return response_data[0], audio
        else:
            return response_data[0], None
