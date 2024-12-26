import streamlit as st
import os
from PIL import Image, ExifTags
import pytesseract
import io
import base64
from gtts import gTTS
import pygame

st.set_page_config(page_title="استخراج النص من الصور", layout="wide")

# تحديد مسار Tesseract (إذا كان ضروريًا)
# pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# CSS لتنسيق الصفحة (كما هو)
st.markdown(
    """
    <style>
    /* ... (جميع أنماط CSS كما هي) ... */
    </style>
    """,
    unsafe_allow_html=True,
)

# دالة لتصحيح اتجاه الصورة (تم نقلها خارج الكتلة with)
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
        pass  # تجاهل الأخطاء إذا كانت بيانات EXIF غير متوفرة
    return image

# الشريط الجانبي (كما هو)
with st.sidebar:
    # ...

# وظيفة تحويل النص إلى كلام (كما هي)
if operation == "تحويل النص إلى صوت":
    # ...

# وظيفة استخراج النصوص من صورة واحدة
elif operation == "استخراج النصوص من الصور":
    st.markdown("<h1 class='rtl-text'>استخراج النصوص من الصور</h1>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("اختر صورة:", type=["png", "jpg", "jpeg", "webp"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image = correct_image_orientation(image)  # تصحيح الاتجاه
        st.image(image, caption="الصورة المحملة", use_container_width=True)

        with st.spinner("جاري تحليل النصوص..."): # هنا تم تصحيح مكان الدالة
            try:
                text = pytesseract.image_to_string(image, lang='ara+eng')
            except Exception as e:
                st.error(f"حدث خطأ أثناء تحليل الصورة: {e}")
                st.stop()
        # عرض النص المكتشف (كما هو)
        st.markdown("<div class='rtl-label'>النص المكتشف:</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='text-container'>{text}</div>", unsafe_allow_html=True)

        # وظيفة لتحميل النص (تم تحسينها)
        def create_download_link(text, filename="extracted_text.txt"):
            val = io.BytesIO()
            val.write(text.encode('utf-8'))
            val.seek(0)
            b64 = base64.b64encode(val.read()).decode('utf-8')
            return f'<a class="download-button" href="data:text/plain;base64,{b64}" download="{filename}">تحميل النص كمستند</a>'

        st.markdown("<div class='button-container'>", unsafe_allow_html=True)
        st.markdown(create_download_link(text), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# وظيفة استخراج النصوص من جميع الصور في مجلد (تم تبسيطها)
elif operation == "استخراج جميع النصوص من الصور في المجلد":
    st.markdown("<h1 class='rtl-text'>استخراج النصوص من جميع الصور في المجلد</h1>", unsafe_allow_html=True)
    images_folder = st.text_input("أدخل مسار مجلد الصور:", "")
    output_folder = st.text_input("أدخل مسار مجلد حفظ النصوص:", "")
    if st.button("استخراج النصوص من المجلد"):
        if not os.path.exists(images_folder):
            st.error("مسار مجلد الصور غير صحيح.")
        elif not os.path.exists(output_folder):
            st.error("مسار مجلد حفظ النصوص غير صحيح.")
        else:
            with st.spinner("جاري استخراج النصوص..."):
                try:
                    if not os.path.exists(output_folder):
                        os.makedirs(output_folder)
                    for image_name in os.listdir(images_folder):
                        if image_name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                            image_path = os.path.join(images_folder, image_name)
                            try:
                                image = Image.open(image_path)
                                image = correct_image_orientation(image)
                                text = pytesseract.image_to_string(image, lang='ara+eng')
                                text_filename = os.path.splitext(image_name)[0] + ".txt"
                                text_file_path = os.path.join(output_folder, text_filename)
                                with open(text_file_path, "w", encoding="utf-8") as f:
                                    f.write(text)
                            except Exception as e:
                                st.error(f"حدث خطأ أثناء معالجة الصورة {image_name}: {e}")
                    st.success("تم استخراج النصوص بنجاح!")
                except Exception as e:
                    st.error(f"حدث خطأ عام: {e}")

# ... (بقية الكود)
