# ─────────────────────────────────────────────────────────────────────────────
# Advanced ML/FAMA Bootcamp — Jupyter Environment
# Base: official Jupyter minimal-notebook (Python 3.11, no root needed)
# ─────────────────────────────────────────────────────────────────────────────
FROM jupyter/minimal-notebook:python-3.11

LABEL maintainer="Aventra Digital — ML Team"
LABEL description="Self-contained Jupyter environment for the Advanced ML/FAMA Bootcamp"
LABEL version="1.0.0"

# ── switch to root only to install system deps ────────────────────────────────
USER root
RUN apt-get update --quiet && \
    apt-get install -y --no-install-recommends \
        curl \
        git \
        graphviz \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# ── back to non-root (jovyan = default Jupyter user) ─────────────────────────
USER ${NB_UID}

# ── copy requirements first for Docker layer caching ─────────────────────────
COPY --chown=${NB_UID}:${NB_GID} requirements.txt /tmp/requirements.txt

# ── install all Python packages ───────────────────────────────────────────────
# Use --no-cache-dir to keep image lean
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt

# ── copy the entire bootcamp repo into the container ─────────────────────────
COPY --chown=${NB_UID}:${NB_GID} . /home/jovyan/advance-ml-fama/

# ── set working directory inside container ────────────────────────────────────
WORKDIR /home/jovyan/advance-ml-fama

# ── expose Jupyter port ───────────────────────────────────────────────────────
EXPOSE 8888

# ── Jupyter Lab config: disable token for dev convenience  ───────────────────
# ⚠️  For production or public exposure: remove --NotebookApp.token=''
ENV JUPYTER_ENABLE_LAB=yes

CMD ["start-notebook.sh", \
     "--NotebookApp.token=''", \
     "--NotebookApp.password=''", \
     "--NotebookApp.open_browser=False", \
     "--NotebookApp.notebook_dir=/home/jovyan/advance-ml-fama"]
