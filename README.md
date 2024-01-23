# GPT-English-Tutor

This project is to make AI English teacher Emma, which is made by connecting GPT.
- FrontEnd : ***React***
- BackEnd : ***FastAPI***
- Library : **Redux**, **Socket.IO**

## Environment Variables

1. Create a file named `.env` in your root directory.
2. An OpenAI API key and an Eleven Labs API key are required.

## Frontend: React

### Setup
- Ensure Node.js is installed.
- Install dependencies with `npm install`.
- Start the development server with `npm start`.

### Structure
- `src/`: Source files for React components.
  + `ChatBox/`: Components that send and receive messages
    + `Chat/`
        + `ChatBox.css`:
        + `ChatBox.js`:
        + `ChatBoxSlice.js`:
  + `Socket/`: Socket communication
    + `SocketConn.js`
  + `App.js`
- `public/`: Static assets.

## Backend: FastAPI

### Setup
- Ensure Python is installed.
- Install dependencies with `pip install -r requirements.txt`.
- Run the server with `uvicorn main:app --reload` or `python main.py`.

   
### Structure
- `function/`: AI Message from OpenAI, STT, TTS
- `main.py`: Socket Connection

## Deployment
- FrontEnd : Firebase
- BackEnd : AWS

## Reference
- Link: [ChatGPT Clone with React, SocketIO and OpenAI API 2023][udemy_link]

[udemy_link]: https://www.udemy.com/course/chatgpt-with-react-and-openai-api-2023-build-your-own-app/

- Link: [ChatGPT AI Voice Chatbot Build with React and FAST API Combo][udemy_link]

[udemy_link]: https://www.udemy.com/course/chatgpt-ai-voice-chatbot-build-with-react-and-fast-api-combo/