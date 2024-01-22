import React, { useState, useRef, useEffect } from "react";

const SlowText = (props) => {
    const { speed, text } = props;
    const [placeholder, setPlaceholder] = useState(text[0]);

    const index = useRef(0);

    useEffect(() => {
        function tick() {
            index.current++;
            setPlaceholder((prev) => prev + text[index.current]);
        }
        if (index.current < text.length - 1) {
            let addChar = setInterval(tick, speed);
            return () => clearInterval(addChar);
        }
        }, [placeholder, speed, text]
    );

    return <span>{placeholder}</span>;
}

const Message = ({ content, aiMessage, animate }) => {
    return (
      <div>
          {aiMessage ? ( 
            <div className='chat_message_block'> 
                <div className='chat_person_avatar'>
                    <img src="https://randomuser.me/api/portraits/women/44.jpg" alt="Monika Figi" />
                </div>
                <div className='chat_message_box'>
                    <div className="chat_message_design">
                        <SlowText speed={10} text={content} />
                    </div>              
                </div>
            </div>
          ) : (
            <div className='chat_message_block reversed'> 
                <div className='chat_person_avatar'>
                    <img src="https://randomuser.me/api/portraits/men/35.jpg" alt="Monika Figi" />
                </div>
                <div className='chat_message_box'>
                    <div className="chat_message_design">
                        <span>{content}</span>
                    </div>              
                </div>
            </div>
          )}
    </div>
    );
  };
  
  export default Message;
  