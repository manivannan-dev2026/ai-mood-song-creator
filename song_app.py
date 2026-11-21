import streamlit as st
import speech_recognition as sr
from youtubesearchpython import VideosSearch

st.set_page_config(page_title="Alexa Style Voice Music Player", page_icon="🎙️")

st.title("🎙️ சினிமா ஸ்டைல் Voice Music Player")
st.write("மைக் பட்டனை அழுத்திப் பாடல் பெயரைச் சொல்லுங்கள் (அல்லது டைப் செய்யுங்கள்), நிஜப் பாடல் உடனே ஓடும்!")

# 1. வாய்ஸ் ரெக்கார்டர் (Browser Mic Input)
audio_value = st.audio_input("🎤 மைக்கை அழுத்திப் பேசுங்கள் (எ.கா: 'Play Arabic Kuthu song' அல்லது 'Leo song'):")

song_query = ""

if audio_value:
    r = sr.Recognizer()
    try:
        with sr.AudioFile(audio_value) as source:
            audio_data = r.record(source)
            # பேசியதை எழுத்தாக மாற்றுகிறோம்
            spoken_text = r.recognize_google(audio_data)
            st.success(f"🗣️ நீங்கள் சொன்னது: **{spoken_text}**")
            # "Alexa play..." என்று சொன்னால் அதில் உள்ள தேவையற்ற வார்த்தைகளை நீக்கிப் பாடல் பெயரை மட்டும் எடுக்கிறோம்
            clean_query = spoken_text.lower().replace("alexa", "").replace("play", "").replace("the song", "").strip()
            song_query = clean_query if clean_query else spoken_text
    except Exception:
        st.warning("⚠️ குரல் தெளிவாகக் கேட்கவில்லை. மீண்டும் பேசவும் அல்லது கீழே டைப் செய்யவும்!")

# 2. டைப் செய்தும் தேடும் வசதி (Backup Search)
typed_query = st.text_input("🔍 அல்லது பாடல் பெயரை இங்கே டைப் செய்யவும்:", value=song_query)

if typed_query:
    with st.spinner(f"🎶 '{typed_query}' பாடல் தேடப்படுகிறது..."):
        try:
            search = VideosSearch(typed_query + " official song", limit=1)
            results = search.result()["result"]
            
            if results:
                video_url = results[0]["link"]
                video_title = results[0]["title"]
                st.subheader(f"▶️ இப்போது ஒலிப்பது: {video_title}")
                # நேரடியாக உங்கள் ஆப்பிற்குள்ளேயே நிஜப் பாடல் ஓடும்!
                st.video(video_url, autoplay=True)
            else:
                st.error("❌ பாடல் கிடைக்கவில்லை. வேறு பெயர் சொல்லிப் பாருங்கள்.")
        except Exception as e:
            st.error(f"தேடுவதில் சிறிய தாமதம்: {e}")
          
