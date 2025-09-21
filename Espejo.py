import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import io
import numpy as np

# --- Configuración de la página ---
st.set_page_config(page_title="Espejito App", page_icon="🪞", layout="centered")

# --- Título ---
st.title("✨ Espejito, espejito refleja mi divinidad ✨")

# --- Lista de frases ---
frases = [
    "No busques tu sonrisa en mis reflejos… yo ya la veo florecer dentro de ti.",
    "Eres más radiante de lo que imaginas.",
    "Tu luz interior ilumina más que mil soles.",
    "En ti ya habita la belleza que buscas.",
    "Tu esencia brilla en cada reflejo.",
    "El amor propio es tu espejo más fiel.",
    "Tu divinidad se revela en tu mirada.",
    "La magia que ves afuera nace en tu interior.",
    "Eres un reflejo perfecto de la creación.",
    "Dentro de ti ya florece todo lo que necesitas."
]

# --- Subir imagen ---
uploaded_file = st.file_uploader("Sube tu imagen y descubre tu revelación", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Cargar imagen
    image = Image.open(uploaded_file).convert("RGBA")

    # Aplicar un filtro suave
    image = image.filter(ImageFilter.SMOOTH_MORE)

    # Crear fondo beige con textura ligera
    bg_w, bg_h = image.width + 200, image.height + 300
    beige = np.ones((bg_h, bg_w, 3), dtype=np.uint8) * [235, 225, 210]  # Beige claro
    noise = np.random.normal(0, 8, beige.shape).astype(np.int16)
    textured = np.clip(beige + noise, 0, 255).astype(np.uint8)
    background = Image.fromarray(textured, "RGB").convert("RGBA")

    # Crear marco blanco simple
    marco = Image.new("RGBA", (image.width + 40, image.height + 40), (255, 255, 255, 255))
    marco.paste(image, (20, 20), image)

    # Pegar marco en el centro del fondo
    x = (bg_w - marco.width) // 2
    y = 60
    background.paste(marco, (x, y), marco)

    # Seleccionar una frase aleatoria
    frase = random.choice(frases)

    # Dibujar texto
    draw = ImageDraw.Draw(background)
    try:
        font = ImageFont.truetype("arial.ttf", 36)  # Windows
    except:
        font = ImageFont.load_default()

    text_w, text_h = draw.textsize(frase, font=font)
    text_x = (background.width - text_w) // 2
    text_y = y + marco.height + 40
    draw.text((text_x, text_y), frase, font=font, fill=(60, 50, 40, 255))

    # Mostrar imagen final
    st.image(background, caption="✨ Tu revelación ✨", use_column_width=True)

    # Descargar imagen como botón
    buf = io.BytesIO()
    background.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="📥 Descargar tu revelación",
        data=byte_im,
        file_name="revelacion.png",
        mime="image/png"
    )
