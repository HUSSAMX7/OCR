import streamlit as st
import os
from PIL import Image
import pytesseract
import io
import base64

# تحديد مسار Tesseract وبيانات اللغة بشكل ديناميكي
if os.name == 'nt':  # نظام Windows
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # المسار الافتراضي على ويندوز
    tessdata_dir_config = r'--tessdata-dir "tessdata"'
elif os.name == 'posix':  # أنظمة Linux و macOS
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
    os.environ["TESSDATA_PREFIX"] = "/usr/share/tesseract-ocr/4.00/"  # احتفظ بهذا إذا كان مسار tessdata صحيحًا على نظامك
    tessdata_dir_config = r'--tessdata-dir "tessdata"'
else:
    st.error("نظام التشغيل غير مدعوم.")
    st.stop()

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
        direction: rtl;
        text-align: right;
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
    }
    .stTextArea > div > div > textarea {
        direction: rtl;
        text-align: right;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
# الشريط الجانبي
with st.sidebar:
    st.markdown("<div class='header-text'>استخراج النص من الصور بالذكاء الاصطناعي</div>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    operation = st.radio("اختر نوع العملية :", ("استخراج نص من صورة", "استخراج جميع النصوص من الصور في المجلد"))

if operation == "استخراج نص من صورة":
    st.markdown("<h1 class='rtl-text'>استخراج النص من صورة</h1>", unsafe_allow_html=True)
    st.markdown("<div class='rtl-label'>اختر صورة:</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg", "webp"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="الصورة المحملة", use_container_width=True)

        with st.spinner("جاري تحليل النصوص..."):
            try:
                text = pytesseract.image_to_string(image, lang='ara+eng', config=tessdata_dir_config)
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

        st.markdown("<div class='rtl-label'>النص المكتشف:</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='rtl-text'>{text}</div>", unsafe_allow_html=True)

        def create_download_link(text, filename="extracted_text.txt"):
            val = io.BytesIO()
            val.write(text.encode('utf-8'))
            val.seek(0)
            b64 = base64.b64encode(val.read()).decode('utf-8')
            return f'<a href="data:text/plain;base64,{b64}" download="{filename}">تحميل النص كمستند</a>'

        st.markdown("<div class='button-container'>", unsafe_allow_html=True)
        st.markdown(create_download_link(text), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

elif operation == "استخراج جميع النصوص من الصور في المجلد":
    st.markdown("<h1 class='rtl-text'>استخراج النصوص من جميع الصور في المجلد</h1>", unsafe_allow_html=True)

    uploaded_files = st.file_uploader("اختر صورًا من جهازك:", type=["png", "jpg", "jpeg", "webp"], accept_multiple_files=True)
    if uploaded_files:
        output_folder = "output_texts"
        os.makedirs(output_folder, exist_ok=True)
        with st.spinner("جاري استخراج النصوص..."):
            for uploaded_file in uploaded_files:
                try:
                    image = Image.open(uploaded_file)
                    text = pytesseract.image_to_string(image, lang='ara+eng', config=tessdata_dir_config)
                    text = text.strip()
                    if not text:
                        st.warning(f"لم يتم العثور على أي نص في الصورة: {uploaded_file.name}")
                        continue
                    text_filename = os.path.splitext(uploaded_file.name)[0] + ".txt"
                    text_file_path = os.path.join(output_folder, text_filename)
                    with open(text_file_path, 'w', encoding='utf-8') as text_file:
                        text_file.write(text)
                    st.success(f"تم استخراج النصوص من {uploaded_file.name} وحفظها في {text_filename}")
                except Exception as inner_e:
                    st.error(f"حدث خطأ أثناء معالجة الصورة {uploaded_file.name}: {inner_e}")
        st.write(f"تم حفظ جميع النصوص المستخرجة في المجلد: `{output_folder}`")
else:
    st.write("الرجاء اختيار عملية من الشريط الجانبي.")
