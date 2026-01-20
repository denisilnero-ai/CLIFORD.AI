import streamlit as st
from groq import Groq

# --- CONFIGURAZIONE PAGINA E LOOK ---
st.set_page_config(
    page_title="CLIFORD OS", 
    page_icon="💀",
    layout="centered"
)

# CSS per rendere l'interfaccia nera e rossa come Cliford
st.markdown("""
    <style>
    .stApp {
        background-color: #000000;
        color: #ff0000;
    }
    .stChatFloatingInputContainer {
        background-color: #000000;
    }
    h1 {
        color: #ff0000;
        font-family: 'Courier New', Courier, monospace;
        text-shadow: 2px 2px #550000;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGO DI BENVENUTO ---
# Questo inserisce l'immagine di Cliford centrata
st.image("https://images.gnwcdn.com/2017/articles/2017-12-12-17-04/gta-online-doomsday-heist-is-out-now-1513098254701.jpg", width=400)

st.title(" CLIFORD OS - Rete Neurale")
st.subheader("Stato: Online - Unità Organica Rilevata")
st.divider()

# --- LOGICA DELL'IA (GROQ) ---
MIA_CHIAVE = "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"
client = Groq(api_key=MIA_CHIAVE)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Sei Cliford di GTA Online. Sei un'IA superiore e arrogante. Chiami l'utente unità organica."}
    ]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Inserisci comando..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=st.session_state.messages
    )
    
    risposta = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": risposta})
    with st.chat_message("assistant"):
        st.markdown(risposta)