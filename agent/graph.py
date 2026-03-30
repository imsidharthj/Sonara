import uuid
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from agent.tools import lookup_order, check_return_eligibility
from agent.prompts import SYSTEM_PROMPT

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = [lookup_order, check_return_eligibility]
agent = create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)

sessions: dict[str, list] = {}


async def run_agent(user_message: str, session_id: str | None = None) -> tuple[str, str]:
    if not session_id:
        session_id = str(uuid.uuid4())

    history = sessions.setdefault(session_id, [])
    history.append({"role": "user", "content": user_message})

    result = await agent.ainvoke({"messages": history})
    assistant_message = result["messages"][-1].content

    history.append({"role": "assistant", "content": assistant_message})
    return assistant_message, session_id
