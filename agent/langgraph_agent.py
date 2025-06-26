# agent/langgraph_agent.py

from langgraph.graph import StateGraph
from typing import TypedDict
from datetime import datetime, timedelta
import re

# Import your calendar functions
from backend.calendar_utils import check_availability, book_event

# --- Agent State ---
class AgentState(TypedDict):
    input: str
    response: str

# --- Agent Logic ---
def agent_node(state: AgentState) -> AgentState:
    user_input = state["input"].lower()

    # Try to find a time in the message
    time_match = re.search(r'(\d{1,2})(?:[:.](\d{2}))?\s*(am|pm)?', user_input)
    time_str = time_match.group(0) if time_match else "15:00"

    # Use tomorrow as default date
    date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    if "book" in user_input:
        result = book_event("TailorTalk Meeting", date, convert_time_to_24h(time_str))
        return {"input": state["input"], "response": result}

    elif "free" in user_input or "available" in user_input:
        result = check_availability(date)
        return {"input": state["input"], "response": str(result)}

    else:
        return {
            "input": state["input"],
            "response": "Hi! I can help you check calendar availability or book a meeting. Try saying 'book a meeting tomorrow at 3 PM'."
        }

# --- Convert to 24h time ---
def convert_time_to_24h(time_str: str) -> str:
    try:
        return datetime.strptime(time_str.strip(), "%I:%M %p").strftime("%H:%M")
    except:
        try:
            return datetime.strptime(time_str.strip(), "%I %p").strftime("%H:%M")
        except:
            return "15:00"

# --- LangGraph Wiring ---
workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.set_entry_point("agent")
workflow.set_finish_point("agent")
graph = workflow.compile()

# --- Run Function ---
def run_agent(message: str) -> str:
    result = graph.invoke({"input": message})
    return result["response"]
