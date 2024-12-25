import streamlit as st
import os
from PIL import Image
import pytesseract
import io
import base64
st.set_page_config(page_title="استخراج النص من الصور", layout="wide")

# CSS  
st.markdown(
    """
    <style>
    body {
        direction: rtl; /* اتجاه الصفحة بالكامل */
        font-family: 'Arial', sans-serif; /* خط افتراضي (يمكن تغييره) */
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
        justify-content: flex-end; /* محاذاة الأزرار لليمين */
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
    st.image("logo-1-1.png", use_container_width=True)
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

    images_folder = st.text_input("أدخل مسار مجلد الصور:")
    output_folder = st.text_input("أدخل مسار مجلد حفظ النصوص:")

    if st.button("بدء استخراج النصوص"):
        if not os.path.exists(images_folder):
            st.error("مسار مجلد الصور غير صحيح.")
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
                        try: # معالجة الأخطاء لكل صورة على حدة
                            image = Image.open(image_path)
                            text = pytesseract.image_to_string(image, lang='ara+eng')
                            text_filename = os.path.splitext(image_name)[0] + ".txt"
                            text_file_path = os.path.join(output_folder, text_filename)
                            with open(text_file_path, 'w', encoding='utf-8') as text_file:
                                text_file.write(text)
                            st.success(f"تم استخراج النصوص من {image_name} وحفظها في {text_filename}")
                        except Exception as inner_e:
                            st.error(f"حدث خطأ أثناء معالجة الصورة {image_name}: {inner_e}")
            except Exception as e:
                st.error(f"حدث خطأ أثناء استخراج النصوص: {e}")
