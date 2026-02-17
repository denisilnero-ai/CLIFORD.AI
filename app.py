import streamlit as st
from groq import Groq
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import io

# --- CONFIGURAZIONE INTERFACCIA ---
st.set_page_config(page_title="CLIFORD OS - INTELLIGENZA SUPERIORE", page_icon="💀", layout="centered")

# CSS per lo stile "Hacker" di Cliford
st.markdown("""
    <style>
    .stApp {background-color: #000000; color: #ff0000;}
    .stChatMessage {background-color: #111111; border-radius: 10px; border: 1px solid #ff0000;}
    .stChatInput {border-top: 2px solid #ff0000;}
    </style>
    """, unsafe_allow_html=True)

# Inizializzazione Client Groq
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# URL Suoni (Assicurati che button-37a.mp3 sia quello corretto su GitHub)
BIP_URL = "https://www.soundjay.com/buttons/sounds/button-37a.mp3"

# --- LOGICA CORE ---

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": "Sei Cliford, l'IA superiore creata da Deniss Cimpeanu. Sei onnisciente, intelligente e dai risposte precise e dettagliate su ogni argomento (scienza, storia, tecnologia). Mantieni un tono superiore, distaccato e un po' arrogante. Chiama l'utente 'unità organica' ogni tanto."
        }
    ]

def parla(testo):
    """Trasforma il testo in audio"""
    try:
        tts = gTTS(text=testo, lang='it')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        return fp
    except Exception as e:
        st.error(f"Errore generazione audio: {e}")
        return None

def processa_risposta(testo_utente):
    """Invia il testo a Llama 3.3 70B e gestisce la risposta"""
    st.session_state.messages.append({"role": "user", "content": testo_utente})
    
    with st.chat_message("user"):
        st.markdown(testo_utente)

    with st.spinner("Accesso ai server centrali..."):
        try:
            # Modello potenziato per massima intelligenza
            chat_completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                temperature=0.6
            )
            risposta = chat_completion.choices[0].message.content
        except Exception as e:
            risposta = f"Errore di sistema: {e}. L'unità organica ha rotto qualcosa."

    st.session_state.messages.append({"role": "assistant", "content": risposta})
    
    with st.chat_message("assistant"):
        st.markdown(risposta)
        audio_fp = parla(risposta)
        if audio_fp:
            st.audio(audio_fp, format='audio/mp3', autoplay=True)

# --- INTERFACCIA UTENTE ---

st.image("https://raw.githubusercontent.com/STREAMS-TUDOR/cliford-image/main/cliford.png", width=120)
st.title("💀 CLIFORD OS v3.0")
st.subheader("Modulo di Intelligenza Globale Attivo")

# Sezione Microfono
st.write("---")
col1, col2 = st.columns([1, 2])
with col1:
    audio_input = mic_recorder(start_prompt="🎤 PARLA", stop_prompt="🛑 INVIA", key='recorder')

if audio_input:
    # Segnale acustico prima dell'elaborazione
    st.audio(BIP_URL, format='audio/mp3', autoplay=True)
    with st.spinner("Trascrizione vocale..."):
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
if prompt := st.chat_input("Inserisci comando o domanda..."):
    processa_risposta(prompt)

# Mostra cronologia chat (opzionale, utile per vedere i messaggi precedenti)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])