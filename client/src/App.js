import { useEffect } from "react";
import ChatBox from "./ChatBox/ChatBox";
import { connectSocketServer, removeSession } from "./Socket/SocketConn";
import Recoder from "./Recoder/Recoder";
import { useDispatch } from "react-redux";
import { removeConversations, setConversations } from "./ChatBox/chatBoxSlice";

export default function App() {
  const dispatch = useDispatch();
  
  useEffect(() => {
    connectSocketServer();
  }, []);

  // 페이지를 벗어날 때 이벤트 리스너 추가
  useEffect(() => {
    const handleBeforeUnload = (event) => {
      removeSession(); // 게시물 삭제 함수 호출
      event.returnValue = `변경사항이 저장되지 않을 수 있습니다.`; // 사용자에게 경고 메시지 표시
    };

    window.addEventListener('beforeunload', handleBeforeUnload);

    // 컴포넌트가 언마운트될 때 이벤트 리스너 제거
    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
    };
    }, []);

  return (
    <div>
      {/* <Recoder /> */}
      <ChatBox /> 
    </div>
  )
}


