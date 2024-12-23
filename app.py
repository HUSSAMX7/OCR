import streamlit as st
import os
from PIL import Image
import pytesseract
import io
import base64

# تحديد مسار tessdata بشكل أكثر مرونة
TESSDATA_DIR = os.environ.get("TESSDATA_PREFIX", os.path.join(os.path.dirname(__file__), 'tessdata'))
pytesseract.pytesseract.tesseract_cmd = os.environ.get("TESSERACT_CMD", "tesseract")  # تحديد مسار tesseract

# التحقق من وجود ملفات اللغة
if not os.path.exists(os.path.join(TESSDATA_DIR, 'ara.traineddata')):
    st.error(f"ملف اللغة العربية غير موجود في المسار: {TESSDATA_DIR}. يرجى التأكد من وجوده.")
    st.stop() # إيقاف التطبيق إذا كان الملف مفقوداً

# إعداد الصفحة
st.set_page_config(page_title="استخراج النص من الصور", layout="wide")

# CSS للتنسيق (مع تحسينات)
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
        white-space: pre-wrap; /* يسمح بكسر الأسطر */
    }
    .rtl-label {
        text-align: right;
        font-weight: bold;
        font-size: 20px;
    }
    .stTextArea textarea { /* تحسين حجم مربع النص */
        height: 300px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ... (بقية الكود كما هو مع التعديلات التالية)

if operation == "استخراج نص من صورة":
    # ...
    if uploaded_file is not None:
        # ...
        with st.spinner("جاري تحليل النصوص..."):
            try:
                # تشغيل Tesseract مع تحسينات
                text = pytesseract.image_to_string(image, lang='ara+eng', config=f'--tessdata-dir "{TESSDATA_DIR}"') # استخدام f-string واقتباس المسار
                # ... (بقية الكود كما هو)
            except pytesseract.TesseractNotFoundError: # معالجة خطأ عدم وجود Tesseract
                st.error("لم يتم العثور على برنامج Tesseract. يرجى تثبيته وتحديد مساره في متغير البيئة TESSERACT_CMD.")
            except Exception as e:
                st.error(f"حدث خطأ: {e}")

# ... (بقية الكود كما هو مع التعديلات التالية)

elif operation == "استخراج نصوص من مجلد":
    # ...
    if st.button("ابدأ"):
        # ...
        with st.spinner("جاري معالجة الصور..."):
            try:
                for filename in os.listdir(folder_path):
                    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                        file_path = os.path.join(folder_path, filename)
                        try: # معالجة الأخطاء لكل ملف على حدة
                            image = Image.open(file_path)
                            text = pytesseract.image_to_string(image, lang='ara+eng', config=f'--tessdata-dir "{TESSDATA_DIR}"')
                            output_file = os.path.join(output_folder, os.path.splitext(filename)[0] + ".txt")
                            with open(output_file, "w", encoding="utf-8") as f:
                                f.write(text)
                            st.success(f"تم معالجة: {filename}")
                        except Exception as inner_e:
                            st.error(f"حدث خطأ أثناء معالجة {filename}: {inner_e}") # عرض خطأ خاص بالملف
            except Exception as e:
                st.error(f"حدث خطأ عام: {e}")
