import streamlit as st
import pandas as pd
import urllib.parse

# Configurazione pagina
st.set_page_config(page_title="Collezionista Audible", layout="centered")

# Funzione per caricare i dati e tenerli in memoria (Cache)
@st.cache_data(show_spinner=False)
def load_data(file):
    df = pd.read_excel(file)
    df.columns = [str(c).strip().lower() for c in df.columns]
    return df

st.title("📚 Hunter Libri Cartacei")
st.write("Il file caricato resterà attivo in sessione.")

# --- SIDEBAR PER CARICAMENTO ---
st.sidebar.header("Il Tuo Archivio")
uploaded_file = st.sidebar.file_uploader("Carica Excel dei tuoi libri", type=["xlsx"])

# Se il file è stato caricato, lo salviamo nello stato della sessione
if uploaded_file:
    st.session_state['db_libri'] = load_data(uploaded_file)
    st.sidebar.success("✅ File caricato e memorizzato!")

# --- LOGICA DI RICERCA ---
if 'db_libri' in st.session_state:
    df = st.session_state['db_libri']
    col_titolo = next((c for c in df.columns if 'titolo' in c or 'title' in c), None)

    if col_titolo:
        st.subheader("🔍 Verifica Libro")
        libro_input = st.text_input("Titolo del libro che hai trovato:", "").strip()

        if libro_input:
            testo_ricerca = libro_input.lower()
            match_mio = df[df[col_titolo].astype(str).str.lower().str.contains(testo_ricerca, na=False)]

            if not match_mio.empty:
                st.error(f"🚫 NON COMPRARE: Lo hai già in libreria.")
                st.info(f"Registrato come: {match_mio.iloc[0][col_titolo].upper()}")
            else:
                st.warning("⚠️ Non lo possiedi. Verifica su Audible:")
                query_encoded = urllib.parse.quote(libro_input)
                link_audible = f"https://www.audible.it/search?keywords={query_encoded}"
                
                st.markdown(f"""
                    <div style="background-color: #f9f9f9; padding: 20px; border: 2px solid #ffa500; border-radius: 10px; text-align: center;">
                        <a href="{link_audible}" target="_blank" style="text-decoration: none;">
                            <div style="background-color: #ffa500; color: white; padding: 12px; border-radius: 5px; font-weight: bold;">
                                🔎 CERCA SU AUDIBLE
                            </div>
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.error("Colonna 'Titolo' non trovata nell'Excel.")
else:
    st.info("Carica il tuo file Excel una volta per iniziare. Finché l'app è aperta nel browser, non dovrai ricaricarlo.")
