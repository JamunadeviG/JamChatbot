import streamlit as st  # type: ignore
import backend  

if "chat" not in st.session_state:
    try:
        model = backend.genai.GenerativeModel(
            model_name=backend.MODEL_NAME,
            safety_settings=backend.safety_settings,
            generation_config=backend.generation_config,
        )
        st.session_state.chat = model.start_chat(history=[])
    except Exception as e:
        st.error(f"Failed to initialize chatbot: {e}")
        st.stop()

st.title("Jam Chatbot ✨")

for message in st.session_state.get("messages", []):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Say something..."):
    if "messages" not in st.session_state:
        st.session_state.messages = []
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = st.session_state.chat.send_message(prompt)
        bot_reply = response.text

        with st.chat_message("assistant"):
            st.markdown(bot_reply)

        st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    except Exception as e:
        st.error(f"Error during chat: {e}")
