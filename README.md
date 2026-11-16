<img src="assets/bob.png" alt="Bob, güler yüzlü mavi baretli robot" width="130" align="right">

# IBM Bob · Eyleyen Yapay Zekâ İş Başında (Agentic AI in Action)

> **Üniversite öğrencileri, yazılım mühendisleri ve yapay zekâ araştırmacıları için kapsamlı, uygulamalı ve otonom yazılım geliştirme ekosistemi.**  
> Yapay zekâyı salt bir satır tamamlama (autocomplete) veya metin üreten sohbet robotu (chatbot) olarak değil; planlayan, izin isteyerek araçları yöneten, karmaşık kod tabanlarını analiz eden, testlerle kendini doğrulayan ve insan denetiminde hareket eden **Ajanik bir İş Ortağı (Agentic Partner)** olarak kullanıyoruz.

---

## 📑 Kapsamlı İçindekiler
1. [Büyük Resim: Ajanik Yapay Zekâ Felsefesi](#1-büyük-resim-ajanik-yapay-zekâ-felsefesi)
   - [Chatbot/Autocomplete Yaklaşımından "Ajanik" Paradigmaya](#chatbotautocomplete-yaklaşımından-ajanik-paradigmaya)
   - [IBM Bob'un Rolü ve Çalışma İlkeleri](#ibm-bobun-rolü-ve-çalışma-ilkeleri)
   - [Atölyenin Temel Misyonu](#atölyenin-temel-misyonu)
2. [CampusRoute: Gerçekçi Kampüs Navigasyon Mimarisi](#2-campusroute-gerçekçi-kampüs-navigasyon-mimarisi)
   - [Grafik Teorisi ve Rotalama Motoru (Dijkstra & Erişilebilirlik)](#grafik-teorisi-ve-rotalama-motoru-dijkstra--erişilebilirlik)
   - [Ders Takvimi ve Çakışma Yönetimi (`schedule.py`)](#ders-takvimi-ve-çakışma-yönetimi-schedulepy)
   - [Çalışma Saatleri Motoru (`opening_hours.py` - CR-11)](#çalışma-saatleri-motoru-opening_hourspy---cr-11)
   - [Canlı Kalabalık ve Yoğunluk Takibi (`occupancy.py`)](#canlı-kalabalık-ve-yoğunluk-takibi-occupancypy)
   - [Türkçe Destekli Akıllı Arama Motoru (`search.py`)](#türkçe-destekli-akıllı-arama-motoru-searchpy)
3. [7 Atölye Senaryosunun Detaylı Hikâyesi ve Çözümleri](#3-7-atölye-senaryosunun-detaylı-hikâyesi-ve-çözümleri)
   - [Senaryo 1: Karmaşık Notlardan İnteraktif Çalışma Sayfasına](#senaryo-1-karmaşık-notlardan-interaktif-çalışma-sayfasına)
   - [Senaryo 2: Otomatik Ödev Değerlendirici ve Güvenli Mod](#senaryo-2-otomatik-ödev-değerlendirici-ve-güvenli-mod)
   - [Senaryo 3: Sıfırdan Programlama Dili İnşası: RouteQL (CR-18)](#senaryo-3-sıfırdan-programlama-dili-inşası-routeql-cr-18)
   - [Senaryo 4: Gerçek Bir Modülün JavaScript/Node Ortamına Taşınması (CR-12)](#senaryo-4-gerçek-bir-modülün-javascriptnode-ortamına-taşınması-cr-12)
   - [Senaryo 5: Miras (Legacy) Kodun Analizi ve Emeklilik Planı: `kiosk_router.py` (CR-9)](#senaryo-5-miras-legacy-kodun-analizi-ve-emeklilik-planı-kiosk_routerpy-cr-9)
   - [Senaryo 6: 4 Haftalık Çevik Proje ve Acil Durum Sprint Planlaması](#senaryo-6-4-haftalık-çevik-proje-ve-acil-durum-sprint-planlaması)
   - [Senaryo 7: Teknik Mülakat Meydan Okuması: Açık/Kapalı Saatleri (CR-11)](#senaryo-7-teknik-mülakat-meydan-okuması-açıkkapalı-saatleri-cr-11)
4. [Kullanıcı Arayüzü (UI/UX) ve Gelişmiş Özellikler](#4-kullanıcı-arayüzü-uiux-ve-gelişmiş-özellikler)
   - [Modern Tasarım ve Cam Efekti (Glassmorphism)](#modern-tasarım-ve-cam-efekti-glassmorphism)
   - [İnteraktif SVG Kampüs Haritası](#interaktif-svg-kampüs-haritası)
   - [Koyu/Açık Tema Desteği (CR-15)](#koyuaçık-tema-desteği-cr-15)
   - [Kampüs Etkinlik Takvimi (CR-16)](#kampüs-etkinlik-takvimi-cr-16)
   - [Eko & Sağlık İstatistikleri ve Yazdırma Modu](#eko--sağlık-istatistikleri-ve-yazdırma-modu)
5. [Depo Klasör Hiyerarşisi](#5-depo-klasör-hiyerarşisi)
6. [Hızlı Başlangıç ve Kullanım Rehberi](#6-hızlı-başlangıç-ve-kullanım-rehberi)
7. [Test Takımı ve Doğrulama Raporu](#7-test-takımı-ve-doğrulama-raporu)
8. [Tasarım İlkeleri, Güvenlik ve Katı Kurallar](#8-tasarım-ilkeleri-güvenlik-ve-katı-kurallar)
9. [Takım Çalışması ve Katkı Rehberi](#9-takım-çalışması-ve-katkı-rehberi)

---

## 1. Büyük Resim: Ajanik Yapay Zekâ Felsefesi

### Chatbot/Autocomplete Yaklaşımından "Ajanik" Paradigmaya
Yapay zekâ araçlarının ilk dalgası genellikle iki ana model etrafında şekillendi:
1. **Kod Tamamlama (Autocomplete / Copilot):** Geliştirici yazarken bir sonraki birkaç satırı tahmin eden yardımcılar.
2. **Sohbet Robotları (Chatbots):** Kendisine sorulan sorulara genel cevaplar veren, ancak dosya sistemine dokunamayan, komut çalıştıramayan ve projenin durumunu doğrudan inceleyemeyen sistemler.

**Ajanik Yapay Zekâ (Agentic AI)** ise bu kalıpları temelden kırar:
- **Hedef Odaklılık:** Tek bir kod parçası üretmek yerine, *"CampusRoute uygulamasını çalıştır, testleri geç, eksik olan RouteQL yorumlayıcısını sıfırdan yaz ve doğrula"* gibi üst düzey bir hedefi üstlenir.
- **Döngüsel Akıl Yürütme (ReAct Pattern):** Düşünür (Thought), araç çağırır (Tool Call), aracın çıktısını gözlemler (Observation) ve hedefe ulaşana kadar bu döngüyü sürdürür.
- **Gözlem ve Test Odaklılık:** Yazdığı kodun çalışıp çalışmadığını varsaymaz; terminalde testleri bizzat yürütür, hata mesajlarını analiz eder ve hataları kodu düzelterek giderir.

```
                    ┌────────────────────────┐
                    │      Kullanıcı         │
                    │   Hedef / Yönerge      │
                    └───────────┬────────────┘
                                │
                                ▼
                    ┌────────────────────────┐
             ┌─────►│  Ajan (Akıl Yürütme)   │◄────┐
             │      └───────────┬────────────┘     │
             │                  │                  │
        Gözlem / Sonuç          │ Eylem / Araç     │
             │                  ▼                  │
             │      ┌────────────────────────┐     │
             │      │  Onay Mekanizması      │     │
             │      │  (İnsan Denetimi)      │     │
             │      └───────────┬────────────┘     │
             │                  │                  │
             │                  ▼                  │
             └──────┴── Dosya Yazma / Terminal ────┘
```

### IBM Bob'un Rolü ve Çalışma İlkeleri
Bu depoda kullanılan **IBM Bob**, şu temel ilkeler üzerinde yükselir:
- **İnsan Denetimli Otonomi (Human-in-the-Loop):** Dosya yazma veya kritik terminal komutlarını çalıştırmadan önce kullanıcıya ne yapacağını açıklar ve onay ister.
- **Salt-Okunur İzin Ayrımı (Least Privilege):** Notlandırma gibi inceleme gerektiren görevlerde dosya yazma araçları elinden alınarak sisteme güvenlik katar.
- **Standart Kütüphane Disiplini:** Harici kontrolsüz paket yüklemeleri (`pip install`, `npm install`) yerine dilin kendi standart kütüphanesini ustalıkla kullanır.

### Atölyenin Temel Misyonu
Atölyenin amacı, katılımcılara şu üç temel beceriyi kazandırmaktır:
1. Bir yapay zekâyı **planlama ve mimari tasarım** safhasında bir analist gibi kullanabilmek.
2. Yapay zekânın ürettiği sonuçları **bağımsız testler ve mantıksal sorgulamalarla** denetleyebilmek (Yapay zekâ kendinden emin bir şekilde yanlış iddialarda bulunabilir!).
3. Güvenlik, izinler ve kod kalitesi standartlarından ödün vermeden üretim seviyesinde yazılım teslim edebilmek.

---

## 2. CampusRoute: Gerçekçi Kampüs Navigasyon Mimarisi

**CampusRoute**, üniversite kampüs yaşamının dinamiklerini dijitalleştiren saf bir Python web uygulaması ve kütüphanesidir.

```
                   ┌─────────────────────────────────────────┐
                   │             Web Arayüzü                 │
                   │      (Vanilla HTML5 / CSS3 / ES6)       │
                   └────────────────────┬────────────────────┘
                                        │ REST API (JSON)
                                        ▼
                   ┌─────────────────────────────────────────┐
                   │            api.py (HTTP Sunucu)         │
                   │    Güvenlik Başlıkları & Uç Noktalar    │
                   └───────┬────────────┬────────────┬───────┘
                           │            │            │
            ┌──────────────┴───┐ ┌──────┴─────┐ ┌────┴─────────────┐
            │   routing.py     │ │schedule.py │ │opening_hours.py  │
            │(Dijkstra Grafı)  │ │ (Takvim)   │ │  (Saat Kontrolü) │
            └─────────┬────────┘ └────────────┘ └──────────────────┘
                      │
                      ▼
            ┌─────────────────────────────────────────┐
            │        campus.py (Graf & Veri Modeli)   │
            │           app/data/campus.json          │
            └─────────────────────────────────────────┘
```

### Grafik Teorisi ve Rotalama Motoru (Dijkstra & Erişilebilirlik)
- **Seyrek Kampüs Grafı (Sparse Graph):** Binalar ve yol kavşakları birer düğüm (vertex), kaldırımlar ve koridorlar ise ağırlıklı kenarlardır (edge). Ortalama bir bina sadece 3-4 komşuya bağlı olduğu için adjacency matrix ($O(V^2)$ bellek) yerine **adjacency list** ($O(V + E)$ bellek) tercih edilmiştir.
- **Dijkstra Algoritması:** Python'un yerleşik `heapq` modülüyle çalışır. Öncelik kuyruğunda düğüm mesafe güncellemeleri için *lazy deletion* (eski girdileri atlama) kullanılır. Tuple karşılaştırmalarında düğüm nesnelerinin çökmesini önlemek için `itertools.count()` ile belirleyici sıra numaraları (tie-breaker) eklenmiştir.
- **Erişilebilirlik (CR-13):** Merdiven içeren kenarlar `stairs: true` olarak etiketlenmiştir. "Merdivenlerden Kaçın" seçeneği etkinleştirildiğinde bu kenarlar graf filtrelenerek elenir; yeni bir algoritma yazmaya gerek kalmadan düz ayak rotalama elde edilir.
- **Çoklu Duraklar (`via`):** Örneğin *"Kütüphaneye uğrayarak Mühendisliğe git"* sorgularında Dijkstra ardışık çalıştırılarak rota parçaları birleştirilir.

### Ders Takvimi ve Çakışma Yönetimi (`schedule.py`)
- Öğrencilerin el ile girdiği CSV formatındaki ders programlarını ayrıştırır.
- Haftalık ders saatlerini hesaplar, aynı saat diliminde çakışan oturumları tespit eder (`find_conflicts`).
- İlgili an (`now`) parametresine göre öğrencinin o anda derste olup olmadığını veya bir sonraki dersinin kaç dakika sonra başlayacağını bildirir.

### Çalışma Saatleri Motoru (`opening_hours.py` - CR-11)
- Binaların karmaşık açılış saat dizgilerini (`Mon-Fri 08:00-24:00; Sat 10:00-18:00; Sun closed`) ayrıştırır.
- Gece yarısını aşan aralıkları (örn. `Fri 20:00-02:00` Cuma akşamından Cumartesi sabahına geçiş) ve `24:00` gece yarısı bitiş kuralını kusursuz şekilde yönetir.

### Canlı Kalabalık ve Yoğunluk Takibi (`occupancy.py`)
- Kampüsteki kütüphane, yemekhane ve kafelerden gelen zaman damgalı yoğunluk bildirimlerini değerlendirir.
- Zamansal bozulma (temporal decay) formülüyle eskiyen raporların ağırlığını azaltarak mekanın güncel durumunu `quiet`, `moderate`, `busy`, `packed` olarak etiketler.

### Türkçe Destekli Akıllı Arama Motoru (`search.py`)
- Arama kutusuna yazılan metinleri Türkçe karakter duyarlılığıyla katlar (folding): `I`, `ı`, `İ`, `i` karakterleri tek biçime dönüştürülür.
- Harf hatalarını tolere etmek için `difflib.SequenceMatcher` ile benzerlik puanı hesaplar ve en iyi eşleşen bina/oda önerilerini sunar.

### Bob Doğal Dil Kampüs Asistanı (`ai_assistant.py` & `/api/assistant`)
Harici bir LLM API'sine ya da `pip` kütüphanesine bağımlı olmadan, tamamen **Python 3 standart kütüphanesi** ile çalışan kural ve niyet (intent) tabanlı bir doğal dil işleme motorudur:
- **Niyet Sınıflandırma (Intent Classification):** Kullanıcının yazdığı serbest Türkçe ifadeleri analiz ederek 6 temel niyet sınıfına ayırır:
  1. `study_recommendation`: *"Sessizce ders çalışacak sakin bir yer neresi?"* -> Canlı doluluk oranlarını (`occupancy`) ve yürüme mesafesini hesaplayarak en sakin çalışma alanını önerir ve rotayı otomatik çizer.
  2. `food_cafe`: *"Açık bir kafe bul"*, *"Karnım acıktı yemekhane nerede?"* -> Güncel saat durumuna göre açık olan en yakın yemekhane veya kafeyi bulur.
  3. `step_free_route`: *"Tekerlekli sandalye ile kütüphaneye nasıl giderim?"*, *"Engelsiz rota"* -> Merdivenleri (`avoid_stairs=True`) baypas eden engelsiz rota üretir.
  4. `hours_query`: *"Kütüphane saat kaça kadar açık?"* -> İlgili mekanın açılış ve kapanış saatlerini `opening_hours` motorundan çözümler.
  5. `schedule_query`: *"Bir sonraki dersim ne zaman?"* -> Öğrencinin CSV programını tarayarak yaklaşan dersin sınıfını ve başlangıç saatini bildirir.
  6. `route_query`: *"Girişten spor merkezine nasıl giderim?"* -> İki nokta arasındaki en kısa rotayı hesaplar.
- **Türkçe Kök ve Ek Normalizasyonu:** `mühendisliğe`, `kütüphaneden`, `auditoryumu` gibi çekim eklerini tanıyan yerleşik kök haritası (`STEMS`) ve aksan katlama mekanizması içerir.
- **İnteraktif Web Entegrasyonu:** Kullanıcı bir soru sorduğunda asistan sadece metin üretmekle kalmaz; doğrudan harita üzerinde ilgili rotayı çizer ve form girdilerini günceller.

---

## 3. 7 Atölye Senaryosunun Detaylı Hikâyesi ve Çözümleri

### Senaryo 1: Karmaşık Notlardan İnteraktif Çalışma Sayfasına
- **Senaryo Arka Planı:** CS201 Veri Yapıları dersi vize sınavından önceki gece, öğrencinin tuttuğu dağınık ders notları incelenir.
- **Felsefi/Teknik Hata Tespiti:** Notların 35. satırında yer alan *"Dijkstra, negatif kenar ağırlıklarıyla negatif döngü olmadığı sürece çalışır"* iddiası incelenmiştir. Bu ifadenin **tamamen yanlış** olduğu kanıtlanmıştır: Dijkstra'nın açgözlü (greedy) yaklaşımı, bir düğüm öncelik kuyruğundan çekildiği anda en kısa mesafesinin kesinleştiğini varsayar. Daha sonra karşısına çıkacak negatif bir kenar, daha kısa bir yol sunsa dahi algoritma geriye dönmeyeceği için hatalı sonuç üretir. Çözümün **Bellman-Ford** olduğu gösterilmiş ve somut bir karşıt-örnekle açıklanmıştır.
- **Üretilen Çıktı:** [study-page.html](scenarios/s1-lecture-to-study-page/out/study-page.html)
  - Mermaid `flowchart TD` görsel kavram haritası.
  - BFS, Dijkstra, A* ve Bellman-Ford karşılaştırma tablosu.
  - `<details>` etiketleri içinde gizlenmiş 5 adet öz-değerlendirme sınav sorusu.

---

### Senaryo 2: Otomatik Ödev Değerlendirici ve Güvenli Mod
- **Senaryo Arka Planı:** Bir öğretim asistanının onlarca Lab 4 ödevini adil, objektif ve pedagojik olarak değerlendirmesi simüle edilir.
- **Ajanik İzin Kısıtlaması:** Değerlendirici moduna dosya düzenleme aracı verilmemiştir (`groups: [read, skill]`). Ajan öğrencilerin kodunu düzeltmeye çalışamaz; güvenlik "rica ederek" değil, **yapılandırma ile yetkileri kısıtlayarak** sağlanır.
- **Öğrenci Analizleri:**
  - **Öğrenci A (100 Puan):** `heapq`, tie-breaker ve lazy deletion kullanan, köşe durumları yakalayan kusursuz Dijkstra.
  - **Öğrenci B (47 Puan):** $O(n \log n)$ karmaşıklık iddia etmesine rağmen öncelik kuyruğu yerine her adımda `unvisited` listesini lineer tarayan ($O(V^2)$) ve ulaşılamayan hedeflerde çöken kod.
  - **Öğrenci C (22 Puan):** Ağırlıklı grafikte Dijkstra yerine BFS kullanan (bu yüzden `dorm -> sci` rotasında 500m yerine 700m bulan), birim testi yazmayan ve Dijkstra karmaşıklık teorisini kopyalayan ödev.
- **Üretilen Çıktılar:** [grades.md](scenarios/s2-assignment-grader/out/grades.md) ve pedagojik dil standardını belirleyen [.bob/rules/feedback-tone.md](.bob/rules/feedback-tone.md).

---

### Senaryo 3: Sıfırdan Programlama Dili İnşası: RouteQL (CR-18)
- **Senaryo Arka Planı:** Kampüs bilgi kioskları için operatörlerin rota ve arama betikleri yazabileceği hafif bir alan dili (DSL) gereklidir.
- **Dil Tasarımı & Gramer:**
  ```ebnf
  program   = { line } ;
  line      = [ statement ] [ comment ] NEWLINE ;
  statement = let | route | find | print ;
  let       = "let" IDENT "=" STRING ;
  route     = "route" place "to" place [ "via" place { "," place } ] [ "avoid" "stairs" ] ;
  find      = "find" STRING ;
  print     = "print" ( STRING | IDENT ) ;
  place     = STRING | IDENT ;
  ```
- **Kritik Kurallar:** Program önce bütünüyle taranıp ayrıştırılır (parse-first). Herhangi bir satırda sözdizimi hatası varsa ekrana hiçbir şey basılmadan durum kodu 1 ile çıkılır. Çalışma zamanı hatalarında ise o ana kadar basılmış çıktılar korunur.
- **Üretilen Çıktı:** [routeql.py](scenarios/s3-build-a-language/out/routeql.py)
  - `test_routeql.py` içerisindeki **16 kabul testinin tamamını (16/16)** hatasız geçmektedir. `eval()`, `exec()` veya harici kütüphane kullanılmamıştır.

---

### Senaryo 4: Gerçek Bir Modülün JavaScript/Node Ortamına Taşınması (CR-12)
- **Senaryo Arka Planı:** Kampüs mobil istemcisinde ders programı çakışma mantığının sunucuya gitmeden cihaz üzerinde (on-device) koşması istenmektedir.
- **Diller Arası 10 Kritik Tuzak Çözüldü:**
  1. *Gün Numaralandırması:* Python'da Pazartesi=0 iken JavaScript `Date.getDay()` Pazar=0'dır (`(d.getDay() + 6) % 7` formülüyle çözüldü).
  2. *Negatif Modülo:* Python'da `-1 % 7 = 6` iken JS'de `-1` kalır (`((a % b) + b) % b` uygulandı).
  3. *Tamsayı Bölme:* `(sec + 59) // 60` yerine `Math.floor((sec + 59) / 60)` kullanıldı.
  4. *CSV Tırnak İçinde Virgül:* `"CS203, Section 2"` gibi veriler için basit `split(",")` yerine tam bir CSV durum makinesi yazıldı.
  5. *Sözlük Sırası:* JS nesneleri sayısal anahtarları başa taşıdığından ekleme sırasını korumak için `Map` yapısı kullanıldı.
- **Üretilen Çıktılar:** [schedule.mjs](scenarios/s4-translate-code/out/schedule.mjs), [schedule.test.mjs](scenarios/s4-translate-code/out/schedule.test.mjs), [package.json](scenarios/s4-translate-code/out/package.json).
  - `node:test` ile koşturulan **20 birim testin 20'si de başarıyla geçer.**

---

### Senaryo 5: Miras (Legacy) Kodun Analizi ve Emeklilik Planı: `kiosk_router.py` (CR-9)
- **Senaryo Arka Planı:** 2023 yılı hackathon prototipinden kalma, tek harfli değişken isimleriyle yazılmış ve hiç yorum satırı olmayan 339 satırlık `kiosk_router.py` dosyasının analizi.
- **Çözümlenen Mimari:** Dosyanın çift yönlü bağlı liste (`_N`) ve sözlük (`dict`) kullanarak $O(1)$ Least-Recently-Used (LRU) önbellekleme yaptığı; ulaşılamayan rotaları dahi önbelleğe aldığı tespit edilmiştir.
- **Üretilen Çıktı:** [analysis.md](scenarios/s5-understand-legacy-code/out/analysis.md)
  - 5 ana bölümün satır aralıkları haritası.
  - Mermaid çağrı akış şeması.
  - Bileşenin `campusroute.routing` ile ikame edilerek güvenle emekliye ayrılma yol haritası.

---

### Senaryo 6: 4 Haftalık Çevik Proje ve Acil Durum Sprint Planlaması
- **Senaryo Arka Planı:** 4 kişilik bir öğrenci takımının CampusRoute v2.0 "Erişilebilir Kampüs" sürümünü 4 haftada teslim etmesi planlanır.
- **Kapasite ve Gerçekçilik:** Haftalık 1 saatlik takım toplantıları düşülerek toplam 142 net görev saati planlanmıştır. Ada'nın 2. haftadaki vize sınavları hesaba katılmıştır.
- **Kriz Yönetimi:** 3. haftada takım üyesi Mert'in hastalanması simüle edilmiş; kritik olmayan "Karanlık Tema" ertelenerek zorunlu gereksinimler (CR-11, CR-13, CR-19) vaktinde teslim edilecek şekilde dinamik B-planı oluşturulmuştur.
- **Üretilen Çıktı:** [sprint-plan.md](scenarios/s6-project-plan/plans/sprint-plan.md) (Görev matrisi, Mermaid Gantt takvimi, revize kapasite tablosu).

---

### Senaryo 7: Teknik Mülakat Meydan Okuması: Açık/Kapalı Saatleri (CR-11)
- **Senaryo Arka Planı:** Synthetic Labs "Junior Backend Geliştirici" pozisyonu için 25 dakikalık teknik mülakat ev ödevi.
- **İş Mantığı:** `is_open(hours, now)` fonksiyonu geliştirilerek `test_opening_hours.py` içerisindeki tüm sınır durumlar (ters gün aralığı, geçersiz saatler, gece yarısını aşan vardiyalar, `closed` istisnaları) kapsanmıştır.
- **Üretilen Çıktı:** [opening_hours.py](scenarios/s7-career-and-interview/challenge/opening_hours.py)
  - **14 mülakat testinin tamamı (14/14)** başarıyla geçmektedir.

---

## 4. Kullanıcı Arayüzü (UI/UX) ve Gelişmiş Özellikler

CampusRoute, saf vanilla teknolojilerle (harici framework ve font olmadan) geliştirilmiş modern ve ikonik bir web arayüzüne sahiptir.

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ [📍] CampusRoute   IBM Bob · Akıllı Kampüs Rehberi         [🌙] [● Çevrimiçi] [TR]│
├───────────────────────────────────────┬─────────────────────────────────────────┤
│ ┌─ Rota Planlayıcı ─────────────────┐ │ ┌─ İnteraktif Kampüs Planı ───────────┐ │
│ │ [A] Başlangıç: [ Ana Giriş      ] │ │ │                                     │ │
│ │ [B] Hedef:     [ ENG-B204       ] │ │ │           (Kuzey Yurdu)             │ │
│ │ [x] Merdivenlerden Kaçın (CR-13)  │ │ │                 │                   │ │
│ │ [ En Kısa Rotayı Bul ] [🖨 Yazdır] │ │ │                 ▼                   │ │
│ │ ───────────────────────────────── │ │ │           (Kütüphane)═══(Kafe)      │ │
│ │ 580 m, ~8 dk ✨ (Engelsiz)        │ │ │                 │                   │ │
│ │ 🔥 ~29 kcal   🌱 81 g CO₂         │ │ │                 ▼                   │ │
│ └───────────────────────────────────┘ │ │         (Mühendislik B)             │ │
│ ┌─ Kampüste Ara ────────────────────┐ │ │                                     │ │
│ │ [ Kütüphane, B204 ara...        ] │ │ ├─────────────────────────────────────┤ │
│ │ [📚 Kütüphane] [☕ Kafe] [⚙ Müh.] │ │ │ ── Aktif Rota  ┈┈ Merdiven  ══ Kapalı│ │
│ └───────────────────────────────────┘ │ └─────────────────────────────────────┘ │
│ ┌─ Kampüs Etkinlikleri (CR-16) ─────┐ │                                         │
│ │ 🎓 Yapay Zekâ Semineri [Rotayı Çiz]│ │                                         │
│ └───────────────────────────────────┘ │                                         │
└───────────────────────────────────────┴─────────────────────────────────────────┘
```

### Modern Tasarım ve Cam Efekti (Glassmorphism)
- Canlı çivit mavi/mor gradyanlar, yuvarlatılmış kartlar (`border-radius: 16px`) ve hafif derinlik gölgeleri.
- Sistem çevrimiçi olduğunu gösteren yeşil nabız (pulse) animasyonu.
- Mobil cihazlar ve masaüstü ekranlar için akıcı responsive ızgara (grid) düzeni.

### İnteraktif SVG Kampüs Haritası
- Binalar ve yollar matematiksel koordinatlarıyla SVG üzerinde çizilir.
- Merdivenler kırmızı kesikli çizgilerle, kapalı yürüyüş yolları yeşil hatlarla, bulunan en kısa rota ise parlayan neon mavi çizgiyle vurgulanır.
- **Haritadan Rotalama:** Haritadaki herhangi bir bina dairesine tıklandığında hedef alanına otomatik atanır ve rota hemen hesaplanır.

### Koyu/Açık Tema Desteği (CR-15)
- Başlıktaki `☀️ / 🌙` butonu ile kullanıcılar arayüzü istedikleri an aydınlık veya karanlık moda geçirebilir. Tercih tarayıcı hafızasında (`localStorage`) saklanır.

### Kampüs Etkinlik Takvimi (CR-16)
- `/api/events` uç noktasından beslenen dinamik kart; seminer, spor turnuvaları ve sosyal buluşmaları listeler. *"Rotayı Çiz"* butonu ile tek tıkla o etkinliğin binasına yol tarifi alınır.

### Eko & Sağlık İstatistikleri ve Yazdırma Modu
- Hesaplanan her rota için adım mesafesi baz alınarak **yakılan kalori (~kcal)** ve toplu taşıma/araca kıyasla **önlenen karbon salımı (g CO₂)** hesaplanır.
- Kiosk kullanıcıları için `@media print` stil şablonu ile rota yönergeleri gereksiz menülerden arındırılarak yazdırılabilir.

---

## 5. Depo Klasör Hiyerarşisi

```
bobathon/
├── .bob/                             # Bob kural ve yetenek yapılandırmaları
│   ├── rules/
│   │   └── feedback-tone.md          # Öğrenci geri bildirim üslup kuralları
│   ├── skills/                       # Özel yetenek tanımları
│   └── custom_modes.yaml             # Salt-okunur ve kısıtlı ajan modları
├── app/                              # CampusRoute Çekirdek Uygulaması
│   ├── campusroute/                  # Python paket kaynak kodları
│   │   ├── __init__.py
│   │   ├── __main__.py               # CLI giriş kapısı
│   │   ├── api.py                    # REST API & Statik Dosya Sunucusu
│   │   ├── campus.py                 # Graf veri modeli ve Campus sınıfı
│   │   ├── cli.py                    # Terminal komutları (route, search, next, serve)
│   │   ├── occupancy.py              # Yoğunluk hesaplama motoru
│   │   ├── opening_hours.py          # CR-11 çalışma saatleri çözümleyicisi
│   │   ├── routing.py                # Dijkstra en kısa yol algoritması
│   │   ├── schedule.py               # Ders programı ve çakışma modülü
│   │   ├── search.py                 # Türkçe destekli fuzzy arama
│   │   └── legacy/
│   │       └── kiosk_router.py       # CR-9 kapsamında emekliye ayrılacak miras kod
│   ├── data/                         # JSON ve CSV sentetik veritabanı
│   │   ├── campus.json               # Kampüs binaları, koordinatları ve kenarları
│   │   ├── crowd.sample.json         # Örnek kalabalık bildirimleri
│   │   ├── events.sample.json        # CR-16 kampüs etkinlikleri
│   │   └── schedule.sample.csv       # Örnek öğrenci ders programı
│   ├── docs/                         # Mimari dokümanlar ve BACKLOG.md
│   ├── tests/                        # 69 adet unittest birim testi
│   └── web/                          # Modern web arayüzü (index.html, style.css, app.js)
├── scenarios/                        # 7 Bağımsız Atölye Senaryosu
│   ├── s1-lecture-to-study-page/     # Ders notu özetleme & çalışma sayfası
│   ├── s2-assignment-grader/         # Otomatik notlandırma yeteneği
│   ├── s3-build-a-language/          # RouteQL dil yorumlayıcısı
│   ├── s4-translate-code/            # JavaScript schedule modülü portu
│   ├── s5-understand-legacy-code/    # Miras kod analiz raporu
│   ├── s6-project-plan/              # Çevik sprint planlaması
│   └── s7-career-and-interview/      # Açılış saatleri teknik mülakatı
├── assets/                           # Görseller ve ikonlar
├── AGENTS.md                         # Ajanlar için operasyonel kurallar
├── GUIDE.md                          # İngilizce detaylı atölye kılavuzu
├── README.md                         # Kapsamlı Türkçe ana kılavuz
└── setup-check.sh                    # Ortam denetleme betiği
```

---

## 6. Hızlı Başlangıç ve Kullanım Rehberi

### 1. Kurulum ve Ortam Denetimi
Terminali açın ve ortamınızın gereksinimleri karşıladığından emin olun:
```bash
bash setup-check.sh
```

### 2. Web Sunucusunu Başlatma
Uygulama sunucusunu 8000 portunda ayağa kaldırmak için:
```bash
cd app
python3 -m campusroute serve --port 8000
```
Tarayıcınızdan **[http://127.0.0.1:8000](http://127.0.0.1:8000)** adresini açarak uygulamayı kullanmaya başlayabilirsiniz.

### 3. Komut Satırı Arayüzü (CLI) Kullanımı
Sunucu açmadan doğrudan terminal üzerinden sorgu yapmak için:

- **En Kısa Rota Hesaplama:**
  ```bash
  cd app
  python3 -m campusroute route "Main Gate" "ENG-B204"
  ```
- **Merdivensiz (Engelsiz) Rota:**
  ```bash
  python3 -m campusroute route "Main Gate" "ENG-B204" --avoid-stairs
  ```
- **Yer ve Oda Arama:**
  ```bash
  python3 -m campusroute search "kütüphane"
  ```
- **Sıradaki Dersi Öğrenme:**
  ```bash
  python3 -m campusroute next --now "2027-03-01T09:30"
  ```

### 4. RouteQL Betiği Çalıştırma
Geliştirilen RouteQL yorumlayıcısını çalıştırmak için:
```bash
python3 scenarios/s3-build-a-language/out/routeql.py scenarios/s3-build-a-language/examples/01-basics.rql
```

---

## 7. Test Takımı ve Doğrulama Raporu

Sistemdeki tüm bileşenler bağımsız testlerle korunmaktadır. Aşağıdaki komutlar aracılığıyla tüm sistemi saniyeler içinde doğrulayabilirsiniz:

```bash
# 1. CampusRoute Çekirdek Testleri (69 Test)
cd app && python3 -m unittest discover -s tests

# 2. RouteQL Yorumlayıcı Kabul Testleri (16 Test)
python3 scenarios/s3-build-a-language/test_routeql.py

# 3. JavaScript/Node Schedule Port Testleri (20 Test)
node --test scenarios/s4-translate-code/out/

# 4. Mülakat Görevi Çalışma Saatleri Testleri (14 Test)
cd scenarios/s7-career-and-interview/challenge && python3 -m unittest test_opening_hours.py
```

### Test Özeti Tablosu
| Test Kategorisi | Test Dosyası / Modül | Koşucu | Test Sayısı | Durum |
|---|---|---|:---:|:---:|
| API & Güvenlik Başlıkları | `app/tests/test_api.py` | `unittest` | 12 | ✅ Geçti |
| Kampüs Graf Modeli | `app/tests/test_campus.py` | `unittest` | 13 | ✅ Geçti |
| Dijkstra & Rotalama | `app/tests/test_routing.py` | `unittest` | 9 | ✅ Geçti |
| Ders Programı & Çakışma | `app/tests/test_schedule.py` | `unittest` | 20 | ✅ Geçti |
| Arama & Türkçe Karakter | `app/tests/test_search.py` | `unittest` | 6 | ✅ Geçti |
| Yoğunluk & Kalabalık | `app/tests/test_occupancy.py` | `unittest` | 6 | ✅ Geçti |
| Açılış Saatleri Entegrasyonu | `app/tests/test_opening_hours.py` | `unittest` | 4 | ✅ Geçti |
| Doğal Dil AI Asistan | `app/tests/test_assistant.py` | `unittest` | 6 | ✅ Geçti |
| RouteQL Yorumlayıcısı | `scenarios/s3-build-a-language/test_routeql.py` | `unittest` | 16 | ✅ Geçti |
| JavaScript Schedule Portu | `scenarios/s4-translate-code/out/schedule.test.mjs` | `node:test` | 20 | ✅ Geçti |
| Mülakat Ev Ödevi | `scenarios/s7-career-and-interview/challenge/test_opening_hours.py` | `unittest` | 14 | ✅ Geçti |
| **TOPLAM** | **Bütünleşik Doğrulama Takımı** | — | **126** | **%100 BAŞARILI** |

---

## 8. Bob Agentic AI ve Güvenlik Altyapısı (`.bob/`)

Projenin kök dizinindeki `.bob/` klasörü, IBM Bob ajanının davranışlarını, izin sınırlarını ve özel becerilerini belirleyen kurumsal ajan konfigürasyonunu barındırır:

### 1. Özel Ajan Modları (`.bob/custom_modes.yaml`)
- **`grader` (Ödev Değerlendirici):** `groups: [read, skill]` yetkisiyle sınırlandırılmıştır; dosya yazma yetkisi bulunmadığı için öğrenci kodunu bozamaz veya hile yapamaz.
- **`campus-guide` (Kampüs Rehberi):** Yalnızca harita, rotalama, erişilebilirlik ve mekan sorgulamalarında uzmanlaşmış rehber modu.
- **`code-auditor` (Kod & Güvenlik Denetçisi):** Harici paket kullanımını (`pip`/`npm`), güvensiz fonksiyonları (`eval`/`exec`) ve kural ihlallerini denetleyen bağımsız güvenlik modu.

### 2. Ajan Becerileri (Skills)
- **`campus-guide` (`.bob/skills/campus-guide/SKILL.md`):** Kampüs graf teorisi, engelsiz rotalama, bina açılış saatleri ve yoğunluk analizini yürüten uzman ajan becerisi.
- **`code-auditor` (`.bob/skills/code-auditor/SKILL.md`):** Kod tabanındaki determinizmi, güvenlik başlıklarını, bellek tüketimini ve standart kütüphane uyumluluğunu doğrulayan otomatik denetim becerisi.

### 3. Ajanik Mühendislik Kuralları (Rules)
- **`feedback-tone.md`:** Öğrenci geri bildirimlerinde yapıcı, teşvik edici ve öğretici dili garanti altına alan pedagojik kural seti.
- **`agentic-engineering.md`:** Test güdümlü geliştirme (TDD), kök neden tespiti, standart kütüphane sadakati ve güvenli ajan davranışı ilkelerini zorunlu kılan mühendislik anayasası.

---

## 9. Tasarım İlkeleri, Güvenlik ve Katı Kurallar

Bu depoda kod geliştiren ajanların ve yazılımcıların uymakla yükümlü olduğu katı kurallar:
1. **Harici Bağımlılık Yasağı:** Kod tabanına `pip install` veya `npm install` gerektirecek hiçbir harici paket eklenemez. Yalnızca Python ve Node.js yerleşik standart kütüphaneleri kullanılır.
2. **Güvenli Yorumlama:** Yorumlayıcılarda, API'de veya iş mantığında `eval`, `exec`, `compile`, `os.system` veya `subprocess` çağrıları kesinlikle yasaktır.
3. **Miras Kodu Koruma:** `kiosk_router.py` dosyası ve senaryo girdi dokümanları doğrudan değiştirilemez. Tüm katılımcı çıktıları `out/` veya `plans/` klasörlerine yazılır.
4. **Yerel Ağ Kısıtı:** HTTP sunucuları yalnızca `127.0.0.1` (localhost) adresine bağlanır; dış ağlara dinleme açamaz.
5. **Sentetik Veri Gizliliği:** Kişi adları, programlar ve lokasyonlar tamamen sentetiktir; gerçek kişisel bilgi veya gizli veri eklenemez.
6. **TDD Disiplini:** Testler başarısız olduğunda testlerin beklenen değerleri değil, iş mantığını yürüten kaynak kod düzeltilir.

---

## 10. Takım Çalışması ve Katkı Rehberi

Takım arkadaşlarınızla birlikte çalışırken şu adımları izleyebilirsiniz:
1. Bir takım üyesi depoyu GitHub üzerinden **Fork** eder ve diğer arkadaşlarını **Collaborator** olarak ekler.
2. Ekip üyeleri depoyu yerel bilgisayarlarına klonlar:
   ```bash
   git clone https://github.com/<kullanici-adiniz>/bobathon.git
   cd bobathon
   ```
3. Yeni bir özellik veya senaryo için dal (branch) açılır:
   ```bash
   git switch -c senaryo-adi
   ```
4. Geliştirmeler tamamlanıp testler yeşile döndükten sonra değişiklikler commit edilip dala gönderilir:
   ```bash
   git add .
   git commit -m "feat: yeni özellik eklendi"
   git push -u origin senaryo-adi
   ```
5. GitHub üzerinden bir Çekme İsteği (Pull Request) açılarak takım içi kod incelemesi yapılır.

---

*Bu kapsamlı dokümantasyon, **IBM Bob** ekosistemine ve CampusRoute kurumsal mimarisine tam uyumlu olarak hazırlanmıştır.*
