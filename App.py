import streamlit as st
import pandas as pd
import urllib.parse

# Configurazione della pagina
st.set_page_config(page_title="Hunter Libri Pro", layout="centered")

# --- CONFIGURAZIONE GOOGLE DRIVE ---
FILE_ID = "1toFD8s-pQYppHAp5RSPod6Ad9vnxMw-B"
DIRECT_URL = f'https://drive.google.com/uc?export=download&id={FILE_ID}'

@st.cache_data(ttl=300)
def load_data():
    try:
        df = pd.read_excel(DIRECT_URL)
        df.columns = [str(c).strip().lower() for c in df.columns]
        return df
    except Exception:
        return None

# Caricamento dati
df = load_data()

# --- SIDEBAR ---
st.sidebar.header("📊 Stato Archivio")

if df is not None:
    num_titoli = len(df)
    st.sidebar.metric("Libri registrati", num_titoli)
    st.sidebar.success("✅ Sincronizzato")
    
    col_titolo = next((c for c in df.columns if 'titolo' in c or 'title' in c), None)
    
    # --- AREA PRINCIPALE ---
    st.title("📚 Hunter Libri")
    
    if col_titolo:
        st.subheader("🔍 Verifica Titolo")
        libro_input = st.text_input("Inserisci il nome del libro trovato:", "").strip()

        if libro_input:
            testo_ricerca = libro_input.lower()
            match_mio = df[df[col_titolo].astype(str).str.lower().str.contains(testo_ricerca, na=False)]

            if not match_mio.empty:
                st.error("🚫 NON COMPRARE: Lo hai già in collezione!")
                st.info(f"Trovato come: {match_mio.iloc[0][col_titolo].upper()}")
            else:
                st.warning("⚠️ Non presente nel tuo archivio.")
                st.write("Verifica se esiste su Audible prima di acquistarlo:")
                
                query_encoded = urllib.parse.quote(libro_input)
                link_audible = f"https://www.audible.it/search?keywords={query_encoded}"
                
                # HTML pulito per evitare errori di sintassi
                bottone_html = f"""
                <div style="background-color: #f9f9f9; padding: 20px; border: 2px solid #ffa500; border-radius: 10px; text-align: center;">
                    <p style="color: #333; font-weight: bold;">CONDIZIONE ACQUISTO:</p>
                    <a href="{link_audible}" target="_blank" style="text-decoration: none;">
                        <div style="background-color: #ffa500; color: white; padding: 12px; border-radius: 5px; font-weight: bold; margin-top: 10px;">
                            🔎 CERCA SU AUDIBLE
                        </div>
                    </a>
                </div>
                """
                st.markdown(bottone_html, unsafe_allow_html=True)
    else:
        st.error("Errore: Colonna 'Titolo' non trovata nel file.")
else:
    st.title("📚 Hunter Libri")
    st.error("Errore di connessione a Google Drive. Verifica la condivisione del file.")
