# 🐳 Docker Quickstart — Advanced ML/FAMA Bootcamp

> **Zero Python install needed.** Docker pulls everything automatically.

---

## ✅ Prerequisites

| Tool | Minimum Version | Download |
|------|----------------|---------|
| Docker Desktop | 4.x | https://www.docker.com/products/docker-desktop/ |
| Docker Compose | v2 (bundled with Desktop) | — |
| RAM | 8 GB recommended | — |
| Disk | ~6 GB free (image + packages) | — |

---

## 🚀 Quick Start (3 commands)

```bash
# 1. Clone / open the repo
cd advance-ml-fama

# 2. Build & start everything
docker compose up --build

# 3. Open JupyterLab in your browser
#    → http://localhost:8888
```

That's it. No Python, no pip, no virtual environments.

---

## 🔗 Service URLs

| Service | URL | Used In |
|---------|-----|---------|
| **JupyterLab** |
 | All sessions |
| **MLflow UI** (standalone) | http://localhost:5001 | Sessions 04 & 08 |

---

## 📁 Folder Navigation Inside JupyterLab

```
advance-ml-fama/          ← repo root (auto-mounted)
├── day1/
│   ├── 01_ai_ml_dl_llm_landscape/
│   │   └── notebook.ipynb  ← open this first
│   ├── 02_data_quality_leakage/
│   └── ...
├── day2/
│   └── ...
└── topics/               ← content briefs (reference only)
```

Open any `notebook.ipynb` file in JupyterLab and start running cells.

---

## ⚙️ Common Commands

```bash
# Start in background (detached)
docker compose up -d

# Stop all services
docker compose down

# Rebuild after changing requirements.txt or Dockerfile
docker compose up --build

# View live logs
docker compose logs -f jupyter

# Open a shell inside the container
docker exec -it fama-jupyter bash

# Run a single notebook from command line (non-interactive)
docker exec fama-jupyter jupyter nbconvert \
  --to notebook --execute \
  day1/01_ai_ml_dl_llm_landscape/notebook.ipynb \
  --output day1/01_ai_ml_dl_llm_landscape/notebook_executed.ipynb
```

---

## 🌐 Azure ML Setup (Day 2 only)

For sessions 09 and 10 you need Azure credentials:

```bash
# 1. Copy the example env file
cp .env.example .env

# 2. Edit .env with your real values
#    AZURE_SUBSCRIPTION_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
#    AZURE_RESOURCE_GROUP=your-rg-name
#    AZURE_ML_WORKSPACE=your-workspace-name

# 3. Restart with credentials loaded
docker compose down && docker compose up -d
```

> ⚠️ **Never commit `.env` to git** — it's already in `.gitignore`

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---------|-----|
| Port 8888 already in use | `docker compose down` first, or change port in `docker-compose.yml` |
| Package not found | Add it to `requirements.txt`, then `docker compose up --build` |
| Slow first build | Normal — downloading ~2 GB of packages. Subsequent starts are instant. |
| Permission error on Windows | Run Docker Desktop as Administrator |
| Notebook changes not saving | Check that the volume mount is active: `docker inspect fama-jupyter` |
| `shap` or `lightgbm` build error | Increase Docker Desktop RAM to 8 GB in Settings → Resources |

---

## 🔄 Updating Packages

```bash
# 1. Edit requirements.txt — add/change version
# 2. Rebuild
docker compose up --build

# Your notebooks and data are preserved (volume-mounted, not baked in)
```

---

## 🧹 Full Cleanup

```bash
# Stop + remove containers, networks, volumes
docker compose down --volumes

# Also remove the built image
docker rmi advance-ml-fama-jupyter

# Nuclear option: prune everything Docker (careful!)
# docker system prune -a
```

---

*Questions? Check [MASTER_CONTENT_PLAN.md](MASTER_CONTENT_PLAN.md) for the full curriculum index.*
