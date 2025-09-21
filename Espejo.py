import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter, ImageEnhance
import numpy as np
import io
import random
import os

# -------------------------
# Config
# -------------------------
st.set_page_config(page_title="Espejito Místico", page_icon="🪞", layout="centered")

# CSS (fondo texturizado tipo vintage, tipografías y botón)
st.markdown("""
<style>
/* Fondo vintage / marfil */
[data-testid="stAppViewContainer"] {
    background-image: url('https://www.transparenttextures.com/patterns/paper-fibers.png');
    background-color: #fdfcf7;
}

/* Título elegante */
.title {
    font-family: Georgia, 'Times New Roman', serif;
    font-style: italic;
    font-size: 36px;
    color: #5a4635;
    text-align: center;
    margin-bottom: 0.1rem;
}

/* Subtitulo */
.subtitle {
    font-family: Georgia, serif;
    font-size: 16px;
    color: #7a6f5a;
    text-align: center;
    margin-top: 0;
    margin-bottom: 16px;
}

/* Estilo del uploader (estético y legible) */
div.file_uploader_label > label {
    font-weight: 600;
    color: #5a4635;
}
.css-1kyxreq .st-bf {}

/* Personaliza el dropzone (puede variar según versión de streamlit) */
[data-testid="stFileUploaderDropzone"] {
    background: linear-gradient(135deg, #fff8ec, #f6e8d6);
    border-radius: 14px;
    padding: 14px;
    border: 1px solid rgba(0,0,0,0.06);
    box-shadow: 0 4px 14px rgba(0,0,0,0.06);
    color: #4a3a33;
}

/* Botón de descarga */
.stDownloadButton>button {
    background: linear-gradient(135deg, #f0e6d8, #efe3c8);
    color: #3e2f2f;
    border: none;
    padding: 8px 14px;
    border-radius: 10px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# Encabezado
st.markdown('<div class="title">✨ Espejito, espejito refleja mi divinidad ✨</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Sube tu imagen y descubre tu revelación</div>', unsafe_allow_html=True)

# -------------------------
# Frases (lista)
# -------------------------
PHRASES = [
    "No busques tu sonrisa en mis reflejos… yo ya la veo florecer dentro de ti.",
    "El reflejo guarda secretos que tu alma ya conoce.",
    "Tu luz interior es la verdadera respuesta del espejo.",
    "El misterio del reflejo está en tu propia mirada.",
    "Cada brillo es un susurro de tu esencia eterna.",
    "Tu sonrisa interior ilumina incluso lo invisible.",
    "Lo que ves fuera es solo un eco de tu ser.",
    "Hoy el reflejo te recuerda: ya eres suficiente.",
    "En tu mirada habita un jardín de verdades.",
    "La calma que buscas ya vive dentro de ti."
]

# -------------------------
# Helper: detectar bounding box interno transparente de marco.png
# -------------------------
def get_transparent_bbox(alpha_channel, threshold=10):
    """
    Recibe el canal alpha (PIL Image 'L') y devuelve bbox de área transparente (left, upper, right, lower)
    Considera transparente donde alpha <= threshold.
    Si no encuentra transparencia, devuelve None.
    """
    arr = np.array(alpha_channel)
    mask = arr <= threshold
    coords = np.argwhere(mask)
    if coords.size == 0:
        return None
    # coords are (y, x)
    y0, x0 = coords.min(axis=0)
    y1, x1 = coords.max(axis=0)
    return (int(x0), int(y0), int(x1)+1, int(y1)+1)

# -------------------------
# Cargar marco.png (debe estar en la misma carpeta)
# -------------------------
MARCO_PATH = "marco.png"
marco_img = None
if os.path.exists(MARCO_PATH):
    try:
        marco_img = Image.open(MARCO_PATH).convert("RGBA")
    except Exception as e:
        st.warning(f"No se pudo abrir 'marco.png': {e}")
else:
    st.info("Nota: coloca 'marco.png' (PNG con centro transparente) en la carpeta del proyecto para usar el marco realista.")

# Mostrar un espejo vacío (generado) si no hay marco
def crear_espejo_local_sintetico(size=(500,650)):
    W, H = size
    base = Image.new("RGBA", size, (253, 252, 247, 255))  # marfil
    draw = ImageDraw.Draw(base)
    bbox = [40, 40, W-40, H-90]
    # marco blanco-hueso con doble contorno sutil
    draw.ellipse(bbox, outline="#e8e6de", width=16)
    draw.ellipse([bbox[0]+12, bbox[1]+12, bbox[2]-12, bbox[3]-12], outline="#f6f4ef", width=6)
    # texturita interior ligera
    interior = Image.new("RGBA", (bbox[2]-bbox[0], bbox[3]-bbox[1]), (249,246,240,255))
    # aplicar ruido sutil
    noise = Image.effect_noise(interior.size, 10).convert("L")
    interior.putalpha(255)
    interior = Image.composite(interior, Image.new("RGBA", interior.size, (240,235,225,255)), noise)
    base.paste(interior, (bbox[0], bbox[1]), interior)
    return base

# -------------------------
# Uploader (label exactamente como pediste)
# -------------------------
uploaded = st.file_uploader("Sube tu imagen y descubre tu revelación", type=["jpg","jpeg","png"])

# Preview area: siempre mostramos un espejo vacío si no hay imagen
if uploaded is None:
    # si hay marco.png, mostrar marco (sin foto)
    if marco_img:
        # crear lienzo con fondo marfil y pegar marco centrado
        canvas = Image.new("RGBA", (700, 900), (253,252,247,255))
        m_w, m_h = marco_img.size
        pos = ((canvas.width - m_w)//2, 120)
        # crear textura interior si marco tiene transparencia:
        alpha = marco_img.split()[-1]
        bbox = get_transparent_bbox(alpha)
        if bbox:
            # pintar interior con textura marfil
            interior = Image.new("RGBA", (bbox[2]-bbox[0], bbox[3]-bbox[1]), (249,246,240,255))
            # ligero ruido
            noise = Image.effect_noise(interior.size, 8).convert("L")
            interior.putalpha(255)
            interior = Image.composite(interior, Image.new("RGBA", interior.size, (245,240,230,255)), noise)
            canvas.paste(interior, (pos[0]+bbox[0], pos[1]+bbox[1]), interior)
        canvas.paste(marco_img, pos, marco_img)
        st.image(canvas, use_column_width=False, width=420, caption="Tu espejo mágico te espera 🪞")
    else:
        sintetico = crear_espejo_local_sintetico((500,650))
        st.image(sintetico, use_column_width=False, width=420, caption="Tu espejo mágico te espera 🪞")
else:
    # -------------------------
    # Procesar imagen subida
    # -------------------------
    try:
        user_img = Image.open(uploaded).convert("RGBA")
    except Exception as e:
        st.error("No se pudo abrir la imagen. Asegúrate de subir un archivo JPG/PNG válido.")
        st.stop()

    # si tenemos marco.png y su canal alpha define hueco, usamos ese hueco
    if marco_img:
        alpha = marco_img.split()[-1]
        bbox = get_transparent_bbox(alpha)
        if bbox:
            # dimensiones del hueco dentro del marco
            inner_w = bbox[2] - bbox[0]
            inner_h = bbox[3] - bbox[1]
            # escalado proporcional: usar ImageOps.fit para cubrir exactamente inner_w x inner_h sin distorsión
            user_fitted = ImageOps.fit(user_img, (inner_w, inner_h), method=Image.LANCZOS, centering=(0.5,0.45))
            # aplicar filtros suaves
            user_fitted = user_fitted.filter(ImageFilter.GaussianBlur(radius=0.6))
            user_fitted = ImageEnhance.Color(user_fitted).enhance(0.95)
            user_fitted = ImageEnhance.Brightness(user_fitted).enhance(1.02)
            user_fitted = ImageEnhance.Contrast(user_fitted).enhance(0.98)
            # preparar canvas grande
            canvas = Image.new("RGBA", (max(marco_img.width, inner_w+160), max(marco_img.height+120, inner_h+300)), (253,252,247,255))
            pos = ((canvas.width - marco_img.width)//2, 120)
            # crear textura interior y pegarla donde corresponde
            interior = Image.new("RGBA", (inner_w, inner_h), (249,246,240,255))
            noise = Image.effect_noise(interior.size, 8).convert("L")
            interior = Image.composite(interior, Image.new("RGBA", interior.size, (245,240,230,255)), noise)
            canvas.paste(interior, (pos[0]+bbox[0], pos[1]+bbox[1]), interior)
            # pegar foto luego (debajo del marco)
            canvas.paste(user_fitted, (pos[0]+bbox[0], pos[1]+bbox[1]), user_fitted)
            # pegar marco encima
            canvas.paste(marco_img, pos, marco_img)
        else:
            # si no detecta transparencia, usar un fitting en área central
            inner_w, inner_h = min(560, user_img.width), min(720, user_img.height)
            user_fitted = ImageOps.fit(user_img, (inner_w, inner_h), method=Image.LANCZOS, centering=(0.5,0.45))
            user_fitted = user_fitted.filter(ImageFilter.GaussianBlur(radius=0.6))
            canvas = Image.new("RGBA", (700,900), (253,252,247,255))
            pos = ((canvas.width - user_fitted.width)//2, 200)
            canvas.paste(user_fitted, pos, user_fitted)
            # pegar marco centrado (escalado)
            marco_resized = ImageOps.contain(marco_img, (int(user_fitted.width*1.2), int(user_fitted.height*1.2)))
            marco_pos = ((canvas.width - marco_resized.width)//2, pos[1]-20)
            canvas.paste(marco_resized, marco_pos, marco_resized)
    else:
        # si no hay marco.png, usar método sintético: oval interior y marco dibujado
        # definir inner target
        inner_w, inner_h = 360, 480
        user_fitted = ImageOps.fit(user_img, (inner_w, inner_h), Image.LANCZOS, centering=(0.5,0.45))
        user_fitted = user_fitted.filter(ImageFilter.GaussianBlur(radius=0.6))
        canvas = crear_espejo_local_sintetico((700,900)).convert("RGBA")
        pos = ((canvas.width - inner_w)//2, 200)
        # crear máscara oval
        mask = Image.new("L", (inner_w, inner_h), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse([0,0,inner_w,inner_h], fill=255)
        canvas.paste(user_fitted, pos, mask)

    # -------------------------
    # Añadir frase aleatoria sobre la imagen (dentro del área inferior)
    # -------------------------
    frase = random.choice(PHRASES)
    draw = ImageDraw.Draw(canvas)
    # intentar DejaVuSerif-Italic o fallback
    try:
        font = ImageFont.truetype("DejaVuSerif-Italic.ttf", 28)
    except:
        try:
            font = ImageFont.truetype("DejaVuSerif.ttf", 28)
        except:
            font = ImageFont.load_default()

    # calcular posición de texto: justo debajo del marco (o sobre el área inferior)
    margin_bottom = 40
    text_bbox = draw.textbbox((0,0), frase, font=font)
    text_w, text_h = text_bbox[2]-text_bbox[0], text_bbox[3]-text_bbox[1]
    text_x = (canvas.width - text_w)//2
    text_y = canvas.height - text_h - margin_bottom

    # Sombra ligera para legibilidad
    shadow_color = (255,255,255,220)
    draw.text((text_x+1, text_y+1), frase, font=font, fill=shadow_color)
    draw.text((text_x, text_y), frase, font=font, fill=(90,70,60,255))

    # Mostrar el resultado en la app
    st.image(canvas, use_column_width=False, width=420, caption="✨ Tu revelación ✨")

    # -------------------------
    # Descargar (PNG)
    # -------------------------
    buf = io.BytesIO()
    canvas.convert("RGB").save(buf, format="PNG", quality=95)
    buf.seek(0)
    st.download_button("📥 Descargar post (PNG)", data=buf, file_name="post_espejo.png", mime="image/png")

# -------------------------
# Nota: coloca 'marco.png' en la misma carpeta si quieres usar marco realista.
# -------------------------
