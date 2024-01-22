import React, { useEffect, useRef, useState } from 'react'
import Message from './Message';
import MessageInput from './MessageInput';
import { useSelector } from 'react-redux';
import { removeSession, sendFileToServer } from '../../Socket/SocketConn';
import RecoderMessage from './MessageRecoder';


const Messages = ({ content, aiMessage, animate, chatId }) => {
    // const conversation = {
    //     id: "1",
    //     messages: [{
    //         id: "1",
    //         content: "Hello",
    //         aiMessage: true,
    //         animate: false
    //     }]
    // }
    const { selectedConversationId, conversations } = useSelector(
        (state) => state.chatBox
    );
    const conversationId = useSelector((state) => state.chatBox.selectedConversationId);

    const conversation = conversations.find(
        (item) => item.id ===  selectedConversationId
    );

    const scrollRef = useRef();
    const scrollToButton = () => {
        scrollRef.current.scrollIntoView({ behavior: "smooth" })
    }
    useEffect(
        scrollToButton,
        [conversation?.messages]
    )

    const handleStop = async(bloburl) => {    
        const response = await fetch(bloburl);
        const blob = await response.blob();
        const arrayBuffer = await blob.arrayBuffer();

        if (arrayBuffer.byteLength < 1) {
            console.log("arrayBuffer.byteLength: ", arrayBuffer.byteLength);
            alert("값이 너무 작거나 없습니다.");

        } else {
            sendFileToServer(conversationId, arrayBuffer);
        }
    }

    const [isVoiceBtn, setIsVoiceBtn] = useState(false);
    const handleReset = () => { 
        alert("Reset Conversation");
        removeSession();
    }

    return (
        <div id='chat_container' className='--dark-theme'>
            <div className='header_nav'>
                {isVoiceBtn ? (<>
                <div>
                    <button 
                        className="tv_change_button btn_icon_text"
                        onClick={() => setIsVoiceBtn(false)}
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <line x1="22" y1="2" x2="11" y2="13"></line>
                            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                        </svg>
                    </button>
                </div>
                </>) : (<>
                <div>
                    <button 
                        className="tv_change_button btn_icon_voice"
                        onClick={() => setIsVoiceBtn(true)}
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 512 512">
                            <path d="M256 0C114.84 0 0 114.84 0 256s114.84 256 256 256 256-114.84 256-256S397.16 0 256 0zm0 480C132.48 480 32 379.52 32 256S132.48 32 256 32s224 100.48 224 224-100.48 224-224 224z"></path>
                            <path d="M352 160H160v192h192V160z"></path>
                        </svg>
                    </button>
                </div>
                </>)}
                <button 
                    className="remove_button btn_icon_remove"
                    onClick={() => handleReset()}
                >
                    <svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="100" height="100" viewBox="0 0 50 50">
                        <path d="M 21 2 C 19.354545 2 18 3.3545455 18 5 L 18 7 L 10.154297 7 A 1.0001 1.0001 0 0 0 9.984375 6.9863281 A 1.0001 1.0001 0 0 0 9.8398438 7 L 8 7 A 1.0001 1.0001 0 1 0 8 9 L 9 9 L 9 45 C 9 46.645455 10.354545 48 12 48 L 38 48 C 39.645455 48 41 46.645455 41 45 L 41 9 L 42 9 A 1.0001 1.0001 0 1 0 42 7 L 40.167969 7 A 1.0001 1.0001 0 0 0 39.841797 7 L 32 7 L 32 5 C 32 3.3545455 30.645455 2 29 2 L 21 2 z M 21 4 L 29 4 C 29.554545 4 30 4.4454545 30 5 L 30 7 L 20 7 L 20 5 C 20 4.4454545 20.445455 4 21 4 z M 11 9 L 18.832031 9 A 1.0001 1.0001 0 0 0 19.158203 9 L 30.832031 9 A 1.0001 1.0001 0 0 0 31.158203 9 L 39 9 L 39 45 C 39 45.554545 38.554545 46 38 46 L 12 46 C 11.445455 46 11 45.554545 11 45 L 11 9 z M 18.984375 13.986328 A 1.0001 1.0001 0 0 0 18 15 L 18 40 A 1.0001 1.0001 0 1 0 20 40 L 20 15 A 1.0001 1.0001 0 0 0 18.984375 13.986328 z M 24.984375 13.986328 A 1.0001 1.0001 0 0 0 24 15 L 24 40 A 1.0001 1.0001 0 1 0 26 40 L 26 15 A 1.0001 1.0001 0 0 0 24.984375 13.986328 z M 30.984375 13.986328 A 1.0001 1.0001 0 0 0 30 15 L 30 40 A 1.0001 1.0001 0 1 0 32 40 L 32 15 A 1.0001 1.0001 0 0 0 30.984375 13.986328 z"></path>
                    </svg>
                </button>
            </div>
            <div className='chat_container_inner'>
                {conversation?.messages.map((item, index) => (
                <Message
                    key={item.id} 
                    content={item.content} 
                    aiMessage={item.aiMessage} 
                    animate={index === conversation.messages.length - 1 && item.aiMessage}
                />
                ))}
                <div ref={scrollRef}></div>
            </div>

            {isVoiceBtn ? 
            (<>         
                <div>
                    <MessageInput />     
                </div>    
            </>) : (<>
                <div>
                    <RecoderMessage handleStop={handleStop}/>     
                </div>
            </>)        
            }
        </div>
    )
}

export default Messages;