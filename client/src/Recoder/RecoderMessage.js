import { ReactMediaRecorder } from 'react-media-recorder'
// import { RecordIcon } from './RecordIcon' //jsx 파일만 가능
// import { BsChatLeft } from "react-icons/bs";

const RecoderMessage = ({handleStop}) => {
  return (
    <ReactMediaRecorder
      audio 
        onStop={handleStop}
        render={({ startRecording, stopRecording, status }) => (

            <div>
                <button 
                    onMouseDown={startRecording}
                    onMouseUp={stopRecording}
                    className='voice_button'
                >
                </button>
                <p className='record_status_text'>{status}</p>
            </div>

        )}
    >
        RecoderMessage
    </ReactMediaRecorder>
  )
}

export default RecoderMessage;