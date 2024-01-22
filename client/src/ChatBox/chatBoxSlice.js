import { createSlice } from "@reduxjs/toolkit";

//conversations 데이터 구조
// [{ 
//     id: "bd579cf7-15d0-4333-8569-cd432d3bacce", 
//     messages: [{id: "27c814fe-163f-4355-b593-6cee3766d703", content: "hello", aiMessage: false}]
// },
//  { 
//     id: "bd579cf7-15d0-4333-8569-cd432d3bacce", 
//     messages: [{id: "27c814fe-163f-4355-b593-6cee3766d703", content: "hello", aiMessage: false}]
// }]
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
            //message => {id: "27c814fe-163f-4355-b593-6cee3766d703", content: "hello", aiMessage: false}

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
            //console.log("[chatBoxSlice] > setConversations > action.payload: ", action.payload)
            state.conversations = action.payload;
            state.sessionEstablished = true;  
        },
        setConversationHistory: (state, action) => {
            //console.log("[chatBoxSlice] > setConversationHistory > action.payload: ", action.payload)
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