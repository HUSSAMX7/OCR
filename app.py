import streamlit as st
import os
from PIL import Image
import pytesseract
import io
import base64

# تحديد مسار tessdata النسبي داخل المشروع
TESSDATA_DIR = os.path.join(os.path.dirname(__file__), 'tessdata')
os.environ["TESSDATA_PREFIX"] = TESSDATA_DIR

# إعداد الصفحة
st.set_page_config(page_title="استخراج النص من الصور", layout="wide")

# CSS للتنسيق
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
    </style>
    """,
    unsafe_allow_html=True,
)

# الشريط الجانبي
with st.sidebar:
    st.markdown("<h3>استخراج النص من الصور</h3>", unsafe_allow_html=True)
    operation = st.radio("اختر نوع العملية:", ("استخراج نص من صورة", "استخراج نصوص من مجلد"))

# استخراج النص من صورة
if operation == "استخراج نص من صورة":
    st.header("استخراج النص من صورة")
    uploaded_file = st.file_uploader("اختر صورة:", type=["png", "jpg", "jpeg", "webp"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="الصورة المحملة", use_column_width=True)

        with st.spinner("جاري تحليل النصوص..."):
            try:
                # تشغيل Tesseract
                text = pytesseract.image_to_string(image, lang='ara+eng', config='--tessdata-dir ' + TESSDATA_DIR)
                text = text.strip()
                if not text:
                    st.warning("لم يتم العثور على أي نص في الصورة.")
                else:
                    st.text_area("النص المكتشف:", text, height=200)

                    # رابط لتحميل النص المكتشف
                    def create_download_link(text, filename="extracted_text.txt"):
                        val = io.BytesIO()
                        val.write(text.encode('utf-8'))
                        val.seek(0)
                        b64 = base64.b64encode(val.read()).decode('utf-8')
                        return f'<a href="data:text/plain;base64,{b64}" download="{filename}">تحميل النص كمستند</a>'

                    st.markdown(create_download_link(text), unsafe_allow_html=True)
            except Exception as e:
                st.error(f"حدث خطأ: {e}")

# استخراج النصوص من مجلد
elif operation == "استخراج نصوص من مجلد":
    st.header("استخراج النصوص من جميع الصور في مجلد")
    folder_path = st.text_input("أدخل مسار مجلد الصور:")
    output_folder = st.text_input("أدخل مسار حفظ النصوص:")

    if st.button("ابدأ"):
        if not os.path.exists(folder_path):
            st.error("مسار مجلد الصور غير صحيح.")
        elif not os.path.exists(output_folder):
            os.makedirs(output_folder)

        with st.spinner("جاري معالجة الصور..."):
            try:
                for filename in os.listdir(folder_path):
                    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                        file_path = os.path.join(folder_path, filename)
                        image = Image.open(file_path)
                        text = pytesseract.image_to_string(image, lang='ara+eng', config='--tessdata-dir ' + TESSDATA_DIR)
                        output_file = os.path.join(output_folder, os.path.splitext(filename)[0] + ".txt")
                        with open(output_file, "w", encoding="utf-8") as f:
                            f.write(text)
                        st.success(f"تم معالجة: {filename}")
            except Exception as e:
                st.error(f"حدث خطأ: {e}")
