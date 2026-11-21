import streamlit as st
import streamlit.components.v1 as components
from youtubesearchpython import VideosSearch
import random

st.set_page_config(page_title="Hands-Free Voice DJ", page_icon="🎙️")

st.title("🎙️ 'Hey Siri' ஸ்டைல் Hands-Free DJ")
st.write("ஒருமுறை மைக் அனுமதி கொடுத்தால் போதும்; அதன்பிறகு போனைத் தொடாமலேயே பேசலாம்!")

# URL வழியாக குரல் கட்டளை வந்தால் பாடலைப் பிளே செய்யும் பகுதி
query_params = st.query_params
mood_val = query_params.get("mood", "")

if mood_val:
    any_songs = [
        "Arabic Kuthu Tamil video song",
        "Naa Ready Leo Tamil song",
        "Rowdy Baby Tamil video song",
        "Munbe Vaa Tamil melody song",
        "Why This Kolaveri Di official song"
    ]
    if any(w in mood_val.lower() for w in ["எது", "சரி", "any", "anything", "random"]):
        search_q = random.choice(any_songs)
        st.success("🤖 Siri DJ: சரி, உங்களுக்காக ஒரு சூப்பர் பாடலைப் போடுகிறேன்! 🎶")
    else:
        search_q = f"{mood_val} Tamil hit song"
        st.success(f"🤖 Siri DJ: '{mood_val}' மூடிற்கு ஏற்ற பாடல் இதோ! 🎶")

    search = VideosSearch(search_q, limit=1)
    res = search.result()["result"]
    if res:
        st.subheader(f"▶️ {res['title']}")
        st.video(res["link"], autoplay=True)

    if st.button("🔄 மீண்டும் குரல் கட்டளைக்குத் திரும்ப (Listen Again)"):
        st.query_params.clear()
        st.rerun()

else:
    # தொடர்ச்சியாகக் குரலைக் கவனிக்கும் Hands-Free JavaScript இயந்திரம்
    siri_html = """
    <div style="text-align:center; padding:20px; background:#1e1e2f; color:white; border-radius:15px;">
        <h3 id="status">🎙️ கீழே உள்ள பட்டனை ஒருமுறை அழுத்தி Hands-Free ஆன் செய்யவும்</h3>
        <p id="heard" style="color:#00ffcc; font-size:18px;"></p>
        <button onclick="startSiri()" style="padding:12px 25px; font-size:16px; background:#ff4b4b; color:white; border:none; border-radius:25px; cursor:pointer;">
            🟢 Start Hands-Free Mode
        </button>
    </div>

    <script>
    let step = "wake";
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.lang = 'en-IN';

    function speak(text, callback) {
        const msg = new SpeechSynthesisUtterance(text);
        msg.lang = 'en-US';
        msg.onend = callback;
        window.speechSynthesis.speak(msg);
    }

    function startSiri() {
        recognition.start();
        document.getElementById("status").innerText = "👂 கவனித்துக் கொண்டிருக்கிறேன்... 'Hey Siri Play the song' என்று சொல்லுங்கள்!";
    }

    recognition.onresult = function(event) {
        const last = event.results.length - 1;
        const command = event.results[last][0].transcript.toLowerCase();
        document.getElementById("heard").innerText = "🗣️ கேட்டது: " + command;

        if (step === "wake" && (command.includes("play") || command.includes("song") || command.includes("siri"))) {
            recognition.stop();
            step = "mood";
            document.getElementById("status").innerText = "🤖 What mood? (எது வேணாலும் சரி / Happy / Love என்று சொல்லுங்கள்)";
            speak("What mood?", function() {
                recognition.lang = 'ta-IN';
                recognition.start();
            });
        } else if (step === "mood") {
            recognition.stop();
            document.getElementById("status").innerText = "🎶 பாடல் தேடப்படுகிறது...";
            const url = new URL(window.parent.location.href);
            url.searchParams.set('mood', command);
            window.parent.location.href = url.toString();
        }
    };
    </script>
    """
    components.html(siri_html, height=230)
  
