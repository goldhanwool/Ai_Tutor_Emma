import React from 'react'
import Messages from './Messages';
import { v4 as uuid } from "uuid";
import { useDispatch, useSelector } from 'react-redux';
import { setSelectedConversationId } from '../chatBoxSlice';

const ChatMain = () => {
    const dispatch = useDispatch();
    const chatId = useSelector((state) => state.chatBox.selectedConversationId);
    
    //chatId를 먼저 할당해야함. 텍스트를 쓰면서 할당시 useState와 같이 바로 반영되지 않음
    if (!chatId) {
        const conversationId = uuid();
        dispatch(setSelectedConversationId(conversationId));
        //console.log(`[ChatMain] > new chatId: ${conversationId}`);
    } else {
        
        //console.log(`[ChatMain] > chatId: ${chatId}`);
    }

    return (
        <div>
            {!chatId ? ( 
                <div>Id creating ...</div> 
            ) : (
                <Messages />
            )
            }
        </div>
    )
}

export default ChatMain;