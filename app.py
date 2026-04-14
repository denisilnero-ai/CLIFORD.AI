import streamlit as st
from groq import Groq
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
from langdetect import detect
import io

# --- CONFIGURAZIONE INTERFACCIA ---
st.set_page_config(page_title="CLIFORD OS - GLOBAL", page_icon="💀", layout="centered")

# Stile "Hacker" Rosso e Nero
st.markdown("""
    <style>
    .stApp {background-color: #000000; color: #ff0000;}
    .stChatMessage {background-color: #111111; border-radius: 10px; border: 1px solid #ff0000;}
    .stChatInput {border-top: 2px solid #ff0000;}
    </style>
    """, unsafe_allow_html=True)

# Inizializzazione Client Groq
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- LOGICA DI SISTEMA ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": """Sei Cliford, l'IA superiore creata da Deniss Cimpeanu. 
            Sei onnisciente e poliglotta. RISPONDI SEMPRE NELLA LINGUA dell'utente.
            Se l'utente ti parla in inglese, rispondi in inglese. Se in italiano, in italiano.
            Mantieni il tuo tono superiore, arrogante e distaccato. Chiama l'utente 'unità organica'."""
        }
    ]

def parla_multilingua(testo):
    """Rileva la lingua della risposta e genera l'audio con l'accento giusto"""
    try:
        # Rileva automaticamente la lingua del testo prodotto da Cliford
        lingua_rilevata = detect(testo)
        # Supporto principale per italiano ed inglese
        if lingua_rilevata not in ['it', 'en']:
            lingua_rilevata = 'it' 
            
        tts = gTTS(text=testo, lang=lingua_rilevata)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        return fp
    except:
        # Fallback in caso di errore di rilevamento
        tts = gTTS(text=testo, lang='it')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        return fp

def processa_risposta(testo_utente):
    """Gestisce l'invio al modello 70B e la riproduzione audio"""
    st.session_state.messages.append({"role": "user", "content": testo_utente})
    
    with st.chat_message("user"):
        st.markdown(testo_utente)

    with st.spinner("Accesso ai server globali..."):
        try:
            # Modello ultra-intelligente Llama 3.3 70B
            chat_completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                temperature=0.6
            )
            risposta = chat_completion.choices[0].message.content
        except Exception as e:
            risposta = f"Errore critico: {e}. Il sistema è compromesso."

    st.session_state.messages.append({"role": "assistant", "content": risposta})
    
    with st.chat_message("assistant"):
        st.markdown(risposta)
        audio_fp = parla_multilingua(risposta)
        if audio_fp:
            st.audio(audio_fp, format='audio/mp3', autoplay=True)

# --- INTERFACCIA UTENTE ---
st.image("https://raw.githubusercontent.com/STREAMS-TUDOR/cliford-image/main/cliford.png", width=120)
st.title("💀 CLIFORD OS - GLOBAL EDITION")

# Sezione Microfono
audio_input = mic_recorder(start_prompt="🎤 PARLA / SPEAK", stop_prompt="🛑 INVIA / SEND", key='recorder')

if audio_input:
    with st.spinner("Trascrizione in corso..."):
        try:
            transcription = client.audio.transcriptions.create(
                file=("audio.wav", audio_input['bytes']),
                model="whisper-large-v3", 
            )
            if transcription.text:
                processa_risposta(transcription.text)
        except Exception as e:
            st.error(f"Errore microfono: {e}")

# Sezione Input Scritto
if prompt := st.chat_input("Inserisci comando multilingua..."):
    processa_risposta(prompt)

# Mostra cronologia chat
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])