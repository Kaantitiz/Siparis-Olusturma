import streamlit as st
import pandas as pd
import json
import io
from datetime import datetime
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, PatternFill

# Sayfa ayarları
st.set_page_config(
    page_title="Sipariş Çalışması :)",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Başlık
st.title("🏭 BOSCH Sipariş İşlemleri")
st.caption("3 Excel dosyasından son.json formatında çıktı oluşturma")

# Global değişkenler
if 'process_bosch' not in st.session_state:
    st.session_state.process_bosch = False

def process_bosch_codes(bosch_ref):
    """Bosch ürün kodlarını işle - başına 3E- ekle ve boşlukları temizle"""
    if pd.isna(bosch_ref):
        return ''
    
    code_str = str(bosch_ref).strip()
    
    # Boşlukları temizle
    code_str = code_str.replace(' ', '')
    
    # Başında 3E- yoksa ekle
    if not code_str.startswith('3E-'):
        code_str = '3E-' + code_str
    
    return code_str

def determine_depot_code(siparis_notu):
    """Sipariş Notu'ndan depo kodunu belirle - sadece belirli kodlar"""
    if pd.isna(siparis_notu) or siparis_notu == "":
        return ""
    
    siparis_str = str(siparis_notu).strip()
    
    # Sipariş Notu'ndan ilk 3 karakteri al (depo kodu)
    if len(siparis_str) >= 3:
        depo_kodu = siparis_str[:3].lower()  # Küçük harfe çevir
        
        # Sadece belirli depo kodlarını kabul et
        allowed_codes = ['aas', 'das', 'mas', 'bas', 'eas']
        
        if depo_kodu in allowed_codes:
            return depo_kodu
        else:
            # Geçersiz depo kodu için boş string döndür
            return ""
    
    return ""

def create_sutun1(siparis_notu, bosch_no):
    """Sütun1 oluştur - Sipariş Notu + Bosch No birleşimi"""
    siparis_str = str(siparis_notu) if pd.notna(siparis_notu) else ""
    bosch_str = str(bosch_no) if pd.notna(bosch_no) else ""
    
    # Boşlukları temizle ve birleştir
    siparis_clean = siparis_str.replace(' ', '')
    bosch_clean = bosch_str.replace(' ', '')
    
    return siparis_clean + bosch_clean

def process_bosch_three_excel():
    """BOSCH için 3-Excel işlemi - son.json formatında çıktı"""
    try:
        # Excel dosyalarını kontrol et
        if not bakiye_raporu or not inbound_excel or not siparis_kalemleri:
            st.error("⚠️ BOSCH işlemi için 3 Excel dosyası da yüklenmelidir!")
            return None
        
        # 1. ADIM: Bakiye Raporu işleme
        with st.spinner("📊 Bakiye Raporu işleniyor..."):
            bakiye_df = pd.read_excel(bakiye_raporu, engine='openpyxl')
            
            # Bakiye raporunda gerekli kolonları kontrol et
            required_cols_bakiye = ['Sipariş Notu', 'Ürün Grubu', 'Bosch No', 'Fatura ve Sevk Edilmemiş Toplam']
            missing_cols = [col for col in required_cols_bakiye if col not in bakiye_df.columns]
            if missing_cols:
                st.error(f"⚠️ Bakiye raporunda eksik kolonlar: {missing_cols}")
                return None
            
            # Bosch No'yu temizle - başına 3E- ekle ve boşlukları temizle
            bakiye_df['Bosch No'] = bakiye_df['Bosch No'].apply(process_bosch_codes)
            
            st.success(f"✅ Bakiye Raporu yüklendi: {len(bakiye_df)} satır")
            
            # Debug: Bakiye raporu analizi
            st.info(f"📊 Bakiye Raporu Analizi:")
            st.write(f"• Toplam satır: {len(bakiye_df)}")
            st.write(f"• Ürün Grubu dağılımı: {bakiye_df['Ürün Grubu'].value_counts().to_dict()}")
        
        # 2. ADIM: InBound Excel işleme
        with st.spinner("📦 InBound Excel işleniyor..."):
            inbound_df = pd.read_excel(inbound_excel, engine='openpyxl')
            
            # InBound'da gerekli kolonları kontrol et
            required_cols_inbound = ['Cari', 'Sipariş No', 'Ürün Kodu', 'İrsaliye Miktarı']
            missing_cols_inbound = [col for col in required_cols_inbound if col not in inbound_df.columns]
            if missing_cols_inbound:
                st.error(f"⚠️ InBound dosyasında eksik kolonlar: {missing_cols_inbound}")
                return None
            
            # Cari kolonunda BOSCH markası olan ürünleri filtrele
            bosch_pattern = r'BOSCH\s+SANAYİ\s+VE\s+TİCARET\s+A\.?\Ş\.?|BOSCH\s+SANAYI\s+VE\s+TICARET\s+A\.?\S\.?'
            bosch_inbound = inbound_df[inbound_df['Cari'].astype(str).str.contains(bosch_pattern, case=False, na=False, regex=True)]
            
            # Eğer regex ile bulamazsa basit arama yap
            if len(bosch_inbound) == 0:
                bosch_inbound = inbound_df[inbound_df['Cari'].astype(str).str.contains('BOSCH', case=False, na=False)]
            
            # Debug: Toplam InBound satır sayısı
            st.info(f"📊 InBound Excel Analizi:")
            st.write(f"• Toplam satır: {len(inbound_df)}")
            st.write(f"• BOSCH filtresi sonucu: {len(bosch_inbound)} satır")
            
            if len(bosch_inbound) > 0:
                # InBound verilerini bakiye raporuna ekle
                for _, row in bosch_inbound.iterrows():
                    new_row = {
                        'Sipariş Notu': row['Sipariş No'],
                        'Ürün Grubu': 'DEPO',  # InBound'dan gelenler için DEPO
                        'Bosch No': process_bosch_codes(row['Ürün Kodu']),
                        'Fatura ve Sevk Edilmemiş Toplam': row['İrsaliye Miktarı']
                    }
                    bakiye_df = pd.concat([bakiye_df, pd.DataFrame([new_row])], ignore_index=True)
                
                st.success(f"✅ InBound veriler eklendi: {len(bosch_inbound)} satır")
            else:
                st.warning("⚠️ InBound dosyasında BOSCH verisi bulunamadı!")
        
        # 3. ADIM: Sipariş Notu ve Bosch No kolonlarını birleştir
        with st.spinner("🔗 Veriler birleştiriliyor..."):
            # Sipariş Notu ve Bosch No kolonlarının içeriklerini boşluksuz olarak birleştir
            bakiye_df['Birleşik_Kod'] = (
                bakiye_df['Sipariş Notu'].astype(str).str.replace(' ', '') + 
                bakiye_df['Bosch No'].astype(str).str.replace(' ', '')
            )
            
            # Ürün Grubu güncellemesi: Bakiye raporundaki ürünler için TEDARİKÇİLER, InBound'dan gelenler için DEPO
            bakiye_df.loc[bakiye_df['Ürün Grubu'] != 'DEPO', 'Ürün Grubu'] = 'TEDARİKÇİ'
            
            st.success("✅ Veriler birleştirildi")
            
            # Debug: Birleştirme sonrası analiz
            st.info(f"📊 Birleştirme Sonrası Analiz:")
            st.write(f"• Toplam satır: {len(bakiye_df)}")
            st.write(f"• Ürün Grubu dağılımı: {bakiye_df['Ürün Grubu'].value_counts().to_dict()}")
        
        # 4. ADIM: Sipariş Kalemleri işleme
        with st.spinner("📋 Sipariş Kalemleri işleniyor..."):
            siparis_df = pd.read_excel(siparis_kalemleri, engine='openpyxl')
            
            # Sipariş kalemlerinde gerekli kolonları kontrol et
            required_cols_siparis = ['SIPARIS_NO', 'STOK_KODU', 'SIPARIS_MIKTARI', 'KALAN_MIKTAR']
            missing_cols_siparis = [col for col in required_cols_siparis if col not in siparis_df.columns]
            if missing_cols_siparis:
                st.error(f"⚠️ Sipariş Kalemleri dosyasında eksik kolonlar: {missing_cols_siparis}")
                return None
            
            # SIPARIS_NO ve STOK_KODU kolonlarının hücrelerini birleştir
            siparis_df['Siparis_Birlesik'] = (
                siparis_df['SIPARIS_NO'].astype(str).str.replace(' ', '') + 
                siparis_df['STOK_KODU'].astype(str).str.replace(' ', '')
            )
            
            st.success(f"✅ Sipariş Kalemleri yüklendi: {len(siparis_df)} satır")
        
        # 5. ADIM: Eşleştirme ve birleştirme
        with st.spinner("🔄 Eşleştirme yapılıyor..."):
            # Bakiye raporuna sipariş bilgilerini ekle
            for idx, bakiye_row in bakiye_df.iterrows():
                birlesik_kod = bakiye_row['Birleşik_Kod']
                
                # Sipariş kalemlerinde eşleşen satırları bul
                matching_siparis = siparis_df[siparis_df['Siparis_Birlesik'] == birlesik_kod]
                
                if len(matching_siparis) > 0:
                    # İlk eşleşen satırı al
                    siparis_row = matching_siparis.iloc[0]
                    bakiye_df.at[idx, 'SIPARIS_NO'] = siparis_row['SIPARIS_NO']
                    bakiye_df.at[idx, 'STOK_KODU'] = siparis_row['STOK_KODU']
                    bakiye_df.at[idx, 'SIPARIS_MIKTARI'] = siparis_row['SIPARIS_MIKTARI']
                    bakiye_df.at[idx, 'KALAN_MIKTAR'] = siparis_row['KALAN_MIKTAR']
                else:
                    # Eşleşme yoksa boş değerler
                    bakiye_df.at[idx, 'SIPARIS_NO'] = ''
                    bakiye_df.at[idx, 'STOK_KODU'] = ''
                    bakiye_df.at[idx, 'SIPARIS_MIKTARI'] = 0
                    bakiye_df.at[idx, 'KALAN_MIKTAR'] = 0
            
            st.success("✅ Eşleştirme tamamlandı")
        
        # 6. ADIM: son.json formatında çıktı oluştur
        with st.spinner("🔍 son.json formatında çıktı oluşturuluyor..."):
            # son.json formatında çıktı oluştur
            final_output = []
            filtered_count = 0
            
            for _, row in bakiye_df.iterrows():
                # Depo kodunu kontrol et
                depo_kodu = determine_depot_code(row['Sipariş Notu'])
                
                # Sadece geçerli depo kodlarına sahip verileri kabul et
                if depo_kodu:
                    # son.json formatında satır oluştur
                    son_row = {
                        'Sipariş Notu': str(row['Sipariş Notu']) if pd.notna(row['Sipariş Notu']) else "",
                        'Depo Kodu': depo_kodu,
                        'Ürün Grubu': str(row['Ürün Grubu']) if pd.notna(row['Ürün Grubu']) else "",
                        'Bosch No': str(row['Bosch No']) if pd.notna(row['Bosch No']) else "",
                        'Sütun1': create_sutun1(row['Sipariş Notu'], row['Bosch No']),
                        'Tahmini Teslim Tarihi': "",
                        'Fatura ve Sevk Edilmemiş Toplam': float(row['Fatura ve Sevk Edilmemiş Toplam']) if pd.notna(row['Fatura ve Sevk Edilmemiş Toplam']) else 0.0
                    }
                    
                    final_output.append(son_row)
                else:
                    filtered_count += 1
            
            # Final DataFrame oluştur
            final_df = pd.DataFrame(final_output)
            
            st.success(f"✅ son.json formatında çıktı oluşturuldu: {len(final_df)} satır")
            
            if filtered_count > 0:
                st.warning(f"⚠️ {filtered_count} satır geçersiz depo kodu nedeniyle filtrelendi")
            
            # son.json formatı analizi
            st.info(f"🎯 son.json Format Analizi:")
            st.write(f"• Toplam satır: {len(final_df)}")
            st.write(f"• Ürün Grubu dağılımı: {final_df['Ürün Grubu'].value_counts().to_dict()}")
            st.write(f"• Depo Kodu dağılımı: {final_df['Depo Kodu'].value_counts().to_dict()}")
            
            return final_df
                
    except Exception as e:
        st.error(f"❌ BOSCH işlemi hatası: {str(e)}")
        return None

def create_excel_file(df):
    """Excel dosyası oluştur - son.json formatında"""
    try:
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='BOSCH_Verileri', index=False)
            
            # Excel dosyasını al
            workbook = writer.book
            worksheet = writer.sheets['BOSCH_Verileri']
            
            # Sütun genişliklerini otomatik ayarla
            for column in worksheet.columns:
                max_length = 0
                column_letter = get_column_letter(column[0].column)
                
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
            
            # Başlık satırını formatla
            for cell in worksheet[1]:
                cell.font = Font(bold=True)
                cell.fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
                cell.font = Font(bold=True, color="FFFFFF")
        
        output.seek(0)
        
        # Dosya adı oluştur - son.json formatında
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"son_json_format_bosch_{timestamp}.xlsx"
        
        return output, filename
        
    except Exception as e:
        st.error(f"❌ Excel oluşturma hatası: {str(e)}")
        return None, None

def create_son_json(df):
    """son.json formatında JSON dosyası oluştur"""
    try:
        # DataFrame'i JSON formatına çevir
        json_data = df.to_dict('records')
        
        # JSON string oluştur
        json_string = json.dumps(json_data, indent=2, ensure_ascii=False)
        
        # BytesIO'ya yaz
        output = io.BytesIO()
        output.write(json_string.encode('utf-8'))
        output.seek(0)
        
        # Dosya adı oluştur
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"son_json_{timestamp}.json"
        
        return output, filename
        
    except Exception as e:
        st.error(f"❌ JSON oluşturma hatası: {str(e)}")
        return None, None

def create_analysis_report(df):
    """Analiz raporu oluştur"""
    try:
        st.subheader("📊 Analiz Raporu")
        
        # Genel istatistikler
        st.info(f"**Genel Bilgiler:**")
        st.write(f"• Toplam satır: {len(df)}")
        st.write(f"• Toplam kolon: {len(df.columns)}")
        
        # Ürün grubu dağılımı
        if 'Ürün Grubu' in df.columns:
            urun_grup_dagilim = df['Ürün Grubu'].value_counts()
            st.info(f"**Ürün Grubu Dağılımı:**")
            for grup, sayi in urun_grup_dagilim.items():
                st.write(f"• {grup}: {sayi} kayıt")
        
        # Depo dağılımı
        if 'Depo Kodu' in df.columns:
            depo_dagilim = df['Depo Kodu'].value_counts()
            st.info(f"**Depo Kodu Dağılımı:**")
            for depo, sayi in depo_dagilim.items():
                st.write(f"• {depo}: {sayi} kayıt")
        
        # Fatura toplamları
        if 'Fatura ve Sevk Edilmemiş Toplam' in df.columns:
            # Artık sayı olarak geldiği için direkt toplama yapabiliriz
            try:
                toplam_fatura = df['Fatura ve Sevk Edilmemiş Toplam'].sum()
                st.info(f"**Fatura Toplamları:**")
                st.write(f"• Toplam Fatura: {toplam_fatura:,.0f} adet")
            except Exception as e:
                st.info(f"**Fatura Toplamları:**")
                st.write(f"• Fatura verileri işlenirken hata: {str(e)}")
        
    except Exception as e:
        st.error(f"❌ Analiz raporu hatası: {str(e)}")

# Sidebar
with st.sidebar:
    st.header("📁 Excel Dosya Yükleme")
    
    # Excel dosyalarını yükle
    bakiye_raporu = st.file_uploader(
        "📊 Bakiye Raporu Excel",
        type=['xlsx', 'xls'],
        help="Bakiye raporu Excel dosyasını yükleyin"
    )
    
    inbound_excel = st.file_uploader(
        "📦 InBound Excel",
        type=['xlsx', 'xls'],
        help="InBound Excel dosyasını yükleyin"
    )
    
    siparis_kalemleri = st.file_uploader(
        "📋 Sipariş Kalemleri Excel",
        type=['xlsx', 'xls'],
        help="Sipariş kalemleri Excel dosyasını yükleyin"
    )
    
    st.markdown("---")
    
    # İşlem butonları
    if st.button("🚀 BOSCH Verilerini İşle", type="primary", use_container_width=True):
        if bakiye_raporu and inbound_excel and siparis_kalemleri:
            st.session_state.process_bosch = True
        else:
            st.error("⚠️ Tüm Excel dosyaları yüklenmelidir!")
    
    st.markdown("---")
    
    # KURALLAR AÇIKLAMASI
    st.header("📋 İŞLEM KURALLARI")
    st.info("""
    **1. Bakiye Raporu:**
    • Sipariş Notu, Ürün Grubu, Bosch No, Fatura ve Sevk Edilmemiş Toplam
    • Bosch No başına 3E- eklenir
    • Boşluklar temizlenir
    
    **2. InBound Excel:**
    • Cari kolonunda BOSCH markası olan ürünler
    • Sipariş No → Sipariş Notu'na eklenir
    • Ürün Kodu → Bosch No'ya eklenir
    • İrsaliye Miktarı → Fatura kolonuna eklenir
    • Ürün Grubu = DEPO olarak işaretlenir
    
    **3. Sipariş Kalemleri:**
    • SIPARIS_NO + STOK_KODU birleştirilir
    • Eşleşen veriler eklenir
    
    **4. Çıktı Formatı:**
    • son.json formatında Excel ve JSON
    • Depo Kodu = Sipariş Notu'dan ilk 3 karakter (küçük harf)
    • Sadece belirli depo kodları: aas, das, mas, bas, eas
    • Sütun1 = Sipariş Notu + Bosch No birleşimi
    • Geçersiz depo kodları filtrelenir
    """)
    
    st.markdown("---")
    
    # Dosya durumu
    uploaded_count = sum(1 for file in [bakiye_raporu, inbound_excel, siparis_kalemleri] if file is not None)
    st.write(f"**📁 Yüklenen Dosya:** {uploaded_count}/3")
    
    if uploaded_count == 3:
        st.success("✅ Tüm dosyalar hazır!")
    elif uploaded_count > 0:
        st.warning(f"⚠️ {uploaded_count}/3 dosya yüklendi")
    else:
        st.info("ℹ️ Lütfen Excel dosyalarını yükleyin")

# Ana işlem akışı
if st.session_state.get('process_bosch', False):
    st.session_state.process_bosch = False
    
    # BOSCH verilerini işle
    final_df = process_bosch_three_excel()
    
    if final_df is not None:
        st.success("🎉 BOSCH işlemi başarıyla tamamlandı!")
        
        # Sonuçları göster
        st.subheader("📊 İşlenen Veriler")
        st.dataframe(final_df, use_container_width=True)
        
        # Analiz raporu
        create_analysis_report(final_df)
        
        # Dosya oluşturma butonları
        col1, col2 = st.columns(2)
        
        with col1:
            # Excel dosyası oluştur - son.json formatında
            excel_output, excel_filename = create_excel_file(final_df)
            if excel_output:
                st.download_button(
                    label="📥 son.json Format Excel İndir",
                    data=excel_output,
                    file_name=excel_filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
        
        with col2:
            # JSON dosyası oluştur
            json_output, json_filename = create_son_json(final_df)
            if json_output:
                st.download_button(
                    label="📥 JSON Dosyasını İndir",
                    data=json_output,
                    file_name=json_filename,
                    mime="application/json",
                    use_container_width=True
                )
        
        # Veri kontrol butonları
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔍 JSON Veri Kontrolü", use_container_width=True):
                st.json(final_df.to_dict('records'))
        
        with col2:
            if st.button("📊 Format Kontrolü", use_container_width=True):
                st.info("🎯 son.json Format Kontrolü:")
                st.write(f"• Toplam satır: {len(final_df)}")
                st.write(f"• Toplam kolon: {len(final_df.columns)}")
                st.write(f"• Kolonlar: {list(final_df.columns)}")
                
                # Örnek satır göster
                if len(final_df) > 0:
                    st.write("**Örnek Satır:**")
                    st.json(final_df.iloc[0].to_dict())

# Sayfa sonu
st.markdown("---")
st.markdown("*BOSCH Sipariş İşlemleri v3.0 - son.json Format*")
