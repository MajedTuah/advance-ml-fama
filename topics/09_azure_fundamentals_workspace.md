# ☁️ Topic 09 — Azure Fundamentals & Azure ML Workspace
> **Schedule:** Day 2 | 9:00 AM – 10:00 AM | Duration: 60 min
> **Folder:** `day2/01_azure_fundamentals/`
> **Status:** 🔲 Pending Build

---

## 🎯 Learning Objectives
1. Navigate Azure portal and understand core Azure service categories
2. Provision and configure an Azure Machine Learning Workspace
3. Understand the key components of Azure ML (Compute, Datastore, Environments, Models)
4. Connect to Azure ML from Python SDK v2

---

## 🧠 Core Concepts

### 1. Azure Core Concepts (ML-Relevant)
| Azure Concept | ML Equivalent | Description |
|--------------|--------------|-------------|
| **Resource Group** | Project namespace | Logical container for all resources |
| **Subscription** | Billing account | Where costs are billed |
| **Region** | Data center location | Choose closest to data for compliance/latency |
| **Storage Account** | Data lake | Blob storage for datasets and artifacts |
| **Container Registry** | Docker image store | Custom training/serving environments |
| **Key Vault** | Secrets manager | Store API keys, passwords securely |

### 2. Azure ML Workspace — The Central Hub
The Azure ML Workspace is the top-level resource that organizes all ML assets:

```
Azure ML Workspace
├── Compute
│   ├── Compute Clusters (training)
│   ├── Compute Instances (interactive notebooks)
│   └── Inference Clusters (serving)
├── Data
│   ├── Datastores (connections to storage)
│   └── Data Assets (versioned datasets)
├── Jobs
│   ├── Training Jobs (command jobs)
│   ├── Pipeline Jobs (multi-step)
│   └── Sweep Jobs (hyperparameter tuning)
├── Models
│   └── Model Registry (versioned + staged)
├── Environments
│   └── Custom Docker environments for training
└── Endpoints
    ├── Online Endpoints (real-time)
    └── Batch Endpoints (bulk scoring)
```

### 3. Azure ML Compute Options
| Type | Use Case | Billed When |
|------|----------|-------------|
| **Compute Instance** | Interactive development, notebooks | When running |
| **Compute Cluster** | Training jobs (auto-scales to 0) | During job execution only |
| **Serverless Compute** | On-demand, no provisioning | Per-job (new in SDK v2) |
| **Kubernetes (AKS)** | Production inference at scale | Always on |
| **Managed Online Endpoint** | Managed real-time inference | Always on |

### 4. Azure ML SDK v2 — Python Connection
```python
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential

# Authenticate
try:
    credential = DefaultAzureCredential()
    credential.get_token("https://management.azure.com/.default")
except Exception:
    credential = InteractiveBrowserCredential()

# Connect to workspace
ml_client = MLClient(
    credential=credential,
    subscription_id="your-subscription-id",
    resource_group_name="your-resource-group",
    workspace_name="your-workspace-name"
)

print("Connected to workspace:", ml_client.workspace_name)
print("Location:", ml_client.workspaces.get(ml_client.workspace_name).location)
```

### 5. Key Azure ML SDK v2 Concepts
```python
# List compute targets
for compute in ml_client.compute.list():
    print(f"{compute.name} | {compute.type} | {compute.provisioning_state}")

# List registered models
for model in ml_client.models.list():
    print(f"{model.name} | v{model.version} | {model.stage}")

# List datastores
for ds in ml_client.datastores.list():
    print(f"{ds.name} | {ds.type}")
```

### 6. Workspace Architecture Diagram
```
┌────────────────────────────────────────────────────────────┐
│                   Azure Subscription                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Resource Group                          │   │
│  │                                                      │   │
│  │  ┌──────────────┐  ┌────────────┐  ┌─────────────┐ │   │
│  │  │  Azure ML    │  │  Storage   │  │  Key Vault  │ │   │
│  │  │  Workspace   │  │  Account   │  │             │ │   │
│  │  │              │  │  (Blobs)   │  │  Secrets    │ │   │
│  │  │  Compute     │  │            │  │             │ │   │
│  │  │  Models      │  │  Datasets  │  └─────────────┘ │   │
│  │  │  Jobs        │  │  Artifacts │                   │   │
│  │  │  Endpoints   │  └────────────┘  ┌─────────────┐ │   │
│  │  └──────────────┘                  │  Container  │ │   │
│  │                                    │  Registry   │ │   │
│  │                                    │  (Images)   │ │   │
│  │                                    └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────┘
```

### 7. Azure ML vs. On-Premise Comparison
| Aspect | On-Premise | Azure ML |
|--------|-----------|---------|
| Compute provisioning | Weeks | Minutes |
| Scaling | Manual, limited | Auto-scale to 0 (cost-efficient) |
| Experiment tracking | Manual (MLflow self-hosted) | Built-in |
| Model registry | Manual | Built-in with staging |
| Security | Custom IAM | Azure RBAC, VNET integration |
| Cost | CAPEX (hardware) | OPEX (pay-per-use) |

---

## 📊 Diagrams & Visuals Required

| # | Diagram | Type | Notebook Cell |
|---|---------|------|---------------|
| 1 | Azure ML Workspace component map | Nested box diagram | Cell 4 |
| 2 | Workspace architecture (resources + connections) | Annotated architecture | Cell 6 |
| 3 | Compute options comparison (when to use each) | Decision table + visual | Cell 8 |
| 4 | On-premise vs. Azure ML comparison | Side-by-side comparison chart | Cell 10 |

---

## 🏋️ Activities

### Activity 1 — Portal Exploration (15 min)
- Navigate to [ml.azure.com](https://ml.azure.com)
- Explore: Studio → Compute → Datastores → Models → Environments
- Screenshot the workspace overview and identify each component

### Activity 2 — Connect via SDK v2 (25 min)
- Install `azure-ai-ml`, `azure-identity`
- Authenticate using `InteractiveBrowserCredential`
- List all compute targets, datastores, and registered models
- Confirm connection with `print(ml_client.workspace_name)`

### Activity 3 — Architecture Diagram (code)
- Use matplotlib to draw the Azure ML Workspace component map
- Color-code by category (Compute = blue, Data = green, Models = orange)

---

## 📝 Notebook Cell Plan

```
Cell 01 [MD]   → Session intro: why cloud ML?
Cell 02 [MD]   → Azure core concepts for ML practitioners
Cell 03 [MD]   → Azure ML Workspace — what it is, why it matters
Cell 04 [Code] → Workspace component map diagram
Cell 05 [MD]   → Azure ML Compute options explained
Cell 06 [Code] → Workspace architecture diagram
Cell 07 [MD]   → SDK v2 authentication + connection
Cell 08 [Code] → Connect to workspace + list resources
Cell 09 [Code] → Compute comparison decision chart
Cell 10 [Code] → On-premise vs. Azure ML comparison
Cell 11 [MD]   → Key Takeaways + Quiz
```

---

## 📁 Files to Create

```
day2/01_azure_fundamentals/
├── README.md
└── notebook.ipynb
```

> ⚠️ **Note:** Activities require Azure subscription access. Notebook can run in mock mode using `config_mock.json` if no subscription available.

---

## 📝 Key Takeaways
- Azure ML Workspace is the single pane of glass for all ML operations in Azure
- Compute clusters auto-scale to zero — you only pay when training is running
- SDK v2 is the modern standard — avoid the deprecated SDK v1 patterns
- Managed Online Endpoints handle infrastructure complexity so you can focus on the model
- Resource Groups keep related services organized and billed together

---

## ❓ Quiz Questions
1. What is the difference between a Compute Instance and a Compute Cluster in Azure ML?
2. Why would you choose Azure ML over self-hosted MLflow?
3. What does `DefaultAzureCredential` try first when authenticating?
4. What is a Datastore in Azure ML and how does it differ from a Data Asset?
5. What does "auto-scale to zero" mean and why is it important for training costs?

---

## 📖 Further Reading
- [Azure ML Documentation](https://learn.microsoft.com/en-us/azure/machine-learning/)
- [Azure ML SDK v2 Quickstart](https://learn.microsoft.com/en-us/azure/machine-learning/quickstart-create-resources)
- [Azure ML vs. Amazon SageMaker vs. GCP Vertex AI Comparison](https://learn.microsoft.com/en-us/azure/architecture/data-guide/technology-choices/data-science-and-machine-learning)
- [Microsoft Learn — Azure ML Free Learning Path](https://learn.microsoft.com/en-us/training/paths/use-azure-machine-learning-pipelines-for-automation/)
