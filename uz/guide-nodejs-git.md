# Node.js ilovani GitHub’dan deploy qilish

Bu qo‘llanmada GitHub’dagi Express (yoki Next.js, NestJS) ilovani panelga ulaymiz: har `git push` dan keyin sayt o‘zi yangilanadi.

**Kerak bo‘ladi:** GitHub repozitoriy, serverga yo‘naltirilgan domen (masalan `api.example.uz`).

## 1. Ilovani tayyorlang

Panel ilovani sayt papkasidagi **`app.js`** fayli orqali ishga tushiradi va portni `PORT` muhit o‘zgaruvchisida beradi. Repozitoriy ildizida `app.js` bo‘lsin:

```js
const express = require("express");
const app = express();

app.get("/", (req, res) => res.json({ ok: true }));

app.listen(Number(process.env.PORT), "127.0.0.1", () => {
  console.log("listening on", process.env.PORT);
});
```

**Next.js yoki NestJS** bo‘lsa, `app.js` ni o‘zingiz yozishingiz shart emas: 2-qadamda saytni **CMS / Framework → Node.js → Next.js** (yoki NestJS) bilan yarating. Panel ilovani to‘g‘ri port va manzilda ishga tushiradigan `app.js` ni o‘zi yozadi. Git deploy repozitoriyda yo‘q fayllarni o‘chirmaydi, shuning uchun bu fayl joyida qoladi — repozitoriydagi kod bilan ishlayveradi.

`package.json` da kerakli paketlar bo‘lsin. `node_modules` ni repozitoriyga qo‘shmang.

## 2. Node.js sayt yarating

1. **Saytlar → «Sayt yaratish» → Node.js** (Next.js va NestJS uchun — **CMS / Framework → Node.js → Next.js / NestJS**).
2. Domen: `api.example.uz`, kerakli Node.js versiyasi (boshqa versiyalar — **Tizim → Ilovalar**).
3. **«Sayt yaratish»**.

## 3. Repozitoriyni ulang

![Git](../images/git.png)

1. Sayt sahifasida **«Git»** plitkasi.
2. **Repozitoriy manzili:**
   - ochiq repo — `https://github.com/user/app.git`;
   - yopiq repo — `git@github.com:user/app.git` va sahifadagi **deploy kalitini** GitHub’da **Settings → Deploy keys** ga qo‘shing.
3. **Branch:** `main`.
4. **Deploy’dan keyin buyruq:**

   ```bash
   npm ci --omit=dev || npm install --omit=dev
   ```

   Build kerak bo‘lsa (Next.js, NestJS, TypeScript):

   ```bash
   npm ci && npm run build
   ```

5. **«Ulash va yuklab olish»** (yopiq repoda — kalitni qo‘shgach **«Deploy»**).

Deploy logida har bir qadam ko‘rinadi; oxirida sayt xizmati qayta ishga tushadi. Batafsil — [Git orqali deploy](git-deploy.md).

## 4. Muhit o‘zgaruvchilari

Maxfiy qiymatlarni (baza manzili, API kalitlar) repozitoriyga yozmang. **Sozlamalar → Backend → Muhit o‘zgaruvchilari**:

```text
NODE_ENV=production
DATABASE_URL=mysql://app_user:parol@localhost:3306/app_db
JWT_SECRET=...
```

Saqlanganda ilova qayta ishga tushadi. Baza kerak bo‘lsa — [Ma’lumotlar bazalari](databases.md).

## 5. Har push’da avtomatik deploy

1. Git sahifasidagi **webhook manzilini** nusxalang.
2. GitHub: **Settings → Webhooks → Add webhook** — Payload URL: webhook manzili, Content type: `application/json`, **Just the push event**.
3. Panel sertifikati o‘zi imzolangan bo‘lsa, **SSL verification** ni o‘chiring yoki panelga ishonchli sertifikat oling ([Panel manzili va SSL](panel-access.md)).

Endi `git push origin main` dan bir necha soniya o‘tib sayt yangilanadi; deploy kim tomonidan ishga tushgani (**webhook orqali**) logda ko‘rinadi.

CI’dan (GitHub Actions va boshqalar) deploy’ni [API](api-reference.md) orqali ham boshlash mumkin: `POST /api/v2/git` va `{"domain":"api.example.uz","action":"deploy"}` (Premium tarif).

## 6. SSL va tekshirish

1. **SSL sertifikatlar → Let’s Encrypt** ([SSL sertifikatlar](ssl.md)).
2. `https://api.example.uz` ni oching.

## Muammo bo‘lsa

| Belgi | Nima qilish |
|---|---|
| Sayt **502** qaytaradi | Ilova ishga tushmagan: **Loglar → Ilova logi**. Ko‘pincha `PORT` o‘rniga qattiq yozilgan port yoki `app.js` yo‘q |
| Deploy «buyruq xato bilan tugadi» | Deploy logining oxiri — odatda `npm` xatosi yoki yetishmayotgan paket |
| Deploy 20 daqiqada to‘xtadi | Buyruqda `npm start` kabi to‘xtamaydigan buyruq bor — uni olib tashlang |
| O‘zgarish ko‘rinmayapti | Webhook GitHub’da yashil belgi bilanmi (**Recent Deliveries**) va branch to‘g‘rimi |

Batafsil — [Python va Node.js saytlar](python-nodejs.md).
