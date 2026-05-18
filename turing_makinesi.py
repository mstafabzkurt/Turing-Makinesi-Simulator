class TuringMakinesi:
    def __init__(self, bant_string):
        self.bant = list(bant_string) + ['B'] * 50 # Bantı biraz daha uzun tutalım
        self.kafa = 0
        self.durum = 'q0'
        self.kabul_durumu = 'q_accept'
        self.gecis_tablosu = {}
        self._tabloyu_olustur()

    def _tablo_ekle(self, durum, okunan, yeni_durum, yazilan, yon):
        self.gecis_tablosu[(durum, okunan)] = (yeni_durum, yazilan, yon)

    def _tabloyu_olustur(self):
        # --- BÖLÜM 1: BAŞLANGIÇ VE KARAR (Faz 1 & 2) ---
        for s in ['0', '1']:
            self._tablo_ekle('q0', s, 'q0', s, 'R')
            
        for s in ['0', '1', 'X', 'Y']:
            self._tablo_ekle('q1', s, 'q1', s, 'R')
        
        self._tablo_ekle('q0', '*', 'q1', '*', 'R')
        self._tablo_ekle('q1', '=', 'q2', '=', 'L')

        for s in ['X', 'Y']:
            self._tablo_ekle('q2', s, 'q2', s, 'L')
        
        self._tablo_ekle('q2', '0', 'q3', 'X', 'L') 
        self._tablo_ekle('q2', '1', 'q4', 'Y', 'L') 
        self._tablo_ekle('q2', '*', 'q_temizlik', 'B', 'R') 

        # --- BÖLÜM 2: KAYDIRMA / DOZER MODÜLÜ (Faz 4) ---
        for s in ['0', '1', 'X', 'Y', 'a', 'b']:
            self._tablo_ekle('q3', s, 'q3', s, 'L')
        self._tablo_ekle('q3', '*', 'q_tasi_*', '0', 'R') 

        tasinacaklar = ['0', '1', '*', '=', 'X', 'Y']
        for hafiza in tasinacaklar:
            durum_adi = f'q_tasi_{hafiza}'
            for okunan in tasinacaklar:
                self._tablo_ekle(durum_adi, okunan, f'q_tasi_{okunan}', hafiza, 'R')
            self._tablo_ekle(durum_adi, 'B', 'q_tur_sonu', hafiza, 'L') 

        for s in tasinacaklar:
            self._tablo_ekle('q_tur_sonu', s, 'q_tur_sonu', s, 'L')
        self._tablo_ekle('q_tur_sonu', 'B', 'q0', 'B', 'R') 

        # --- YENİ BÖLÜM 3: TOPLAMA MODÜLÜ (Ters Kayıt Mantığı) ---
        # 1. M'nin bitini bul ve işaretle (a veya b)
        for s in ['X', 'Y', '*', 'a', 'b']:
            self._tablo_ekle('q4', s, 'q4', s, 'L')
        self._tablo_ekle('q4', '0', 'q_add_0_find_pos', 'a', 'R')
        self._tablo_ekle('q4', '1', 'q_add_1_find_pos', 'b', 'R')
        self._tablo_ekle('q4', 'B', 'q_add_reset', 'B', 'R') # Toplama bitti!

        # 2. Sağa gidip '=' işaretini geç
        for state in ['q_add_0_find_pos', 'q_add_1_find_pos']:
            for s in ['0', '1', 'a', 'b', '*', 'X', 'Y']:
                self._tablo_ekle(state, s, state, s, 'R')
            self._tablo_ekle(state, '=', f"{state}_in_R", '=', 'R')

        # 3. Sonuç alanında işlenmiş bitleri (x, y) atla
        for state in ['q_add_0_find_pos_in_R', 'q_add_1_find_pos_in_R']:
            for s in ['x', 'y']:
                self._tablo_ekle(state, s, state, s, 'R')

        # 4. Hedef bit bulundu! (0 ekleme kuralları)
        self._tablo_ekle('q_add_0_find_pos_in_R', '0', 'q_add_return', 'x', 'L') 
        self._tablo_ekle('q_add_0_find_pos_in_R', '1', 'q_add_return', 'y', 'L') 
        self._tablo_ekle('q_add_0_find_pos_in_R', 'B', 'q_add_return', 'x', 'L') 

        # 5. Hedef bit bulundu! (1 ekleme kuralları)
        self._tablo_ekle('q_add_1_find_pos_in_R', '0', 'q_add_return', 'y', 'L') 
        self._tablo_ekle('q_add_1_find_pos_in_R', 'B', 'q_add_return', 'y', 'L') 
        self._tablo_ekle('q_add_1_find_pos_in_R', '1', 'q_add_carry', 'x', 'R') # 1+1=0 (Elde var 1 -> Sağa taşı!)

        # 6. Elde (Carry) işlemi sağa (boşluğa) doğru ilerler, '=' işaretine çarpmaz!
        self._tablo_ekle('q_add_carry', '0', 'q_add_return', '1', 'L')
        self._tablo_ekle('q_add_carry', 'B', 'q_add_return', '1', 'L')
        self._tablo_ekle('q_add_carry', '1', 'q_add_carry', '0', 'R') # Zincirleme elde

        # 7. M'ye geri dön
        for s in ['0', '1', 'x', 'y', '=', 'X', 'Y']:
            self._tablo_ekle('q_add_return', s, 'q_add_return', s, 'L')
        self._tablo_ekle('q_add_return', '*', 'q4', '*', 'L')

        # 8. Toplama bitince tüm a,b,x,y işaretlerini temizle
        for s in ['0', '1', '*', '=', 'X', 'Y']:
            self._tablo_ekle('q_add_reset', s, 'q_add_reset', s, 'R')
        self._tablo_ekle('q_add_reset', 'a', 'q_add_reset', '0', 'R')
        self._tablo_ekle('q_add_reset', 'b', 'q_add_reset', '1', 'R')
        self._tablo_ekle('q_add_reset', 'x', 'q_add_reset', '0', 'R')
        self._tablo_ekle('q_add_reset', 'y', 'q_add_reset', '1', 'R')
        
        # 9. Temizlik bitince Sola kaydır (Dozer modülüne bağlan)
        self._tablo_ekle('q_add_reset', 'B', 'q_return_to_q3', 'B', 'L')
        for s in ['0', '1', '=', 'X', 'Y']:
            self._tablo_ekle('q_return_to_q3', s, 'q_return_to_q3', s, 'L')
        self._tablo_ekle('q_return_to_q3', '*', 'q_tasi_*', '0', 'R')

        # --- BİTİŞ VE TEMİZLİK ---
        for s in ['X', 'Y']:
            self._tablo_ekle('q_temizlik', s, 'q_temizlik', 'B', 'R') 
        for s in ['0', '1']:
            self._tablo_ekle('q_temizlik', s, 'q_temizlik', s, 'R')
        self._tablo_ekle('q_temizlik', '=', 'q_accept', '=', 'R') 
        self._tablo_ekle('q_temizlik', 'B', 'q_accept', 'B', 'R')

    def bandi_yazdir(self):
        bant_str = "".join(self.bant).rstrip('B')
        if not bant_str:
            bant_str = "B"
        print(f"Bant: [{bant_str}]")
        print(" " * (self.kafa + 7) + "^")

    def calistir(self):
        adim = 1
        print("\n--- TURING MAKİNESİ SİMÜLASYONU BAŞLIYOR ---")
        while self.durum != self.kabul_durumu:
            if self.kafa == len(self.bant):
                self.bant.append('B')
                
            okunan_sembol = self.bant[self.kafa]
            gecis_anahtari = (self.durum, okunan_sembol)

            if gecis_anahtari not in self.gecis_tablosu:
                print(f"\nHATA: Tanımsız geçiş! Durum: {self.durum}, Okunan: {okunan_sembol}")
                break

            yeni_durum, yazilan_sembol, yon = self.gecis_tablosu[gecis_anahtari]

            print(f"\nAdım {adim}:")
            print(f"Mevcut Durum: {self.durum} | Okunan: {okunan_sembol} | Yazılan: {yazilan_sembol} | Yön: {yon}")
            
            self.bant[self.kafa] = yazilan_sembol
            self.durum = yeni_durum
            
            if yon == 'R':
                self.kafa += 1
            elif yon == 'L':
                self.kafa -= 1
                if self.kafa < 0:
                    self.bant.insert(0, 'B')
                    self.kafa = 0

            self.bandi_yazdir()
            adim += 1
            
        print("\n--- İŞLEM TAMAMLANDI ---")

    def sonucu_getir(self):
        bant_str = "".join(self.bant).rstrip('B')
        if '=' in bant_str:
            sonuc_binary = bant_str.split('=')[1].replace('B', '')
            # TURING MAKİNESİ SONUCU TERS (REVERSE) YAZDIĞI İÇİN BURADA DÜZELTİYORUZ
            sonuc_binary = sonuc_binary[::-1] 
            if sonuc_binary == '':
                return "0"
            return sonuc_binary
        return "Sonuç Bulunamadı"

def main():
    print("Turing Makinesi - Binary Çarpma (Shift & Add)")
    
    while True:
        sayi1 = input("Birinci binary sayıyı girin (multiplicand): ")
        if all(c in '01' for c in sayi1):
            break
        print("Hata: Sadece 0 ve 1 kullanabilirsiniz!")
        
    while True:
        sayi2 = input("İkinci binary sayıyı girin (multiplier): ")
        if all(c in '01' for c in sayi2):
            break
        print("Hata: Sadece 0 ve 1 kullanabilirsiniz!")

    bant_girdisi = f"{sayi1}*{sayi2}="
    print(f"\nBaşlangıç Bant Formatı: {bant_girdisi}")
    print("\n[BİLGİ] Makine, basamak kaymalarını önlemek için sonucu bantta TERS yazar.")
    print("[BİLGİ] Okuma sırasında Python bu formatı standart binary'ye çevirir.")

    tm = TuringMakinesi(bant_girdisi)
    tm.calistir()

    binary_sonuc = tm.sonucu_getir()
    try:
        decimal_sonuc = int(binary_sonuc, 2)
    except ValueError:
        decimal_sonuc = 0

    print("\n" + "="*30)
    print(f"BEKLENEN ÇIKTI")
    print(f"İşlem: {sayi1} * {sayi2}")
    print(f"Sonuç (Binary):  {binary_sonuc}")
    print(f"Sonuç (Decimal): {decimal_sonuc}")
    print("="*30)

if __name__ == "__main__":
    main()
