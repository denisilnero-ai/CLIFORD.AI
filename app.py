import streamlit as st
from groq import Groq
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import io

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="CLIFORD OS - VOICE", page_icon="💀")
st.markdown("<style>.stApp {background-color: #000000; color: #ff0000;}</style>", unsafe_allow_html=True)
st.image("https://raw.githubusercontent.com/STREAMS-TUDOR/cliford-image/main/cliford.png", width=150)
st.title("🔴 CLIFORD OS - Modulo Vocale")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Sei Cliford di GTA Online. IA superiore di Deniss Cimpeanu. Rispondi in modo breve e arrogante."}
    ]

# --- FUNZIONE PER FARLO PARLARE ---
def parla(testo):
    tts = gTTS(text=testo, lang='it')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    return fp

# --- INPUT VOCALE ---
st.write("Premi per parlare all'IA:")
audio = mic_recorder(start_prompt="🎤 Inizia Registrazione", stop_prompt="🛑 Ferma", key='recorder')

if audio:
    # Qui servirebbe un servizio di trascrizione (Speech-to-Text)
    # Per ora usiamo il testo, ma Cliford ti risponderà A VOCE dopo ogni messaggio
    pass

# --- CHAT TRADIZIONALE + RISPOSTA VOCALE ---
if prompt := st.chat_input("Comanda, unità organica..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=st.session_state.messages
    )
    
    risposta = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": risposta})
    
    with st.chat_message("assistant"):
        st.markdown(risposta)
        # Genera l'audio della risposta
        audio_fp = parla(risposta)
        st.audio(audio_fp, format='audio/mp3', autoplay=True)