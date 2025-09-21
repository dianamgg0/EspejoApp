import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import io

# --- Fondo de la app ---
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f5f0e6;
    background-image: url("https://www.transparenttextures.com/patterns/paper-fibers.png");
    background-size: cover;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# --- Título elegante ---
st.markdown(
    """
    <h1 style='text-align: center; 
               font-family: "Georgia", "Times New Roman", serif; 
               font-style: italic; 
               font-size: 42px; 
               color: #4b3832;'>
        ✨ Espejito, espejito refleja mi divinidad ✨
    </h1>
    """,
    unsafe_allow_html=True
)

st.write("### Sube tu imagen y descubre tu revelación")

# --- Frases ---
frases = [
    "No busques tu sonrisa en mis reflejos… yo ya la veo florecer dentro de ti.",
    "En cada mirada descubres la luz que siempre ha estado en tu interior.",
    "El reflejo es solo un eco de tu verdadera esencia.",
    "Tus ojos ya saben el secreto que tu corazón susurra.",
    "El espejo no inventa, solo te recuerda quién eres.",
    "Tu divinidad brilla más allá de cualquier reflejo.",
    "El misterio que buscas ya habita en ti.",
    "La paz que anhelas se refleja en tu propia mirada.",
    "El espejo te sonríe porque reconoce tu luz.",
    "Dentro de ti florece el jardín de tu verdad."
]

# --- Subir imagen ---
uploaded_file = st.file_uploader("Sube tu imagen", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    imagen = Image.open(uploaded_file).convert("RGB")

    # --- Filtro suave ---
    imagen = imagen.filter(ImageFilter.SMOOTH)

    # --- Redimensionar ---
    imagen = imagen.resize((500, 600))

    # --- Fondo beige con textura ---
    fondo = Image.new("RGB", (600, 800), (245, 240, 230))

    # --- Pegar foto ---
    fondo.paste(imagen, (50, 80))

    # --- Dibujar marco ---
    draw = ImageDraw.Draw(fondo)
    draw.rectangle([(45, 75), (555, 685)], outline=(90, 70, 60), width=8)

    # --- Frase aleatoria ---
    frase = random.choice(frases)
    font = ImageFont.truetype("DejaVuSerif-Italic.ttf", 22)

    # Centrar frase
    text_w, text_h = draw.textbbox((0, 0), frase, font=font)[2:]
    x = (600 - text_w) // 2
    y = 720
    draw.text((x, y), frase, fill=(60, 45, 40), font=font)

    # --- Mostrar imagen ---
    st.image(fondo, caption="✨ Tu revelación ✨", use_column_width=True)

    # --- Descargar imagen ---
    buf = io.BytesIO()
    fondo.save(buf, format="PNG")
    byte_im = buf.getvalue()
    st.download_button(
        label="📥 Descargar tu post",
        data=byte_im,
        file_name="revelacion.png",
        mime="image/png"
    )
