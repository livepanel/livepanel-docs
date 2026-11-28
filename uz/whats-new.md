# Yangiliklar

LivePanel yangi versiyani har 6 soatda va administrator kirganda tekshiradi; u avtomatik yoki **Yangilash** tugmasi bilan o‘rnatiladi — [Yangilanishlar va xabarnomalar](updates-notifications.md). Versiya raqami — sana va vaqt (UTC): `YYYY.MM.DD.HHMM`. Joriy versiya panel menyusining pastida ko‘rinadi. Bu sahifada oxirgi o‘zgarishlar — yangisi tepada.

## 2026.11.28.1534 — Avtomatik yangilash sozlamasi

- **Sozlamalar → Avtomatik yangilash**: yangilanishlarni avtomatik qabul qilishni yoqish yoki o‘chirish mumkin. Standart holatda o‘chirilgan.
- O‘chirilgan bo‘lsa, yangi versiya chiqqanda ekranning yuqori o‘ng burchagida `{versiya} Yangilanish mavjud` xabari va **Yangilash** tugmasi chiqadi; panel tugma bosilganda yangilanadi — [Yangilanishlar va xabarnomalar](updates-notifications.md).

## 2026.11.26.1641 — Veb-firewall (WAF) va wildcard SSL boshqa DNS bilan

- **Veb-firewall (WAF)** — har bir sayt uchun ModSecurity + OWASP CRS: bloklash yoki faqat kuzatish rejimi, WordPress/Drupal/Nextcloud istisnolari, to‘xtatilgan so‘rovlar ro‘yxati va noto‘g‘ri ishlagan qoidani bir bosishda o‘chirish — [Sayt xavfsizligi](site-security.md#veb-firewall-waf).
- **Wildcard SSL DNS boshqa joyda bo‘lsa ham** ishlaydi: registratorda bitta `_acme-challenge` NS yozuvi yetadi, panel aniq yozuvni ko‘rsatadi — [SSL sertifikatlar](ssl.md#wildcard-sertifikat-premium).
- API v2: `GET /sites/waf`, sayt sozlamalarida `waf`, `waf_app`, `waf_skip`.

## 2026.11.26.1605 — Sayt statistikasi

- **Tashriflar hisoboti** (GoAccess) yana ochiladi: oldin sahifa doim «yuklanmoqda» holatida qolardi. Hisobot avvalgidek paneldan ajratilgan (sandbox) holda ochiladi — [Statistika](statistics.md).

## 2026.11.26.1523 — Wildcard SSL va DNSSEC

- **Wildcard SSL (Premium)** — domen va barcha subdomenlari uchun bitta Let’s Encrypt sertifikati (`example.uz` + `*.example.uz`). Panel tekshiruv TXT yozuvini DNS zonasiga o‘zi qo‘shadi va o‘chiradi, sertifikat avtomatik yangilanadi — [SSL sertifikatlar](ssl.md#wildcard-sertifikat-premium).
- **DNSSEC** — zona imzolanadi, panel registratorga qo‘yiladigan DS yozuvini ko‘rsatadi — [Domenlar va DNS](dns.md#dnssec).
- API v2: `POST /sites/ssl` da `wildcard`, `POST /dns` da `dnssec` amali — [API v2](api-reference.md).

## 2026.11.26.0718 — Litsenziya himoyasi

- Free kaliti faol Premium litsenziyani almashtira olmaydi (`409 license_not_better`); bir tarifda muddati uzunrog‘i qoladi.
- Ishlamaydigan «kod bilan faollashtirish» olib tashlandi: pullik kalitlar to‘lovdan keyin o‘zi keladi — [Litsenziya va tariflar](license.md#litsenziya-kalitlari-qanday-himoyalangan).
- livepanel.uz kalitni faqat litsenziya egasi bo‘lgan serverga beradi.

## 2026.11.25 — API v2

- **API v2 (Premium)**: paneldagi deyarli hamma imkoniyat API orqali — saytlar, fayllar, bazalar, DNS, pochta, FTP, cron, zaxira, Git, akkauntlar, limitlar, brending va server. 13 bo‘lim, har biri uchun «o‘qish» va «yozish» ruxsati — [API tokenlar](api-tokens.md), [API v2 ma’lumotnomasi](api-reference.md).
- PHP, Node.js va Bash misollari, OpenAPI fayli: [openapi.json](https://wiki.livepanel.uz/openapi.json). Hujjatni sun’iy intellektga berish uchun har sahifada «AI uchun nusxalash» tugmasi va `.md` havolasi bor.
- Fayl menejeri: mavjud papka yaratilsa `file_exists`; yuklashda `overwrite=1` bilan faylni almashtirish mumkin.
- Zaxira (Google Drive, Dropbox) ulanishi faqat panelning o‘z manziliga qaytadi.
