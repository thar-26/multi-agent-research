from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from dotenv import load_dotenv
import os

load_dotenv()

# ── LLM and Search Tool ───────────────────────────────────────
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
search_tool = TavilySearchResults(max_results=5)

# ── State Definition ──────────────────────────────────────────
class ResearchState(TypedDict):
    topic: str
    subtopics: List[str]
    search_results: List[dict]
    extracted_info: List[str]
    final_report: str

# ── Agent 1: Planner ──────────────────────────────────────────
def planner_agent(state: ResearchState) -> ResearchState:
    print(f"\n[Planner] Breaking down topic: {state['topic']}")
    response = llm.invoke(f"""
    You are a research planner. Break down the following topic into 4 specific subtopics 
    that together give a comprehensive understanding of the subject.
    
    Topic: {state['topic']}
    
    Return ONLY a Python list of 4 subtopic strings, nothing else.
    Example format: ["subtopic 1", "subtopic 2", "subtopic 3", "subtopic 4"]
    """)
    
    try:
        import ast
        subtopics = ast.literal_eval(response.content.strip())
    except:
        subtopics = [
            f"{state['topic']} overview",
            f"{state['topic']} current trends",
            f"{state['topic']} challenges",
            f"{state['topic']} future outlook"
        ]
    
    print(f"[Planner] Subtopics: {subtopics}")
    return {**state, "subtopics": subtopics}

# ── Agent 2: Searcher ─────────────────────────────────────────
def searcher_agent(state: ResearchState) -> ResearchState:
    print(f"\n[Searcher] Searching for information...")
    all_results = []
    
    for subtopic in state['subtopics']:
        print(f"[Searcher] Searching: {subtopic}")
        results = search_tool.invoke(subtopic)
        for r in results:
            all_results.append({
                "subtopic": subtopic,
                "url": r.get("url", ""),
                "content": r.get("content", "")
            })
    
    print(f"[Searcher] Found {len(all_results)} sources")
    return {**state, "search_results": all_results}

# ── Agent 3: Extractor ────────────────────────────────────────
def extractor_agent(state: ResearchState) -> ResearchState:
    print(f"\n[Extractor] Extracting key information...")
    extracted = []
    
    for result in state['search_results']:
        if not result['content']:
            continue
        response = llm.invoke(f"""
        Extract the most important facts and insights from this text.
        Be concise — 3-5 bullet points maximum.
        Focus on: data, statistics, key findings, expert opinions.
        
        Subtopic: {result['subtopic']}
        Text: {result['content'][:1500]}
        
        Return bullet points only, starting each with •
        """)
        extracted.append(f"[{result['subtopic']}]\n{response.content}")
    
    print(f"[Extractor] Extracted info from {len(extracted)} sources")
    return {**state, "extracted_info": extracted}

# ── Agent 4: Writer ───────────────────────────────────────────
def writer_agent(state: ResearchState) -> ResearchState:
    print(f"\n[Writer] Generating final report...")
    
    all_info = "\n\n".join(state['extracted_info'])
    
    response = llm.invoke(f"""
    You are an expert research writer. Write a comprehensive, well-structured research report.
    
    Topic: {state['topic']}
    
    Research findings:
    {all_info}
    
    Write a report with these sections:
    1. Executive Summary (2-3 sentences)
    2. Key Findings (4-6 bullet points with specific data)
    3. Detailed Analysis (3-4 paragraphs covering the subtopics)
    4. Challenges and Considerations
    5. Future Outlook
    6. Conclusion
    
    Make it professional, data-driven, and cite specific facts from the research.
    Use clear headings for each section.
    """)
    
    print(f"[Writer] Report generated!")
    return {**state, "final_report": response.content}

# ── Build the Graph ───────────────────────────────────────────
def build_research_graph():
    graph = StateGraph(ResearchState)
    
    graph.add_node("planner", planner_agent)
    graph.add_node("searcher", searcher_agent)
    graph.add_node("extractor", extractor_agent)
    graph.add_node("writer", writer_agent)
    
    graph.set_entry_point("planner")
    graph.add_edge("planner", "searcher")
    graph.add_edge("searcher", "extractor")
    graph.add_edge("extractor", "writer")
    graph.add_edge("writer", END)
    
    return graph.compile()

def run_research(topic: str) -> dict:
    graph = build_research_graph()
    initial_state = ResearchState(
        topic=topic,
        subtopics=[],
        search_results=[],
        extracted_info=[],
        final_report=""
    )
    result = graph.invoke(initial_state)
    return result