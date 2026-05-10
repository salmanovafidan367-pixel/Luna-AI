import streamlit as st
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="Luna AI", page_icon="🌙")
st.title("🌙 Luna: Bu Gece Ay Çok Güzel")

# API Ayarı - Son attığın anahtarı buraya ekledim
API_KEY = "AIzaSyDKtlKq7DKlnrpsfWfvBfQ1GlH9BPPjcac"

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Kurulum hatası: {e}")

# Sohbet Geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = []

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
            # Luna'nın cevabı
            response = model.generate_content(prompt)
            if response and response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("Luna şu an cevap üretemedi.")
        except Exception as e:
            st.error(f"Bağlantı Hatası: {e}")
            st.info("Anahtarın henüz aktif olmamış olabilir. Lütfen 2 dakika bekleyip tekrar yaz.")

        except Exception as e:
            st.error(f"Sistemsel bir sorun oluştu: {e}")
