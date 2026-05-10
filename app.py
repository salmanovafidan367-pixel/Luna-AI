import streamlit as st
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="Luna AI", page_icon="🌙")
st.title("🌙 Luna: Senin Akıllı Asistanın")

# API Ayarı - Yeni anahtarını buraya tam olarak ekledim
API_KEY = "AIzaSyDKtlKq7DKlnrpsfWfvBfQ1GlH9BPPjcac"
genai.configure(api_key=API_KEY)

# Luna'nın Kişiliği ve Model Seçimi
# En yeni ve hızlı model olan 'gemini-1.5-flash'ı kullanıyoruz
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
            # Sistem talimatı
            luna_instruction = "Senin adın Luna. Nazik, neşeli ve yardımcı bir asistansın."
            response = model.generate_content(f"{luna_instruction}\n\nSoru: {prompt}")
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.write("Luna şu an sessiz kaldı, lütfen tekrar sormayı dene.")
                
        except Exception as e:
            st.error(f"Bağlantı hatası: {e}")
            
            if not success:
                st.error("Google şu an bu isteğe yanıt veremiyor. Lütfen API anahtarının aktif olduğundan emin ol.")

        except Exception as e:
            st.error(f"Sistemsel bir sorun oluştu: {e}")
