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
    previousConversation = [];
    existingConversation = sessions[data['sessionId']]
    
    if existingConversation == []:
        ex_message_obj = { 
            'role': 'user',
            'content': ''
        }
        previousConversation.append(ex_message_obj)
    else:
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

    if data['sessionId'] in sessions:
        aiMessage = {
            'content': openai_message,
            'id': str(uuid.uuid4()),
            'aiMessage': True,
            'animate': True
        }

        if not sessions[data['sessionId']]:
            con_dict = {
                'id': data['conversationId'],
                'messages': [data['message'], aiMessage]
            }
            sessions[data['sessionId']].append(con_dict)

        else:
            for session in sessions[data['sessionId']]:
                session['messages'].append(data['message'])
                session['messages'].append(aiMessage)

        response_data = sessions[data['sessionId']]
     
        if type == 'audio':
            return response_data[0], audio
        else:
            return response_data[0], None
