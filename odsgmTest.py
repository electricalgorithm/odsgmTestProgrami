# License: MPL-v2
# Made by github.com/electricalgorithm
import tabula;
import pandas;
from datetime import datetime;
from datetime import timedelta;

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

def kontrol(cevaplar, cevapanahtari, gecenSure):
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

    # Test sonuçlarının yazdılırma kısmı aşağıdadır.
    cvpAnahtariSoruSayisi = len(cevapanahtari);
    dogrulukYuzdesi = round(dogruSayisi*100/cvpAnahtariSoruSayisi, 2);
    ortalamaSure = round(gecenSure.total_seconds()/cvpAnahtariSoruSayisi, 2);
    netMiktarı = dogruSayisi - yanlisSayisi/4;
    print(f"""
    {"-"*10}Test Sonuçları{"-"*10}
    * Doğru Sayısı: {dogruSayisi}, Yanlış Sayısı: {yanlisSayisi}, Boş sayısı: {bosSayisi}
    * ---- Netiniz: {netMiktarı}
    * ---- Doğruluk yüzdeniz: %{dogrulukYuzdesi}

    * {cvpAnahtariSoruSayisi} soruluk testi çözmek için harcadığınız süre: {gecenSure}
    * ---- Soru başı harcanan ortalama süre: {ortalamaSure} saniye
    """);


print(f"""
{"-"*35}
|     Kazanım Testleri Çözücü     |
|  -  -  -  -  -  -  -  -  -  -   |
|Bu program, MEB'e bağlı ODSGM ta-|
|rafından yayınlanan testlerin ce-|
|vap anahtarına bakılarak kontrol |
|edilmesinin zorluğunu gidermek   |
|adına yazılmıştır. Benim gibi tüm|
|öğrencilere yararlı olması dileği|
|ile...                           |
|                                 |
| Lisans: MPL-2.0                 |
| Fikir sahibi: electricalgorithm |
|                                 |
| # Test Kodları                  |
| "[ders baş harfi]+[sınıf]"      |
| örn. bm -> Biyoloji Mezun       |
|      f11 -> Fizik 11. Sınıf     |
|                                 |
| Programdan çıkmak için "kapat"  |
| komutunu girebilirsiniz.        |
{"-"*35}
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
        dersTest = dersTest.split(':');
        dersKodu = dersTest[0];
        testSayisi = int(dersTest[1]);
        print("\n## Cevap girme formatı: ABCDEAACDE (...)")
        print("## Cevabını bilmediğiniz soru için 'O' giriniz.")
        # Süre burada başlatılacaktır.
        baslangicZamani = datetime.now()
        yanitlar = input("\nCevaplarınızı giriniz ~> ").upper();
        bitisZamani = datetime.now();
        # Süre burada bitirilecektir.
        yanitListesi = list(yanitlar);
        kontrol(yanitListesi, cevapAnahtari(dersKodu, testSayisi), (bitisZamani - baslangicZamani));
    except ValueError as err:
        print("\n\tGirdiğiniz komutta hata vardır. Lütfen tekrar deneyiniz.\n");
        print(err);
