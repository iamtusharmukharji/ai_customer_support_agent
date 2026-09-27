Here is the complete `README.md` content in a single Markdown code block so you can easily copy and paste it:

```markdown
# Enterprise Production AI Support Agent

A production-grade, deterministic, and scalable customer support orchestration system built with **LangGraph**, **FastAPI**, **Pydantic**, and **MySQL**. 

This system moves beyond basic "LLM wrappers" or naive prompt-chaining by implementing an in-memory **Finite State Machine (FSM)** architecture. It cleanly decouples **AI Orchestration** from **Business Logic** and **Database Operations** using strict layered architecture patterns.

---

## Architecture & Dependency Layering

To prevent non-deterministic LLM behavior from coupling directly to database models or business rules, the project follows strict enterprise software engineering principles:


```

[ User Input / Client ]
│
▼
[ FastAPI API Layer ]
│
▼
[ LangGraph Orchestration Layer ]
│
├────────► Nodes (Units of Execution)
├────────► Conditional Edges (Deterministic Routing)
└────────► State (Single Source of Truth)
│
▼
[ AI Tool Layer ]
│
▼
[ Service Layer (Business Logic) ]
│
▼
[ Repository Layer (SQL / Data Access) ]
│
▼
[ MySQL Database ]

```

### Key Architectural Rules
1. **Zero Raw SQL in Graph Code:** LangGraph nodes only handle orchestration and state transformations. Database access is completely abstracted into Repositories and Services.
2. **Structured LLM Enforcement:** All LLM decisions (intent classification, entity extraction) use **Pydantic Structured Outputs** with step-by-step reasoning (Chain-of-Thought) to eliminate unpredictable string parsing.
3. **Pure Node & Edge Execution:** Nodes perform work and return partial state dictionaries. Edges act strictly as dynamic routers based on current state values.

---

## State Graph Execution Flow


```

```
              ┌─────────┐
              │  START  │
              └────┬────┘
                   │
                   ▼
        ┌─────────────────────┐
        │   classify_intent   │  <-- LLM + Pydantic Schema Extraction
        └──────────┬──────────┘
                   │
         { route_intent Edge }
                   │
 ┌───────────┬─────┴─────┬───────────┐
 ▼           ▼           ▼           ▼

```

┌─────┐    ┌───────┐   ┌────────┐  ┌───────┐
│ FAQ │    │ ORDER │   │ REFUND │  │ HUMAN │
└──┬──┘    └───┬───┘   └───┬────┘  └───┬───┘
│           │           │           │
└───────────┴─────┬─────┴───────────┘
▼
┌───────────────────┐
│ generate_response │
└─────────┬─────────┘
│
▼
┌─────┐
│ END │
└─────┘

```

---

## Tech Stack & Tooling

* **Orchestration:** LangGraph, LangChain (`langchain-core`, `langchain-openai`)
* **Framework & Schema Validation:** FastAPI, Pydantic v2
* **Data Persistence:** MySQL, SQLAlchemy / PyMySQL
* **Environment & Package Management:** Python 3.11+, `python-dotenv`
* **Testing:** Pytest

---

## Repository Structure


```

ai-support-agent/
│
├── app/
│   ├── api/                  # HTTP route handlers and dependencies
│   │   ├── routes/
│   │   │   └── chat.py
│   │   └── dependencies.py
│   │
│   ├── ai/                   # LLM clients, structured schemas, system prompts
│   │   ├── llm.py
│   │   ├── structured_output.py
│   │   └── prompts/
│   │
│   ├── graph/                # LangGraph orchestration state machine
│   │   ├── state.py          # Shared state definition (SupportState)
│   │   ├── nodes.py          # Pure execution nodes
│   │   ├── edges.py          # Conditional routing functions
│   │   └── graph.py          # Graph compilation & topology assembly
│   │
│   ├── tools/                # Agent tools bridging graph to services
│   │   ├── order_tools.py
│   │   └── refund_tools.py
│   │
│   ├── services/             # Business rules layer
│   │   ├── order_service.py
│   │   └── refund_service.py
│   │
│   ├── db/                   # Database access layer
│   │   ├── database.py
│   │   ├── models/           # SQLAlchemy ORM models
│   │   └── repositories/     # Data access logic (Repository pattern)
│   │
│   └── main.py               # Application entrypoint
│
├── tests/                    # Unit, graph, and API integration test suites
│   ├── graph/
│   │   └── test_graph.py
│   └── api/
│
├── .env.example
├── requirements.txt
└── README.md

```

---

## Getting Started

### 1. Prerequisites
* Python 3.11+
* Running MySQL instance
* OpenAI API Key (or supported LLM provider)

### 2. Environment Setup
Clone the repository and set up a virtual environment:

```bash
git clone [https://github.com/your-username/ai-support-agent.git](https://github.com/your-username/ai-support-agent.git)
cd ai-support-agent

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

```

Configure your `.env` file:

```env
GEMINI_API_KEY=<api_key>
GEMINI_URL=https://generativelanguage.googleapis.com/v1beta/
DB_HOST=localhost
DB_PORT=3360
DB_SCHEMA_NAME=ai_support_agent
DB_USERNAME=<mysql username>
DB_PAASWORD=<mysql password>

```

---

## Running the Graph & Tests

### Execute Graph via Test Suite

Because module paths resolve relative to the package root, execute graph scripts or pytest modules using Python's `-m` flag:

```bash
# Run internal test runner script
python -m app.graph.test_graph

# Run test suite with pytest
pytest tests/

```

### Run API Server

```bash
uvicorn app.main:app --reload

```

Access API documentation at `http://localhost:8000/docs`.

---

## Key Development Milestones

* [x] **Milestone 1: FSM Foundations** — Setup `StateGraph`, explicit state typing, nodes, deterministic conditional edges, and execution visualization.
* [x] **Milestone 2: LLM Intent Classifier** — Structured intent extraction (`FAQ`, `ORDER`, `REFUND`, `HUMAN`, `UNKNOWN`) and entity parsing using Pydantic models.
* [ ] **Milestone 3: Data & Tool Integration** — Layered Repository/Service design hooking MySQL context into graph tools.
* [ ] **Milestone 4: Response Synthesis** — Context-aware structured response generation.
* [ ] **Milestone 5: Self-Correction Loops** — Output evaluation nodes and dynamic retry edges for failed response validations.
* [ ] **Milestone 6: Productionization** — Docker containerization, async connection pooling, rate-limiting, and evaluation metrics.

---

## License

Distributed under the MIT License. See `LICENSE` for details.

```

```