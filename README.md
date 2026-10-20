# Ridgeline approval desk

TechHub challenge 410: **Keep an API Key in Streamlit Secrets**. Full instructions, data dictionary and hints: https://techhub.byuaccounting.net/t/410-streamlit-keep-an-api-key-in-streamlit-secrets/9410/

*Ridgeline series:* you work in accounting at Ridgeline Home & Tool, a home-improvement retailer with eleven stores
in Utah and Idaho and a distribution center.

Accounts payable wants a small web app for approving vendor invoices: pick a vendor, see its pending invoices, approve them or put them on hold. `app.py` does all of that through the TechHub API sandbox, but it expects the API key typed into the code, which is how keys leak. Fix that, then use the app.

## Get your own copy

Click **Use this template › Create a new repository**. Keep the name `ridgeline-approval-app` and make it **Public**.
(Or open it straight in a codespace: https://codespaces.new/techhub-training/ridgeline-approval-app?quickstart=1.) Work in your copy, not this one.

## Open it

**In your browser (nothing to install):** on your copy of this repository, click **Code › Codespaces › Create codespace on main**.
The app installs and starts by itself, and a preview opens in a few minutes. Stop the codespace when you're done
(github.com/codespaces › ••• › Stop) so it doesn't use your free hours.

**On your computer:** you need Python 3.10 or newer and Git.

```
git clone https://github.com/<you>/ridgeline-approval-app.git
cd ridgeline-approval-app
python -m venv .venv
source .venv/bin/activate          # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```
## Your API key goes in secrets, never in the code

This repository is public: anything you commit, anyone can read, forever (deleting it later doesn't remove it from
the history). Streamlit keeps keys in a separate file that you never commit:

1. Get a free key for the TechHub API sandbox at https://techhub.byuaccounting.net/api/ (it starts with `thk_`).
2. Create the file `.streamlit/secrets.toml` (in Codespaces: right-click in the file list › New Folder `.streamlit`, then New File `secrets.toml`) containing:

   ```toml
   TECHHUB_API_KEY = "thk_..."
   ```

3. Add the line `.streamlit/secrets.toml` to `.gitignore`, so Git never picks the file up. `git status` should not list it.


## Your task

1. Set up your key in secrets (above). Don't paste it into `app.py`.
2. In `app.py`, replace the line `API_KEY = "thk_PASTE_YOUR_KEY_HERE"` with code that reads `st.secrets["TECHHUB_API_KEY"]`.
   If the key is missing, show a clear message with `st.error` and stop with `st.stop()`, rather than crashing.
3. Run the app. Treasury just called: **Canyon Coat Paints** (V1005) reported a change of bank account by email, which
   is a classic fraud pattern. Use your app to put **every pending Canyon Coat Paints invoice on hold**, with a hold
   reason such as `Vendor bank change: verify by phone`. Leave other vendors' invoices alone.
4. Commit and push `app.py` and `.gitignore` (not `secrets.toml`). Then publish the app on Streamlit Community Cloud
   and paste your key into the app's **Settings › Secrets** there, in the same `TECHHUB_API_KEY = "..."` form.

## Publish it on Streamlit Community Cloud

1. Commit and push your work to GitHub.
2. Sign in at [share.streamlit.io](https://share.streamlit.io) with your GitHub account.
3. **Create app › Deploy a public app from GitHub**: pick this repository, branch `main`, main file `app.py`.
4. Open **Advanced settings › Secrets** and paste `TECHHUB_API_KEY = "thk_..."`. Click **Deploy**. The app gets a public address like `https://<name>.streamlit.app`.

Every push to `main` redeploys the app. An app nobody visits for a while goes to sleep; the first visitor wakes it up.


## Check your answer

Enter your API key and your GitHub username in the TechHub checker. It checks the invoices in the sandbox and reads `app.py` and `.gitignore` from your copy of this repository (and makes sure no key or `secrets.toml` is in it). Checker: https://techhub.byuaccounting.net/check/?c=410

The worked solution is on the [`solution` branch](https://github.com/techhub-training/ridgeline-approval-app/tree/solution). Try it yourself first.
