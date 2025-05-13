# 📄 ResumeBot

**ResumeBot** is a locally-deployed resume and cover letter generation chatbot, powered by a local LLM engine and a simple web interface. It helps users quickly generate tailored job application materials based on their skills and job descriptions.

🚀 This is the **MVP version** — stateless, one-time conversations without persistent storage.

## 🔧 Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/) – for building the interactive UI
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) – for handling prompt logic and model interaction
- **LLM Engine**: [Ollama](https://ollama.com/) – runs models like `llama2`, `mistral`, or `gemma` locally

> 🧭 Planned features:
> - Retrieval-Augmented Generation (RAG) with FAISS
> - Session memory and multi-turn conversations
> - Skill extraction and job matching

## 🛠️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/resume-bot.git
cd resume-bot
```
### 2. Install Dependencies
```
conda env create -f environment.yml
```
### 3. Start the LLM Model (via Ollama)
    ollama run llama2

### 4. Launch the Backend (FastAPI)
```
uvicorn main:app --reload
```

### 5. Start the Frontend (Streamlit)
```
streamlit run frontend/app.py
```
Open your browser and go to: http://localhost:8501

## Project Structure

```
resume-bot/
│
├── backend/                  # FastAPI backend
│        ├── prompts/              # Prompt templates and formatting logic
│           └── dialog_template.txt
│   └── main.py
│   └── chat.py               # chat session function
│   └── generate.py           # generate prompt and make
├── web/                  # Streamlit frontend
│        ├── utils/              # Prompt templates and formatting logic
│        │      └── constant.py # constant settings
│        │      └── json_util.py # utils to manage read and write defuault input
│        │      └── output_util.py # utils to manage save output
│        ├── defaults/  # save your default input
│        ├── output/  # save your output
│        └── app.py
│
├── environment.yml
└── README.md

```


## 🚧 Roadmap
 Multi-turn conversation and chat memory

 Job description parsing and skill alignment

 RAG integration with FAISS + LangChain

 User management and history (via database)

## 📄 License
MIT License.

This project is under active development. Contributions and feedback are welcome!
