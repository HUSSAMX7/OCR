import streamlit as st
import os
from PIL import Image, ExifTags
from PIL import Image
import pytesseract
import io
import base64
from gtts import gTTS
import pygame

st.set_page_config(page_title="استخراج النص من الصور", layout="wide")
# تحديد مسار Tesseract
#pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# CSS  
# إعداد الصفحة
st.set_page_config(page_title="تحويل النصوص إلى كلام واستخراج النصوص", layout="wide")
# CSS لتنسيق الصفحة
st.markdown(
    """
    <style>
    body {
        direction: rtl; /* اتجاه الصفحة بالكامل */
        font-family: 'Arial', sans-serif; /* خط افتراضي (يمكن تغييره) */
        direction: rtl;
        font-family: 'Arial', sans-serif;
    }
    .rtl-text {
        text-align: right;
@@ -35,7 +41,7 @@
    }
    .button-container {
        display: flex;
        justify-content: flex-end; /* محاذاة الأزرار لليمين */
        justify-content: flex-end;
        width: 100%;
        margin-top: 20px;
        margin-bottom: 20px;
        font-size: 16px;
        border-radius: 5px;
    }
    .stSuccess, .stWarning, .stError {
        direction: rtl;
        text-align: center;
        width: 100%;
        margin-top: 10px;
    }
    .stSuccess > div, .stWarning > div, .stError > div {
        max-width: 500px;
        text-align: center;
        padding: 10px;
        border-radius: 5px;
    }
    .stSuccess > div {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .stWarning > div {
        background-color: #fff3cd;
        color: #856404;
        border: 1px solid #ffeeba;
    }
    .stError > div {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    .stRadio > div {
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
    .stRadio label {
        direction: rtl;
        margin-right: 1em;
    }
    .stRadio > div > div {
        display: inline-flex;
        align-items: center;
        margin-left: 1em;
    }
    .stTextInput > div > div > input, .stNumberInput > div > div > input {
        direction: rtl;
        text-align: right;
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
    .stTextArea > div > div > textarea {
        direction: rtl;
        text-align: right;
    .download-button:hover {
        background-color: #3B3644;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Function to correct image orientation
def correct_image_orientation(image):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = image._getexif()
        if exif is not None:
            orientation_value = exif.get(orientation)
            if orientation_value == 3:
                image = image.rotate(180, expand=True)
            elif orientation_value == 6:
                image = image.rotate(270, expand=True)
            elif orientation_value == 8:
                image = image.rotate(90, expand=True)
    except Exception:
        pass  # Ignore errors if EXIF data is not available
    return image
# Sidebar
# الشريط الجانبي
with st.sidebar:
    st.image("logo-1-1.png", use_container_width=True)  # Replace with the correct path to your image
    #st.image("C:/Users/USER/Desktop/logo-1-1.png", use_container_width=True)
    st.markdown("<div class='header-text'>تطبيق RMG المزود بالذكاء الاصطناعي</div>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    operation = st.radio("اختر نوع العملية :", ("استخراج نص من صورة", "استخراج جميع النصوص من الصور في المجلد"))
    operation = st.radio("اختر نوع العملية :", ("تحويل النص إلى صوت", "استخراج النصوص من الصور", "استخراج جميع النصوص من الصور في المجلد"))
# وظيفة تحويل النص إلى كلام
if operation == "تحويل النص إلى صوت":
    st.markdown("<h1 class='rtl-text'>تحويل النص إلى صوت</h1>", unsafe_allow_html=True)
    arabic_text = st.text_area("اكتب النص هنا:", height=200)

if operation == "استخراج نص من صورة":
    st.markdown("<h1 class='rtl-text'>استخراج النص من صورة</h1>", unsafe_allow_html=True)
    st.markdown("<div class='rtl-label'>اختر صورة:</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg", "webp"])
    if st.button("تشغيل الصوت"):
        try:
            if arabic_text.strip():
                tts = gTTS(arabic_text, lang='ar')
                mp3_fp = io.BytesIO()
                tts.write_to_fp(mp3_fp)
                mp3_fp.seek(0)
                pygame.mixer.init()
                pygame.mixer.music.load(mp3_fp)
                pygame.mixer.music.play()
                st.success("تم تشغيل الصوت بنجاح!")
            else:
                st.warning("الرجاء إدخال نص.")
        except Exception as e:
            st.error(f"حدث خطأ أثناء تشغيل الصوت: {e}")
    if st.button("إيقاف الصوت"):
        try:
            if pygame.mixer.get_init():  # تحقق مما إذا كانت pygame مهيأة
                pygame.mixer.music.stop()
                st.success("تم إيقاف الصوت.")
            else:
                st.warning("لا يوجد صوت قيد التشغيل لإيقافه.")
        except Exception as e:
            st.error(f"حدث خطأ أثناء إيقاف الصوت: {e}")
# وظيفة استخراج النصوص من صورة واحدة
elif operation == "استخراج النصوص من الصور":
    st.markdown("<h1 class='rtl-text'>استخراج النصوص من الصور</h1>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("اختر صورة:", type=["png", "jpg", "jpeg", "webp"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image = correct_image_orientation(image)  # Correct orientation
        st.image(image, caption="الصورة المحملة", use_container_width=True)

        with st.spinner("جاري تحليل النصوص..."):
def correct_image_orientation(image):
                st.error(f"حدث خطأ أثناء تحليل الصورة: {e}")
                st.stop()

        # عرض النص المكتشف مع إطار
        st.markdown("<div class='rtl-label'>النص المكتشف:</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='rtl-text'>{text}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='text-container'>{text}</div>", unsafe_allow_html=True)

        # وظيفة لتحميل النص
        def create_download_link(text, filename="extracted_text.txt"):
            val = io.BytesIO()
            val.write(text.encode('utf-8'))
            val.seek(0)
            b64 = base64.b64encode(val.read()).decode('utf-8')
            return f'<a href="data:text/plain;base64,{b64}" download="{filename}">تحميل النص كمستند</a>'
            return f'<a class="download-button" href="data:text/plain;base64,{b64}" download="{filename}">تحميل النص كمستند</a>'

        st.markdown("<div class='button-container'>", unsafe_allow_html=True)
        st.markdown(create_download_link(text), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# وظيفة استخراج النصوص من جميع الصور في مجلد
elif operation == "استخراج جميع النصوص من الصور في المجلد":
    st.markdown("<h1 class='rtl-text'>استخراج النصوص من جميع الصور في المجلد</h1>", unsafe_allow_html=True)

def create_download_link(text, filename="extracted_text.txt"):
        elif not os.path.exists(output_folder):
            st.error("مسار مجلد حفظ النصوص غير صحيح.")
        else:
            st.spinner("جاري استخراج النصوص...")
            try:
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                for image_name in os.listdir(images_folder):
                    if image_name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                        image_path = os.path.join(images_folder, image_name)
                        try:
                            image = Image.open(image_path)
                            image = correct_image_orientation(image)  # Correct orientation
                            text = pytesseract.image_to_string(image, lang='ara+eng')
                            text_filename = os.path.splitext(image_name)[0] + ".txt"
                            text_file_path = os.path.join(output_folder, text_filename)
