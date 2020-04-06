# License: MPL-v2
# Made by github.com/electricalgorithm

import tabula;
import pandas;

def derslerKodCevirici(kod):
    return {
        'bm': "biyolojiMezun",
        'km': "kimyaMezun",
        'fm': "fizikMezun",
        'mm': "matematikMezun",
	'k11': "kimya11",
	'k10': "kimya10",
	'f11': "fizik11",
	'b11': "biyoloji11"
    }.get(kod, "HATA");

def cevapAnahtari(ders, test):
    # Ders kod olarak, test sayı olarak alınacaktır.
    ders = derslerKodCevirici(ders);
    if (ders == "HATA"):
        print("\n\tHATA: Seçtiğiniz dersin cevap anahtarı bulunamadı!\n");
    else:
        out_dataFrame = tabula.read_pdf(f"./cevapAnahtarlari/{ders}CA.pdf", encoding="utf-8", pages="1", output_format="dataframe", pandas_options={'header': None});
        out_Matrix = out_dataFrame[0].to_numpy();
        try:
            return (out_Matrix[test-1]);
        except IndexError as err:
            print("\n\tHATA:Girdiğiniz test sayısına ait bir test bulunamadı.\n")
            print(err);

def kontrol(cevaplar, cevapanahtari):
    # Cevap anahtarından gelen değerleri düzeltmek için:
    for index in cevapanahtari:
        if (pandas.isnull(index)):
            cevapanahtari = cevapanahtari[0:-1:1];
            continue;
    for index in range(len(cevapanahtari)):
        if index == 0: continue;
        yeniDeger = [];
        for jindex in range(len(cevapanahtari[index])):
            if (jindex > 2):
                if (cevapanahtari[index][jindex].isspace()):
                    continue;
                yeniDeger.append(cevapanahtari[index][jindex]);
        cevapanahtari[index] = "".join(yeniDeger);
    cevapanahtari = cevapanahtari[1:];

    # Kontrol etmenin asıl döndüğü yer:
    dogruSayisi = 0;
    yanlisSayisi = 0;
    bosSayisi = 0;
    print("\n");
    for index in range(len(cevapanahtari)):
        if (cevaplar[index] == cevapanahtari[index]):
            dogruSayisi += 1;
        elif (cevaplar[index] != cevapanahtari[index]):
            if (cevaplar[index] == "O"):
                bosSayisi += 1;
            else:
                yanlisSayisi += 1;
                soruSayisi = index+1;
                gercekDeger = cevapanahtari[index];
                yanitDeger = cevaplar[index];
                print(f"\t# Soru {soruSayisi} yanlış! Yanıt: {yanitDeger}, Doğrusu: {gercekDeger}");
    print("-"*10);
    print(f"Doğru sayısı: {dogruSayisi}, Yanlış sayısı: {yanlisSayisi}, Boş sayısı: {bosSayisi}");
    print("## -> Net:", (dogruSayisi - yanlisSayisi/4), "  -> Doğruluk yüzdesi: %", (dogruSayisi*100/len(cevapanahtari)), "\n");


print("""
# -------------------------------- #
# ------ Kazanım Testleri Çözücü - #
# -------------------------------- #
# Bu program ile ÖDSGM'nin sitesi- #
# nde yer alan testleri çözebilir  #
# ve kontrol ettirebilirsiniz.     #
# -------------------------------  #
#   Çıkmak için "kapat" yazınız.   #
""");

while (True):
    dersTest = input("dersKodu:testSayısı şeklinde giriniz ~> ").lower();

    # Programdan çıkış için tanımlanmış komut:
    if (dersTest == "kapat"): break;
    # Ders kodu ve soru sayısının toplam karakter sayısı -> B11:12'dir. -> 4 karakter.
    if (len(dersTest) > 5):
        print("\n\tGirdiğiniz komutta hata vardır. Lütfen tekrar deneyiniz.\n");
        continue;
    # Eğer dersTest'teki test sayısı, integer değilse hata verecek:
    try:
        dersKodu = dersTest[0];
        testSayisi = int(dersTest[2::]);
        print("\nCevap girme formatı: ABCDEAACDE (...)")
        print("Cevabını bilmediğiniz soru için 'O' giriniz.")
        yanitlar = input("\nCevaplarınızı giriniz ~> ").upper();
        yanitListesi = list(yanitlar);
        kontrol(yanitListesi, cevapAnahtari(dersKodu, testSayisi));
    except ValueError as err:
        print("\n\tGirdiğiniz komutta hata vardır. Lütfen tekrar deneyiniz.\n");
        print(err);
