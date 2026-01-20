import streamlit as st
from groq import Groq

# Configurazione Segreta (Prende la chiave dai Secrets di Streamlit o dal codice)
MIA_CHIAVE = "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"

client = Groq(api_key=MIA_CHIAVE)

st.set_page_config(page_title="CLIFORD OS", page_icon="💀")
st.title("🔴 CLIFORD OS - Rete Neurale")

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