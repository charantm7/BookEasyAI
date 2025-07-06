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
        response = requests.post("http://localhost:8000/chat", json={'message':prompt})

        # st.write("Status_code:", response.status_code)
        # st.write("Raw text: ", response.text)

        if response.status_code == 200:
            reply = response.json().get("reply", "[No reply key]")

        elif response.status_code == 500:
            reply = f"Can you please try again! Ai is overloaded :)"
        else:
            reply = f"Error {response.status_code}"
        st.session_state.chat.append({'role':'ai', "content":reply})
        

    for msg in st.session_state.chat:
        with st.chat_message(msg['role']):
            st.markdown(msg['content'])



if __name__ == '__main__':
    main()