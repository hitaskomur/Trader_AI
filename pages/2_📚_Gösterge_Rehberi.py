# 2_📚_Gösterge_Rehberi.py dosyasının GÜNCEL içeriği

import streamlit as st

st.set_page_config(page_title="Gösterge Rehberi", page_icon="📚")

st.title("📚 Teknik Analiz Rehberi")
st.write("""
Bu sayfada, analiz aracımızda gördüğünüz grafik unsurlarının ve teknik göstergelerin 
ne anlama geldiğini ve nasıl yorumlanması gerektiğini bulabilirsiniz.
""")

st.header("", divider='rainbow')

# === YENİ EKLENEN BÖLÜM: MUM GRAFİKLERİ ===
with st.expander("🕯️ Fiyat Grafiğini Anlamak: Mum Çubukları (Candlesticks)", expanded=True):
    st.subheader("Hisse Senedinin Asıl Fiyatı Hangisi?")
    st.write("""
    Grafikte hisse senedinin asıl fiyatını gösteren tek bir çizgi yoktur. Fiyatın kendisi, grafikte gördüğünüz **yeşil ve kırmızı renkli çubukların (mumların) tamamıdır.** 
    
    Her bir mum çubuğu, seçilen bir zaman dilimindeki (genellikle **bir gün**) fiyat hareketlerinin özetidir ve bize 4 önemli bilgi verir:
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.success("#### YÜKSELİŞ Mumu (Yeşil)")
        st.write("**Anlamı:** Kapanış fiyatı, açılış fiyatından daha **yüksek**.")
        st.markdown("""
        - **Üst Fitil Ucu:** O gün ulaşılan *en yüksek* fiyat.
        - **Gövde Üstü:** Kapanış fiyatı.
        - **Gövde Altı:** Açılış fiyatı.
        - **Alt Fitil Ucu:** O gün görülen *en düşük* fiyat.
        """)

    with col2:
        st.error("#### DÜŞÜŞ Mumu (Kırmızı)")
        st.write("**Anlamı:** Kapanış fiyatı, açılış fiyatından daha **düşük**.")
        st.markdown("""
        - **Üst Fitil Ucu:** O gün ulaşılan *en yüksek* fiyat.
        - **Gövde Üstü:** Açılış fiyatı.
        - **Gövde Altı:** Kapanış fiyatı.
        - **Alt Fitil Ucu:** O gün görülen *en düşük* fiyat.
        """)
    
    st.info("""
    **Özetle:** Grafiğe bakarken tek bir çizgi aramak yerine, yeşil ve kırmızı mumların dizisinin anlattığı hikayeyi okursunuz. Bu hikaye size alıcıların mı yoksa satıcıların mı daha güçlü olduğunu gösterir.
    """, icon="💡")


# --- RSI Açıklaması ---
with st.expander("🔵 RSI (Göreceli Güç Endeksi)"):
    st.subheader("Ne İşe Yarar?")
    st.write("""
    RSI, bir hisse senedinin fiyat hareketlerinin **hızını ve değişimini** ölçer. Temel amacı, hissenin **"Aşırı Alım"** mı yoksa **"Aşırı Satım"** mı olduğunu tespit etmektir. 0 ile 100 arasında bir değer alır.
    """)
    
    st.subheader("Nasıl Yorumlanır?")
    st.info("""
    - **70 Seviyesi ve Üzeri (Aşırı Alım):** Hissenin çok fazla ve çok hızlı alındığı, fiyatların aşırı şiştiği anlamına gelir. Bu bölgede bir **düzeltme veya düşüş** beklenebilir.
    
    - **30 Seviyesi ve Altı (Aşırı Satım):** Hissenin çok fazla ve çok hızlı satıldığı, fiyatların aşırı düştüğü anlamına gelir. Bu bölgeden bir **tepki yükselişi** beklenebilir.
    
    - **30-70 Arası:** Piyasanın dengede veya kararsız olduğunu gösterir. Tek başına net bir sinyal üretmez.
    """)

# --- MACD Açıklaması ---
with st.expander("🟢 MACD (Hareketli Ortalama Yakınsama/Iraksama)"):
    st.subheader("Ne İşe Yarar?")
    st.write("""
    MACD, bir hissenin **trendinin yönünü ve momentumunu (gücünü)** belirlemek için kullanılır. İki farklı hareketli ortalama arasındaki ilişkiyi gösterir.
    """)

    st.subheader("Nasıl Yorumlanır?")
    st.success("""
    - **AL Sinyali (Altın Kesişim):** Mavi renkli **MACD çizgisi**, turuncu renkli **Sinyal çizgisini** aşağıdan yukarıya doğru kestiğinde oluşur. Bu, yükseliş momentumunun başladığına işaret eder.
    
    - **SAT Sinyali (Ölüm Kesişimi):** Mavi renkli **MACD çizgisi**, turuncu renkli **Sinyal çizgisini** yukarıdan aşağıya doğru kestiğinde oluşur. Bu, düşüş momentumunun başladığına işaret eder.
    
    - **Çizgiler Arasındaki Alan:** Alan ne kadar genişlerse, mevcut trendin o kadar güçlü olduğu anlaşılır.
    """)

# --- Hareketli Ortalamalar (SMA & EMA) ---
with st.expander("🔴 Hareketli Ortalamalar (SMA ve EMA)"):
    st.subheader("Ne İşe Yararlar?")
    st.write("""
    Hareketli ortalamalar, fiyat grafiğindeki dalgalanmaları yumuşatarak ana **trendin yönünü** daha net görmemizi sağlar. Fiyatların (mumların) ortalamanın üzerinde olması genellikle bir yükseliş, altında olması ise bir düşüş sinyali olarak kabul edilir.
    """)

    st.subheader("Farkları Nedir?")
    st.warning("""
    - **SMA (Basit Hareketli Ortalama):** Belirlenen periyottaki (örn: 20 gün) tüm fiyatların aritmetik ortalamasını alır. Trendi daha yavaş takip eder.
    
    - **EMA (Üssel Hareketli Ortalama):** Hesaplamada son günlerdeki fiyatlara daha fazla ağırlık verir. Bu yüzden fiyat değişimlerine daha **hızlı tepki verir** ve daha hassastır.
    """)

# --- Bollinger Bantları ---
with st.expander("⚪ Bollinger Bantları (BB)"):
    st.subheader("Ne İşe Yarar?")
    st.write("""
    Bollinger Bantları, bir hissenin **volatilitesini (oynaklığını)** ölçmek için kullanılır. Ortada bir hareketli ortalama (genellikle 20-günlük SMA) ve onun altında/üstünde iki standart sapma çizgisi bulunur.
    """)

    st.subheader("Nasıl Yorumlanır?")
    st.info("""
    - **Bantların Daralması:** Volatilitenin düştüğünü ve yakında **sert bir fiyat hareketinin** (yukarı veya aşağı) gelebileceğini gösterir. "Fırtına öncesi sessizlik" olarak yorumlanabilir.
    
    - **Bantların Genişlemesi:** Volatilitenin arttığını gösterir. Genellikle sert bir hareket sonrası bantlar genişler.
    
    - **Fiyatın Bantlara Teması:** Fiyatların üst banda değmesi "aşırı alım", alt banda değmesi ise "aşırı satım" olarak yorumlanabilir. Fiyatların genellikle bantlar arasında hareket etmesi beklenir.
    """)