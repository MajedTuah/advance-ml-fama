# 🦙 Topic 11 — Running LLMs Locally: A 10-Minute Guide
> **Reference Guide | Duration: 10 Minutes | Status: 🟢 Completed**

Running Large Language Models (LLMs) locally gives you total privacy, zero cost per token, and the ability to work offline. While training a model requires a supercomputer, **inference** (running it) is now possible on most modern laptops.

---

## 🚀 The Fast Path: Ollama
The quickest way to get an LLM running on macOS, Linux, or Windows is **Ollama**. It bundles the model weights, the inference engine (llama.cpp), and a simple CLI.

### 1. Install (2 Minutes)
- **Windows/macOS:** Download from [ollama.com](https://ollama.com) and run the installer.
- **Linux:** Run the curl command:
  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  ```

### 2. Run Your First Model (3 Minutes)
Open your terminal and run:
```bash
ollama run llama3
```
*This command will automatically download the Llama 3 model (~4.7GB) and start an interactive chat session in your terminal.*

### 3. Try Different Models (2 Minutes)
Depending on your hardware, you might want different sizes:
- **Llama 3 (8B):** Great all-rounder. `ollama run llama3`
- **Mistral (7B):** Excellent efficiency. `ollama run mistral`
- **Phi-3 (Mini):** Ultra-lightweight, runs on almost anything. `ollama run phi3`

---

## 🛠️ Leveling Up: Integration & UI

### The REST API (Connecting to Python)
Ollama runs a local server on port `11434`. You can connect your Python MLOps pipeline to it:

```python
import requests

url = "http://localhost:11434/api/generate"
data = {
    "model": "llama3",
    "prompt": "Explain MLOps in one sentence.",
    "stream": False
}

response = requests.post(url, json=data)
print(response.json()['response'])
```

### Adding a Web Interface
If you prefer a ChatGPT-like experience over a terminal:
- **Open WebUI:** The gold standard for Ollama. Usually run via Docker:
  ```bash
  docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui ghcr.io/open-webui/open-webui:main
  ```
- Then visit `http://localhost:3000`.

---

## 💻 Hardware Cheat Sheet
If the model is slow or crashing, check your **VRAM** (GPU Memory) or **RAM**.

| Model Size | Recommended VRAM/RAM | Performance Note |
| :--- | :--- | :--- |
| **1B - 3B** | 4GB+ | Blazing fast, basic tasks |
| **7B - 8B** | 8GB - 16GB | Sweet spot for most users |
| **13B - 30B** | 24GB - 32GB | High quality, requires beefy GPU |
| **70B+** | 48GB+ | Enterprise grade, slow on consumer gear |

**Pro Tip:** If you don't have a GPU, Ollama will use your CPU (via RAM), but it will be significantly slower.

---

## 📝 Key Takeaways
- **Ollama** is the easiest entry point for local LLMs.
- **Quantization** (the magic that makes this possible) compresses models so they fit on consumer hardware.
- **Local LLMs** $\rightarrow$ **Local API** $\rightarrow$ **Your Application**. This is the foundation of "Private AI."

## ❓ Check Your Understanding
1. What is the default port for the Ollama API?
2. Which model would you choose if you had very limited RAM?
3. Why is a local LLM preferable for handling sensitive corporate data?
