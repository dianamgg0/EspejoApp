import streamlit as st
from PIL import Image, ImageDraw, ImageFont

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
        font-size: 38px;
        font-weight: bold;
        color: #5a4635; /* marrón suave */
        text-align: center;
        text-shadow: 1px 1px 3px #ffffff;
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
    .stFileUploader {
        background: linear-gradient(135deg, #ffffff, #f5f5f5);
        border-radius: 15px;
        padding: 12px;
        font-weight: bold;
        text-align: center;
        color: #444;
        border: 1px solid #ddd;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.08);
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado
st.markdown('<div class="title">✨ Espejito, espejito refleja mi divinidad ✨</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Sube tu imagen y descubre tu revelación</div>', unsafe_allow_html=True)

# --- Función para crear espejo vacío con marco más realista ---
def crear_espejo_vacio():
    img = Image.new("RGB", (500, 650), (253, 252, 247))  # fondo marfil
    draw = ImageDraw.Draw(img)
    bbox = [40, 40, 460, 560]  # límites del óvalo

    # Marco más elegante con grosor doble
    draw.ellipse(bbox, outline="#e6e2d9", width=18)  # borde externo hueso
    draw.ellipse([50, 50, 450, 550], outline="#f5f2eb", width=6)  # borde interno claro

    return img

# Mostrar espejo vacío inicialmente
if "inicial" not in st.session_state:
    st.session_state["inicial"] = True

uploaded_file = st.file_uploader("🪞 Sube tu imagen", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.session_state["inicial"] = False
    image = Image.open(uploaded_file).convert("RGBA")

    # Ajustar tamaño conservando proporción (sin deformar)
    max_width, max_height = 360, 480
    image.thumbnail((max_width, max_height))

    # Crear máscara ovalada
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse([0, 0, image.size[0], image.size[1]], fill=255)

    # Recortar imagen en forma ovalada
    img_oval = Image.new("RGBA", image.size)
    img_oval.paste(image, (0, 0), mask=mask)

    # Crear fondo con marco
    espejo = crear_espejo_vacio().convert("RGBA")
    x_offset = (espejo.size[0] - image.size[0]) // 2
    y_offset = (espejo.size[1] - image.size[1]) // 2 - 20
    espejo.paste(img_oval, (x_offset, y_offset), img_oval)

    # Texto de revelación
    draw = ImageDraw.Draw(espejo)
    try:
        font = ImageFont.truetype("DejaVuSerif-Italic.ttf", 28)
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
