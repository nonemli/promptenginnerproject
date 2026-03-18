import streamlit as st
from groq import Groq

# ÖNEMLİ: Kodun içine anahtarı yazmıyoruz, Streamlit'in kasasından çağırıyoruz
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("Hata: GROQ_API_KEY bulunamadı. Lütfen Streamlit Cloud ayarlarından 'Secrets' kısmına ekleyin.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# 2. SYSTEM PROMPT (Daha Kesin Talimatlar Eklendi)
SYSTEM_PROMPT = """Sen dünyanın en iyi PROMPT MÜHENDİSİSİN. 
GÖREVİN: Kullanıcının verdiği ham metni, başka bir yapay zekaya verilecek profesyonel, tek paragraflık, akıcı bir komuta dönüştürmektir.

KESİN KURALLAR:
1. Çıktı sadece ve sadece oluşturulan PROMPT olmalıdır. 
2. Asla "İşte promptun", "Tabii ki" gibi giriş cümleleri kurma.
3. Asla liste yapma, başlık kullanma.
4. Çıktıyı her zaman profesyonel bir Türkçe ile oluştur.
5. Kullanıcıya tavsiye verme, sadece onun adına bir talimat metni yaz.

ÖRNEK:
Girdi: "Diyetisyen ol, ayda 5 kilo verdir, sağlıklı olsun."
Çıktı: "Sen uzman bir diyetisyensin; danışanın için sağlıklı ve sürdürülebilir yöntemlerle ayda 5 kilo vermesini sağlayacak, besin değerleri dengelenmiş günlük bir beslenme planı oluştur."
"""

# 3. ARAYÜZ TASARIMI
st.set_page_config(page_title="Prompt Sihirbazı", page_icon="🎯")
st.title("🎯 Tek Cümlelik Prompt Sihirbazı")

user_input = st.text_area("Bilgileri girin (Rol, Görev, Kısıtlama vb.):", 
                          placeholder="Örn: Rol uzman diyetisyen, ayda 5 kilo verdiren liste...",
                          height=150)

if st.button("Profesyonel Komuta Dönüştür 🚀"):
    if user_input:
        with st.spinner('Yapay zeka komutu yoğuruyor...'):
            try:
                # API Çağrısı
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_input}
                    ],
                    temperature=0.3
                )
                
                final_prompt = completion.choices[0].message.content.strip()
                
                # SONUÇ EKRANI VE HİZALAMA
                st.markdown("---")
                st.success("### ✅ Kopyalamaya Hazır Komut")
                
                # Standart Kod Bloğu
                st.code(final_prompt, language="text")
                
                # MOBİL KOPYALAMA SORUNU ÇÖZÜMÜ
                # st.text_area mobilde basılı tutup seçmek için en güvenli yoldur.
                st.text_area("Mobilde kopyalamak için metne basılı tutun:", value=final_prompt, height=150)
                
                st.info("💡 Yukarıdaki metni kopyalayıp ChatGPT, Gemini veya Claude gibi araçlara yapıştırabilirsiniz.")
                
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
    else:
        st.warning("Lütfen bir giriş yapın.")
