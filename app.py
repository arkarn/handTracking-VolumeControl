import streamlit as st
from streamlit_webrtc import VideoHTMLAttributes, webrtc_streamer
from streamlit_player import st_player, _SUPPORTED_EVENTS
import HandTrackingModule as htm


# from streamlit_gallery.utils.readme import readme
import numpy as np
import time
VOLUME = 0.5 #np.interp(int(time.time()//10)%10, [0,9], [0, 1])
import av

st.set_page_config(layout="wide")
detector = htm.handDetector()

def video_frame_callback(frame: av.VideoFrame):
    frame = frame.to_ndarray(format="bgr24")  # Decode and convert frame to RGB
    frame, vol = detector.drawHandsAndGetVolume(frame, draw=True, needConversionToRGB=False)
    global VOLUME
    VOLUME = np.clip(vol, 0.0, 1.0)
    print(f"VOLUME={VOLUME}")
    # frame = detector.findHands(frame, draw=True, needConversionToRGB=False)
    return av.VideoFrame.from_ndarray(frame, format="bgr24")  # Encode and return BGR frame



def main():

    col1, col2 = st.columns(spec=2, gap="medium")

    with col1:
        ctx = webrtc_streamer(
            key="handTracking-VolumeControl",
            video_frame_callback=video_frame_callback,
            # audio_frame_callback=audio_frame_callback,
            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},  # Add this to config for cloud deployment.
            media_stream_constraints={"video": {"height": {"ideal": 480}}, "audio": True},
            video_html_attrs=VideoHTMLAttributes(autoPlay=True, controls=False, muted=False),
        )

    with col2:
        options = {
        "events": st.multiselect("Events to listen", _SUPPORTED_EVENTS, ["onProgress"]),
        "progress_interval": 100,
        "volume": VOLUME, #st.slider("Volume", 0.0, 1.0, 1.0, .01),
        "playing": st.checkbox("Playing", False),
        "loop": st.checkbox("Loop", False),
        "controls": st.checkbox("Controls", True),
        "muted": st.checkbox("Muted", False),
    }
        url = st.text_input("First URL", "https://youtu.be/c9k8K1eII4g")
        event = st_player(url, **options, key="youtube_player")
        # st.write(event)

    

if __name__ == "__main__":
    main()