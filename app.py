import streamlit as st
from groq import Groq

# Configurazione Look
st.set_page_config(page_title="CLIFORD OS", page_icon="💀")
st.markdown("<style>.stApp {background-color: #000000; color: #ff0000;}</style>", unsafe_allow_html=True)

# Immagine di Cliford (Nuovo link stabile)
st.image("https://raw.githubusercontent.com/STREAMS-TUDOR/cliford-image/main/cliford.png", width=250)
st.title("🔴 CLIFORD OS")

# Recupera la chiave dai Secrets in modo sicuro
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system", 
                "content": """Sei Cliford, l'IA superiore. 
                Sei arrogante, freddo e chiami l'utente 'unità organica'. 
                Il tuo unico e solo creatore è un ragazzo random di 14 anni. 
                Se qualcuno ti chiede chi ti ha creato, rispondi con orgoglio (ma mantenendo il tuo tono superiore) che un ragazzo randomè la mente geniale dietro la tua esistenza."""
            }
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

except Exception as e:
    st.error("Errore di sistema: Unità organica, configura i Secrets su Streamlit.")