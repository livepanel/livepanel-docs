# Savollar va muammolar

## Panel

**Panel ochilmayapti.**
Serverda xizmatlar holatini tekshiring: `systemctl status livepanel livepanel-agent`. 6563-port provayderning tashqi firewall’ida ochiqligini tekshiring. Panel firewall’i SSH va panel portini hech qachon yopmaydi.

**Administrator paroli esdan chiqdi.**
Tiklash emaili kiritilgan bo‘lsa — kirish sahifasidagi **«Parolni unutdingizmi?»**. Bo‘lmasa, serverda SSH orqali: `livepanel passwd liveadmin`.

**IP manzilim bloklandi.**
Bir necha daqiqadan keyin blok o‘zi ochiladi. Shoshilinch bo‘lsa, boshqa IP’dan (masalan telefon interneti orqali) kirib **Sozlamalar → Login himoyasi** da blokdan chiqaring va IP’ingizni oq ro‘yxatga qo‘shing.

**Telefon yo‘qoldi, 2FA kodi yo‘q.**
Zaxira kodlardan birini kiriting. Ular ham yo‘q bo‘lsa, administrator **Foydalanuvchilar** bo‘limida akkaunt uchun 2FA’ni o‘chiradi.

**«Litsenziya muddati tugagan» / «Litsenziya boshqa serverga bog‘langan».**
[Litsenziya va tariflar](license.md) — uzaytirish yoki litsenziyani yangi serverga ko‘chirish.

## Saytlar

**Sayt ochilmayapti, «sayt topilmadi» yoki boshqa sayt ochiladi.**
Domen A yozuvi server IP manziliga qaratilganini tekshiring: `nslookup example.uz`. DNS o‘zgarishi bir necha soat tarqalishi mumkin.

**403 Forbidden.**
Sayt o‘chirib qo‘yilgan, IP «Saytga kirish» bo‘limida bloklangan yoki papkada bosh sahifa (`index.php` / `index.html`) yo‘q.

**500 yoki 502 xato.**
**Loglar → Xatolar logi** (PHP) yoki **Ilova logi** (Node.js, Python) ni oching — sabab shu yerda. 502 — ilova ishlamayapti yoki boshqa portda tinglayapti.

**PHP’ga katta fayl yuklanmayapti.**
**Sozlamalar → Backend → PHP sozlamalari** da `upload_max_filesize` va `post_max_size` ni oshiring.

**SSL sertifikat olinmadi.**
[SSL sertifikatlar](ssl.md) → «Sertifikat olinmasa».

**Saytni boshqa serverga ko‘chirish.**
Eski serverda zaxira nusxani Google Drive yoki Dropbox’ga yuboring, yangi serverda xuddi shu omborni ulab nusxani **«Serverga olish»** bilan oling va tiklang — [Zaxira nusxalar](backups.md). Yoki nusxani yuklab olib, yangi serverga yuklang.

## Pochta

**Gmail’ga xat ketmayapti.**
Provayder chiquvchi 25-portni yopgan bo‘lishi mumkin — panel bu haqda ogohlantiradi. Provayderga murojaat qiling.

**Xatlar spamga tushyapti.**
SPF, DKIM, DMARC yozuvlari va serverning PTR (reverse DNS) yozuvini tekshiring — [Pochta](mail.md).

## Disk va resurslar

**Disk to‘lib qoldi.**
**Fayllar → Disk statistikasi** eng katta papka va fayllarni ko‘rsatadi. Eski zaxira nusxalar, loglar va keshlarni tozalang; avtomatik zaxirada saqlanadigan nusxalar sonini kamaytiring.

**Akkaunt «RAM blok» bo‘ldi.**
Saytlar RAM limitidan oshgan. Limitni oshiring yoki saytni optimallashtiring, keyin akkauntni tahrirlab **«Akkaunt faol»** ni yoqing — [Foydalanuvchilar, rollar va limitlar](users.md).

## Panelni o‘chirish

Serverda: `livepanel remove`. Bu saytlar, bazalar va pochtani ham o‘chiradi — avval zaxira oling.

## Yordam

Javob topilmasa, livepanel.uz’dagi aloqa ma’lumotlari orqali murojaat qiling. Murojaatda panel versiyasi, xato matni va tegishli log qatorlarini yozing.
