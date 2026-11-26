# SSL sertifikatlar

SSL sertifikat sayt bilan brauzer orasidagi trafikni shifrlaydi va sayt `https://` orqali ochiladi. Panel **Let’s Encrypt**’dan bepul sertifikatni bir bosishda oladi va muddatidan oldin avtomatik yangilaydi.

![SSL sertifikatlar](../images/ssl.png)

## Sertifikat olish

1. Domen (va `www` aliasi) **shu server IP manziliga yo‘naltirilgan** bo‘lsin. DNS o‘zgarishi tarqalishi bir necha daqiqadan bir necha soatgacha davom etadi.
2. Sayt sahifasida **«SSL sertifikatlar»** plitkasini oching.
3. **«Yangi sertifikat»** tugmasini bosing.
4. Saytni va turini tanlang:
   - **Let’s Encrypt** — ishonchli, bepul, 90 kunlik; panel uni o‘zi yangilaydi.
   - **O‘z-o‘zidan imzolangan** — trafikni shifrlaydi, lekin brauzer ogohlantiradi. Domeni hali yo‘naltirilmagan sinov saytlari uchun.
5. **Email** ixtiyoriy: Let’s Encrypt muddat bilan bog‘liq muammolar haqida shu manzilga yozadi.
6. **«Barcha HTTP so‘rovlarni HTTPS’ga yo‘naltirish»** ni yoqib qo‘ying.
7. Tasdiqlang. Sertifikat bir necha soniyada o‘rnatiladi.

Sertifikat saytning domeni va barcha aliaslari uchun olinadi.

## Sertifikatlar ro‘yxati

Jadvalda sayt, turi, amal qilish muddati va HTTPS’ga yo‘naltirish holati ko‘rinadi. Satr menyusidan:

- **Qayta chiqarish** — sertifikatni yangidan olish (masalan, alias qo‘shgandan keyin);
- **HTTPS’ga yo‘naltirishni yoqish/o‘chirish**;
- **Sertifikatni o‘chirish** — sayt faqat HTTP orqali ishlaydi.

## Wildcard sertifikat (Premium)

Wildcard sertifikat domenning o‘zi va **barcha subdomenlari** uchun bitta sertifikat: `example.uz` va `*.example.uz`. Bu imkoniyat faqat **Premium** litsenziyali panellarda ishlaydi.

Shartlar:

- domenning DNS zonasi shu panelda bo‘lishi kerak — [Domenlar va DNS](dns.md);
- registratorda domenning NS serverlari shu serverga yo‘naltirilgan bo‘lishi kerak (`dig NS example.uz`).

Olish tartibi: **Yangi sertifikat** → **Let’s Encrypt** → **Wildcard: \*.domen ham** belgisini qo‘ying. Let’s Encrypt domenni DNS orqali tekshiradi. Panel `_acme-challenge` TXT yozuvini zonaga o‘zi qo‘shadi va tekshiruvdan keyin o‘chiradi. Sertifikat avtomatik yangilanadi, yangilanishda ham shu yo‘l ishlatiladi.

Wildcard sertifikatli sayt o‘z sayti bo‘lmagan barcha subdomenlarga ham javob beradi (`server_name` ga `*.domen` qo‘shiladi). O‘z sayti bor subdomenlar avvalgidek o‘z saytini ochadi.

Xatolar:

- **zona yo‘q** — avval **Domenlar va DNS** bo‘limida zonani yarating;
- **NS shu serverga yo‘naltirilmagan** — registratorda NS’ni almashtiring va tarqalishini kuting.

## Avtomatik yangilanish

Let’s Encrypt sertifikatlari muddati tugashidan oldin o‘zi yangilanadi. Muddati 14 kundan kam qolgan va yangilanmagan sertifikat haqida panel sayt egasi va administratorga email yuboradi.

## Sertifikat olinmasa

- **Domen boshqa IP’ga yo‘naltirilgan** — A yozuvini tekshiring: `nslookup example.uz`.
- **80-port yopiq** — Let’s Encrypt tekshiruvi 80-port orqali o‘tadi. Firewall’da HTTP qoidasi turishi kerak — [Firewall](firewall.md).
- **Cloudflare proxy (to‘q sariq bulut)** yoqilgan — vaqtincha o‘chiring yoki Cloudflare’da SSL rejimini «Full» qiling.
- **Juda ko‘p urinish** — Let’s Encrypt bir domen uchun urinishlarni cheklaydi; bir soatdan keyin qayta urining.

Panelning o‘zi uchun SSL — [Panel manzili va SSL](panel-access.md).
