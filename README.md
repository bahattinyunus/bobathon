<img src="assets/bob.png" alt="Bob, güler yüzlü mavi baretli robot" width="120" align="right">

# IBM Bob · Eyleyen Yapay Zekâ İş Başında (Agentic AI in Action)

> **Üniversite öğrencileri ve geliştiriciler için uygulamalı, otonom yapay zekâ atölye ve geliştirme platformu.**  
> Yapay zekâyı salt bir otomatik kod tamamlama (autocomplete) aracı olarak değil; planlayan, izin isteyerek hareket eden, kod yazan, senaryoları çözen ve testlerle doğrulanıp denetlenen bir **Ajanik Ortak (Agentic Partner)** olarak kullanıyoruz.

---

## 📌 İçindekiler
1. [Proje Hakkında ve Genel Bakış](#proje-hakkında-ve-genel-bakış)
2. [Depo Mimarisi ve Klasör Yapısı](#depo-mimarisi-ve-klasör-yapısı)
3. [Tamamlanan Kapsamlı Geliştirmeler](#tamamlanan-kapsamlı-geliştirmeler)
   - [Senaryo 1: Karmaşık Notlardan İnteraktif Çalışma Sayfasına](#senaryo-1-karmaşık-notlardan-interaktif-çalışma-sayfasına)
   - [Senaryo 2: Otomatik Ödev Değerlendirici ve Güvenli Mod](#senaryo-2-otomatik-ödev-değerlendirici-ve-güvenli-mod)
   - [Senaryo 3: Sıfırdan Programlama Dili: RouteQL](#senaryo-3-sıfırdan-programlama-dili-routeql)
   - [Senaryo 4: Modül Taşınabilirliği: JavaScript/Node Portu](#senaryo-4-modül-taşınabilirliği-javascriptnode-portu)
   - [Senaryo 5: Eski Kod Tabanı Analizi: Kiosk Router](#senaryo-5-eski-kod-tabanı-analizi-kiosk-router)
   - [Senaryo 6: 4 Haftalık Çevik Proje ve Sprint Planı](#senaryo-6-4-haftalık-çevik-proje-ve-sprint-planı)
   - [Senaryo 7: Mülakat Görevi: Çalışma Saatleri Çözücü](#senaryo-7-mülakat-görevi-çalışma-saatleri-çözücü)
   - [CampusRoute Uygulama Çekirdeği İyileştirmeleri](#campusroute-uygulama-çekirdeği-iyileştirmeleri)
4. [Hızlı Başlangıç ve Çalıştırma Kılavuzu](#hızlı-başlangıç-ve-çalıştırma-kılavuzu)
5. [Test Takımı ve Doğrulama](#test-takımı-ve-doğrulama)
6. [Katı Kurallar ve Tasarım İlkeleri](#katı-kurallar-ve-tasarım-ilkeleri)
7. [Takım Çalışması ve Katkı Rehberi](#takım-çalışması-ve-katkı-rehberi)

---

## Proje Hakkında ve Genel Bakış

Bu depo, gerçekçi bir üniversite kampüs navigasyon sistemi olan **CampusRoute** üzerinde çalışmak ve yapay zekânın ajanik yeteneklerini deneyimlemek üzere tasarlanmıştır.

CampusRoute; öğrencilerin ders programlarını yükleyebildiği, kampüsteki binalar arasında en kısa yürüyüş rotalarını (merdivensiz erişim seçenekleriyle birlikte) bulabildiği, anlık yoğunlukları takip edebildiği ve bina açılış saatlerini sorgulayabildiği hafif, güvenli ve bağımsız (üçüncü parti bağımlılığı olmayan) bir Python uygulamasıdır.

### Temel Özellikler
- **Saf Standart Kütüphane:** Dış kütüphane bağımlılığı (`pip install` veya `npm install`) bulunmaz. Yalnızca Python 3.9+ ve Node.js 18+ yerleşik modülleri kullanılır.
- **Güvenlik Odaklı Mimari:** Sunucu yalnızca `127.0.0.1` adresine bağlanır. Okuma-yazma izinleri katı şekilde ayrılmıştır; `eval`, `exec` veya `subprocess` gibi potansiyel tehlikeli yapılar kesinlikle kullanılmaz.
- **Yüksek Test Kapsamı:** Çekirdek sistemden türetilmiş dillerine kadar 117'den fazla birim ve kabul testi ile %100 yeşil doğrulama.

---

## Depo Mimarisi ve Klasör Yapısı

```
bobathon/
├── .bob/                             # Bob yetenek ve özel mod yapılandırmaları
│   ├── rules/
│   │   └── feedback-tone.md          # Öğrenci geri bildirimlerinde nezaket ve yapıcı ton kuralı
│   ├── skills/                       # Yeniden kullanılabilir uzmanlık becerileri (skills)
│   └── custom_modes.yaml             # Salt-okunur izin kısıtlı özel ajan modları
├── app/                              # CampusRoute Çekirdek Uygulaması
│   ├── campusroute/                  # Python uygulama paketi
│   │   ├── __init__.py
│   │   ├── __main__.py               # CLI giriş noktası
│   │   ├── api.py                    # REST API sunucusu ve güvenlik başlıkları
│   │   ├── campus.py                 # Kampüs grafı, bina ve oda modelleri
│   │   ├── cli.py                    # Terminal komut satırı arayüzü
│   │   ├── occupancy.py              # Kalabalık ve yoğunluk hesaplama
│   │   ├── opening_hours.py          # CR-11 çalışma saatleri çözümleme motoru
│   │   ├── routing.py                # Dijkstra en kısa yol ve erişilebilirlik yönlendirmesi
│   │   ├── schedule.py               # Haftalık ders programı ayrıştırma ve çakışma tespiti
│   │   ├── search.py                 # Türkçe destekli metin ve yer arama motoru
│   │   └── legacy/
│   │       └── kiosk_router.py       # CR-9 kapsamında emekliye ayrılacak eski prototip router
│   ├── data/                         # Sentetik kampüs verileri, ders programı ve kalabalık örnekleri
│   ├── docs/                         # Mimari dokümanlar ve ürün gereksinim listesi (BACKLOG.md)
│   ├── tests/                        # 67 adet kapsamlı unittest senaryosu
│   └── web/                          # Güvenli, frameworksüz vanilla web arayüzü (HTML/CSS/JS)
├── scenarios/                        # 7 Bağımsız Atölye Senaryosu
│   ├── s1-lecture-to-study-page/     # Ders notlarını interaktif HTML çalışma sayfasına dönüştürme
│   │   ├── lecture-week7-shortest-paths.md
│   │   └── out/study-page.html       # Mermaid diyagramlı, düzeltilmiş interaktif çalışma sayfası
│   ├── s2-assignment-grader/         # Notlandırma yeteneği ve öğrenci ödev değerlendirmesi
│   │   ├── rubric.md, assignment.md, submissions/
│   │   └── out/grades.md             # A, B ve C öğrencileri için detaylı değerlendirme raporu
│   ├── s3-build-a-language/          # RouteQL dil tasarımı ve yorumlayıcısı
│   │   ├── routeql-spec.md, test_routeql.py
│   │   └── out/routeql.py            # 16 kabul testini geçen tam fonksiyonel yorumlayıcı
│   ├── s4-translate-code/            # schedule.py modülünün JavaScript/Node ortamına taşınması
│   │   ├── out/schedule.mjs          # ES Module formatında sıfır bağımlı JS implementasyonu
│   │   ├── out/schedule.test.mjs     # 20 adet node:test birim testi
│   │   └── out/package.json
│   ├── s5-understand-legacy-code/    # Miras kodun analizi ve CR-9 emeklilik planı
│   │   └── out/analysis.md           # LRU önbellek yapısı, akış şeması ve göç analizi
│   ├── s6-project-plan/              # 4 haftalık takım sprint planı ve risk yönetimi
│   │   └── plans/sprint-plan.md      # Kapasite matrisi, Mermaid Gantt takvimi ve acil durum planı
│   └── s7-career-and-interview/      # Yazılım geliştirici mülakat meydan okuması
│       └── challenge/
│           ├── opening_hours.py      # 14/14 test başarımlı çalışma saati çözümleyicisi
│           └── test_opening_hours.py
├── assets/                           # Görseller ve simgeler
├── AGENTS.md                         # Ajanlar için operasyonel kurallar ve bağlam
├── GUIDE.md                          # Detaylı İngilizce atölye kılavuzu
├── index.html                        # Web tabanlı interaktif kılavuz sayfası
└── setup-check.sh                    # 30 saniyelik ortam ve kurulum denetleme betiği
```

---

## Tamamlanan Kapsamlı Geliştirmeler

Bu depoda, atölye kapsamındaki tüm senaryolar ve çekirdek uygulama eksiksiz bir şekilde geliştirilmiş, doğrulanmış ve belgelenmiştir:

### Senaryo 1: Karmaşık Notlardan İnteraktif Çalışma Sayfasına
- **Dosya:** [study-page.html](scenarios/s1-lecture-to-study-page/out/study-page.html)
- **Yapılanlar:** CS201 En Kısa Yol ders notları analiz edilerek şık, responsive ve modern bir HTML çalışma sayfası inşa edildi.
- **Kritik Hata Düzeltildi:** Notlardaki *"Dijkstra negatif ağırlıklı kenarlarla döngü olmadığı sürece çalışır"* şeklindeki yaygın sınav yanılgısı tespit edildi; karşıt-örnekle (counter-example) açıklanarak Bellman-Ford ile farkı vurgulandı.
- **Mermaid Akış Diyagramı:** Algoritmalar arasındaki ilişkileri gösteren `flowchart TD` görselleştirmesi ve `<details>` blokları içinde gizlenmiş 5 adet öz-değerlendirme sınav sorusu eklendi.

### Senaryo 2: Otomatik Ödev Değerlendirici ve Güvenli Mod
- **Dosyalar:** [grades.md](scenarios/s2-assignment-grader/out/grades.md), [feedback-tone.md](.bob/rules/feedback-tone.md)
- **Yapılanlar:** Rubrik kriterlerine göre Öğrenci A (100), Öğrenci B (47) ve Öğrenci C (22) için harfiyen alıntılanmış kanıtlar, güçlü yönler ve yapıcı gelişim önerileri içeren kapsamlı değerlendirme raporu hazırlandı.
- **Pedagojik Ton Kuralı:** Öğrenciye geri bildirim verirken kırıcı veya aşağılayıcı ifadelerden kaçınan, daima bir güçlü yönle başlayan ve somut yönlendirmeler sunan `.bob/rules/feedback-tone.md` kuralı sisteme entegre edildi.

### Senaryo 3: Sıfırdan Programlama Dili: RouteQL
- **Dosya:** [routeql.py](scenarios/s3-build-a-language/out/routeql.py)
- **Yapılanlar:** Kampüs kioskları için `let`, `route`, `to`, `via`, `avoid stairs`, `find`, `print` ifadelerini destekleyen EBNF uyumlu tam bir betik yorumlayıcısı yazıldı.
- **Tasarım:** Sözdizimi hatalarında program çalıştırılmadan hata satırını raporlar; çalışma zamanında değişkenleri çözümler ve `campusroute` çekirdeğiyle entegre rotalama/arama yapar.
- **Test Başarımı:** `test_routeql.py` içerisindeki **16 kabul testinin tamamı (16/16) eksiksiz geçti.**

### Senaryo 4: Modül Taşınabilirliği: JavaScript/Node Portu
- **Dosyalar:** [schedule.mjs](scenarios/s4-translate-code/out/schedule.mjs), [schedule.test.mjs](scenarios/s4-translate-code/out/schedule.test.mjs)
- **Yapılanlar:** `schedule.py` modülü; gün numaralandırma farkları (Python Pazartesi=0 iken JS Pazar=0), negatif tamsayı modülo davranışı (`%`), CSV tırnak içi virgül ayrıştırma kuralları ve tamsayı bölme detayları gözetilerek saf Node.js ES modülüne dönüştürüldü.
- **Test Başarımı:** `node:test` ve `node:assert/strict` ile yazılan **20 birim testin tamamı (20/20) başarıyla çalışmaktadır.**

### Senaryo 5: Eski Kod Tabanı Analizi: Kiosk Router
- **Dosya:** [analysis.md](scenarios/s5-understand-legacy-code/out/analysis.md)
- **Yapılanlar:** 339 satırlık dokümante edilmemiş `kiosk_router.py` dosyasının mimari haritası çıkarıldı.
- **Önbellek & Akış:** Çift yönlü bağlı liste + hash map ile kurulan O(1) LRU önbellekleme mekanizması çözümlendi. CR-9 kapsamında bu bileşenin güvenle emekliye ayrılması ve `campusroute.routing` ile ikame edilmesi için göç planı sunuldu.

### Senaryo 6: 4 Haftalık Çevik Proje ve Sprint Planı
- **Dosya:** [sprint-plan.md](scenarios/s6-project-plan/plans/sprint-plan.md)
- **Yapılanlar:** 4 kişilik sentetik geliştirme takımı için 142 net çalışma saatini kapsayan, toplantı ve sınav kısıtlarını gözeten 4 haftalık sprint planı hazırlandı.
- **Dinamik Yönetim:** Takım üyesi Mert'in 3. haftada hastalanması senaryosu modellenerek, zorunlu teslimatları (CR-11, CR-13, CR-19) riske atmayan, görev kaydırmalı B-planı ve Mermaid Gantt şeması oluşturuldu.

### Senaryo 7: Mülakat Görevi: Çalışma Saatleri Çözücü
- **Dosya:** [opening_hours.py](scenarios/s7-career-and-interview/challenge/opening_hours.py)
- **Yapılanlar:** `campus.json` içerisindeki tüm karmaşık çalışma saatlerini (`Mon-Fri 08:00-24:00; Sat 10:00-18:00`, gece yarısını aşan aralıklar, `closed` istisnaları) ayrıştıran `is_open(hours, now)` fonksiyonu geliştirildi.
- **Test Başarımı:** `test_opening_hours.py` içerisindeki **14 testin tamamı (14/14) firesiz geçti.**

### CampusRoute Uygulama Çekirdeği İyileştirmeleri
- **CR-11 "Açık / Kapalı" Durumu:** `opening_hours` motoru doğrudan `/api/places` uç noktasına entegre edildi. Yer ve arama sonuçlarında binaların o an açık veya kapalı olduğu rozetlerle gösterilir.
- **CR-15 Koyu / Açık Tema Değiştirici:** Başlık çubuğuna eklenen tema anahtarı (`☀️ / 🌙`) ile kullanıcı tercihine göre kalıcı (`localStorage`) tema değişimi sağlandı.
- **CR-16 Kampüs Etkinlik Takvimi:** `/api/events` uç noktası ve etkinlik kartları eklendi. Öğrenciler kampüsteki panel, turnuva ve atölyeleri görüp *"Rotayı Çiz"* ile anında yol tarifi alabilir.
- **Eko & Sağlık Metrikleri:** Hesaplanan her rota için adım mesafesine bağlı tahmini kalori yakımı (`~kcal`) ve karbon tasarrufu (`g CO₂`) dinamik olarak sunulur.
- **Yazdırma Desteği:** `@media print` stilleri ile rota ve adım talimatlarını temiz bir çıktı formatında yazdırma olanağı eklendi.
- **Genel Test Durumu:** Çekirdek test takımı 63'ten **69 teste çıkarıldı ve %100 başarı sağlandı (Toplam: 119 test).**

---

## Hızlı Başlangıç ve Çalıştırma Kılavuzu

### 1. Ortam Kontrolü
Sistem gereksinimlerini ve ortamınızı test etmek için terminalde şu komutu çalıştırın:
```bash
bash setup-check.sh
```

### 2. CampusRoute Web Sunucusunu Başlatma
Uygulamayı yerel makinenizde çalıştırmak için:
```bash
cd app
python3 -m campusroute serve --port 8000
```
Ardından tarayıcınızda [http://127.0.0.1:8000](http://127.0.0.1:8000) adresine gidin.

### 3. Komut Satırından Rota Sorgulama (CLI)
Sunucu başlatmadan doğrudan terminalden rota hesaplamak için:
```bash
cd app
python3 -m campusroute route "Main Gate" "ENG-B204"
# Merdivenlerden kaçınmak için:
python3 -m campusroute route "Main Gate" "ENG-B204" --avoid-stairs
```

### 4. RouteQL Betiği Çalıştırma
```bash
python3 scenarios/s3-build-a-language/out/routeql.py scenarios/s3-build-a-language/examples/01-basics.rql
```

---

## Test Takımı ve Doğrulama

Tüm modüller ve senaryolar bağımsız test takımlarıyla korunmaktadır. Aşağıdaki komutlarla tüm sistemi tek seferde doğrulayabilirsiniz:

```bash
# 1. CampusRoute Çekirdek Testleri (69 test)
cd app && python3 -m unittest discover -s tests

# 2. RouteQL Dil Kabul Testleri (16 test)
python3 scenarios/s3-build-a-language/test_routeql.py

# 3. JavaScript/Node Schedule Port Testleri (20 test)
node --test scenarios/s4-translate-code/out/

# 4. Mülakat Görevi Çalışma Saatleri Testleri (14 test)
cd scenarios/s7-career-and-interview/challenge && python3 -m unittest test_opening_hours.py
```

> **Toplam Doğrulanan Test Sayısı:** **119 test / 119 Başarılı (0 Hata)**

---

## Katı Kurallar ve Tasarım İlkeleri

Ajanlar ve katkı sağlayan geliştiriciler için geçerli temel kurallar:
1. **Harici Paket Yasağı:** Proje saf Python ve Node.js standart kütüphaneleriyle çalışır. `pip install` veya `npm install` gerektiren kod eklenemez.
2. **Güvenli Yürütme:** Yorumlayıcılarda veya uygulama kodunda `eval()`, `exec()`, `compile()`, `os.system()` veya `subprocess` çağrıları yasaktır.
3. **Miras Kod Koruması:** `kiosk_router.py` ve senaryo girdi dosyaları değiştirilemez; yalnızca `out/` ve `plans/` klasörlerine çıktı üretilir.
4. **Sentetik Veri:** Tüm kişi, öğrenci, yer ve program verileri kurgusaldır. Gerçek kişisel veri eklenemez.
5. **Test Güvenirliği:** Testler başarısız olduğunda beklenen test değeri değil, kaynak kod düzeltilir.

---

## Takım Çalışması ve Katkı Rehberi

Takım halinde çalışırken şu adımları izleyebilirsiniz:
1. Depoyu çatallayın (Fork) ve ekip üyelerini ortak çalışan (Collaborator) olarak ekleyin.
2. Depoyu yerel makinenize klonlayın:
   ```bash
   git clone https://github.com/<kullanici-adiniz>/bobathon.git
   cd bobathon
   ```
3. Kendi özelliğiniz için yeni bir dal (branch) açın:
   ```bash
   git switch -c senaryo-adi
   ```
4. Çıktılarınızı ilgili `scenarios/<senaryo>/out/` dizininde oluşturup testleri çalıştırın.
5. Değişiklikleri kaydedip dalınıza gönderin:
   ```bash
   git add scenarios/
   git commit -m "feat(s3): RouteQL yorumlayıcısı tamamlandı"
   git push -u origin senaryo-adi
   ```
6. GitHub üzerinden bir Çekme İsteği (Pull Request) açın ve takım arkadaşınızın incelemesini talep edin.

---

*Bu kapsamlı dokümantasyon ve geliştirmeler **IBM Bob** ekosistemine ve CampusRoute mimarisine tam uyumlu olarak hazırlanmıştır.*
