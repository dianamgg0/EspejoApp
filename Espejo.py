import streamlit as st
import random

# Lista de frases
frases = [
    "La belleza está en los detalles más simples.",
    "Sonríe, es gratis y poderoso.",
    "Cada día es una nueva oportunidad.",
    "El silencio también habla.",
    "Menos es más.",
    "La elegancia está en la sencillez.",
    "Todo fluye, nada permanece.",
    "El presente es lo único real.",
    "La calma es la nueva riqueza.",
    "Respira, todo está bien."
]

# Configuración de la página
st.set_page_config(page_title="Frases Elegantes", page_icon="✨", layout="centered")

# Estilo blanco y elegante
st.markdown(
    """
    <style>
    body {
        background-color: white;
        color: black;
        font-family: "Helvetica Neue", sans-serif;
        text-align: center;
    }
    .stButton button {
        background-color: black;
        color: white;
        border-radius: 12px;
        padding: 8px 20px;
        font-size: 16px;
    }
    .stButton button:hover {
        background-color: #444;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título
st.title("✨ Frases Minimalistas ✨")

# Mostrar imagen
st.image("cf45ae96-3759-4d93-8b30-3b261a036df9.png", use_container_width=True)

# Mostrar frase aleatoria
if "frase" not in st.session_state:
    st.session_state.frase = random.choice(frases)

st.markdown(f"### {st.session_state.frase}")

# Botón para cambiar frase
if st.button("Cambiar frase ✨"):
    st.session_state.frase = random.choice(frases)
    st.experimental_rerun()
