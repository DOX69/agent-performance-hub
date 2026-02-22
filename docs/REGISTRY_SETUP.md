# 📦 Installation Guide

This guide explains how to install `aph-cli` directly from our private GitHub repository, as the package is distributed via GitHub Releases and GitHub Actions Artifacts instead of a traditional PyPI registry.

---

## 🔑 1. Authentication (One-time setup)

Since this repository is private, standard installation commands (`uv pip install git+https...`) will prompt for your GitHub credentials. We recommend using a GitHub Personal Access Token (PAT) for seamless installation.

### Step A: Generate a Token
1. Go to **GitHub Settings** -> **Developer settings** -> **Personal access tokens** -> **Tokens (classic)**.
2. Click **Generate new token (classic)**.
3. Name it "APH CLI Access".
4. Select the following scope:
   - `repo` (Full control of private repositories, necessary to read private code)
5. Click **Generate token** and copy it immediately.

### Step B: Configure Environment
You can embed the token directly into the installation URL. Set it as an environment variable to keep it secure:

**Mac/Linux (Zsh/Bash):**
```bash
export GITHUB_PAT="YOUR_PAT_TOKEN"
```

**Windows (PowerShell):**
```powershell
$env:GITHUB_PAT="YOUR_PAT_TOKEN"
```

*(Alternatively, if you have SSH keys configured for GitHub, you can use `git+ssh` instead of `git+https` without needing a PAT).*

---

## 🚀 2. Installation

You can install `aph-cli` directly from the Git repository.

### Install Stable Version (Production)
This installs the latest code from the `main` branch.

**Using HTTPS & PAT:**
```bash
uv pip install "git+https://${GITHUB_PAT}@github.com/DOX69/agent-performance-hub.git@main"
```

**Using SSH (if configured):**
```bash
uv pip install "git+ssh://git@github.com/DOX69/agent-performance-hub.git@main"
```

*(You can also manually download the `.whl` file from the **Releases** page on GitHub and run `uv pip install <path-to-file.whl>`)*

### Install Beta Version (Staging)
This installs the latest development version from the `staging` branch.

**Using HTTPS & PAT:**
```bash
uv pip install "git+https://${GITHUB_PAT}@github.com/DOX69/agent-performance-hub.git@staging"
```

**Using SSH (if configured):**
```bash
uv pip install "git+ssh://git@github.com/DOX69/agent-performance-hub.git@staging"
```

*(You can also download the `aph-package` artifact from the latest successful **GitHub Actions** run on the `staging` branch, extract the zip, and install the `.whl` file directly).*

---

## 🔄 3. Update

To update to the latest version, run the same `install` command but add the `--upgrade` (or `-U`) flag to force `uv pip` to fetch the latest commit.

```bash
uv pip install --upgrade "git+ssh://git@github.com/DOX69/agent-performance-hub.git@main"
```

---

## 🛠️ Release Process (For Maintainers)

The project uses a **Staging -> Production** workflow. We no longer use GitHub Packages PyPI due to lack of native support for the PyPI protocol.

### 1. Develop & Beta Release
- Create a feature branch.
- Merge your changes into the `staging` branch.
- **Action**: GitHub Actions automatically builds the package and attaches it as a downloadable **Artifact** to the workflow run.
- **Test**: Users can install it directly from the staging branch:
  ```bash
  uv pip install --upgrade "git+ssh://git@github.com/DOX69/agent-performance-hub.git@staging"
  ```

### 2. Production Release
- Once the Beta is verified on `staging`:
- Merge `staging` into `main`.
- Create a new tag on `main` and push it to origin (e.g., `v0.1.3`).
- **Action**: GitHub Actions automatically builds the package and attaches it as a release asset to the new **GitHub Release**.
- **Users**: Can now install from `main` or download the release assets manually:
  ```bash
  uv pip install --upgrade "git+ssh://git@github.com/DOX69/agent-performance-hub.git@main"
  ```
