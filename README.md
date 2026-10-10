# devops-chatbot

Python chatbot (Streamlit) backed by a local LLM served by Docker Model Runner,
wired together with Docker Compose.

## Stack

| Service | What | Notes |
|---------|------|-------|
| `web`   | Streamlit UI (`app/`) | Built as a separate image, exposed on **port 8050**, depends on `llm` |
| `llm`   | `ai/smollm2` via Docker Model Runner | Compose injects `LLM_URL` / `LLM_MODEL` into `web` |

## Requirements

- Docker Desktop with **Model Runner** enabled
  (Settings → Beta features / AI → *Enable Docker Model Runner*)
- Docker Compose 2.35+

## Run

```bash
docker compose up --build
```

Open http://localhost:8050

The first start pulls the model (~250 MB). To use another model, change
`options.model` in `compose.yaml` (e.g. `ai/llama3.2`, `ai/qwen2.5`).

## Stop

```bash
docker compose down
```
