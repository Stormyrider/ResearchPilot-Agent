import streamlit as st
from agent import agent, thread_id, user_id, init_db, save_to_db
from agent import Context

# Initialize database (if not already)
init_db()

st.set_page_config(page_title="ResearchPilot", page_icon="🔬", layout="wide")
st.title("🔬 ResearchPilot")
st.caption("Your AI research assistant – search private knowledge, the web, and save reports.")

# Session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
if prompt := st.chat_input("Ask a research question..."):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call the agent
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result = agent.invoke(
                    {
                        "messages": [
                            {"role": "user", "content": prompt}
                        ]
                    },
                    {
                        "configurable": {
                            "thread_id": thread_id
                        }
                    },
                    context=Context(user_id)
                )

                final_message = result["messages"][-1]
                if isinstance(final_message.content, list):
                    answer = "".join(item.get("text", "") for item in final_message.content if item.get("type") == "text")
                else:
                    answer = final_message.content

                # Show tool calls (optional)
                for msg in result["messages"]:
                    if getattr(msg, "tool_calls", None):
                        for call in msg.tool_calls:
                            st.caption(f"🛠️ Tool: `{call['name']}` → `{call['args']}`")

                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

                # Save to database
                save_to_db(user_id, thread_id, prompt, answer)

            except Exception as e:
                st.error(f"Agent error: {type(e).__name__} – {e}")