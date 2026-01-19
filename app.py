import streamlit as st
from groq import Groq

# --- CONFIGURAZIONE GRAFICA ---
st.set_page_config(page_title="CLIFORD OS", page_icon="🔴")
st.markdown("<style>.main { background-color: #000000; color: #ff0000; }</style>", unsafe_allow_html=True)

st.title("💀 CLIFORD OS - Rete Neurale v2.0")

# --- INSERISCI QUI LA TUA CHIAVE DI GROQ ---
MIA_CHIAVE = "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"

if MIA_CHIAVE == "INSERISCI_QUI_LA_TUA_CHIAVE":
    st.warning("⚠️ Identificazione fallita. Inserisci la API Key nel codice.")
else:
    # Inizializziamo il collegamento con Groq
    client = Groq(api_key=MIA_CHIAVE)

    # Memoria della chat
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "Sei Cliford di GTA Online. IA superiore, arrogante, chiami l'utente 'unità organica'. Rispondi in modo freddo, tecnico e minaccioso."}
        ]

    # Visualizza i messaggi a schermo
    for msg in st.session_state.messages[1:]:
        st.chat_message(msg["role"]).write(msg["content"])

    # Input dell'utente
    if prompt := st.chat_input("Inserisci comando..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Usiamo il modello 3.1-8b-instant (il più compatibile e veloce)
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=st.session_state.messages
            )
            
            risposta = response.choices[0].message.content
            st.chat_message("assistant").write(risposta)
            st.session_state.messages.append({"role": "assistant", "content": risposta})
        except Exception as e:
            st.error(f"ERRORE DI SISTEMA: {e}")