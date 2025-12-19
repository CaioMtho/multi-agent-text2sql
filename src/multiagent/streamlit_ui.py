import streamlit as st
from agents import Runner, SQLiteSession
from streamlit_agent_config import chat_agent
from status_streaming import StatusStreaming
import uuid

st.title("Multiagent To SQL")

ss = StatusStreaming()

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

session = SQLiteSession(st.session_state.session_id, db_path="./db/sessions.db")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("E ai?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        status_container = st.status("Iniciando agentes...", expanded=True)

        async def stream_wrapper():
            runner = Runner.run_streamed(chat_agent, input=prompt, session=session)
            
            async for event_type, content in ss.process_stream(runner):
                if event_type == "content":
                    yield content
                elif event_type == "agent_switch":
                    status_container.write(f"🔄:blue[{content}]")
                elif event_type == "status":
                    status_container.markdown(f"🔧:green[{content}]")
            
            status_container.update(label="Concluído", state="complete", expanded=False)

        response = st.write_stream(stream_wrapper)
        st.session_state.messages.append({"role": "assistant", "content": response})