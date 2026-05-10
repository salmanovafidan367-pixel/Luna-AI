import streamlit as st
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="Luna AI", page_icon="🌙")
st.title("🌙 Luna: Bu gün Ay harika gozüküyor")

# API Ayarı
API_KEY = "AIzaSyCuBPFaFysKBqjPsnUHO3o2qY57voTtNaI"
genai.configure(api_key=API_KEY)

# Sohbet Geçmişini Başlat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski mesajları ekranda göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan girdi al
if prompt := st.chat_input("Luna'ya bir şeyler sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # 404 hatasını çözmek için farklı model isimlerini sırayla deniyoruz
            success = False
            for model_name in ['gemini-1.5-flash', 'gemini-pro', 'models/gemini-pro']:
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(f"Senin adın Luna. Nazikçe cevap ver: {prompt}")
                    if response:
                        st.markdown(response.text)
                        st.session_state.messages.append({"role": "assistant", "content": response.text})
                        success = True
                        break
                except:
                    continue # Bir model çalışmazsa diğerini dene
            
            if not success:
                st.error("Google şu an bu isteğe yanıt veremiyor. Lütfen API anahtarının aktif olduğundan emin ol.")

        except Exception as e:
            st.error(f"Sistemsel bir sorun oluştu: {e}")
