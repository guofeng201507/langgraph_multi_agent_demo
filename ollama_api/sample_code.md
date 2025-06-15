# 🧭 Ollama API Endpoints (`ollama serve`)

The `ollama serve` backend provides several HTTP API endpoints on `http://localhost:11434`. Here's a concise guide to the most useful ones:

## Main API Endpoints

| Endpoint        | Method | Purpose                                             |
|-----------------|--------|-----------------------------------------------------|
| `/api/generate` | POST   | Single-shot text generation                         |
| `/api/chat`     | POST   | Multi-turn chat interface (like ChatGPT)            |
| `/api/create`   | POST   | Create a new model from a modelfile                 |
| `/api/pull`     | POST   | Pull a model from Ollama registry                   |
| `/api/push`     | POST   | Push a local model to the registry                  |
| `/api/tags`     | GET    | List all locally available models                   |
| `/api/show`     | POST   | Get metadata/configuration for a specific model     |
| `/api/delete`   | DELETE | Delete a local model                                |

---

## 🔍 Key Usage Examples

### 1. Generate (single prompt)
```json
POST /api/generate
{
  "model": "llama2",
  "prompt": "Translate to French: Hello world",
  "stream": false
}


Chat (multi-turn)

POST /api/chat
{
  "model": "qwen3:8b",
  "messages": [
    {"role": "user", "content": "Explain recursion"},
    {"role": "assistant", "content": "Sure! Recursion is..."}
  ],
  "stream": false
}

3. List Models
GET /api/tags

4. Model Info
POST /api/show
{
  "name": "deepseek-coder:6.7b"
}

