import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration

RTC_CONFIGURATION = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.frame_count = 0

    def recv(self, frame):
        self.frame_count += 1
        if self.frame_count % 60 == 0:
            st.experimental_set_query_params(frame_count=self.frame_count)
        return frame

def main():
    st.title("Live Stream")

    webrtc_ctx = webrtc_streamer(
        key="example",
        rtc_configuration=RTC_CONFIGURATION,
        video_processor_factory=VideoProcessor,
        async_processing=True,
    )

    if webrtc_ctx.video_transformer:
        st.write("Transforming video...")
    else:
        st.write("Waiting for input...")

    st.write(f"Frame count: {st.experimental_get_query_params().get('frame_count', [0])[0]}")

if __name__ == "__main__":
    main()

