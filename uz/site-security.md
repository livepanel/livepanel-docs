# Sayt xavfsizligi va skanerlash

## Saytga kirish (IP bo‘yicha)

![Saytga kirish](../images/site-access.png)

Sayt sahifasidagi **«Saytga kirish»** plitkasi saytni kim ocha olishini IP manzil yoki tarmoq bo‘yicha belgilaydi. Qoida saytning barcha sahifalari va fayllariga qo‘llanadi; panelga va SSL sertifikatini yangilashga ta’sir qilmaydi.

**Kirish rejimi:**

- **Hamma uchun ochiq** — standart.
- **Faqat ro‘yxatdagi manzillarga ruxsat** — ofis yoki ishlab chiqish serverlari uchun. Ro‘yxatda bo‘lmagan har kim «403 Forbidden» ko‘radi — o‘z IP manzilingizni ham qo‘shishni unutmang.
- **Ro‘yxatdagi manzillarni bloklash** — muammo tug‘dirayotgan botlar va hujumchilar uchun.

Ro‘yxatga har qatorga bitta IP (`203.0.113.7`) yoki tarmoq (`198.51.100.0/24`) yoziladi; IPv6 ham bo‘ladi.

> Sayt Cloudflare kabi proxy orqali ishlasa, Nginx tashrifchining emas, proxy’ning IP manzilini ko‘radi — bu holda qoida kutilganidek ishlamaydi.

Shu sahifada **login va parol bilan himoya** holati ham ko‘rinadi; **«Sozlash»** uni sayt sozlamalarida ochadi ([Sayt sozlamalari](site-settings.md) → HTTP avtorizatsiya).

## Skanerlash (antivirus)

![Skanerlash](../images/scan.png)

**«Skanerlash»** plitkasi sayt papkasidagi barcha fayllarni **ClamAV** antivirusi bilan viruslar, web-shell va zararli kodga tekshiradi. Skanerlash fonda, past ustuvorlikda ishlaydi — sayt sekinlashmaydi.

ClamAV serverda o‘rnatilgan bo‘lishi kerak: administrator uni **Tizim → Ilovalar** → `clamav` dan o‘rnatadi. Virus bazasi ~300 MB yuklanadi, skanerlash paytida ~1 GB RAM ishlatiladi.

1. **«Skanerlash»** tugmasini bosing. Sayt hajmiga qarab bir necha daqiqa davom etadi.
2. Natija: **«Tahdid topilmadi»** yoki **«N ta shubhali fayl topildi»** — fayl yo‘li va tahdid nomi bilan.
3. Har bir topilgan fayl uchun:
   - **Karantinga** — fayl saytdan olib qo‘yiladi va ishlamaydi; xato bilan olingan bo‘lsa **Tiklash** mumkin;
   - **Butunlay o‘chirish**.

Sayt buzilgan bo‘lsa: zararli fayllarni olib tashlang, CMS va plaginlarni yangilang, barcha parollarni (panel, FTP, baza, CMS administratori) almashtiring.

## Veb-firewall (WAF)

![Veb-firewall](../images/waf.png)

**Sayt sozlamalari → Veb-firewall (WAF)** — har bir sayt uchun ModSecurity va OWASP Core Rule Set (CRS 3.3). U saytga keladigan so‘rovlarni tekshiradi va SQL injection, XSS, fayl yo‘lini buzish (`../`), buyruq kiritish hamda zararli skanerlarni to‘xtatadi.

**Rejimlar:**

- **O‘chiq** — so‘rovlar tekshirilmaydi;
- **Faqat kuzatish** — hech narsa to‘xtatilmaydi, shubhali so‘rovlar faqat yoziladi. Yangi saytda avval shu rejimni bir-ikki kun sinab ko‘ring;
- **Bloklash** — hujum belgisi bor so‘rov `403` bilan to‘xtatiladi.

**Sayt ilovasi** — WordPress, Drupal, Nextcloud, DokuWiki yoki XenForo tanlansa, CRS’ning shu ilova uchun tayyor istisnolari yoqiladi va admin panel, muharrir kabi qismlar noto‘g‘ri bloklanmaydi.

**Oxirgi to‘xtatilgan so‘rovlar** jadvalida vaqt, IP, so‘rov va ishlagan qoidalar (ID va tavsif) ko‘rinadi. Agar qoida oddiy foydalanuvchini to‘xtatayotgan bo‘lsa (false positive), uning yonidagi **«Bu qoidani o‘chirish»** tugmasini bosing — ID **O‘chirilgan qoidalar** ro‘yxatiga tushadi. Keyin **Saqlash**ni bosing. Qoidani faqat shu saytda o‘chiradi.

Birinchi marta yoqilganda panel ModSecurity paketlarini o‘zi o‘rnatadi (bir daqiqagacha). Har bir WAF yoqilgan sayt Nginx’ga taxminan 10–15 MB xotira qo‘shadi. API orqali: sayt sozlamalarida `waf`, `waf_app`, `waf_skip`, hodisalar — `GET /sites/waf` ([API v2](api-reference.md)).

## Boshqa himoya choralari

- Saytga so‘rovlar chegarasi — [Sayt sozlamalari](site-settings.md) → Xavfsizlik.
- Server darajasidagi firewall — [Firewall](firewall.md).
- Panel, SSH, FTP va pochtaga parol tanlash hujumlaridan himoya — [Panel sozlamalari va xavfsizlik](panel-settings.md).
