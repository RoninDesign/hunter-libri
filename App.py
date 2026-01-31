import streamlit as st
import pandas as pd
import urllib.parse

# Configurazione della pagina per l'uso da smartphone
st.set_page_config(page_title="Hunter Libri Pro", layout="centered")

# --- CONFIGURAZIONE GOOGLE DRIVE ---
# ID estratto dal tuo link
FILE_ID = "1toFD8s-pQYppHAp5RSPod6Ad9vnxMw-B"
DIRECT_URL = f'https://drive.google.com/uc?export=download&id={FILE_ID}'

@st.cache_data(ttl=300) # Ricarica i dati dal Drive ogni 5 minuti
def load_data():
    try:
        # Lettura del file Excel direttamente da Google Drive
        df = pd.read_excel(DIRECT_URL)
        # Pulizia nomi colonne: tutto minuscolo e senza spazi
        df.columns = [str(c).strip().lower() for c in df.columns]
        return df
    except Exception as e:
        return None

# Caricamento dati
df = load_data()

# --- SIDEBAR (Colonna Sinistra) ---
st.sidebar.header("📊 Stato Archivio")

if df is not None:
    # Conteggio dei titoli presenti nell'Excel
    num_titoli = len(df)
    st.sidebar.metric("Libri registrati", num_titoli)
    st.sidebar.success("✅ Database sincronizzato")
    
    # Identificazione colonna Titolo
    col_titolo = next((c for c in df.columns if 'titolo' in c or 'title' in c), None)
    
    # --- AREA PRINCIPALE ---
    st.title("📚 Hunter Libri")
    
    if col_titolo:
        st.subheader("🔍 Verifica Titolo")
        libro_input = st.text_input("Inserisci il nome del libro trovato:", "").strip()

        if libro_input:
            testo_ricerca = libro_input.lower()
            # Controllo se il titolo è già presente nel tuo Excel
            match_mio = df[df[col_titolo].astype(str).str.lower().str.contains(testo_ricerca, na=False)]

            if not match_mio.empty:
                # SE LO HAI GIÀ
                st.error(f"🚫 NON COMPRARE: Lo hai già in collezione!")
                st.info(f"Trovato come: **{match_mio.iloc[0][col_titolo].upper()}**")
            else:
                # SE NON LO HAI
                st.warning("⚠️ Non presente
