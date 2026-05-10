import streamlit as st
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="Luna AI", page_icon="🌙")
st.title("🌙 Luna: Yıldızlar ve Ay ne kadar ilgi cekici..")

# API Ayarı - Burayı senin gerçek anahtarınla sabitledim
API_KEY = "AIzaSyCuBPFaFysKBqjPsnUHO3o2qY57voTtNaI"
genai.configure(api_key=API_KEY)

# Luna'nın Kişiliği ve Model Seçimi
system_prompt = "Senin adın Luna. Nazik, neşeli ve bilgili bir asistansın."
model = genai.GenerativeModel('gemini-1.5-flash')

# Sohbet Geçmişini Başlat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski mesajları ekranda göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan girdi al
if prompt := st.chat_input("Luna'ya bir şeyler sor..."):
    # Kullanıcı mesajını göster ve kaydet
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Luna'nın cevabını oluştur
    with st.chat_message("assistant"):
        try:
            # Sistem talimatıyla beraber mesajı gönder
            full_prompt = f"{system_prompt}\n\nKullanıcı: {prompt}"
            response = model.generate_content(full_prompt)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
