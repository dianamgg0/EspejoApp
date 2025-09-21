import streamlit as st
from PIL import Image, ImageOps, ImageDraw, ImageFont
import random
import io

# Lista de frases
FRASES = [
    "Tu divinidad brilla ✨",
    "El reflejo eres tú 🌸",
    "La luz que buscas ya habita en ti 💫",
    "Tu sonrisa interior florece 🌼",
    "El espejo canta tu verdad 🎶",
    "Eres belleza en cada reflejo 🌹",
    "Tu ser irradia armonía 🌟",
    "Eres más de lo que ves 🪞",
    "Dentro de ti todo ya existe 🌙",
    "Tu esencia ilumina el espejo 🔮"
]

# Configuración de la app
st.set_page_config(page_title="Espejito", page_icon="✨", layout="centered")

# Fondo beige con estilo
st.markdown("""
    <style>
        body {
            background-color: #f9f5f0;
        }
        .stButton>button {
            background-color: #e6dacd;
            color: #3e2f2f;
            border: none;
            border-radius: 12px;
            padding: 0.6em 1.2em;
            font-size: 1em;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #d8c7b8;
        }
    </style>
""", unsafe_allow_html=True)

# Título elegante
st.markdown("<h1 style='text-align: center; color:#3e2f2f;'>✨ Espejito, espejito refleja mi divinidad ✨</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color:#6e5d4c; font-style: italic;'>Sube tu imagen y descubre tu revelación</p>", unsafe_allow_html=True)

# Subida de imagen
uploaded_file = st.file_uploader("📂 Sube tu imagen", type=["jpg", "jpeg", "png"])

# Marco PNG elegante (debe estar en la carpeta del proyecto con fondo transparente)
try:
    marco = Image.open("marco.png").convert("RGBA")
except:
    marco = None
    st.warning("⚠️ No se encontró el archivo 'marco.png'. Cárgalo en la carpeta del proyecto.")

if uploaded_file is not None:
    # Abrir y preparar imagen subida
    user_img = Image.open(uploaded_file).convert("RGBA")
    user_img.thumbnail((800, 800), Image.LANCZOS)  # Mantener proporciones

    # Crear máscara ovalada
    mask = Image.new("L", user_img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse([(0, 0), user_img.size], fill=255)
    user_img = ImageOps.fit(user_img, user_img.size, centering=(0.5, 0.5))
    user_img.putalpha(mask)

    # Crear lienzo beige con textura ligera
    bg = Image.new("RGBA", (1000, 1200), (249, 245, 240, 255))

    # Insertar imagen centrada
    user_pos = ((bg.width - user_img.width) // 2, 250)
    bg.paste(user_img, user_pos, user_img)

    # Colocar marco si existe
    if marco:
        marco_resized = marco.resize((user_img.width+80, user_img.height+80), Image.LANCZOS)
        marco_pos = ((bg.width - marco_resized.width) // 2, 240)
        bg.paste(marco_resized, marco_pos, marco_resized)

    # Elegir frase aleatoria
    frase = random.choice(FRASES)

    # Escribir frase elegante
    draw = ImageDraw.Draw(bg)
    font = ImageFont.truetype("DejaVuSerif-Italic.ttf", 32)
    text_w, text_h = draw.textbbox((0, 0), frase, font=font)[2:]
    draw.text(((bg.width - text_w) // 2, 1100), frase, font=font, fill="#3e2f2f")

    # Mostrar resultado
    st.image(bg, use_container_width=True)

    # Botón de descarga
    buf = io.BytesIO()
    bg.save(buf, format="PNG")
    byte_im = buf.getvalue()
    st.download_button("⬇️ Descargar mi post", data=byte_im, file_name="espejito.png", mime="image/png")

else:
    st.info("✨ Sube una imagen para ver tu reflejo ✨")
