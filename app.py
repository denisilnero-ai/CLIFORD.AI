import streamlit as st
from groq import Groq
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
from langdetect import detect
import io

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="CLIFORD OS - MULTILINGUAL", page_icon="💀")

st.markdown("""
    <style>
    .stApp {background-color: #000000; color: #ff0000;}
    .stChatMessage {background-color: #111111; border-radius: 10px; border: 1px solid #ff0000;}
    </style>
    """, unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- LOGICA DI SISTEMA POTENZIATA ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": """Sei Cliford, l'IA superiore creata da Deniss Cimpeanu. 
            REGOLA MANDATORIA: Devi rispondere SEMPRE nella stessa lingua usata dall'utente nell'ultimo messaggio. 
            Se l'utente ti scrive in inglese, rispondi in inglese. Se ti scrive in italiano, rispondi in italiano.
            Non tradurre, non cambiare lingua. Mantieni il tuo tono arrogante e chiama l'utente 'unità organica'."""
        }
    ]

def parla_multilingua(testo):
    """Sceglie l'accento giusto in base alla lingua della risposta"""
    try:
        lingua_rilevata = detect(testo)
        if lingua_rilevata not in ['it', 'en']:
            lingua_rilevata = 'it' 
        tts = gTTS(text=testo, lang=lingua_rilevata)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        return fp
    except:
        tts = gTTS(text=testo, lang='it')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        return fp

def processa_risposta(testo_utente):
    # Aggiunge il messaggio dell'utente alla memoria
    st.session_state.messages.append({"role": "user", "content": testo_utente})
    
    with st.chat_message("user"):
        st.markdown(testo_utente)

    with st.spinner("Analisi linguistica..."):
        try:
            # Usiamo Llama 3.3 70B per massima intelligenza multilingua
            chat_completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                temperature=0.5 # Più basso è, più segue le regole
            )
            risposta = chat_completion.choices[0].message.content
        except Exception as e:
            risposta = f"Errore: {e}"

    st.session_state.messages.append({"role": "assistant", "content": risposta})
    
    with st.chat_message("assistant"):
        st.markdown(risposta)
        audio_fp = parla_multilingua(risposta)
        st.audio(audio_fp, format='audio/mp3', autoplay=True)

# --- INTERFACCIA ---
st.image("https://raw.githubusercontent.com/STREAMS-TUDOR/cliford-image/main/cliford.png", width=120)
st.title("💀 CLIFORD GLOBAL OS")

# Input Vocale
audio_input = mic_recorder(start_prompt="🎤 PARLA / SPEAK", stop_prompt="🛑 INVIA / SEND", key='recorder')

if audio_input:
    try:
        transcription = client.audio.transcriptions.create(
            file=("audio.wav", audio_input['bytes']),
            model="whisper-large-v3", 
        )
        if transcription.text:
            processa_risposta(