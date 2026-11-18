import streamlit as st
import numpy as np
from gtts import gTTS
import io
import wave

st.set_page_config(page_title="AI Mood Song Creator", page_icon="🎵")

st.title("🎵 AI தமிழ் பாடல் & இசை உருவாக்கி")
st.write("உங்கள் மனநிலையைத் தேர்ந்தெடுங்கள்; அதற்கேற்ற பாடல் வரிகளும் இசையும் உடனே உருவாகும்!")

# 1. மனநிலைக்கு ஏற்ற பாடல் வரிகள் மற்றும் இசை சுரங்கள் (Frequencies)
mood_data = {
    "😊 மகிழ்ச்சி (Happy)": {
        "lyrics": "வானம் இன்று புதிதாய் சிரிக்கிறதே, வாழ்க்கை என்றும் அழகாய் மலர்கிறதே! புதிய பாதை நம்மை அழைக்கிறதே, வெற்றிப் பூக்கள் எங்கும் விரிகிறதே!",
        "notes": [261.63, 329.63, 392.00, 523.25, 392.00, 523.25], # துள்ளலான மேஜர் சுரங்கள்
        "speed": 0.35
    },
    "🔥 உத்வேகம் (Motivational)": {
        "lyrics": "தடைகள் உடைத்து நீ முன்னேறி வா, உன்னால் முடியும் என்று நம்பி வா! தோல்வி என்பது வெற்றியின் படிக்கட்டு, துணிந்து நின்றால் உலகம் உன் கைதட்டும்!",
        "notes": [293.66, 349.23, 440.00, 587.33, 440.00, 587.33], # வேகமான உத்வேக சுரங்கள்
        "speed": 0.30
    },
    "😌 அமைதி (Relaxing / Calm)": {
        "lyrics": "தென்றல் காற்று மெல்ல வீசுதே, மனதின் பாரம் யாவும் கரையுதே! நிலவின் ஒளியில் அமைதி பிறக்குதே, இனிய கனவுகள் கண்களில் மிதக்குதே!",
        "notes": [220.00, 261.63, 329.63, 392.00, 329.63, 261.63], # மென்மையான சுரங்கள்
        "speed": 0.60
    },
    "💔 சோகம் (Sad / Emotional)": {
        "lyrics": "மௌனமான இரவில் நினைவுகள் பேசுதே, பிரிவின் வலியில் இதயம் ஏங்குதே! கடந்து போன நாட்கள் மீண்டும் வருமா, கலங்கும் கண்களின் கண்ணீர் ஆறுமா!",
        "notes": [220.00, 246.94, 261.63, 329.63, 246.94, 220.00], # மைனர் சுரங்கள்
        "speed": 0.65
    }
}

# இசை உருவாக்கும் பைத்தான் ஃபங்ஷன் (Music Synthesizer)
def create_music_wav(notes, duration_per_note):
    sample_rate = 44100
    audio_data = np.array([], dtype=np.float32)
    
    for freq in notes * 2: # மெட்டை 2 முறை இசைக்கிறோம்
        t = np.linspace(0, duration_per_note, int(sample_rate * duration_per_note), False)
        # பியானோ போன்ற மென்மையான ஒலி அலை உருவாக்கம்
        wave_tone = 0.5 * np.sin(2 * np.pi * freq * t) * np.exp(-2 * t)
        audio_data = np.concatenate((audio_data, wave_tone))
        
    audio_int16 = np.int16(audio_data * 32767)
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_int16.tobytes())
    buf.seek(0)
    return buf

# பயனர் தேர்வு செய்யும் பகுதி
selected_mood = st.selectbox("இப்போது உங்கள் மனநிலை (Mood) எப்படி உள்ளது?", list(mood_data.keys()))
custom_line = st.text_input("நீங்கள் ஏதேனும் ஒரு வரியைச் சேர்க்க விரும்பினால் இங்கே டைப் செய்யவும் (Optional):")

if st.button("🎶 பாடல் & இசையை உருவாக்கு (Generate Song)"):
    info = mood_data[selected_mood]
    final_lyrics = info["lyrics"]
    if custom_line.strip():
        final_lyrics += " " + custom_line.strip()
        
    st.subheader("📜 உங்கள் பாடல் வரிகள்:")
    st.success(final_lyrics)
    
    # 1. பின்னணி இசை உருவாக்கம்
    st.subheader("🎹 பின்னணி இசை மெட்டு (Background Music):")
    music_buf = create_music_wav(info["notes"], info["speed"])
    st.audio(music_buf, format="audio/wav")
    
    # 2. தமிழ்க் குரல் ஒலி உருவாக்கம்
    st.subheader("🎙️ பாடல் வரிகள் குரல் வடிவில் (Tamil Voice):")
    try:
        tts = gTTS(text=final_lyrics, lang='ta')
        voice_buf = io.BytesIO()
        tts.write_to_fp(voice_buf)
        voice_buf.seek(0)
        st.audio(voice_buf, format="audio/mp3")
    except Exception as e:
        st.warning("குரல் ஒலி உருவாக்குவதில் சிறிய தாமதம் ஏற்பட்டுள்ளது. மீண்டும் முயற்சிக்கவும்.")
