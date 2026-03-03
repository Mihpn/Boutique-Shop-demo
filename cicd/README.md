# 🗂️ CICD — Trung tâm chỉ huy DevSecOps

Đây là **thư mục duy nhất** bạn cần quan tâm để setup và vận hành pipeline CI/CD.

```
cicd/
├── README.md                  ← File này — hướng dẫn toàn bộ
└── argocd-application.yaml    ← CD: ArgoCD manifest (apply lên K8s)

.github/workflows/             ← CI: GitHub Actions (phải giữ ở đây — quy định của GitHub)
└── devsecops-ci.yml
```

---

## 📋 Checklist chạy lần đầu (thứ tự quan trọng!)

```
[ ] Bước 1: Tạo GitHub Secrets
[ ] Bước 2: Push code lên GitHub → CI tự chạy
[ ] Bước 3: Cài ArgoCD trên Master Node
[ ] Bước 4: Sửa repoURL → Apply argocd-application.yaml
[ ] Bước 5: Truy cập app tại http://online-boutique.kihpn.local
```

---

## 🔑 Bước 1: Tạo GitHub Secrets

**GitHub Repo → Settings → Secrets and variables → Actions → New repository secret**

| Secret | Giá trị | Lấy ở đâu |
|---|---|---|
| `DOCKERHUB_USERNAME` | `kihpn1711` | Tên đăng nhập Docker Hub |
| `DOCKERHUB_TOKEN` | `dckr_pat_...` | hub.docker.com → Account Settings → Security → New Access Token |

---

## 🚀 Bước 2: Trigger CI Pipeline

```powershell
# Từ máy Windows (thư mục gốc project)
cd d:\DevOps\Projects\demo\microservices-demo

git add .
git commit -m "feat: add DevSecOps CI/CD pipeline"
git push origin main
```

**GitHub Actions sẽ tự chạy 11 jobs song song:**
```
Lint (Hadolint) → Build image → Trivy Security Scan → Push to Docker Hub
                                                        Tag: <git-sha> + latest
```
Xem tiến trình tại: **GitHub Repo → tab Actions**

---

## 🛠️ Bước 3: Cài ArgoCD trên Master Node

SSH vào 192.168.1.111, chạy lần lượt:

```bash
# Cài ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Đợi sẵn sàng
kubectl wait --for=condition=available deployment/argocd-server -n argocd --timeout=300s

# Lấy mật khẩu admin
kubectl get secret argocd-initial-admin-secret -n argocd \
  -o jsonpath="{.data.password}" | base64 -d && echo

# Mở UI qua NodePort
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "NodePort"}}'
kubectl get svc argocd-server -n argocd   # Xem NodePort được cấp
# Truy cập: https://192.168.1.111:<NodePort>   login: admin / <password trên>
```

---

## 🎯 Bước 4: Apply ArgoCD Application

```bash
# ⚠️ Mở file và thay YOUR_GITHUB_USERNAME trước
nano ~/cicd/argocd-application.yaml

# Apply
kubectl apply -f ~/cicd/argocd-application.yaml

# Kiểm tra trạng thái
kubectl get applications -n argocd
kubectl get pods -n online-boutique -w
```

---

## 🔄 Luồng CI/CD tổng thể

```
git push → GitHub Actions (CI)
               ├── Lint Dockerfile (Hadolint)
               ├── Build image local
               ├── Trivy Security Scan (báo cáo bảng)
               └── Push image → Docker Hub (tag: git-sha)

ArgoCD (CD) ─── poll GitHub repo mỗi 3 phút ──→
               ├── Phát hiện thay đổi Helm Chart
               ├── helm upgrade online-boutique
               └── selfHeal + prune tự động
```

### Tại sao ArgoCD chạy được sau NAT?

ArgoCD dùng **Pull-based model** — nó **chủ động gửi request HTTPS ra ngoài** (outbound port 443) tới GitHub.
Kết nối outbound HTTPS luôn đi qua NAT mà không cần mở port hay VPN.

---

## ⚙️ Upgrade / Rollback

```bash
# Thay đổi image tag trong values.yaml → git push → ArgoCD tự sync

# Rollback khẩn cấp (không cần Git)
argocd app rollback online-boutique 1

# Xem lịch sử sync
argocd app history online-boutique
```
