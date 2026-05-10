import streamlit as st
import google.generativeai as genai

# 1. Sayfa Ayarları
st.set_page_config(page_title="Luna AI", page_icon="🌙")
st.title("🌙 Luna: Bu Gece Ay Çok Güzel")

# 2. Yeni API Anahtarın (image_cfa21a.png'den aldım)
API_KEY = "AIzaSyAixBcHynUB242qhgJrxX9pZ0VQwrJh9nU"

try:
    genai.configure(api_key=API_KEY)
    # Hatalı olan yer düzeltildi: GenerativeModel (ai kelimesi yok)
    model = genai.GenerativeModel('gemini-1.5-flash')
    success = True
except Exception as e:
    st.error(f"Kurulum hatası: {e}")
    success = False

# 3. Sohbet Geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Eski Mesajları Göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Mesajlaşma Alanı
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
                    st.warning("Luna şu an sessiz kalmayı tercih ediyor.")
            except Exception as e:
                st.error(f"Bağlantı Hatası: {e}")