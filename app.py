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
    st.subheader("Escribe aquí el texto que gustarías escuchar")

try:
    os.mkdir("temp")
except:
    pass

st.subheader("Una pequeña prueba. Copia y pega el siguiente texto")
st.write(
    "Humpty Dumpty se sentó en un muro,"
    "Humpty Dumpty tuvo una gran caída,"
    "Ni todos los caballos del rey ni todos los hombres del rey"
    "pudieron reconstruir a Humpty"
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
