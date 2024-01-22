import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    sessionEstablished: false,
    conversations: [], 
    selectedConversationId: null,
    audio: null,
    inputStop: false,
}

const chatBoxSlice = createSlice({
    name: 'chatBox', // name은 reducer의 이름이다.
    initialState,
    reducers: {
        setSelectedConversationId: (state, action) => {
            state.selectedConversationId = action.payload;
        },
        addMessage: (state, action) => {
            const { message, conversationId } = action.payload;

            const conversation = state.conversations.find(
                (item) => item.id === conversationId
            );
            
            if (conversation) {
                conversation.messages.push(message);
            } else {
                state.conversations.push({
                    id: conversationId,
                    messages: [message], //객체를 리스트에 밀어넣는다.
                });
            }
        },
        setConversations: (state, action) => {
            state.conversations = action.payload;
            state.sessionEstablished = true;  
        },
        setConversationHistory: (state, action) => {
            const { id, messages } = action.payload;

            const conversation = state.conversations.find(
                (item) => item.id === id
            );
            if (conversation) {
                conversation.messages = messages;
            } else {
                state.conversations.push({
                    id,
                    messages,
                });
            }
        },
        removeConversations: (state) => {
            state.conversations = [];
            state.selectedConversationId = null;
        },
        setInputStop: (state, action) => {
            state.inputStop = action.payload;
        },
    },
})//createSlice

export const { 
    setSelectedConversationId,
    addMessage,
    setConversations,
    setConversationHistory,
    removeConversations,
    setInputStop
} = chatBoxSlice.actions;

export default chatBoxSlice.reducer;