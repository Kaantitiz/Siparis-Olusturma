# 🚀 Sipariş Oluşturma Sistemi

Bu proje, sipariş oluşturma ve yönetimi için geliştirilmiş gelişmiş araçları içerir. Streamlit tabanlı web uygulaması olarak tasarlanmıştır.

## 📋 Özellikler

### 🏭 BOSCH Sipariş İşlemleri
- 3 Excel dosyasından son.json formatında çıktı oluşturma
- BOSCH ürün kodları için özel işlemler
- Depo kodu belirleme
- Gelişmiş veri doğrulama

### ⚡ Excel Dönüştürme Aracı
- Ultra hızlı Excel dönüştürücü
- 100.000+ satırlık dosyalar için optimize edilmiş
- Marka eşleştirme (Schaeffler, ZF, Delphi, Valeo, Filtron, Mann, Bosch)
- Paralel işleme desteği
- Çoklu format desteği

## 🛠️ Teknolojiler

- **Python 3.8+**
- **Streamlit** - Web arayüzü
- **Pandas** - Veri işleme
- **OpenPyXL** - Excel işlemleri
- **XlsxWriter** - Gelişmiş Excel formatları
- **NumPy** - Sayısal işlemler

## 📦 Kurulum

### Gereksinimler
```bash
pip install -r requirements.txt
```

### Çalıştırma
```bash
streamlit run main.py
```

## 📁 Proje Yapısı

```
Sipariş Oluşturma/
├── main.py                          # Ana sayfa
├── pages/
│   ├── bosch_islemleri.py          # BOSCH işlemleri
│   └── SiparişOluşturma.py         # Excel dönüştürücü
├── requirements.txt                 # Python bağımlılıkları
├── .gitignore                      # Git ignore dosyası
└── README.md                       # Bu dosya
```

## 🔧 Kullanım

### Ana Sayfa
Ana sayfa, iki ana modül arasında geçiş yapmanızı sağlar:
- BOSCH Sipariş İşlemleri
- Excel Dönüştürme Aracı

### BOSCH İşlemleri
1. 3 Excel dosyasını yükleyin:
   - Bakiye Raporu
   - Inbound Excel
   - Sipariş Kalemleri
2. "BOSCH İşlemi Yap" butonuna tıklayın
3. son.json formatında çıktıyı indirin

### Excel Dönüştürücü
1. Ana Excel dosyasını yükleyin
2. İsteğe bağlı olarak 8 farklı marka Excel dosyasını yükleyin
3. "Ultra Hızlı Marka Eşleştirme Yap" butonuna tıklayın
4. Dönüştürülmüş veriyi indirin

## 📊 Desteklenen Markalar

- **Schaeffler LUK** - Tedarikçi bakiye işleme
- **ZF İthal** - LEMFÖRDER, TRW, SACHS markaları
- **ZF Yerli** - LEMFÖRDER, TRW, SACHS markaları
- **Delphi** - Tedarikçi bakiye işleme
- **Valeo** - Tedarikçi bakiye işleme
- **Filtron** - Tedarikçi bakiye işleme
- **Mann** - Tedarikçi bakiye işleme
- **Bosch** - Depo ve tedarikçi bakiye işleme

## 🚀 Performans Özellikleri

- **Cache Sistemi** - Hızlı veri erişimi
- **Paralel İşleme** - Çoklu marka eşleştirme
- **Vektörel İşlemler** - Pandas optimizasyonu
- **Bellek Yönetimi** - Büyük dosyalar için optimize edilmiş

## 🔍 Hata Ayıklama

### Cache Temizleme
Eğer uygulama hata verirse:
1. "Cache Temizle" butonuna tıklayın
2. Sayfayı yenileyin
3. Gerekirse "Sayfayı Yeniden Başlat" butonunu kullanın

### Log Mesajları
Uygulama, tüm işlem adımlarını detaylı olarak gösterir:
- ✅ Başarılı işlemler
- ⚠️ Uyarılar
- ❌ Hatalar
- 🔍 Debug bilgileri

## 📝 Lisans

Bu proje özel kullanım için geliştirilmiştir. Tüm hakları KT tarafından saklıdır.

## 🤝 Katkıda Bulunma

1. Projeyi fork edin
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Branch'inizi push edin (`git push origin feature/AmazingFeature`)
5. Pull Request oluşturun

## 📞 İletişim

Proje hakkında sorularınız için:
- GitHub Issues kullanın
- Proje sahibi ile iletişime geçin

## 🔄 Güncellemeler

### v1.0
- İlk sürüm
- BOSCH işlemleri
- Excel dönüştürücü
- Marka eşleştirme sistemi
- Ultra hızlı performans optimizasyonu

---

**Not:** Bu proje, sipariş yönetimi süreçlerini otomatikleştirmek ve hızlandırmak için tasarlanmıştır. Büyük veri setleri için optimize edilmiştir.
