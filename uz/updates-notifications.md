# Yangilanishlar va xabarnomalar

## Avtomatik yangilanish

Yangilanishlar **Sozlamalar → Avtomatik yangilash** bo‘limida boshqariladi (faqat administrator).

- **Yangilanishlarni avtomatik qabul qilish** — yoqilgan bo‘lsa, yangi versiya chiqishi bilan panel o‘zi yangilanadi.
- Standart holatda **o‘chirilgan**: yangi versiya chiqsa, ekranning yuqori o‘ng burchagida `{versiya} Yangilanish mavjud` xabari va **Yangilash** tugmasi chiqadi. Tugma bosilganda panel yangilanadi va sahifa yangi versiyada qayta ochiladi. Yangilamaguningizcha xabar turaveradi; panel eng oxirgi versiyaga o‘tgach xabar yo‘qoladi.
- Bo‘limda o‘rnatilgan versiya va mavjud yangilanish ham ko‘rinadi, **Yangilash** tugmasi u yerda ham bor.

Qanday ishlaydi:

- Server yangi versiyani **har 6 soatda** tekshiradi. Administrator panelga kirganda ham tekshiruv boshlanadi.
- Yangi versiya livepanel.uz’dan yuklanadi va **raqamli imzosi** hamda nazorat summasi tekshiriladi — imzosiz yoki o‘zgartirilgan paket o‘rnatilmaydi.
- O‘rnatilgandan keyin panel ishlashi tekshiriladi; muammo bo‘lsa, **oldingi versiyaga avtomatik qaytadi** va panel «Yangilab bo‘lmadi» deb ko‘rsatadi.
- Saytlar yangilanish paytida ishlashda davom etadi.

Joriy versiya kirish sahifasining pastida va chap menyuning pastida ko‘rinadi (masalan `2026.11.25`).

Yangi versiyani darhol tekshirish kerak bo‘lsa, serverda:

```bash
systemctl start livepanel-update.service
```

> Yangilanish litsenziya faol bo‘lganda ishlaydi.

## Email xabarnomalar

Panel muhim hodisalar haqida **push@livepanel.uz** manzilidan email yuboradi. Xat akkauntning **tiklash emailiga** keladi ([Panel sozlamalari va xavfsizlik](panel-settings.md)) va foydalanuvchi panelda tanlagan tilda yoziladi. Bir hodisa haqida qayta-qayta xat yuborilmaydi.

| Hodisa | Kimga |
|---|---|
| Akkauntga yangi IP manzildan kirildi | akkaunt egasiga |
| Disk 90% dan ko‘p to‘ldi | administratorga |
| Server xizmati to‘xtadi (Nginx, MySQL, PHP-FPM va boshqalar) | administratorga |
| SSL sertifikat muddati 14 kundan kam qoldi | sayt egasiga va administratorga |
| Akkaunt RAM limiti tufayli bloklandi | akkaunt egasiga va administratorga |

Xat kelmasa: tiklash emaili kiritilganini va «Spam» papkasini tekshiring.
