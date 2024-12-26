import streamlit as st
import os
from PIL import Image
import pytesseract
import io
import base64
from gtts import gTTS

# إعداد الصفحة
st.set_page_config(page_title="تحويل النصوص إلى كلام واستخراج النصوص", layout="wide")

# CSS لتنسيق الصفحة
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
    .header-text {
        text-align: right;
        font-weight: bold;
        font-size: 20px;
        margin-bottom: 20px;
    }
    .button-container {
        display: flex;
        justify-content: flex-end;
        width: 100%;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .stButton>button {
        display: block;
        margin-right: 0;
        margin-left: auto;
        min-width: 150px;
        max-width: 300px;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 5px;
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
    .download-button {
        display: inline-block;
        text-decoration: none;
        background-color: #2A2630;
        color: white;
        padding: 10px 20px;
        font-size: 16px;
        border: none;
        border-radius: 5px;
        text-align: center;
        cursor: pointer;
    }
    .download-button:hover {
        background-color: #3B3644;
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

# الشريط الجانبي
with st.sidebar:
    st.image("logo-1-1.png", use_container_width=True)
    st.markdown("<div class='header-text'>تطبيق RMG المزود بالذكاء الاصطناعي</div>", unsafe_allow_html=True)
    operation = st.radio("اختر نوع العملية :", ("تحويل النص إلى صوت", "استخراج النصوص من الصور", "استخراج جميع النصوص من الصور في المجلد"))

# وظيفة تحويل النص إلى كلام
if operation == "تحويل النص إلى صوت":
    st.markdown("<h1 class='rtl-text'>تحويل النص إلى صوت</h1>", unsafe_allow_html=True)
    arabic_text = st.text_area("اكتب النص هنا:", height=200)

    if st.button("تشغيل الصوت"):
        try:
            if arabic_text.strip():
                # إنشاء ملف صوتي
                tts = gTTS(arabic_text, lang='ar')
                mp3_fp = io.BytesIO()
                tts.write_to_fp(mp3_fp)
                mp3_fp.seek(0)

                # تحويل الصوت إلى صيغة base64 لتضمينها في HTML
                mp3_base64 = base64.b64encode(mp3_fp.read()).decode('utf-8')
                audio_html = f"""
                <audio controls autoplay>
                    <source src="data:audio/mp3;base64,{mp3_base64}" type="audio/mp3">
                </audio>
                """
                st.markdown(audio_html, unsafe_allow_html=True)
                st.success("تم تشغيل الصوت بنجاح!")
            else:
                st.warning("الرجاء إدخال نص.")
        except Exception as e:
            st.error(f"حدث خطأ أثناء تشغيل الصوت: {e}")

# وظائف أخرى حسب الاختيار
elif operation == "استخراج النصوص من الصور":
    st.markdown("<h1 class='rtl-text'>استخراج النصوص من الصور</h1>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("اختر صورة:", type=["png", "jpg", "jpeg", "webp"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="الصورة المحملة", use_container_width=True)

        with st.spinner("جاري تحليل النصوص..."):
            try:
                text = pytesseract.image_to_string(image, lang='ara+eng')
                text = text.strip()
                if not text:
                    st.warning("لم يتم العثور على أي نص في الصورة.")
                    st.stop()
            except pytesseract.TesseractNotFoundError:
                st.error("لم يتم العثور على Tesseract. تأكد من تثبيته وإضافة مساره بشكل صحيح.")
                st.stop()
            except Exception as e:
                st.error(f"حدث خطأ أثناء تحليل الصورة: {e}")
                st.stop()

        # عرض النص المكتشف مع إطار
        st.markdown("<div class='rtl-label'>النص المكتشف:</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='text-container'>{text}</div>", unsafe_allow_html=True)

elif operation == "استخراج جميع النصوص من الصور في المجلد":
    st.markdown("<h1 class='rtl-text'>استخراج النصوص من جميع الصور في المجلد</h1>", unsafe_allow_html=True)
    # يمكن إضافة المزيد من التفاصيل هنا حسب الحاجة.
