import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps

st.set_page_config(page_title="✨ Espejito mágico ✨", page_icon="✨", layout="centered")

# CSS personalizado
st.markdown("""
    <style>
    .stApp {
        background: url('https://www.transparenttextures.com/patterns/paper-fibers.png');
        background-color: #fdfcf7; /* tono marfil claro */
        color: #333;
        font-family: 'Georgia', serif;
    }
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #5a4635;
        text-align: center;
        text-shadow: 1px 1px 2px #ffffff;
    }
    .subtitle {
        font-size: 20px;
        font-style: italic;
        color: #7a6f5a;
        text-align: center;
        margin-top: -10px;
        margin-bottom: 20px;
    }
    /* Botón elegante */
    .stFileUploader label div[data-testid="stFileUploaderDropzone"] {
        background: linear-gradient(135deg, #fff8e7, #f2e1c6);
        border-radius: 20px;
        padding: 15px;
        border: 2px solid #d4af37; /* dorado */
        box-shadow: 2px 2px 8px rgba(0,0,0,0.15);
        font-weight: bold;
        color: #5a4635;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado
st.markdown('<div class="title">✨ Espejito, espejito refleja mi divinidad ✨</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Sube tu imagen y descubre tu revelación</div>', unsafe_allow_html=True)

# --- Función para crear espejo vacío con marco dorado ---
def crear_espejo_vacio():
    img = Image.new("RGB", (500, 600), (253, 252, 247))  # fondo marfil
    draw = ImageDraw.Draw(img)

    bbox = [40, 40, 460, 560]  # marco ovalado

    # Capa dorada (imitando realismo con varios anillos)
    for i, color in enumerate(["#d4af37", "#f5deb3", "#d4af37"]):
        offset = i * 4
        draw.ellipse(
            [bbox[0]-offset, bbox[1]-offset, bbox[2]+offset, bbox[3]+offset],
            outline=color, width=6
        )

    # Textura dentro del óvalo (sutil)
    interior = Image.new("RGB", (420, 520), "#fdfaf3")
    texture = ImageOps.colorize(Image.new("L", (20, 20), 128), "#fefefe", "#eae4d3")
    for y in range(0, interior.size[1], 20):
        for x in range(0, interior.size[0], 20):
            interior.paste(texture, (x, y))

    img.paste(interior, (40, 40))
    return img

# Mostrar espejo vacío inicialmente
if "inicial" not in st.session_state:
    st.session_state["inicial"] = True

uploaded_file = st.file_uploader("🪞 Sube tu imagen", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.session_state["inicial"] = False
    image = Image.open(uploaded_file).convert("RGBA")

    # ✅ Mantener proporción al ajustar tamaño
    image.thumbnail((400, 500), Image.LANCZOS)

    # Crear máscara ovalada
    mask = Image.new("L", (image.size[0], image.size[1]), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse([0, 0, image.size[0], image.size[1]], fill=255)

    # Recortar imagen en forma ovalada
    img_oval = Image.new("RGBA", image.size)
    img_oval.paste(image, (0, 0), mask=mask)

    # Crear fondo con marco
    espejo = crear_espejo_vacio().convert("RGBA")

    # Centrar la imagen dentro del óvalo
    x = (espejo.size[0] - image.size[0]) // 2
    y = (espejo.size[1] - image.size[1]) // 2
    espejo.paste(img_oval, (x, y), img_oval)

    # Texto de revelación
    draw = ImageDraw.Draw(espejo)
    try:
        font = ImageFont.truetype("arial.ttf", 28)
    except:
        font = ImageFont.load_default()

    frase = "✨ Tu divinidad brilla ✨"
    text_w, text_h = draw.textbbox((0,0), frase, font=font)[2:]
    img_w, img_h = espejo.size
    x = (img_w - text_w) / 2
    y = img_h - text_h - 20
    draw.text((x, y), frase, font=font, fill="#5a4635", stroke_width=1, stroke_fill="#ffffff")

    st.image(espejo, caption="Aquí está tu reflejo ✨", use_column_width=True)
else:
    espejo_vacio = crear_espejo_vacio()
    st.image(espejo_vacio, caption="Tu espejo mágico te espera 🪞", use_column_width=True)
