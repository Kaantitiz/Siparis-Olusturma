import streamlit as st
import os

# Sayfa ayarları
st.set_page_config(
    page_title="Sipariş Çalışması :)",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS stilleri
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    
    .page-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        color: white;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .page-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.2);
    }
    
    .page-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .page-title {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .page-description {
        font-size: 1rem;
        opacity: 0.9;
        line-height: 1.4;
    }
    
    .info-box {
        border-radius: 10px;
        padding: 1.5rem;
        margin: 2rem 0;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Ana başlık
st.markdown('<h1 class="main-header">🏠 Sipariş Oluşturma Ana Sayfa</h1>', unsafe_allow_html=True)

# Açıklama
st.markdown("""
<div class="info-box">
    <h3>📋 Proje Hakkında</h3>
    <p>Bu proje, sipariş oluşturma ve yönetimi için geliştirilmiş araçları içerir. 
    Aşağıdaki sayfalardan birini seçerek işlemlerinizi gerçekleştirebilirsiniz.</p>
</div>
""", unsafe_allow_html=True)

# Sayfa kartları
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="page-card" onclick="window.location.href='/bosch_islemleri'">
        <div class="page-icon">🏭</div>
        <div class="page-title">BOSCH Sipariş İşlemleri</div>
        <div class="page-description">
            3 Excel dosyasından son.json formatında çıktı oluşturma. 
            BOSCH ürün kodları için özel işlemler ve depo kodu belirleme.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tıklanabilir buton
    if st.button("🏭 BOSCH İşlemleri Sayfasına Git", key="bosch_btn", use_container_width=True):
        st.switch_page("pages/bosch_islemleri.py")

with col2:
    st.markdown("""
    <div class="page-card" onclick="window.location.href='/SiparişOluşturma'">
        <div class="page-icon">⚡</div>
        <div class="page-title">Excel Dönüştürme Aracı</div>
        <div class="page-description">
            Ultra hızlı Excel dönüştürücü. 100.000+ satırlık dosyalar için optimize edilmiş. 
            Marka eşleştirme ve veri işleme.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tıklanabilir buton
    if st.button("⚡ Excel Dönüştürücü Sayfasına Git", key="excel_btn", use_container_width=True):
        st.switch_page("pages/SiparişOluşturma.py")

# Alt bilgi
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🚀 <strong>Sipariş Oluşturma Sistemi v1.0</strong></p>
    <p>Gelişmiş veri işleme ve sipariş yönetimi araçları</p>
    <p>Sipariş Çalışması sayfasının tüm hakları KT tarafından saklıdır.</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📚 Sayfa Bilgileri")
    
    st.subheader("🏭 BOSCH İşlemleri")
    st.write("• 3 Excel dosyası işleme")
    st.write("• son.json formatında çıktı")
    st.write("• Depo kodu belirleme")
    st.write("• BOSCH ürün kodları")
    
    st.markdown("---")
    
    st.subheader("⚡ Excel Dönüştürücü")
    st.write("• Ultra hızlı işleme")
    st.write("• Marka eşleştirme")
    st.write("• 100.000+ satır desteği")
    st.write("• Çoklu format desteği")
    
    st.markdown("---")
    
    st.header("🔧 Teknik Bilgiler")
    st.write("• Streamlit tabanlı")
    st.write("• Python 3.8+ gerekli")
    st.write("• Pandas & OpenPyXL")
    st.write("• Responsive tasarım")
