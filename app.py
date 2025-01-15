elif operation == "استخراج جميع النصوص من الصور في المجلد":
    st.markdown("<h1 class='rtl-text'>استخراج النصوص من الصور في المجلد</h1>", unsafe_allow_html=True)
    folder_path = st.text_input("أدخل مسار المجلد (مثال: C:/Users/اسم_المستخدم/Desktop/اسم_المجلد):")

    if st.button("استخراج النصوص"):
        if folder_path.strip():
            if os.path.exists(folder_path) and os.path.isdir(folder_path):
                output_texts = {}
                with st.spinner("جاري تحليل النصوص من الصور..."):
                    try:
                        image_files = [
                            f for f in os.listdir(folder_path)
                            if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
                        ]
                        if not image_files:
                            st.warning("لم يتم العثور على أي صور صالحة في المجلد.")
                            st.stop()

                        for file_name in image_files:
                            file_path = os.path.join(folder_path, file_name)
                            image = Image.open(file_path)
                            text = pytesseract.image_to_string(image, lang='ara+eng').strip()
                            output_texts[file_name] = text

                        st.success("تم استخراج النصوص بنجاح!")
                        for file_name, text in output_texts.items():
                            st.markdown(f"<div class='rtl-label'>النص من الصورة: {file_name}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='text-container'>{text}</div>", unsafe_allow_html=True)

                    except Exception as e:
                        st.error(f"حدث خطأ أثناء تحليل الصور: {e}")
            else:
                st.error("المسار المدخل غير موجود أو ليس مجلداً صالحاً. الرجاء إدخال مسار مجلد صحيح.")
        else:
            st.warning("الرجاء إدخال مسار مجلد.")
