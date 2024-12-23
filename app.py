import streamlit as st
import os
import urllib.request
from PIL import Image
import pytesseract
import io
import base64

# تحديد المسار إلى Tesseract
try:
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"  # تحقق من المسار حسب بيئتك
except Exception as e:
    st.error(f"فشل في العثور على Tesseract: {e}")

# إعداد وتحميل ملف اللغة العربية
tessdata_dir = os.path.expanduser("~/.tesseract/tessdata")
os.makedirs(tessdata_dir, exist_ok=True)
ara_traineddata_path = os.path.join(tessdata_dir, "ara.traineddata")

if not os.path.exists(ara_traineddata_path):
    try:
        with st.spinner("جاري تحميل ملف اللغة العربية..."):
            url = "https://raw.githubusercontent.com/tesseract-ocr/tessdata_best/master/ara.traineddata"
            urllib.request.urlretrieve(url, ara_traineddata_path)
    except Exception as e:
        st.error(f"فشل تحميل ملف ara.traineddata: {e}")
        st.stop()

# تحديث متغير البيئة لتحديد tessdata_dir
os.environ["TESSDATA_PREFIX"] = os.path.dirname(tessdata_dir)

# إعداد الصفحة
st.set_page_config(page_title="استخراج النص من الصور", layout="wide")

# CSS
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
    st.markdown("<h1>استخراج النص من الصور</h1>", unsafe_allow_html=True)
    operation = st.radio("اختر نوع العملية:", ("استخراج نص من صورة", "استخراج النصوص من مجلد"))

if operation == "استخراج نص من صورة":
    st.markdown("<h2 class='rtl-text'>استخراج النص من صورة</h2>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("اختر صورة:", type=["png", "jpg", "jpeg", "webp"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="الصورة المحملة", use_container_width=True)

        with st.spinner("جاري تحليل النصوص..."):
            try:
                text = pytesseract.image_to_string(image, lang='ara+eng').strip()
                if not text:
                    st.warning("لم يتم العثور على نص في الصورة.")
                else:
                    st.markdown("<h3 class='rtl-label'>النص المكتشف:</h3>", unsafe_allow_html=True)
                    st.text_area("", text, height=200)

                    def create_download_link(text, filename="extracted_text.txt"):
                        b64 = base64.b64encode(text.encode('utf-8')).decode('utf-8')
                        return f'<a href="data:text/plain;base64,{b64}" download="{filename}">تحميل النص</a>'

                    st.markdown(create_download_link(text), unsafe_allow_html=True)
            except Exception as e:
                st.error(f"حدث خطأ: {e}")

elif operation == "استخراج النصوص من مجلد":
    st.markdown("<h2 class='rtl-text'>استخراج النصوص من جميع الصور في المجلد</h2>", unsafe_allow_html=True)

    images_folder = st.text_input("أدخل مسار مجلد الصور:")
    output_folder = st.text_input("أدخل مسار مجلد حفظ النصوص:")

    if st.button("بدء استخراج النصوص"):
        if not os.path.exists(images_folder):
            st.error("مسار مجلد الصور غير صحيح.")
        elif not os.path.exists(output_folder):
            os.makedirs(output_folder)

        try:
            for image_name in os.listdir(images_folder):
                if image_name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    image_path = os.path.join(images_folder, image_name)
                    try:
                        image = Image.open(image_path)
                        text = pytesseract.image_to_string(image, lang='ara+eng')
                        text_file_path = os.path.join(output_folder, f"{os.path.splitext(image_name)[0]}.txt")
                        with open(text_file_path, 'w', encoding='utf-8') as text_file:
                            text_file.write(text)
                        st.success(f"تم استخراج النصوص من {image_name}")
                    except Exception as e:
                        st.error(f"خطأ مع الصورة {image_name}: {e}")
        except Exception as e:
            st.error(f"حدث خطأ أثناء استخراج النصوص: {e}")
