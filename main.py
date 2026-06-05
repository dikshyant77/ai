from hf import generate_response

import io
import streamlit as st

def export_bytes(history):
    text = "".join([f"Q{i}: {h['question']}\nA{i}: {h['answer']}\n\n" for i, h in enumerate(history,1)])
    return io.BytesIO(text.encode("utf-8"))

def setup_ui():
    st.set_page_config(page_title="Ai teaching Assistant", layout= "centered")
    st.title("Ai teaching assistant")
    st.write("Ask me anything about various subjects, and I'll provide an insightful answer.")
    st.session_state.setdefault("history", [])

    col_clear, col_export = st.columns([1,2])
    with col_clear:
        if st.button("Clear conversation"):
            st.sessions_state.history = []
            st.rerun()
            with col_export:
                if st.session_state.history:
                    st.download_button(
                        label = "Export chat history",
                        data=export_bytes(st.session.history),
                        file_name = "Ai teaching assistant conversation.txt",
                        mine="text/plain",
                    )
    user_input = st.text_input("ENTER YOUR QUESTION HERE")
    if st.button("ask"):
        q = user_input.strip()
        if q:
            with st.spinner("Generating AI Response..."):
                a = generate_response(q, temperature=0.3)
            st.session_state.history.insert(0,{"question": q, "answer": a})
            st.rerun()
        else:
            st.warning("Please enter a question before clicking Ask.")
    
    st.markdown("### Conversation History")
    st.markdown(CSS, unsafe_allow_html=True)

    cards = []
    for i, h in enumerate(st.sessions_state.history, 1):
        cards.append(f'<div class="qa-card"><div class="q">Q{i}: {h["question"]}</div<>div ')
    st.markdown('<div class="history-wrap">' + "".join(cards)+"</div>", unsafe_allow_html=True)

def main():
    setup_ui()

if __name__ == "__main__":
    main()