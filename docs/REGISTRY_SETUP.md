# 📦 Registry Setup & Installation Guide

This guide explains how to install `aph-cli` from our private GitHub Packages registry.

---

## 🔑 1. Authentication (One-time setup)

Since this package is hosted on a private registry, you need to authenticate using a GitHub Personal Access Token (PAT).

### Step A: Generate a Token
1. Go to **GitHub Settings** -> **Developer settings** -> **Personal access tokens** -> **Tokens (classic)**.
2. Click **Generate new token (classic)**.
3. Name it "APH CLI Access".
4. Select the following scope:
   - `read:packages` (Required to download the package)
5. Click **Generate token** and copy it immediately.

### Step B: Configure Environment
We recommend setting up environment variables to handle authentication securely.

**Mac/Linux (Zsh/Bash):**
Add this to your `~/.zshrc` or `~/.bashrc`:

```bash
# Replace YOUR_GITHUB_USERNAME and YOUR_PAT_TOKEN
export UV_INDEX_URL="https://YOUR_GITHUB_USERNAME:YOUR_PAT_TOKEN@pypi.pkg.github.com/DOX69/simple"
```

Then reload your shell:
```bash
source ~/.zshrc
```

**Windows (PowerShell):**
```powershell
[System.Environment]::SetEnvironmentVariable("UV_INDEX_URL", "https://YOUR_GITHUB_USERNAME:YOUR_PAT_TOKEN@pypi.pkg.github.com/DOX69/simple", "User")
```

---

## 🚀 2. Installation

Once authentication is set up, you can install `aph-cli` directly.

### Install Stable Version (Production)
This installs the latest tagged release (e.g., `v0.1.3`).

```bash
uv pip install aph-cli
```

### Install Beta Version (Staging)
This installs the latest development version from the `staging` branch.

```bash
# Install the latest pre-release
uv pip install --pre aph-cli

# Or verify available versions
uv pip index versions aph-cli
```

---

## 🔄 3. Update

To update to the latest version:

```bash
uv pip install --upgrade aph-cli
```

---

## 🛠️ Release Process (For Maintainers)

The project uses a **Staging -> Production** workflow with dynamic versioning.

### 1. Develop & Beta Release
- Create a feature branch.
- Merge your changes into the `staging` branch.
- **Action**: GitHub Actions automatically builds and publishes a **Beta** version (e.g., `0.1.3.dev14+g7a8b9c`).
- **Test**: Install the beta version locally to verify:
  ```bash
  uv pip install --pre --upgrade aph-cli
  ```

### 2. Production Release
- Once the Beta is verified on `staging`:
- Merge `staging` into `main`.
- Create a new tag on `main` and push it to origin (e.g., `v0.1.3`).
- **Action**: GitHub Actions automatically builds and publishes the **Production** version (e.g., `0.1.3`).
- **Users**: Can now run `uv pip install --upgrade aph-cli`.

---

## ❓ Troubleshooting

**Error: "401 Unauthorized"**
- Verify your PAT has `read:packages` scope.
- Check if your `UV_INDEX_URL` is correctly set with `echo $UV_INDEX_URL`.
- Ensure you are using your GitHub username, not your email.

**Error: "Package not found"**
- Ensure you are looking at the correct registry URL: `https://pypi.pkg.github.com/DOX69/simple`.
- If installing a beta version, ensure you use the `--pre` flag.
