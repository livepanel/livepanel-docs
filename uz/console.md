# Server buyruqlari

Serverda SSH orqali, root sifatida, `livepanel` buyrug‘i ishlaydi. Mavjud buyruqlar ro‘yxati:

```bash
livepanel --help
```

| Buyruq | Vazifasi |
|---|---|
| `livepanel ip-access on` | Panelga IP orqali kirishni yoqish — 6563-port hamma uchun ochiq |
| `livepanel ip-access off` | Panel faqat panel manzillari orqali ochiladi — 6563-port tashqaridan yopiladi |
| `livepanel ip-access status` | IP orqali kirish holatini ko‘rsatish |
| `livepanel passwd NAME` | Panel akkauntiga yangi parol o‘rnatish |
| `livepanel remove` | LivePanel’ni va u o‘rnatgan hamma narsani o‘chirish |
| `livepanel --help` | Buyruqlar ro‘yxati |

Noma’lum buyruq kiritilsa, terminal buni aytadi va ro‘yxatni `livepanel --help` orqali ko‘rish mumkinligini eslatadi.

## IP orqali kirish

```bash
livepanel ip-access off
```

6563-port tashqaridan yopiladi va panel faqat o‘z manzili orqali ochiladi, masalan `https://panel.example.uz`. Serverning o‘zidan (`127.0.0.1`) kirish ochiq qoladi. Buyruq Let’s Encrypt yoki o‘z sertifikati bor [panel manzili](panel-access.md) bo‘lsagina ishlaydi — bunday manzil bo‘lmasa, IP orqali kirish yoqilganicha qoladi.

Panel manzili ishlamay qolsa (DNS, domen muddati va hokazo), IP orqali kirishni qayta yoqing:

```bash
livepanel ip-access on
```

Xuddi shu sozlama panelda ham bor: **Sozlamalar → Panel manzillari → IP orqali kirish**.

## Panel paroli

```bash
livepanel passwd liveadmin
```

Yangi parol so‘raladi. Bo‘sh qoldirilsa, panel parolni o‘zi yaratib, ekranga chiqaradi.

## Panelni o‘chirish

```bash
livepanel remove
```

Saytlar va ularning fayllari, ma’lumotlar bazalari, pochta, SSL sertifikatlar, zaxira nusxalar, veb, baza, FTP va pochta serverlari hamda **Ilovalar** bo‘limidan o‘rnatilgan dasturlar o‘chiriladi. Buyruq uch marta tasdiq so‘raydi: `Y` (Yes), ekranda ko‘rsatilgan bir martalik kod va yana bir `Y`. Keyin har bir bosqich o‘z qatorida 0% dan 100% gacha bajarilish foizini ko‘rsatadi.

> Bu amalni qaytarib bo‘lmaydi. Avval kerakli ma’lumotlarning zaxira nusxasini oling — [Zaxira nusxalar](backups.md).
