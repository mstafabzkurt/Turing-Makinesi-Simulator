# Turing Makinesi ile Binary Çarpma (Shift & Add) ⚙️

Bu proje, modern işlemcilerin aritmetik mantık birimlerinde (ALU) yaygın olarak kullanılan **"Kaydır ve Topla" (Shift and Add)** algoritmasını, tek bantlı (single-tape) bir Turing Makinesi üzerinde simüle eden bir Python programıdır.

Özdevinirler Kuramı (Automata Theory) prensiplerine uygun olarak geliştirilen bu simülatör, rastgele erişimli belleği (RAM) olmayan deterministik bir sistemde karmaşık aritmetik işlemlerin ve bellek yönetiminin nasıl modellenebileceğini göstermektedir.

## 🎯 Özellikler

* **Tek Bantlı Simülasyon:** Yalnızca okuma, yazma ve sağa/sola hareket yetenekleriyle tam Turing simülasyonu.
* **Modüler Mimari:** Algoritma; Karar Verme, Blok Kaydırma (Dozer) ve İkili Toplama (Add) olmak üzere üç bağımsız duruma (state) ayrıştırılmıştır.
* **Veri Bütünlüğü Koruması:** `Çarpılan * Çarpan =` formatındaki giriş bandı, işlemler sırasında özel taşıma algoritmalarıyla korunur.
* **Ters Kayıt (Reverse Store) Mimarisi:** Toplama işlemi sırasında oluşan elde (carry) bitlerinin bant üzerindeki sınır işaretlerini (örn. `=` işareti) ezmesini engellemek için, sonuç bant üzerine ters LSB-MSB yönünde yazılır ve okuma anında düzeltilir.
* **Adım Adım İzleme:** Makinenin durum geçişleri, okuma/yazma eylemleri ve kafa hareketleri terminal üzerinden adım adım izlenebilir.

## 🧠 Çalışma Mantığı

Makine aşağıdaki adımları sürekli bir döngü halinde işler:
1.  **Bul ve Oku:** `=` işaretini bulur, sola kayar ve çarpanın ilk işlenmemiş bitini (`0` veya `1`) okuyup geçici olarak işaretler (`X` veya `Y`).
2.  **Karar:** Eğer okunan bit `1` ise Toplama modülüne gider, `0` ise atlar.
3.  **Topla (Opsiyonel):** 1. sayının (multiplicand) bitlerini tek tek `=` ötesine taşır ve ikili matematik kurallarıyla ekler.
4.  **Kaydır (Zorunlu Shift):** 1. sayının sonuna `0` ekler. Bant formatının bozulmaması için geri kalan tüm verileri (*, 2. sayı ve =) dozer mantığıyla birer hücre sağa kaydırır.
5.  **Döngü ve Temizlik:** İşlenmemiş çarpan biti kalmayana kadar başa döner. Bittiğinde geçici sembolleri temizler ve kabul durumuna (`q_accept`) geçer.

