import io from 'socket.io-client';
import { store } from '../store'
import { setInputStop, setConversationHistory, setConversations } from '../ChatBox/chatBoxSlice';


let socket;
const localUrl = "http://localhost:8000"

export const connectSocketServer = () => {

    socket = io(`${localUrl}`);
    socket.on('connect', () => {
        console.log(`...>> Connected to Socket server Id -> ${socket.id}`);
        const socketId = socket.id;

        // server session check 
        socket.emit('session-history', {
            sessionId: localStorage.getItem('sessionId'), //localStroage에서 세션 아이디를 가져옴
        });

        socket.on('session-details', (data) => {
            console.log(`....>> [Socket session-details] -> ${data}`);
             
            //!주의! data는 string이다. Json.parse를 해줘야한다. 
            const { sessionId, conversations } = JSON.parse(data);
            console.log(`....>> [Socket session-details] -> ${sessionId}`);
            localStorage.setItem('sessionId', sessionId);//localStroage에 세션 아이디 저장 
            store.dispatch(setConversations(conversations));
        });

        // **response from server -> socket.on('message'...
        // [
        //   {
        //     'id': 'fa2ec32f-4e15-4188-829a-bb8f4c999385', 
        //     'messages': [
        //         {'id': 'd9542952-ed1c-4cbe-9cf8-a7d7688c520d', 'content': 'hello', 'aiMessage': False, 'animate': False}, 
        //         {'id': 'b7c57f8a-386f-4329-a780-daf226ca1c18', 'content': 'Hello, I am AI', 'aiMessage': True, 'animate': True}
        //         ]
        //    },
        // ]
        socket.on('server-message', (data) => { //오디오 파일도 같이 들어와야함. 
            store.dispatch(setConversationHistory(JSON.parse(data)));
        });

        socket.on('response-upload-file', (data) => {
            //console.log(`....>> [Socket message] -> ${data}`); //type is 'Object' -> [object, arrayBuffer] 형식으로 들어옴 
            const audioBlob = new Blob([data], { type: 'audio/mp3' });  //arrayBuffer를 생성자에 넣다
            // Blob을 이용해 오디오 URL 생성
            const audioUrl = URL.createObjectURL(audioBlob);
            // 오디오 URL을 사용하여 오디오 재생
            const audio = new Audio(audioUrl);

            store.dispatch(setInputStop(false));
            audio.play();
        });
        socket.on('reponse-remove-session', (data) => {
            console.log(`....>> [Socket reponse-remove-session] -> ${data}`); 
        });

    });
}

export const sendMessageToBackend = (message, conversationId) => {
    socket.emit('client-message', {
        sessionId: localStorage.getItem('sessionId'),
        message, 
        conversationId
    });
}

export const removeSession = () => {
    socket.emit('remove-session', {
        sessionId: localStorage.getItem('sessionId'),
    });
    store.dispatch(setConversations([]));
    socket.disconnect();    
    connectSocketServer();
}

export const sendFileToServer = (conversationId, file) => {
    store.dispatch(setInputStop(true));

    socket.emit('upload-file', {
        sessionId: localStorage.getItem('sessionId'), //localStroage에서 세션 아이디를 가져옴
        conversationId: conversationId,
        data: file
    });
}
