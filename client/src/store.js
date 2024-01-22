import { configureStore } from "@reduxjs/toolkit";
import chatBoxReducer from "./ChatBox/chatBoxSlice";

export const store = configureStore({
  reducer: {
    chatBox: chatBoxReducer,
  },
});



