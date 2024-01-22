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

    const handleKeyPressed = (event) => {
        if (event.code === "Enter" && content.length > 0) {
            proceedMessage();
        }
    };

    return (
        <div className='chat_input_container'>
          <div className='chat_input_container_inner'>
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
