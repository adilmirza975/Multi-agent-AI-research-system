# Multi-Agent AI Research System

This project automates the process of researching a topic end-to-end: it searches the web, reads the most relevant source, writes a structured report, and critiques its own output — all through a set of coordinated AI agents.

---

## Problem Statement

Researching any topic manually is slow and repetitive. It typically involves:

- Searching multiple sources to find reliable, up-to-date information
- Opening and reading through long articles to extract the relevant content
- Manually organizing findings into a coherent, structured report
- Reviewing the report for gaps, weak points, or missing depth

Doing this for every topic is time-consuming and inconsistent — quality depends entirely on how much effort is put in each time.

## Solution

This pipeline solves this with a **4-agent pipeline**, where each agent has a single, well-defined responsibility and passes its output to the next:

| Step | Agent | Responsibility |
|------|-------|-----------------|
| 1 | **Search Agent** | Searches the web (via Tavily) for recent, reliable sources on the topic |
| 2 | **Reader Agent** | Picks the most relevant result and scrapes its full content (via BeautifulSoup) |
| 3 | **Writer Chain** | Synthesizes the search results + scraped content into a structured report (Introduction, Key Findings, Conclusion, Sources) |
| 4 | **Critic Chain** | Reviews the generated report and produces a score, strengths, areas to improve, and a one-line verdict |

The result: a single topic in → a written, structured report **and** an honest critique of that report, out — with no manual searching or reading required.

All agents are powered by **Mistral AI** through **LangChain**, and the entire flow is exposed through a clean **Streamlit** UI (`app.py`) so progress is visible live, step by step, in the browser — instead of only in a terminal.

---

## Tech Stack

- **LLM Orchestration:** LangChain
- **LLM:** Mistral AI (`mistral-medium-latest`)
- **Web Search:** Tavily API
- **Web Scraping:** BeautifulSoup, Requests
- **UI:** Streamlit
- **Deployment:** Render

---

## Project Structure

```
Multi-agent-AI-research-system/
├── agents.py          # Agent + chain definitions (search agent, reader agent, writer chain, critic chain)
├── tools.py            # Tools used by agents (web_search via Tavily, scrape_url via BeautifulSoup)
├── pipeline.py          # Terminal-based version of the pipeline (runs all 4 steps sequentially)
├── app.py               # Streamlit UI — runs the same pipeline with live step-by-step progress
├── requirements.txt      # Python dependencies
└── .env                  # API keys (not committed)
```

---

## Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/adilmirza975/Multi-agent-AI-research-system.git
cd Multi-agent-AI-research-system
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the project root with:
```
MISTRAL_API_KEY=your_mistral_api_key
TAVILY_API_KEY=your_tavily_api_key
```

---

## Usage

### Option A — Run in the terminal
```bash
python pipeline.py
```
You'll be prompted to enter a topic, and the pipeline will print each step's output (search results → scraped content → report → critique) directly to the console.

### Option B — Run the Streamlit app (recommended)
```bash
streamlit run app.py
```
Then, in the browser:
1. Enter a research topic in the input field
2. Click **Run research**
3. Watch the live step tracker as the pipeline moves through Search → Read → Write → Critique
4. View the final report and critic feedback in separate tabs
5. Download the report as a `.md` file if needed

---

## Output

Each run produces:
- **Final Report** — Introduction, Key Findings (3+ points), Conclusion, and Sources
- **Critic Feedback** — a score out of 10, strengths, areas to improve, and a one-line verdict

---

## Deployment

The app is deployed on **Render** as a Streamlit web service. Ensure the `MISTRAL_API_KEY` and `TAVILY_API_KEY` environment variables are set in the Render dashboard before deploying.

---

## Topics Covered

- Multi-agent AI systems (LangChain)
- LLM integration (Mistral AI)
- Web search & retrieval (Tavily API)
- Web scraping (BeautifulSoup, Requests)
- Prompt engineering
- Streamlit UI development
- Python backend development
- Deployment (Render)
