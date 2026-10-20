"""Ridgeline approval desk (TechHub challenge 410).

Reads Ridgeline's pending vendor invoices from the TechHub API sandbox and approves them or puts them on hold.
It isn't safe to run yet: the API key belongs in Streamlit secrets, not in the code. README.md says how to fix that."""
import requests
import streamlit as st

API = "https://techhub.byuaccounting.net/api/v1"

st.set_page_config(page_title="Ridgeline approval desk", layout="wide")
st.title("Ridgeline approval desk")

# TODO: this repository is public, so never paste your real key here. Put it in .streamlit/secrets.toml
# and read it with st.secrets["TECHHUB_API_KEY"] (README.md, step 3).
API_KEY = "thk_PASTE_YOUR_KEY_HERE"

session = requests.Session()
session.headers.update({"X-API-Key": API_KEY, "User-Agent": "Ridgeline-approval-desk/1.0"})


def get_all(path: str, **params) -> list[dict]:
    """GET every page of a list endpoint."""
    rows, url, params = [], f"{API}{path}", {**params, "per_page": 100}
    while url:
        r = session.get(url, params=params, timeout=20)
        r.raise_for_status()
        body = r.json()
        rows += body["data"]
        url, params = body["links"]["next"], None
    return rows


@st.cache_data(ttl=600)
def vendors() -> dict[str, str]:
    return {v["vendor_id"]: v["name"] for v in get_all("/vendors", sort="name")}


names = vendors()
vendor_id = st.sidebar.selectbox("Vendor", list(names), format_func=lambda v: f"{names[v]} ({v})")
pending = get_all("/invoices", vendor_id=vendor_id, approval_status="pending", sort="invoice_date")

st.subheader(f"Pending invoices: {names[vendor_id]}")
if not pending:
    st.info("Nothing pending for this vendor.")
else:
    st.dataframe([{k: i[k] for k in ("invoice_id", "vendor_invoice_number", "invoice_date", "due_date", "amount", "po_number")}
                  for i in pending], hide_index=True)
    chosen = st.multiselect("Invoices", [i["invoice_id"] for i in pending])
    reason = st.text_input("Hold reason (needed to put on hold)")
    approve, hold = st.columns(2)
    action = None
    if approve.button("Approve", disabled=not chosen):
        action = {"approval_status": "approved"}
    if hold.button("Put on hold", disabled=not chosen or not reason.strip()):
        action = {"approval_status": "on_hold", "hold_reason": reason.strip()}
    if action:
        for invoice_id in chosen:
            r = session.patch(f"{API}/invoices/{invoice_id}", json=action, timeout=20)
            if r.ok:
                st.success(f"{invoice_id}: {action['approval_status']}")
            else:
                st.error(f"{invoice_id}: {r.json().get('error', {}).get('message', r.status_code)}")
        st.button("Refresh the list")

with st.expander("Changes saved under this key"):
    st.json(session.get(f"{API}/me", timeout=20).json())
