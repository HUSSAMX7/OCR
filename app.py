import streamlit as st
import os
from PIL import Image
import pytesseract
import io
import base64
from gtts import gTTS

# إعداد الصفحة
st.set_page_config(page_title="برنامج RMG المزود بالذكاء الاصطناعي", layout="wide")

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

# الشريط الجانبي
with st.sidebar:
    st.image("logo-1-1.png", use_container_width=True)
    st.markdown("<div style='text-align: right; font-size: 20px; font-weight: bold;'>تطبيق RMG المزود بالذكاء الاصطناعي</div>", unsafe_allow_html=True)
    operation = st.radio("اختر نوع العملية:", ("تحويل النص إلى صوت", "استخراج النصوص من الصور", "استخراج جميع النصوص من الصور في المجلد"))

# إدارة حالة الصوت
if "audio_base64" not in st.session_state:
    st.session_state.audio_base64 = None  # لتخزين ملف الصوت
if "audio_playing" not in st.session_state:
    st.session_state.audio_playing = False  # حالة تشغيل الصوت

# وظيفة تحويل النص إلى كلام
if operation == "تحويل النص إلى صوت":
    st.markdown("<h1 class='rtl-text'>تحويل النص إلى صوت</h1>", unsafe_allow_html=True)
    arabic_text = st.text_area("اكتب النص هنا:", height=200)

    # زر لتشغيل الصوت
    if st.button("تشغيل الصوت"):
        if not st.session_state.audio_playing:  # إذا لم يتم تشغيل الصوت
            if arabic_text.strip():
                try:
                    # إنشاء ملف صوتي
                    tts = gTTS(arabic_text, lang='ar')
                    mp3_fp = io.BytesIO()
                    tts.write_to_fp(mp3_fp)
                    mp3_fp.seek(0)

                    # تحويل الصوت إلى صيغة base64
                    st.session_state.audio_base64 = base64.b64encode(mp3_fp.read()).decode('utf-8')
                    st.session_state.audio_playing = True
                    st.success("تم تشغيل الصوت!")
                except Exception as e:
                    st.error(f"حدث خطأ أثناء تشغيل الصوت: {e}")
            else:
                st.warning("الرجاء إدخال نص.")
        else:
            st.warning("الصوت قيد التشغيل بالفعل.")

    # زر لإيقاف الصوت
    if st.button("إيقاف الصوت"):
        if st.session_state.audio_playing:
            st.session_state.audio_playing = False
            st.success("تم إيقاف الصوت!")
        else:
            st.warning("لا يوجد صوت قيد التشغيل.")

     # عرض مشغل الصوت إذا كان الصوت قيد التشغيل
    if st.session_state.audio_base64 and st.session_state.audio_playing:
        audio_html = f"""
        <audio controls autoplay>
            <source src="data:audio/mp3;base64,{st.session_state.audio_base64}" type="audio/mp3">
        #</audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)

# وظيفة استخراج النصوص من صورة واحدة
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

        # وظيفة لتحميل النص
        def create_download_link(text, filename="extracted_text.txt"):
            val = io.BytesIO()
            val.write(text.encode('utf-8'))
            val.seek(0)
            b64 = base64.b64encode(val.read()).decode('utf-8')
            return f'<a class="download-button" href="data:text/plain;base64,{b64}" download="{filename}">تحميل النص كمستند</a>'

        st.markdown("<div class='button-container'>", unsafe_allow_html=True)
        st.markdown(create_download_link(text), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# وظيفة استخراج النصوص من جميع الصور في مجلد
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
            try:
                for image_name in os.listdir(images_folder):
                    if image_name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                        image_path = os.path.join(images_folder, image_name)
                        try:
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
