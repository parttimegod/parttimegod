# Bu projeyi mülakatta savunmak

Kodun tamamını ezberleme. Aşağıdaki kararları SQL'i göstererek açıklayabil.

1. **Tablonun grain'i ne?** Bir müşteri × bir ay. Subscription join'inden
   sonra neden önce bu düzeyde SUM aldığımızı ve COUNT'un aksi hâlde
   nasıl şişeceğini göster.
2. **LAG niye doğrudan aktif abonelikler üzerinde çalışmıyor?** Aradaki
   iptal ayı yoksa önceki satır önceki ay değildir. Takvim ve müşteri
   cross join'i bu boşluğu sıfır gelirli bir satıra dönüştürüyor.
3. **Yeni müşteri ve geri dönen müşteri nasıl ayrılıyor?** Önceki ay sıfır
   olması tek başına yeterli değil; ilk ücretli ay olan cohort_month da gerekir.
4. **NRR büyürken toplam gelir düşebilir mi?** Yeni/geri dönen müşteriler
   NRR hesabına girmez. Açılış müşterilerinin gelirini takip ediyoruz.
   Bu fixture'da Şubat NRR'sini elle hesapla: 190 / 270.
5. **Cohort'un gelecek ayını niye sıfır yazmıyoruz?** Gözlem yok; kayıp
   müşteri bilgisi yok. Geleceği sıfır saymak yeni cohort'ları cezalandırır.
6. **İki kez veri yüklersem ne olur?** Doğal anahtar + ON CONFLICT aynı
   kayıtları günceller; ayrı load_run her yüklemeyi kaydeder. Kaynakta
   bulunmayan eski satırlar otomatik silinmez; bu tasarımın sınırını anlat.
7. **İndeks her sorguyu hızlandırır mı?** Tüm müşterileri/tüm ayları
   okuyan dönüşümde sequential scan makul olabilir. EXPLAIN planını
   görmeden performans yüzdesi iddia etme.

Pratik görev: modelden bakmadan aylık yeni müşteri, churn müşteri ve
geri dönen müşteri sayılarını ayrı FILTER koşullarıyla hesaplayan bir
sorgu yaz. Sonra ilk ayın NRR'sinin neden NULL olduğunu açıkla.

CV'de kullanabileceğin, ancak kodu ve bu kararları savunabildikten sonra
eklemen gereken proje cümlesi:

> Built a PostgreSQL/dbt subscription analytics pipeline with 5 SQL
> models, 20 data-quality tests and 5 hand-checked integration checks;
> reconciled MRR movements and cohort retention across 240,000 synthetic
> customer-month records.

Bu cümle bir portföy uygulamasını anlatır; üretim deneyimi veya SQL
uzmanlığı unvanı iddia etmez. dbt/SQL kodunu AI yardımıyla geliştirdiysen
mülakatta yaptığın doğrulamalar ve anlayabildiğin kararlar üzerinden konuş.
