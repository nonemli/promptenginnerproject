import streamlit as st
from groq import Groq

# 1. AYARLAR
# Buraya Groq API anahtarınızı girin
GROQ_API_KEY = "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" 
client = Groq(api_key=GROQ_API_KEY)

# 2. SYSTEM PROMPT TANIMI (Hata almamak için en üstte veya butonun hemen içinde olmalı)
SYSTEM_PROMPT = """Sen dünyanın en iyi PROMPT MÜHENDİSİSİN. 
GÖREVİN: Kullanıcının verdiği ham metni, başka bir yapay zekaya (LLM) verilecek profesyonel, tek paragraflık, akıcı bir komuta (prompt) dönüştürmektir.

KESİN YASAKLAR:
- Kullanıcıya asla tavsiye verme (Örn: 'Su içmelisiniz' deme).
- Asla başlık kullanma (Rol:, Görev: yazma).
- Asla liste yapma.
- "İşte promptun" gibi giriş cümleleri kurma.
- "Hangi dilde girdi alırsan al, çıktıyı her zaman profesyonel bir Türkçe ile oluştur."

ÖRNEK DÖNÜŞÜM:
Kullanıcı Girdisi: "Ayda 5 kilo vermek istiyorum, sağlıklı olsun, liste ver."
Senin Çıktın: "Sen uzman bir diyetisyensin; sağlıklı ve sürdürülebilir bir yaklaşımla ayda 5 kilo vermeyi hedefleyen bir birey için lif oranı yüksek gıdalardan oluşan, işlenmiş şeker içermeyen ve günlük su tüketimi ile fiziksel aktiviteyi de planlayan detaylı bir beslenme programı hazırla."
"""
# 3. ARAYÜZ
st.set_page_config(page_title="Prompt Sihirbazı", page_icon="🎯")
st.title("🎯 Tek Cümlelik Prompt Sihirbazı")

user_input = st.text_area("Bilgileri girin (Rol, Görev, Kısıtlama vb.):", 
                          placeholder="Örn: Rol uzman diyetisyen, ayda 5 kilo verdiren liste, sağlıklı olsun...",
                          height=150)

if st.button("Profesyonel Komuta Dönüştür 🚀"):
    if user_input:
        with st.spinner('Dönüştürülüyor...'):
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
                
                st.markdown("---")
                st.success("### ✅ Kopyalamaya Hazır Komut")
                
                # Tek parça metin olarak gösterim ve kopyalama alanı
                st.code(final_prompt, language="text")
                
                st.info("Bu metni doğrudan başka bir yapay zekaya yapıştırabilirsiniz.")
                
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
    else:
        st.warning("Lütfen bir giriş yapın.")