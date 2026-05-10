import streamlit as st
import google.generativeai as genai

# 1. Sayfa Ayarları
st.set_page_config(page_title="Luna AI", page_icon="🌙")
st.title("🌙 Luna: Bu Gece Ay Çok Güzel")

# 2. Yeni API Anahtarın (Görseldeki yeni anahtarı buraya ekledim)
API_KEY = "AIzaSyAixBcHynUB242qhgJrxX9pZ0VQwrJh9nU"

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeaiModel('gemini-1.5-flash')
    success = True
except Exception as e:
    st.error(f"Kurulum hatası: {e}")
    success = False

# 3. Sohbet Geçmişi Başlatma
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Eski Mesajları Ekrana Basma
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Kullanıcı Girişi ve Yanıt Mekanizması
if prompt := st.chat_input("Luna'ya bir şeyler sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if success:
        with st.chat_message("assistant"):
            try:
                response = model.generate_content(prompt)
                if response and response.text:
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                else:
                    st.warning("Luna şu an cevap üretemedi.")
            except Exception as e:
                st.error(f"Bağlantı Hatası: {e}")
                st.info("Yeni anahtarın aktifleşmesi 1-2 dakika sürebilir.")
