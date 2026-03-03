# 🛒 Online Boutique — DevSecOps Demo

> Demo project: Triển khai 12 microservices trên K8s On-Premise với CI/CD pipeline hoàn chỉnh.

## 🏗 Tech Stack

| Layer | Công nghệ |
|---|---|
| **Application** | 12 Microservices (Go, Python, Java, C#, Node.js) |
| **Container** | Docker, Docker Hub (`kihpn1711/*`) |
| **Orchestration** | Kubernetes (On-Premise, VMware) |
| **Packaging** | Helm Chart (startup ordering via initContainers) |
| **CI** | GitHub Actions (Hadolint + Trivy + Docker Build/Push) |
| **CD** | ArgoCD (GitOps, Pull-based, Auto-sync) |

## 📁 Cấu trúc Project

```
.
├── .github/workflows/
│   └── devsecops-ci.yml           # CI Pipeline — 11 services matrix
├── cicd/
│   ├── argocd-application.yaml    # CD — ArgoCD Application
│   └── README.md                  # Setup Guide đầy đủ
├── online-boutique-chart/         # Helm Chart (5 nhóm khởi động)
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/                 # 15 templates + helpers
└── src/                           # Source code 12 services
```

## 🔄 CI/CD Pipeline

```
Developer → git push → GitHub Actions (CI)
                          ├── Hadolint (Lint Dockerfile)
                          ├── Trivy (Security Scan)
                          └── Docker Build & Push (tag: git-sha)

ArgoCD (CD) → poll GitHub mỗi 3 phút → helm upgrade tự động
```

## 🚀 Quick Start

```bash
# 1. Thêm GitHub Secrets: DOCKERHUB_USERNAME + DOCKERHUB_TOKEN
# 2. Push code → CI tự chạy
# 3. Trên K8s master node:
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl apply -f cicd/argocd-application.yaml
```

Chi tiết: xem [`cicd/README.md`](cicd/README.md)

## 📜 License

Apache License 2.0
