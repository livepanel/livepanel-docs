# Yangilanishlar va xabarnomalar

## Avtomatik yangilanish

LivePanel o‘zini avtomatik yangilaydi — qo‘lda hech narsa qilish shart emas.

- Server yangi versiyani **har 6 soatda** tekshiradi. Administrator panelga kirganda ham tekshiruv boshlanadi.
- Yangi versiya livepanel.uz’dan yuklanadi va **raqamli imzosi** hamda nazorat summasi tekshiriladi — imzosiz yoki o‘zgartirilgan paket o‘rnatilmaydi.
- O‘rnatilgandan keyin panel ishlashi tekshiriladi; muammo bo‘lsa, **oldingi versiyaga avtomatik qaytadi**.
- Saytlar yangilanish paytida ishlashda davom etadi.

Joriy versiya kirish sahifasining pastida va chap menyuning pastida ko‘rinadi (masalan `2026.11.25`).

Yangilanishni darhol ishga tushirish kerak bo‘lsa, serverda:

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
