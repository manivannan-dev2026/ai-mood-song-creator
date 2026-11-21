import streamlit as st
import numpy as np
from scipy.io.wavfile import write
from gtts import gTTS
import random

st.set_page_config(page_title="Namma AI Music Studio", page_icon="🎧")

st.title("🎧 நம்ம AI Music Studio")
st.write("கீழே உள்ள பட்டனை அழுத்திய உடனே இசையும் தமிழ்ப் பாடலும் சத்தமாக ஒலிக்கும்!")

songs = {
    "🌟 உற்சாகம் (Energetic)": {
        "text": "புதிய விடியல் நம்மை அழைக்கிறதே, கனவுகள் யாவும் நனவாகிறதே! வானம் தாண்டி பறந்திடுவோம், வெற்றியின் சிகரம் தொட்டிடுவோம்!",
        "freqs": [261.63, 329.63, 392.00, 523.25, 659.25],
        "speed": 0.30
    },
    "🌙 இரவுப் பயணம் (Night Melody)": {
        "text": "நிலவின் ஒளியில் சாலை நீளுதே, தென்றல் காற்று பாடல் பாடுதே! இரவின் அமைதியில் இசை பிறக்க, இதயம் மகிழ்ச்சியில் மிதக்கிறதே!",
        "freqs": [220.00, 261.63, 329.63, 392.00, 329.63],
        "speed": 0.45
    },
    "☕ காலை புத்துணர்ச்சி (Morning)": {
        "text": "காலைக் கதிரவன் புன்னகை வீசுதே, புதிய நம்பிக்கை இதயத்தில் பிறக்குதே!",
        "freqs": [293.66, 369.99, 440.00, 587.33],
        "speed": 0.35
    }
}

mood = st.selectbox("🎶 இசை வகையைத் தேர்ந்தெடுக்கவும்:", list(songs.keys()))
custom_line = st.text_input("✍️ உங்கள் சொந்த வரிகளைச் சேர்க்க (Optional):")

if st.button("▶️ Play Song", type="primary", use_container_width=True):
    info = songs[mood]
    lyric = info["text"]
    if custom_line.strip():
        lyric = f"{lyric} {custom_line.strip()}"
        
    st.success(f"🎤 **பாடல் வரிகள்:**\n\n{lyric}")
    
    # 1. பின்னணி இசை உருவாக்கம் (.wav)
    sr = 44100
    track = np.array([], dtype=np.float32)
    for f in info["freqs"] * 3:
        t = np.linspace(0, info["speed"], int(sr * info["speed"]), False)
        tone = 0.6 * np.sin(2 * np.pi * f * t) * np.exp(-1.5 * t)
        track = np.concatenate((track, tone))
    write("beat.wav", sr, np.int16(track * 32767))
    
    # 2. தமிழ்க் குரல் பாடல் உருவாக்கம் (.mp3)
    tts = gTTS(text=lyric, lang='ta')
    tts.save("vocal.mp3")
    
    # இரண்டு பிளேயர்களிலும் தெளிவாகக் காட்டுகிறோம்
    st.subheader("🎙️ 1. பாடல் குரல் (Tamil Song Voice):")
    with open("vocal.mp3", "rb") as f1:
        st.audio(f1.read(), format="audio/mp3", autoplay=True)
        
    st.subheader("🎹 2. பின்னணி இசை மெட்டு (Background Music):")
    with open("beat.wav", "rb") as f2:
        st.audio(f2.read(), format="audio/wav")
