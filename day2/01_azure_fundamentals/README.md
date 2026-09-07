# ☁️ Topic 09 — Azure Fundamentals & Azure ML Workspace

> **Session:** Day 2 | 9:00 AM – 10:00 AM (60 min)  
> **Location:** `day2/01_azure_fundamentals/`  
> **Prerequisites:** Python 3.9+, Basic Machine Learning lifecycle understanding

---

## 🎯 Learning Objectives

By the end of this session, you will be able to:
1. **Navigate the Azure Cloud Ecosystem**: Understand Azure resource hierarchies (Subscriptions, Resource Groups, Regions) and key services powering AI and MLOps.
2. **Master the Azure ML Workspace**: Provision, configure, and navigate the central hub organizing data, compute, environments, models, pipelines, and endpoints.
3. **Optimize Compute & Costs**: Choose between Compute Instances, Auto-scaling Compute Clusters (scale-to-zero), Serverless Compute, and Managed Endpoints.
4. **Programmatically Manage Assets with Azure ML SDK v2**: Authenticate using `DefaultAzureCredential` and manage assets using clean Python code.

---

## 🧭 Navigating Azure Services for AI & MLOps

Building enterprise-grade AI applications requires more than just training code. Azure provides a coordinated ecosystem of services:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            AZURE SUBSCRIPTION                               │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                        RESOURCE GROUP                                 │  │
│  │                                                                       │  │
│  │   ┌───────────────────────────────────────────────────────────────┐   │  │
│  │   │                     Azure ML Workspace                        │   │  │
│  │   │  • Compute Clusters (Training)   • Model Registry             │   │  │
│  │   │  • Compute Instances (Notebooks) • Managed Online Endpoints   │   │  │
│  │   │  • Data Assets & Datastores      • Pipelines & Job History    │   │  │
│  │   └───────────────────────────────┬───────────────────────────────┘   │  │
│  │                                   │ Linked Companion Resources        │  │
│  │       ┌───────────────────────────┼───────────────────────────┐       │  │
│  │       ▼                           ▼                           ▼       │  │
│  │  ┌──────────────┐            ┌──────────────┐            ┌──────────┐ │  │
│  │  │Azure Storage │            │  Azure Key   │            │  Azure   │ │  │
│  │  │ Account Blob │            │    Vault     │            │Container │ │  │
│  │  │ (Data/Blobs) │            │  (Secrets)   │            │ Registry │ │  │
│  │  └──────────────┘            └──────────────┘            └──────────┘ │  │
│  │       ▲                           ▲                           ▲       │  │
│  │       └───────────────────────────┼───────────────────────────┘       │  │
│  │                                   │ Telemetry & Logs                  │  │
│  │                              ┌────┴─────────┐                         │  │
│  │                              │ Application  │                         │  │
│  │                              │   Insights   │                         │  │
│  │                              └──────────────┘                         │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1. The Core Infrastructure Quartet
When you create an Azure ML Workspace, Azure automatically provisions 4 essential companion services in your Resource Group:

| Companion Service | Role in MLOps Lifecycle | Practical Example |
|---|---|---|
| **Azure Storage Account** | Default datastore & artifact storage | Stores raw datasets, parquet files, output weights (`model.pkl`), and logs |
| **Azure Key Vault** | Secure secrets & credential store | Stores database connection strings, S3 keys, and third-party API tokens |
| **Azure Container Registry (ACR)** | Docker image repository | Stores customized Docker images used to execute distributed training runs |
| **Application Insights** | Live monitoring & telemetry | Tracks latency, request volume, error rates, and exceptions from deployed models |

---

## 🏛️ Azure ML Workspace Asset Taxonomy

The Workspace is organized into two primary planes in **Azure ML Studio** ([ml.azure.com](https://ml.azure.com)):

```
Azure ML Studio
├── 🛠️ Authoring
│   ├── Notebooks (Interactive Jupyter in browser)
│   ├── Automated ML (No-code / Low-code AutoML search)
│   └── Designer (Drag-and-drop ML pipeline builder)
│
├── 📦 Assets (Versioned & Tracked)
│   ├── Data (Datastores & Versioned Data Assets)
│   ├── Jobs (Command Jobs, Sweep Jobs, Pipeline Jobs)
│   ├── Components (Modular, reusable pipeline blocks)
│   ├── Models (Model Registry with staging & lineage)
│   └── Environments (Conda + Docker runtime specifications)
│
└── ⚙️ Manage
    ├── Compute (Instances, Clusters, Attached Compute)
    ├── Endpoints (Real-time Online & Batch Inference)
    └── Linked Services (Databricks, Synapse, Key Vaults)
```

---

## 💻 Compute Selection Guide & Cost Strategies

| Compute Type | Scaling Behavior | Billing Model | Best Suited For |
|---|---|---|---|
| **Compute Instance** | Single node (fixed) | Billed 100% of time VM is Running | Interactive EDA, quick prototyping, debugging |
| **Compute Cluster** | Auto-scales **0 → N nodes** | **Billed ONLY during job execution** | Production training, heavy hyperparameter sweeps |
| **Serverless Compute** | Managed on-demand | Billed per-job with zero setup | Occasional training jobs without managing clusters |
| **Managed Online Endpoint** | Auto-scales on QPS/CPU | Billed per active replica VM | Real-time REST API serving with blue/green deployment |
| **Batch Endpoint** | Spins up compute on trigger | Billed only during scoring run | Nightly bulk scoring of millions of rows |

> 💡 **Cost Optimization Golden Rule**: Always set `min_instances = 0` on training compute clusters with an `idle_time_before_scale_down = 120` seconds. This ensures you pay **$0** when training jobs are finished!

---

## 🐍 Azure ML SDK v2 Python Quickstart

Azure ML SDK v2 uses clean, declarative Python objects:

```python
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

# 1. Authenticate & Connect
credential = DefaultAzureCredential()
ml_client = MLClient(
    credential=credential,
    subscription_id="<YOUR_SUBSCRIPTION_ID>",
    resource_group_name="<YOUR_RESOURCE_GROUP>",
    workspace_name="<YOUR_WORKSPACE_NAME>"
)

print(f"Connected to Workspace: {ml_client.workspace_name}")

# 2. Inspect Available Compute
for cluster in ml_client.compute.list():
    print(f"Compute: {cluster.name} | Type: {cluster.type} | State: {cluster.provisioning_state}")

# 3. Inspect Registered Models
for model in ml_client.models.list():
    print(f"Model: {model.name} | Version: {model.version} | Path: {model.path}")
```

---

## 🏋️ Hands-On Activities

### Activity 1: Portal Navigation & Service Mapping (15 min)
1. Open [ml.azure.com](https://ml.azure.com) and log into your workspace.
2. Locate the linked **Storage Account**, **Key Vault**, and **Container Registry** under the Workspace Overview.
3. Explore the **Compute** tab and examine the difference between Instances and Clusters.

### Activity 2: SDK v2 Connection & Asset Discovery (25 min)
1. Open `notebook.ipynb` in this directory.
2. Execute the SDK v2 connection cell (supports live Azure credentials or built-in offline simulation).
3. Query and visualize your workspace asset inventory, compute scaling profiles, and on-premise vs. cloud comparison matrix.

---

## 📝 Key Takeaways

1. **Workspace is the Single Pane of Glass**: Centralizes all ML assets (data, code, compute, environments, models, endpoints) in one auditable location.
2. **Auto-Scale to Zero Saves Budget**: Always run production training on Compute Clusters configured with `min_instances = 0`.
3. **Companion Services Handle Heavy Lifting**: Blob Storage holds large datasets, Key Vault protects secrets, ACR hosts custom Docker environments, and App Insights monitors production traffic.
4. **SDK v2 is Declarative**: Replaces legacy SDK v1 with standardized YAML/Python specifications compatible with MLOps CI/CD pipelines.

---

## ❓ Quiz / Check Your Understanding

1. **Which companion resource is automatically provisioned with Azure ML to store trained model artifacts and datasets?**
   - *Answer: Azure Storage Account (Blob / ADLS Gen2).*

2. **Why is a Compute Cluster preferred over a Compute Instance for production model training?**
   - *Answer: A Compute Cluster auto-scales to 0 nodes when idle, eliminating idle compute costs, and can scale horizontally across multiple nodes for distributed training.*

3. **What is the primary role of Azure Key Vault in an AI/ML workflow?**
   - *Answer: To securely manage sensitive credentials, database connection strings, and API keys without hardcoding them in code or notebooks.*

4. **What authentication class in `azure.identity` automatically tries environment variables, Managed Identity, and Azure CLI before falling back to browser login?**
   - *Answer: `DefaultAzureCredential`.*

---

## 📖 Further Reading
- [Official Azure Machine Learning Documentation](https://learn.microsoft.com/en-us/azure/machine-learning/)
- [Azure ML SDK v2 Python API Reference](https://learn.microsoft.com/en-us/python/api/overview/azure/ai-ml-readme)
- [Enterprise Security and Architecture for Azure ML](https://learn.microsoft.com/en-us/azure/machine-learning/concept-enterprise-security)
