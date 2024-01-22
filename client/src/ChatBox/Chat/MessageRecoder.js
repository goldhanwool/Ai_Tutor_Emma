import { ReactMediaRecorder } from 'react-media-recorder'
import '../ChatBox.css'
import { useSelector } from 'react-redux';

const RecoderMessage = ({handleStop}) => {
  const inputStopStaus = useSelector((state) => state.chatBox.inputStop);

  return (
    <div className='chat_voice_container'>
        <div className='chat_voice_container_inner'>
          <ReactMediaRecorder
              audio 
              onStop={handleStop}
              render={({ startRecording, stopRecording, status }) => (
                  <div>
                    <div>
                    {status !== "recording" ? (
                      <>
                        <button 
                            onMouseDown={startRecording}
                            onMouseUp={stopRecording}
                            className='audio_ready_button'
                            disabled={inputStopStaus === true}
                        >
                        <p className='record_status_text'>Ready</p>
                        </button>
                      </>                        
                      ) : (
                        <>
                          <button 
                              onMouseDown={startRecording}
                              onMouseUp={stopRecording}
                              className='audio_recoder_button'
                              disabled={inputStopStaus === true}
                          >
                          <p className='record_status_text'>Recoder</p>
                          </button>
                        </>                        
                      )}       
                  </div>
                  </div>
              )}
          >
              RecoderMessage
          </ReactMediaRecorder>
        </div>
      </div>

  )
}

export default RecoderMessage;