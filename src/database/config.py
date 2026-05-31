try:
    import streamlit as st  # type: ignore[import]
except ImportError:
    from types import SimpleNamespace
    st = SimpleNamespace(
        write=lambda *args, **kwargs: None,
        error=lambda *args, **kwargs: None,
        secrets={},
    )

st.write("Config loading...")

try:
    from supabase import create_client, Client  # type: ignore[import]
    st.write("Supabase import OK")
except Exception:
    try:
        from supabase_py import create_client, Client  # type: ignore[import]
        st.write("Supabase_py import OK")
    except Exception as e:
        st.error(f"Import error: {repr(e)}")
        raise

try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    st.write("Secrets found")
except Exception as e:
    st.error(f"Secrets error: {repr(e)}")
    raise

supabase: Client = create_client(url, key)
st.write("Client created")