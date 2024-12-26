import streamlit as st
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

# وظيفة تحويل النص إلى كلام
st.markdown("<h1 class='rtl-text'>تحويل النص إلى صوت</h1>", unsafe_allow_html=True)
arabic_text = st.text_area("اكتب النص هنا:", height=200)

# إنشاء حالة لتتبع الصوت
if "audio_base64" not in st.session_state:
    st.session_state.audio_base64 = None  # لتخزين ملف الصوت
if "audio_playing" not in st.session_state:
    st.session_state.audio_playing = False  # حالة تشغيل الصوت

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
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)
