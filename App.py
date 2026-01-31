import streamlit as st
import pandas as pd
import urllib.parse

# Configurazione per visualizzazione ottimale su smartphone
st.set_page_config(page_title="Collezionista Audible", layout="centered")

st.title("📚 Hunter Libri Cartacei")
st.write("Compra il libro solo se è su Audible e non lo possiedi già.")

# --- CARICAMENTO DATABASE PERSONALE ---
st.sidebar.header("Il Tuo Archivio")
uploaded_file = st.sidebar.file_uploader("Carica Excel dei tuoi libri", type=["xlsx"])

if uploaded_file:
    try:
        # Carichiamo il database dei libri già posseduti
        df = pd.read_excel(uploaded_file)
        # Normalizzazione nomi colonne
        df.columns = [str(c).strip().lower() for c in df.columns]
        
        # Individuazione colonna Titolo
        col_titolo = next((c for c in df.columns if 'titolo' in c or 'title' in c), None)
        
        if not col_titolo:
            st.error("Il file Excel deve avere una colonna chiamata 'Titolo'.")
        else:
            # INTERFACCIA DI RICERCA AL MERCATINO
            st.subheader("🔍 Verifica Libro")
            libro_input = st.text_input("Titolo del libro che hai trovato:", "").strip()

            if libro_input:
                testo_ricerca = libro_input.lower()
                
                # 1. CONTROLLO POSSESSO
                match_mio = df[df[col_titolo].astype(str).str.lower().str.contains(testo_ricerca, na=False)]

                if not match_mio.empty:
                    st.error(f"🚫 NON COMPRARE: Lo hai già in libreria.")
                    st.info(f"Registrato come: {match_mio.iloc[0][col_titolo].upper()}")
                else:
                    # 2. SE NON LO POSSIEDO, VERIFICO SU AUDIBLE
                    st.warning("⚠️ Non lo possiedi. Verifica se è un titolo Audible:")
                    
                    # Generazione link per ricerca rapida su Audible Italia
                    query_encoded = urllib.parse.quote(libro_input)
                    link_audible = f"https://www.audible.it/search?keywords={query_encoded}"
                    
                    # --- FIX ERRORE QUI ---
                    st.markdown(f"""
                        <div style="background-color: #f9f9f9; padding: 20px; border: 2px solid #ffa500; border-radius: 10px; text-align: center;">
                            <p style="color: #333; font-weight: bold;">CONDIZIONE PER L'ACQUISTO:</p>
                            <p style="font-size: 0.9em; color: #666;">Il libro va comprato solo se esiste la versione audio su Audible.</p>
                            <a href="{link_audible}" target="_blank" style="text-decoration: none;">
                                <div style="background-color: #ffa500; color: white; padding: 12px; border-radius: 5px; font-weight: bold; margin-top: 10px;">
                                    🔎 CERCA SU AUDIBLE
                                </div>
                            </a>
                        </div>
                        """, unsafe_allow_html=True) # <--- CORRETTO DA unsafe_base64 A unsafe_allow_html
                    
                    st.caption("Clicca il tasto arancione: se Audible lo trova, procedi con l'acquisto!")

    except Exception as e:
        st.error(f"Errore tecnico: {e}")
else:
    st.info("Carica il tuo file Excel per iniziare il controllo dei titoli.")
