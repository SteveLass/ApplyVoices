import streamlit as st
import speech_recognition as sr
import google.generativeai as genai

# 🔐 Configuration API Gemini (ta clé ici)
GENAI_API_KEY = "AIzaSyBHaz9W35BjlP0z0rFkU75L4b7oqmivOKU"  # Remplace par ta clé API

genai.configure(api_key=GENAI_API_KEY)
model = genai.get_model("chat-bison")

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Parlez maintenant...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="fr-FR")
            st.success(f"📝 Vous avez dit : {text}")
            return text
        except sr.UnknownValueError:
            st.error("❌ Je n’ai pas compris.")
        except sr.RequestError:
            st.error("❌ Erreur de service Google.")
    return ""

def chatbot_response(user_input):
    try:
        response = model.predict(messages=[{"author": "user", "content": user_input}])
        return response.last
    except Exception as e:
        return f"Erreur : {str(e)}"

st.title("🤖 Chatbot Vocal avec LLM Gemini")

if "conversation" not in st.session_state:
    st.session_state.conversation = []

mode = st.radio("Mode d'entrée :", ["Texte", "Voix"])

if mode == "Texte":
    user_input = st.text_input("Écrivez ici :", key="text_input")
    if st.button("Envoyer") and user_input:
        response = chatbot_response(user_input)
        st.session_state.conversation.append(("🧑", user_input))
        st.session_state.conversation.append(("🤖", response))

elif mode == "Voix":
    if st.button("🎙️ Parler"):
        voice_input = speech_to_text()
        if voice_input:
            response = chatbot_response(voice_input)
            st.session_state.conversation.append(("🧑", voice_input))
            st.session_state.conversation.append(("🤖", response))

st.markdown("### 💬 Conversation")
for speaker, msg in st.session_state.conversation:
    st.write(f"{speaker} : {msg}")
