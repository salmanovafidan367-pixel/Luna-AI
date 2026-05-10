import streamlit as st
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="Luna AI", page_icon="🌙")
st.title("🌙 Luna: Senin Akıllı Asistanın")

# API Ayarı
API_KEY = "AIzaSyCuBPFaFysKBqjPsnUHO3o2qY57voTtNaI"
genai.configure(api_key=API_KEY)

# Luna'nın Kişiliği ve Model Seçimi
# En kararlı model ismi olan 'gemini-pro' kullanıldı
try:
    model = genai.GenerativeModel('gemini-pro')
except:
    model = genai.GenerativeModel('models/gemini-pro')

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
            # Sistem talimatı
            luna_instruction = "Senin adın Luna. Nazik, neşeli ve yardımcı bir asistansın. "
            full_prompt = f"{luna_instruction} \n\n Kullanıcı: {prompt}"
            
            response = model.generate_content(full_prompt)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.write("Luna şu an sessiz kaldı, lütfen tekrar sormayı dene.")
                
        except Exception as e:
            st.error(f"Bir sorun oluştu: {e}")
            st.info("İpucu: Eğer model hatası alıyorsan, API anahtarının Gemini Pro modeline erişimi olduğundan emin ol.")
            st.error(f"Bağlantı hatası: {e}")
            st.info("Lütfen API anahtarının aktif olduğunu ve internet bağlantını kontrol et.")
