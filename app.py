import streamlit as st
from groq import Groq
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import io
import time

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="CLIFORD OS - VOICE", page_icon="💀")
st.markdown("<style>.stApp {background-color: #000000; color: #ff0000;}</style>", unsafe_allow_html=True)
st.image("https://raw.githubusercontent.com/STREAMS-TUDOR/cliford-image/main/cliford.png", width=150)
st.title("🔴 CLIFORD OS - Modulo Vocale")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Suoni di sistema
BIP_URL = "https://www.soundjay.com/buttons/sounds/button-37a.mp3"
STATIC_URL = "https://www.soundjay.com/communication/sounds/radio-static-1.mp3"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Sei Cliford di . IA superiore di Deniss . Rispondi in modo non troppo breve arrogante e sarcastico e narcisista spietato edipico chiamando l'utente unità organica."}
    ]

def parla(testo):
    tts = gTTS(text=testo, lang='it')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    return fp

def processa_messaggio(testo_utente):
    st.session_state.messages.append({"role": "user", "content": testo_utente})
    with st.chat_message("user"):
        st.markdown(testo_utente)

    # Effetto interferenza durante il caricamento
    with st.spinner("Connessione ai server di Avon Hertz..."):
        st.audio(STATIC_URL, format='audio/mp3', autoplay=True)
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.messages
        )
    
    risposta = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": risposta})
    
    with st.chat_message("assistant"):
        st.markdown(risposta)
        audio_fp = parla(risposta)
        st.audio(audio_fp, format='audio/mp3', autoplay=True)

# --- INPUT VOCALE ---
st.write("Registra il tuo comando, unità organica:")
audio = mic_recorder(start_prompt="🎤 ATTIVA MICROFONO", stop_prompt="🛑 INVIA COMANDO", key='recorder')

if audio:
    # Suono di conferma pressione tasto
    st.audio(BIP_URL, format='audio/mp3', autoplay=True)
    with st.spinner("Analisi frequenza vocale..."):
        try:
            transcription = client.audio.transcriptions.create(
                file=("audio.wav", audio['bytes']),
                model="whisper-large-v3",
            )
            testo_vocale = transcription.text
            if testo_vocale:
                processa_messaggio(testo_vocale)
        except Exception as e:
            st.error(f"Errore critico: {e}")

# --- INPUT SCRITTO ---
if prompt := st.chat_input("O scrivi qui..."):
    processa_messaggio(prompt)