import streamlit as st
import os
from PIL import Image
import pytesseract
import io
import base64
from gtts import gTTS

st.set_page_config(page_title="برنامج RMG المزود بالذكاء الاصطناعي", layout="wide")

st.markdown(
    """
    <style>
    body {
        direction: rtl;
        font-family: 'Arial', sans-serif;
    }
    .rtl-text {
        text-align: right;
        font-size: 18px;
        line-height: 1.8;
        margin-bottom: 20px;
        white-space: pre-wrap;
    }
    .rtl-label {
        text-align: right;
        font-weight: bold;
        font-size: 20px;
    }
    .text-container {
        border: 2px solid #2A2630;
        border-radius: 10px;
        padding: 15px;
        background-color: #f8f9fa;
        color: #2A2630;
        font-size: 16px;
        line-height: 1.6;
        direction: rtl;
        text-align: right;
        white-space: pre-wrap;
        margin-top: 20px;
    }
    audio {
        display: block;
        margin-top: 10px;
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.image("logo-1-1.png", use_container_width=True)
    st.markdown("<div style='text-align: right; font-size: 20px; font-weight: bold;'>تطبيق RMG المزود بالذكاء الاصطناعي</div>", unsafe_allow_html=True)
    operation = st.radio(
        "اختر نوع العملية:", 
        ("تحويل النص إلى صوت", "استخراج النصوص من الصور", "استخراج جميع النصوص من الصور في المجلد")
    )

if "audio_base64" not in st.session_state:
    st.session_state.audio_base64 = None
if "audio_playing" not in st.session_state:
    st.session_state.audio_playing = False

if operation == "تحويل النص إلى صوت":
    st.markdown("<h1 class='rtl-text'>تحويل النص إلى صوت</h1>", unsafe_allow_html=True)
    arabic_text = st.text_area("اكتب النص هنا:", height=200)

    if st.button("تشغيل الصوت"):
        if not st.session_state.audio_playing:
            if arabic_text.strip():
                try:
                    tts = gTTS(arabic_text, lang='ar')
                    mp3_fp = io.BytesIO()
                    tts.write_to_fp(mp3_fp)
                    mp3_fp.seek(0)
                    st.session_state.audio_base64 = base64.b64encode(mp3_fp.read()).decode('utf-8')
                    st.session_state.audio_playing = True
                    st.success("تم تشغيل الصوت!")
                except Exception as e:
                    st.error(f"حدث خطأ أثناء تشغيل الصوت: {e}")
            else:
                st.warning("الرجاء إدخال نص.")
        else:
            st.warning("الصوت قيد التشغيل بالفعل.")

    if st.button("إيقاف الصوت"):
        if st.session_state.audio_playing:
            st.session_state.audio_playing = False
            st.success("تم إيقاف الصوت!")
        else:
            st.warning("لا يوجد صوت قيد التشغيل.")

    if st.session_state.audio_base64 and st.session_state.audio_playing:
        audio_html = f"""
        <audio controls autoplay>
            <source src="data:audio/mp3;base64,{st.session_state.audio_base64}" type="audio/mp3">
        </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)

elif operation == "استخراج النصوص من الصور":
    st.markdown("<h1 class='rtl-text'>استخراج النصوص من الصور</h1>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("اختر صورة:", type=["png", "jpg", "jpeg", "webp"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="الصورة المحملة", use_container_width=True)

        with st.spinner("جاري تحليل النصوص..."):
            try:
                text = pytesseract.image_to_string(image, lang='ara+eng').strip()
                if not text:
                    st.warning("لم يتم العثور على أي نص في الصورة.")
                    st.stop()
            except Exception as e:
                st.error(f"حدث خطأ أثناء تحليل الصورة: {e}")
                st.stop()

        st.markdown("<div class='rtl-label'>النص المكتشف:</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='text-container'>{text}</div>", unsafe_allow_html=True)

elif operation == "استخراج جميع النصوص من الصور في المجلد":
    st.markdown("<h1 class='rtl-text'>استخراج النصوص من الصور في المجلد</h1>", unsafe_allow_html=True)
    folder_path = st.text_input("أدخل مسار المجلد:")

    if st.button("استخراج النصوص"):
        if folder_path.strip() and os.path.isdir(folder_path):
            output_texts = {}
            with st.spinner("جاري تحليل النصوص من الصور..."):
                try:
                    for file_name in os.listdir(folder_path):
                        if file_name.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                            file_path = os.path.join(folder_path, file_name)
                            image = Image.open(file_path)
                            text = pytesseract.image_to_string(image, lang='ara+eng').strip()
                            output_texts[file_name] = text

                    if output_texts:
                        st.success("تم استخراج النصوص بنجاح!")
                        for file_name, text in output_texts.items():
                            st.markdown(f"<div class='rtl-label'>النص من الصورة: {file_name}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='text-container'>{text}</div>", unsafe_allow_html=True)
                    else:
                        st.warning("لم يتم العثور على أي صور صالحة في المجلد.")

                except Exception as e:
                    st.error(f"حدث خطأ أثناء تحليل الصور: {e}")
        else:
            st.warning("الرجاء إدخال مسار مجلد صحيح.")
