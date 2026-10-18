import json
from urllib.request import Request, urlopen
import streamlit as st

def ask_ollama(prompt: str) -> str:
  request_body = {
    "model": "gemma4:e4b",
    "messages": [
      {
        "role": "system",
        "content": "You are AI Peer, a patient AI tutor. Explain ideas clearly, use a small example, and ask one short question to check the learner's understanding."
      },
      {"role": "user", "content": prompt}
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
      answer = ask_ollama(
        f"Team me about {topic} from the beginning, using a sample example."
      )
    st.write(answer)
  else:
    st.warning("Enter a topic before starting.")