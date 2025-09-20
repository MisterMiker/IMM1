import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

# === Estilos personalizados ===
st.markdown(
    """
    <style>
        body {
            background-color: #a4ac86;
            color: #582f0e;
        }
        .stApp {
            background-color: #a4ac86;
            color: #582f0e;
        }
        h1, h2, h3, h4, h5, h6, p, label, div {
            color: #582f0e !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Conversión de Texto a Audio")
image = Image.open('ddhm0xw-fa233b3f-cda4-4c62-981c-6527ea36ac73.png')
st.image(image, width=350)

with st.sidebar:
    st.subheader("Escribe y/o selecciona texto para ser escuchado.")

try:
    os.mkdir("temp")
except:
    pass

st.subheader("Una pequeña Fábula.")
st.write(
    '¡Ay! -dijo el ratón-. El mundo se hace cada día más pequeño. Al principio era tan grande que le tenía miedo. '
    'Corría y corría y por cierto que me alegraba ver esos muros, a diestra y siniestra, en la distancia. '
    'Pero esas paredes se estrechan tan rápido que me encuentro en el último cuarto y ahí en el rincón está '
    'la trampa sobre la cual debo pasar. Todo lo que debes hacer es cambiar de rumbo dijo el gato... y se lo comió. '
    'Franz Kafka.'
)

st.markdown("¿Quieres escucharlo?, copia el texto")
text = st.text_area("Ingrese el texto a escuchar.")

option_lang = st.selectbox("Selecciona el lenguaje", ("Español", "English"))
lg = "es" if option_lang == "Español" else "en"

def text_to_speech(text, lg):
    tts = gTTS(text, lang=lg)
    try:
        my_file_name = text[0:20].strip().replace(" ", "_")
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, text

if st.button("Convertir a Audio"):
    if text.strip():
        result, output_text = text_to_speech(text, lg)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.markdown("## Tu audio:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

        with open(f"temp/{result}.mp3", "rb") as f:
            data = f.read()

        def get_binary_file_downloader_html(bin_file, file_label="File"):
            bin_str = base64.b64encode(data).decode()
            href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">⬇️ Descargar {file_label}</a>'
            return href

        st.markdown(get_binary_file_downloader_html(f"temp/{result}.mp3", file_label="Audio"), unsafe_allow_html=True)
    else:
        st.warning("⚠️ Por favor ingresa un texto para convertir.")

def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)

remove_files(7)
