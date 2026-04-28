\# Multi-Agent AI Research Generator



Type any topic. Get a professional research report in under 90 seconds.



4 specialized AI agents collaborate autonomously — one plans, one searches, 

one extracts, one writes. The result is a structured, cited report you can 

download as a PDF.



\---



\## See it in action



1\. Enter any research topic

2\. Watch 4 agents work in real time

3\. Read the structured report with live sources

4\. Download as a formatted PDF



\---



\## How it works



\*\*Agent 1 — Planner\*\*

Breaks your topic into 4 focused subtopics for comprehensive coverage



\*\*Agent 2 — Searcher\*\*

Searches the web in real time using Tavily Search API, finding 15-20 sources



\*\*Agent 3 — Extractor\*\*

Reads each source and pulls the most important facts, stats, and insights



\*\*Agent 4 — Writer\*\*

Synthesizes everything into a structured report with Executive Summary, 

Key Findings, Detailed Analysis, and Future Outlook



\---



\## Run locally



```bash

git clone https://github.com/thar-26/multi-agent-research

cd multi-agent-research

pip install langgraph langchain-groq langchain-community tavily-python reportlab streamlit python-dotenv

```



Create a `.env` file:

```

GROQ\_API\_KEY=your-groq-key        # free at console.groq.com

TAVILY\_API\_KEY=your-tavily-key    # free at app.tavily.com

```



```bash

streamlit run app.py

```



\---



\## Stack

LangGraph · LLaMA 3 · Groq · Tavily Search · ReportLab · Streamlit · Python

