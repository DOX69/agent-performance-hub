# Setup Secrets & API Keys

To enable the automated workflows (tests, benchmarks, monitoring), you need to configure API keys in your GitHub repository.

## 1. Google Gemini API Key
Required for: **Gemini 3 testing** and **Token Benchmarking**.

**How to get it:**
1.  Go to [Google AI Studio](https://aistudio.google.com/).
2.  Click on **Get API key** (usually in the left sidebar).
3.  Click **Create API key**.
4.  Copy the key string (starts with `AIza...`).

**How to add to GitHub:**
1.  Go to your repo on GitHub: `Settings` > `Secrets and variables` > `Actions`.
2.  Click **New repository secret**.
3.  **Name**: `GOOGLE_API_KEY`
4.  **Secret**: *Paste your key here*.
5.  Click **Add secret**.


## 3. Other Secrets
- `CTX7_API_KEY`: If using Context7 features in CI.
- `N8N_WEBHOOK_URL`: If integrating with n8n workflows.
