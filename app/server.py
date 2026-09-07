import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import your agent and related objects
from agent import get_agent, init_db, save_to_db
from agent import Context

# Initialize the database (if not already)
init_db()

app = FastAPI()

# Allow frontend to call this API (served from same domain, but we keep CORS open)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# We'll use a fixed thread_id and user_id for the demo;
# you can make them session-based later.
THREAD_ID = "web-session-1"
USER_ID = "web-user-1"

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        agent = get_agent()  # lazy load – cached after first call
        result = agent.invoke(
            {
                "messages": [{"role": "user", "content": request.question}]
            },
            {
                "configurable": {"thread_id": THREAD_ID}
            },
            context=Context(USER_ID)
        )

        # Extract final answer
        final_message = result["messages"][-1]
        if isinstance(final_message.content, list):
            answer = "".join(item.get("text", "") for item in final_message.content if item.get("type") == "text")
        else:
            answer = final_message.content

        # Save to database (logs)
        save_to_db(USER_ID, THREAD_ID, request.question, answer)

        return ChatResponse(answer=answer)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Serve the HTML page (index.html) at the root
@app.get("/")
async def get_index():
    # Vercel will serve the file from the current working directory
    return FileResponse("index.html")

# Optional health check for Vercel
@app.get("/health")
async def health():
    return {"status": "ok"}
