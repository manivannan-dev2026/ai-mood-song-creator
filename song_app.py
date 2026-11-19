import streamlit as st
import numpy as np
from scipy.io.wavfile import write
from gtts import gTTS
import random

st.set_page_config(page_title="Namma AI Music Studio", page_icon="🎧", layout="centered")

st.title("🎧 நம்ம AI Music Studio")
st.caption("Spotify-ஐ விடச் சிறப்பானது — உங்கள் மனநிலைக்கு ஏற்ப உடனுக்குடன் இசையும் பாடலும் உருவாகும் தளம்!")

# பாடல் வரிகள் மற்றும் இசை ராகங்கள் (Ragas / Frequencies)
songs_library = {
    "🌟 உற்சாகம் (Energetic Beat)": {
        "lines": [
            "புதிய விடியல் நம்மை அழைக்கிறதே, கனவுகள் யாவும் நனவாகிறதே!",
            "வானம் தாண்டி பறந்திடுவோம், வெற்றியின் சிகரம் தொட்டிடுவோம்!",
            "தடைகள் யாவும் பனிபோல் விலகும், உன்னால் முடியும் உலகம் வணங்கும்!"
        ],
        "freqs": [261.63, 329.63, 392.00, 523.25, 659.25],
        "tempo": 0.25
    },
    "🌙 இரவுப் பயணம் (Night Drive Melody)": {
        "lines": [
            "நிலவின் ஒளியில் சாலை நீளுதே, தென்றல் காற்று பாடல் பாடுதே!",
            "மௌனமான இரவின் அழகினிலே, மனதின் பாரம் மெல்ல கரையுதே!",
            "தூரத்து விளக்குகள் மின்னிச் சிரிக்க, இனிய பயணம் தொடர்கிறதே!"
        ],
        "freqs": [220.00, 261.63, 329.63, 392.00, 329.63],
        "tempo": 0.45
    },
    "☕ காலை புத்துணர்ச்சி (Morning Refresh)": {
        "lines": [
            "காலைக் கதிரவன் புன்னகை வீசுதே, புதிய நம்பிக்கை இதயத்தில் பிறக்குதே!",
            "பறவைகள் பாடும் இசையோடு சேர்ந்து, இன்றைய நாளை இனிதே தொடங்குவோம்!"
        ],
        "freqs": [293.66, 369.99, 440.00, 587.33, 440.00],
        "tempo": 0.35
    }
}

# பின்னணி இசையும் தாளமும் (Beat + Melody) உருவாக்கும் கருவி
def generate_studio_beat(freqs, tempo, filename="studio_beat.wav"):
    sr = 44100
    full_track = np.array([], dtype=np.float32)
    
    for _ in range(3): # 3 சுற்றுகள் இசைக்கிறோம்
        for f in freqs:
            t = np.linspace(0, tempo, int(sr * tempo), False)
            # மென்மையான இசை + பேஸ் தாளம் (Bass Beat)
            melody = 0.4 * np.sin(2 * np.pi * f * t) * np.exp(-2 * t)
            bass = 0.3 * np.sin(2 * np.pi * (f / 2) * t) * np.exp(-4 * t)
            full_track = np.concatenate((full_track, melody + bass))
            
    write(filename, sr, np.int16(full_track * 32767))
    return filename

# பயனர் திரை (Music Player UI)
mood = st.selectbox("🎶 இசை வகையைத் தேர்ந்தெடுக்கவும்:", list(songs_library.keys()))
custom_text = st.text_input("✍️ உங்கள் சொந்த வரிகளைச் சேர்க்க (விரும்பினால்):")

if st.button("▶️ Play Song", use_container_width=True, type="primary"):
    selected = songs_library[mood]
    # ஒவ்வொரு முறை அழுத்தும்போதும் வெவ்வேறு வரிகளைத் தேர்ந்தெடுக்கும்
    chosen_lyric = random.choice(selected["lines"])
    if custom_text.strip():
        chosen_lyric = f"{chosen_lyric} {custom_text.strip()}"
        
    st.markdown(f"### 🎤 இப்போது ஒலிக்கும் பாடல்:\n> *\"{chosen_lyric}\"*")
    
    # இசை மற்றும் குரல் உருவாக்கம்
    beat_file = generate_studio_beat(selected["freqs"], selected["tempo"])
    tts = gTTS(text=chosen_lyric, lang='ta')
    tts.save("vocal.mp3")
    
    col1, col2 = st.columns(2)
    with col1:
        st.caption("🎹 பின்னணி இசை (Studio Beat)")
        st.audio(beat_file, autoplay=True)
    with col2:
        st.caption("🎙️ பாடல் குரல் (AI Vocals)")
        st.audio("vocal.mp3", autoplay=True)
