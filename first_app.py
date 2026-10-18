import json
from urllib.request import Request, urlopen
import streamlit as st

def ask_ollama(messages: list[dict[str, str]]) -> str:
  request_body = {
    "model": "gemma4:e4b",
    "messages": [
      {
        "role": "system",
        "content": "You are AI Peer, a patient AI tutor. Explain ideas clearly, use a small example, and ask one short question to check the learner's understanding."
      },
      *messages
    ],
    "stream": False
  }
  
  request = Request(
    "http://localhost:11434/api/chat",
    data=json.dumps(request_body).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST"
  )
  
  with urlopen(request, timeout=180) as response:
    result = json.loads(response.read().decode("utf-8"))
  
  return result["message"]["content"]

st.title("AI Peer")

## Check if there is any previous historical messages available in the session
if "messages" not in st.session_state:
  st.session_state.messages = []

## write() method is used to write paragraphs
st.write("A local learning companion that can teach at your own pace.")

# Let's get the input from the user

topic = st.text_input(
  "What's on your mind?",
  placeholder="e.g., How language models work?"
)

if st.button("Start Learning"):
  if topic:
    with st.spinner("AI Peer is thinking..."):
      st.session_state.messages.append(
        {
          "role": "user",
          "content": topic
        }
      )
      answer = ask_ollama(st.session_state.messages)
      st.session_state.messages.append(
        {
          "role": "assistant",
          "content": answer
        }
      )
  else:
    st.warning("Enter a topic before starting.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])