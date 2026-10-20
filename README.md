# Ridgeline approval desk: solution

The worked solution to TechHub challenge 410, **Keep an API Key in Streamlit Secrets** (https://techhub.byuaccounting.net/t/410-streamlit-keep-an-api-key-in-streamlit-secrets/9410/).
The starter that students copy is on the `main` branch of https://github.com/techhub-training/ridgeline-approval-app.

The change is a few lines in `app.py`:

```python
try:
    API_KEY = st.secrets["TECHHUB_API_KEY"]
except Exception:   # no secrets file, or no TECHHUB_API_KEY in it
    st.error("No API key found. ...")
    st.stop()
```

and `.gitignore` gets `.streamlit/secrets.toml`. To run it, create `.streamlit/secrets.toml` with
`TECHHUB_API_KEY = "thk_..."` (your own key), then `streamlit run app.py`. On Streamlit Community Cloud the same line goes
in the app's **Settings › Secrets**.

Canyon Coat Paints (V1005) has five pending invoices: INV-00616, INV-00617, INV-00619, INV-00621 and INV-00624.
All five go on hold. To start over in the sandbox, `POST /reset` with your key.

Already committed a key? Deleting it in a new commit isn't enough: it is still in the history. Revoke it (for the
TechHub sandbox, get a new key) and see TechHub challenge 395, *Find a leaked key in the history*.
