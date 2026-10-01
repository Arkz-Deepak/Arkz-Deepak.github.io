# ⚡ Arkz Lab — Central Systems & Documentation Index

[![Live Portal](https://img.shields.io/badge/Live_Portal-lab.deepak-arkz.me-blue?style=flat&logo=google-chrome&logoColor=white)](http://lab.deepak-arkz.me/)
[![Automated Sync](https://github.com/Arkz-Deepak/Arkz-Deepak.github.io/actions/workflows/sync-index.yml/badge.svg)](https://github.com/Arkz-Deepak/Arkz-Deepak.github.io/actions/workflows/sync-index.yml)

The central root domain index portal for **Deepak R** (`@Arkz-Deepak`), deployed at **[`lab.deepak-arkz.me`](http://lab.deepak-arkz.me/)**.

---

## 🌟 Features
- **Central System Index**: Automatically indexes and categorizes all active engineering repositories, ROS 2 packages, computer vision systems, digital twins, and hackathon solutions.
- **GitHub Pages Routing**: Directly links to all deployed project documentation hubs (`lab.deepak-arkz.me/<repo-name>/`).
- **Automated Synchronization**: A scheduled GitHub Actions workflow (`sync-index.yml`) queries the GitHub REST API, verifies live documentation status, and regenerates `data/repositories.json`.
- **Client-Side Live Fallback**: Real-time filtering, instant search, and browser-level live GitHub synchronization.

---

## 🚀 Local Development
```bash
# Clone the repository
git clone https://github.com/Arkz-Deepak/Arkz-Deepak.github.io.git
cd Arkz-Deepak.github.io

# Manually trigger a repository sync
python scripts/sync_repositories.py

# Serve locally
python -m http.server 8000
```
Open `http://localhost:8000` in your web browser.