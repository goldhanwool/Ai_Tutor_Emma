import React, { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux';
import { v4 as uuid } from "uuid";
import { addMessage, createChatId, setSelectedConversationId } from '../chatBoxSlice';
import { sendMessageToBackend } from '../../Socket/SocketConn';

const MessageInput = () => {
    const [content, setContent] = useState("");
    const dispatch = useDispatch();
    const selectedConversationId = useSelector((state) => state.chatBox.selectedConversationId);

    const conversations = useSelector((state) => state.chatBox.conversations);
    //console.log("[MessageInput] > conversations: ", conversations)
    
    //for disable input field
    const selectedConversation = conversations.find(
        (item) => item.id === selectedConversationId
    )
    
    const proceedMessage = () => {
        const message = {
            id: uuid(),
            content,
            aiMessage: false,
            animate: false,
        };

        // Message Obj
        // {
        //     "id": "3affdd91-6849-42f4-ac8f-67dd828b1d79",
        //     "content": "hello",
        //     "aiMessage": false,
        //     "animate": false
        // }
        //console.log("[MessageInput] > proceedMessage > selectedConversationId, message: ", selectedConversationId, message)
        
        // save message to redux store
        let conversationId;
        
        if (!selectedConversationId) {
            conversationId = uuid();
            dispatch(setSelectedConversationId({conversationId})); //id의 key를 확인해봐
        } else {
            conversationId = selectedConversationId;
        }
        
        dispatch(
            addMessage({
                message: message, 
                conversationId: conversationId
        }));
        // send message to backend
        sendMessageToBackend(message, conversationId)
        // reset input field
        setContent("");
    }

    // // 만약 메세지 보내기 버튼이 있다면 아래 함수 활용
    // const handleSendMessage = () => {
    //     if (content.length > 0) {
    //         proceedMessage();
    //     }
    // }

    const handleKeyPressed = (event) => {
        if (event.code === "Enter" && content.length > 0) {
            proceedMessage();
        }
    };

    return (
        <div className='chat_input_container'>
          <div className='chat_input_container_inner'>
            {/* <button className="chat_change_button panel-item btn-icon add-file-button">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <line x1="22" y1="2" x2="11" y2="13"></line>
                    <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                </svg>
            </button> */}
            {/* <!-- 메시지 입력 필드 --> */}
            <input 
              className="chat_input_area panel-item" 
              placeholder="Type a message..." 
              value={content}
              onChange={(e) => setContent(e.target.value)}
              onKeyDown={handleKeyPressed}
            //   disabled={
            //         selectedConversation && 
            //         !selectedConversation.messages[
            //             selectedConversation.messages.length - 1
            //         ].aiMessage
            //     }
            />
            </div>
        </div>
      );
    };


export default MessageInput; 
