import streamlit as st
from supabase import Client, create_client


def _get_required_secret(name: str) -> str:
    value = st.secrets.get(name)
    if not value:
        st.error(
            f"{name} is missing. Add it in .streamlit/secrets.toml locally "
            "and in Streamlit Cloud app secrets for deployment."
        )
        raise RuntimeError(f"Missing Streamlit secret: {name}")
    return str(value)


@st.cache_resource(show_spinner=False)
def get_supabase_client() -> Client:
    """Return a shared client, recreated by reset_supabase_client after failures."""
    url = _get_required_secret("SUPABASE_URL")
    key = _get_required_secret("SUPABASE_KEY")
    return create_client(url, key)


def reset_supabase_client() -> Client:
    get_supabase_client.clear()
    return get_supabase_client()
