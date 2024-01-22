import React, { useEffect, useState } from 'react'
import './Recoder.css'
import { connectSocketServer, sendFileToServer } from '../Socket/SocketConn'
import { useSelector } from 'react-redux';
import io from 'socket.io-client';
import RecoderMessage from './RecoderMessage';
import axios from 'axios'
import { useDispatch } from 'react-redux';
import { v4 as uuid } from "uuid";
import { setSelectedConversationId } from '../ChatBox/chatBoxSlice';

const Recoder = ({audio}) => {
    const dispatch = useDispatch();
   
    const chatId = useSelector((state) => state.chatBox.selectedConversationId);
    
    //chatId를 먼저 할당해야함. 텍스트를 쓰면서 할당시 useState와 같이 바로 반영되지 않음
    if (!chatId) {
        const conversationId = uuid();
        dispatch(setSelectedConversationId(conversationId));
        console.log(`[ChatMain] > new chatId: ${conversationId}`);
    } else {
        console.log(`[ChatMain] > chatId: ${chatId}`);
    }
    
    const [fileContent, setFileContent] = useState('');
    const [isLoading, setIsLoading] = useState(false)
    const [messages, setMessages] = useState([])
    const [blob, setBlob] = useState("")

    // useEffect(() => {
    //     const socket = io('서버 주소');
    //     // 'some_event' 이벤트에 대한 리스너 설정
    //     socket.on('response-upload-file', (data) => {
    //         console.log(`....>> [Socket message] > Recoder -> ${data}`); //type is 'Object' -> [object, arrayBuffer] 형식으로 들어옴 
            
    //         const audioBlob = new Blob([data], { type: 'audio/mp3' }); 
    //         const audioUrl = URL.createObjectURL(audioBlob);
    //         const audio = new Audio(audioUrl);
    //         audio.play();

    //         setFileContent(audio);
    //     });
    // }, []);

    const createBloburl = (data) => {
        //JavaScript의 Blob 객체를 생성하는 것을 나타냅니다. Blob 객체는 불변(immutable)한 데이터를 표현하는 데 사용됩니다.
        const blob = new Blob([data], {type: 'audio/mpeg'}); 
        const url = window.URL.createObjectURL(blob);
        return url;
    }
    const conversationId = useSelector((state) => state.chatBox.selectedConversationId);
    const handleStop = async(bloburl) => {    
        const response = await fetch(bloburl);
        const blob = await response.blob();
        const arrayBuffer = await blob.arrayBuffer();
        sendFileToServer(conversationId, arrayBuffer);
    }

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setFileContent(file);
        } else {
            console.log("no file")
        }
    }    

    const handleSendVoice = async () => {
        if (fileContent !== '') {
            sendFileToServer(fileContent);
        }
    }
    
    return (
    <div id='chat_container' className='--dark-theme'>
    <div className='chat_container_inner'>
      <div className='chat_message_block'> 
          <div className='chat_person_avatar'>
              <img src="https://randomuser.me/api/portraits/women/44.jpg" alt="Monika Figi" />
          </div>
          <div className='chat_message_box'>
              <div className="chat_message_design">
              {/* <span>{content}</span> */}
              {/* {audio ? <audio controls src={audio.audioUrl}></audio> : null} */}
              </div>              
          </div>
      </div>
      <div className='chat_voice_container'>
          <div className='chat_voice_container_inner'>
          {/* <input type="file" onChange={handleFileChange} />
            <button 
                className='voice_button'
                onClick={handleSendVoice}
           ></button> */}
            {/* <audio src={blob} controls /> */}
            <RecoderMessage handleStop={handleStop}/>
        </div>
       </div>
    </div>
    </div>
  )
}

export default Recoder;