# Git orqali deploy

Saytga GitHub, GitLab yoki boshqa Git repozitoriyni ulab, kodni bir bosishda — yoki har `git push` da avtomatik — saytga yuklaysiz. Sayt sahifasidagi **«Git»** plitkasidan ochiladi.

![Git](../images/git.png)

## Repozitoriyni ulash

1. **Repozitoriy manzili**:
   - ochiq repozitoriy: `https://github.com/user/project.git`;
   - yopiq repozitoriy: `git@github.com:user/project.git` (pastdagi deploy kaliti kerak).
2. **Branch** — masalan `main` yoki `master`.
3. **Deploy’dan keyin buyruq** (ixtiyoriy) — fayllar yuklangach sayt papkasida bajariladi:

   | Sayt turi | Misol |
   |---|---|
   | PHP | `composer install --no-dev --optimize-autoloader` |
   | Node.js | `npm install && npm run build --if-present` |
   | Python | `.venv/bin/pip install -r requirements.txt` |

4. **«Ulash va yuklab olish»** ni bosing. Ochiq repozitoriyda fayllar darhol yuklanadi.

## Yopiq repozitoriy: deploy kaliti

Panel saytga alohida **deploy kaliti** (SSH kalit) yaratadi va sahifada ko‘rsatadi. Uni repozitoriyga qo‘shing:

- **GitHub:** repozitoriy → **Settings → Deploy keys → Add deploy key** → kalitni joylang (yozish ruxsati kerak emas).
- **GitLab:** **Settings → Repository → Deploy keys**.

Keyin **«Deploy»** tugmasini bosing.

## Deploy qanday ishlaydi

1. Repozitoriydan tanlangan branch olinadi va sayt papkasiga yoziladi (`git fetch` + `git checkout -f`).
2. Submodullar bo‘lsa, ular ham yangilanadi.
3. Panelning boshlang‘ich sahifasi repozitoriyda bo‘lmasa, olib tashlanadi.
4. Deploy’dan keyingi buyruq bajariladi.
5. Node.js va Python saytlarda xizmat qayta ishga tushiriladi.

**Repozitoriyda yo‘q fayllar o‘chmaydi** — yuklangan rasmlar, `.env`, keshlar joyida qoladi. Hamma amallar sayt foydalanuvchisi nomidan bajariladi.

Buyruqda `node`, `npm`, `npx`, `composer`, `php` va saytning Python muhiti ishlaydi.

> Deploy buyrug‘iga `npm start` kabi to‘xtamaydigan buyruqlarni yozmang — deploy 20 daqiqadan keyin xato bilan to‘xtaydi. Ilovani doimiy ishlatishni sayt xizmati bajaradi ([Python va Node.js saytlar](python-nodejs.md)).

## Webhook: har push’da avtomatik deploy

Sahifadagi **webhook manzili**ni repozitoriyga qo‘shing:

- **GitHub:** **Settings → Webhooks → Add webhook** — Payload URL: webhook manzili, Content type: `application/json`, voqea: **Just the push event**.
- Panel sertifikati o‘zi imzolangan bo‘lsa, **SSL verification** ni o‘chiring (yoki panelga ishonchli sertifikat oling — [Panel manzili va SSL](panel-access.md)).

Manzil maxfiy token saqlaydi — uni boshqalarga bermang. Yangilash tugmasi yangi manzil yaratadi (eskisi ishlamay qoladi).

## Deploy natijasi

Sahifa pastida oxirgi deploy ko‘rinadi: holati, vaqti, kim ishga tushirgani (**paneldan** yoki **webhook orqali**), commit va to‘liq log. Xato bo‘lsa, logda qaysi qadam muvaffaqiyatsiz bo‘lgani yozilgan:

| Xato | Sababi |
|---|---|
| Repozitoriyni yuklab bo‘lmadi | Manzil yoki branch noto‘g‘ri, yopiq repoda deploy kaliti qo‘shilmagan |
| Deploy’dan keyingi buyruq xato bilan tugadi | Buyruq xatosi — logning oxirini ko‘ring |

**«Uzish»** Git sozlamasini olib tashlaydi; sayt fayllari va `.git` papkasi joyida qoladi.
