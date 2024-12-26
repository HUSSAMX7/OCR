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

# وظيفة تحويل النص إلى كلام
st.markdown("<h1 class='rtl-text'>تحويل النص إلى صوت</h1>", unsafe_allow_html=True)
arabic_text = st.text_area("اكتب النص هنا:", height=200)

if "audio_html" not in st.session_state:
    st.session_state.audio_html = None

if st.button("تشغيل/إيقاف الصوت"):
    if arabic_text.strip():
        try:
            # إنشاء ملف صوتي
            tts = gTTS(arabic_text, lang='ar')
            mp3_fp = io.BytesIO()
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)

            # تحويل الصوت إلى صيغة base64
            mp3_base64 = base64.b64encode(mp3_fp.read()).decode('utf-8')
            st.session_state.audio_html = f"""
            <audio controls autoplay>
                <source src="data:audio/mp3;base64,{mp3_base64}" type="audio/mp3">
            </audio>
            """
            st.success("تم تشغيل الصوت!")
        except Exception as e:
            st.error(f"حدث خطأ أثناء تشغيل الصوت: {e}")
    else:
        st.warning("الرجاء إدخال نص.")

if st.session_state.audio_html:
    st.markdown(st.session_state.audio_html, unsafe_allow_html=True)
