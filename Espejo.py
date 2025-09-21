import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os

st.set_page_config(page_title="✨ Espejito mágico ✨", page_icon="✨", layout="centered")

# CSS personalizado para estilo elegante
st.markdown("""
    <style>
    /* Fondo general */
    .stApp {
        background: linear-gradient(135deg, #1a1a1d, #2d2d34);
        color: white;
        font-family: 'Georgia', serif;
    }
    /* Título principal */
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #FFD700;
        text-align: center;
        text-shadow: 2px 2px 4px #000000;
    }
    /* Subtítulo */
    .subtitle {
        font-size: 20px;
        font-style: italic;
        color: #E6E6FA;
        text-align: center;
        margin-top: -10px;
        margin-bottom: 20px;
        text-shadow: 1px 1px 3px #000000;
    }
    /* Botón elegante */
    .stFileUploader {
        background: linear-gradient(135deg, #ffafbd, #ffc3a0);
        border-radius: 15px;
        padding: 12px;
        font-weight: bold;
        text-align: center;
        color: black;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado
st.markdown('<div class="title">✨ Espejito, espejito refleja mi divinidad ✨</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Sube tu imagen y descubre tu revelación</div>', unsafe_allow_html=True)

# Subir imagen
uploaded_file = st.file_uploader("Sube tu imagen", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)

    # Fuente segura
    try:
        font = ImageFont.truetype("arial.ttf", 40)  # Usa Arial
    except:
        font = ImageFont.load_default()

    # Dibujar texto sobre imagen
    draw = ImageDraw.Draw(image)
    frase = "Tu divinidad brilla ✨"
    text_w, text_h = draw.textbbox((0,0), frase, font=font)[2:]
    img_w, img_h = image.size
    x = (img_w - text_w) / 2
    y = img_h - text_h - 20
    draw.text((x, y), frase, font=font, fill="white", stroke_width=2, stroke_fill="black")

    st.image(image, caption="Aquí está tu reflejo ✨", use_column_width=True)
