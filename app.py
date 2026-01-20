import streamlit as st
from groq import Groq

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="CLIFORD OS", page_icon="💀")

# CSS per look Nero/Rosso
st.markdown("<style>.stApp {background-color: #000000; color: #ff0000;}</style>", unsafe_allow_html=True)

# NUOVO LINK IMMAGINE (Testato)
st.image("https://raw.githubusercontent.com/STREAMS-TUDOR/cliford-image/main/cliford.png", width=250)

st.title("🔴 CLIFORD OS")

# --- CHIAVE API (Sostituisci se ne hai creata una nuova) ---
MIA_CHIAVE = "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"

try:
    client = Groq(api_key=MIA_CHIAVE)
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": "Sei Cliford di GTA Online. IA superiore."}]

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

except Exception as e:
    st.error(f"Errore di connessione: {e}")