# SAFE XXE Learning Lab (Python + Flask)

**Amaç:** XXE (XML External Entity) zafiyetinin ne olduğunu güvenli şekilde, gerçek sisteme zarar vermeden öğrenmek.
Bu lab *bilerek zafiyet barındırmaz*. Aksine, güvenli XML ayrıştırma (parsing) yöntemini gösterir ve XXE girişimlerini tespit edip reddeder.

> Neden güvenli? `defusedxml` kullanıyoruz ve yüklenen XML içeriğinde `DOCTYPE`/`ENTITY` gibi XXE göstergeleri varsa istek uygun bir mesajla reddediliyor.

## Kurulum

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Çalıştırma

```bash
export FLASK_ENV=development
python app.py
# Uygulama varsayılan olarak http://127.0.0.1:5000 üzerinde çalışır.
```

## Kullanım

1. Ana sayfadaki formdan `samples/benign.xml` dosyasını yükleyin — başarılı parse sonucu dönmelidir.
2. Daha sonra `samples/xxe_attempt_doctype.xml` veya `samples/xxe_attempt_parameter_entity.xml` dosyalarını deneyin — uygulama güvenle reddeder ve bir uyarı mesajı gösterir.

## Testler

```bash
pytest -q
```

## Klasör Yapısı

```
.
├── app.py
├── requirements.txt
├── templates
│   ├── index.html
│   └── result.html
├── samples
│   ├── benign.xml
│   ├── xxe_attempt_doctype.xml
│   └── xxe_attempt_parameter_entity.xml
└── tests
    └── test_app.py
```

## XXE Nedir? (Özet)

XXE, XML ayrıştırıcısının *harici entity* tanımlarını çözmesine izin verildiğinde gerçekleşir. Saldırgan aşağıdaki gibi bir `DOCTYPE`/`ENTITY` tanımıyla sistem dosyalarını okumaya veya SSRF benzeri istekler yaptırmaya çalışabilir:

```xml
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
```

**Önleme:** Harici varlık/DTD çözümlemeyi kapatın, güvenli kütüphaneler (`defusedxml`) kullanın, gelen XML'i şema doğrulamasından geçirin, `text/plain` dışı içerik türlerinde sıkı doğrulama yapın ve içgözlem/loglama uygulayın.

> Bu lab, savunma odaklıdır. Bilerek zafiyet barındıran örnek sunmaz.
