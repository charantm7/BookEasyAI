import streamlit as st
import requests

def main():
    st.set_page_config(page_title='BookEasy AI', page_icon="🤖")
    
    st.title("🤖 Google calender AI Agent")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    prompt = st.chat_input("Ask me to schedule something....")
    if prompt:
        st.session_state.chat.append({"role":"user", "content":prompt})
        response = requests.post("https://localhost:8000/chat", json={'message':prompt})
        st.session_state.chat.append({'role':'ai', "content":response.json()["reply"]})
        

    for msg in st.session_state.chat:
        with st.chat_message(msg['role']):
            st.markdown(msg['content'])



if __name__ == '__main__':
    main()