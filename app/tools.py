from pathlib import Path
import os

from dotenv import load_dotenv
from langchain.tools import tool
from langchain_tavily import TavilySearch

from knowledge import search_knowledge


load_dotenv()


REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)


tavily = TavilySearch(
    max_results=5,
    topic="general",
    include_answer=True
)


@tool
def search_web(query: str) -> str:
    """Search the live web for current information."""

    if not query.strip():
        return "Error: search query cannot be empty."

    if not os.getenv("TAVILY_API_KEY"):
        return "Error: TAVILY_API_KEY is missing."

    try:
        result = tavily.invoke({
            "query": query
        })

        output = []

        if result.get("answer"):
            output.append(
                f"Summary: {result['answer']}"
            )

        for item in result.get("results", []):
            output.append(
                f"Title: {item.get('title', 'No title')}\n"
                f"URL: {item.get('url', '')}\n"
                f"Content: {item.get('content', '')[:1000]}"
            )

        return "\n\n".join(output)

    except Exception as e:
        return f"Web search error: {e}"


@tool
def search_private_knowledge(query: str) -> str:
    """Search ResearchPilot's private document knowledge base."""

    if not query.strip():
        return "Error: search query cannot be empty."

    try:
        return search_knowledge(query)

    except Exception as e:
        return f"Knowledge search error: {e}"


@tool
def save_report(title: str, content: str) -> str:
    """Save a research report as a Markdown file."""

    if not title.strip():
        return "Error: title cannot be empty."

    if not content.strip():
        return "Error: report content cannot be empty."

    filename = "".join(
        c if c.isalnum() or c in " _-" else "_"
        for c in title
    ).strip()

    file_path = REPORT_DIR / f"{filename}.md"

    file_path.write_text(
        f"# {title}\n\n{content}",
        encoding="utf-8"
    )

    return f"Report saved successfully: {file_path}"


tools = [
    search_web,
    search_private_knowledge,
    save_report
]


if __name__ == "__main__":
    print("\nTesting private knowledge search...\n")

    result = search_private_knowledge.invoke({
        "query": "What is the project code for ResearchPilot?"
    })

    print(result)