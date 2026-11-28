# O‘rnatish

LivePanel toza serverga bitta buyruq bilan, odatda 5–10 daqiqada o‘rnatiladi.

## Talablar

| | Minimal | Tavsiya |
|---|---|---|
| Operatsion tizim | **Ubuntu 22.04 LTS** yoki **Ubuntu 24.04 LTS**, toza o‘rnatilgan | Ubuntu 24.04 LTS |
| Protsessor | 1 vCPU, x86_64 | 2 vCPU va ko‘proq |
| Tezkor xotira | 1 GB | 2 GB va ko‘proq |
| Disk | 10 GB | 20 GB va ko‘proq (SSD) |
| Kirish | root yoki sudo huquqi | — |
| Tarmoq | ommaviy IP manzil | — |

Ochiq bo‘lishi kerak bo‘lgan portlar: **80** va **443** (saytlar va Let’s Encrypt), **6563** (panel), **22** (SSH). Pochta ishlatilsa — 25, 465, 587, 993, 995.

> Serverda boshqa panel (cPanel, Plesk, ISPmanager va hokazo) yoki o‘rnatilgan Nginx/Apache sozlamalari bo‘lmasin. Toza server — muammosiz o‘rnatishning eng ishonchli yo‘li.

## 1. Serverga ulaning

Kompyuteringizdan serverga SSH orqali ulaning (Windows’da PowerShell yoki PuTTY, macOS va Linux’da Terminal):

```bash
ssh root@SERVER_IP
```

## 2. O‘rnatish buyrug‘ini bajaring

```bash
curl -fsSL https://livepanel.uz/install.sh | sudo bash
```

Skript quyidagilarni ketma-ket bajaradi va har bir qadamni ekranda ko‘rsatadi:

1. LivePanel paketini yuklab oladi va uning **imzosi hamda nazorat summasini tekshiradi**;
2. panelni o‘rnatadi;
3. Nginx va tizim PHP’sini (FPM) o‘rnatadi: Ubuntu 22.04’da PHP 8.1, Ubuntu 24.04’da PHP 8.3;
4. MySQL 8 va phpMyAdmin’ni o‘rnatadi;
5. FTP/SFTP serveri (ProFTPD)ni o‘rnatadi;
6. Let’s Encrypt mijozi (certbot) va Node.js LTS’ni o‘rnatadi;
7. hosting agentini ishga tushiradi.

## 3. Kirish ma’lumotlarini saqlang

O‘rnatish tugagach, ekranda shunday yozuv chiqadi:

```text
LivePanel is ready

  Address:   https://SERVER_IP:6563
  Login:     liveadmin
  Password:  ************

  Save this password now: it is shown only once and is not stored.
```

**Parolni darhol saqlab qo‘ying** — u faqat bir marta ko‘rsatiladi va serverda saqlanmaydi. Parol yo‘qolsa, serverda yangisini o‘rnatasiz:

```bash
livepanel passwd liveadmin
```

O‘rnatish logi `/var/log/livepanel-install.log` faylida turadi.

## 4. Panelni oching

Brauzerda `https://SERVER_IP:6563` manzilini oching. Panel dastlab o‘zi yaratgan (self-signed) sertifikatdan foydalanadi, shuning uchun brauzer «Ulanish xavfsiz emas» deb ogohlantiradi — **«Qo‘shimcha» → «Davom etish»** ni bosing. Keyinchalik panelga ishonchli sertifikat yoki domen ulash mumkin: [Panel manzili va SSL](panel-access.md).

Login `liveadmin` va saqlangan parol bilan kiring — [Birinchi kirish va interfeys](first-login.md).

## Panelni o‘chirish

LivePanel va u o‘rnatgan hamma narsani olib tashlash uchun serverda:

```bash
livepanel remove
```

Boshqa server buyruqlari — [Server buyruqlari](console.md).

> Bu buyruq saytlar, bazalar va pochtani ham o‘chiradi. Avval kerakli ma’lumotlarning zaxira nusxasini oling.

## Muammolar

- **«Ubuntu 22.04 or 24.04 LTS is required»** — boshqa OS o‘rnatilgan. Serverni Ubuntu 22.04 yoki 24.04 bilan qayta o‘rnating.
- **Panel ochilmayapti** — 6563-port provayderning tashqi firewall’ida yopiq bo‘lishi mumkin. Hosting provayderingiz boshqaruv panelidan portni oching.
- **O‘rnatish to‘xtab qoldi** — `/var/log/livepanel-install.log` faylining oxirini ko‘ring va buyruqni qayta ishga tushiring.
