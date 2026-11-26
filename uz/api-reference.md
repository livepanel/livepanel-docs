# API v2 ma’lumotnomasi

> **API faqat Premium obunasi bor panellarda ishlaydi.** Free va Pro tariflarda har bir so‘rov `402 upgrade_required` qaytaradi. Tarifni ko‘tarish — [Litsenziya va tariflar](license.md).

API v2 panelning **veb-interfeysidagi barcha imkoniyatlarni** dasturlarga ochadi: saytlar, fayllar, bazalar, DNS, pochta, FTP, cron, zaxira, Git, akkauntlar, limitlar, brending va server sozlamalari. Billing tizimi, Telegram bot, CI/CD yoki o‘z skriptingiz panelda inson qiladigan hamma ishni bajara oladi.

Har bir API so‘rovi panel sahifalari ishlatadigan xuddi o‘sha kod orqali o‘tadi: token o‘z akkaunti panelda qila olmaydigan ishni hech qachon qila olmaydi, token ruxsatlari esa uni yana toraytiradi.

## Boshlash

1. Panelda **Tizim → API tokenlar** bo‘limida token yarating, kerakli bo‘limlar uchun **O‘qish** va/yoki **Yozish** ruxsatini belgilang ([API tokenlar va amallar tarixi](api-tokens.md)).
2. Tokenni darhol saqlang — u faqat bir marta ko‘rsatiladi (`lp_` bilan boshlanadi).
3. Har bir so‘rovda yuboring:

```text
Authorization: Bearer lp_XXXXXXXXXXXXXXXX
```

| | |
|---|---|
| Manzil | `https://SERVER:6563/api/v2/…` yoki panel domeni `https://panel.example.uz/api/v2/…` |
| Format | So‘rov va javob — JSON. `POST`, `PUT`, `PATCH` da `Content-Type: application/json` |
| Noma’lum maydonlar | Rad etiladi (`400 invalid_input`) — faqat hujjatdagi maydonlarni yuboring |
| JSON hajmi | 16 KB gacha (fayl yuklash — alohida, 2 GB gacha) |
| Sertifikat | Panel o‘zi imzolagan sertifikatda ishlasa, unga ishonchli sertifikat oling — [Panel manzili va SSL](panel-access.md) |

Tekshirish — token kimga tegishli va nimalarga ruxsati bor:

```bash
curl -s https://panel.example.uz/api/v2/me -H "Authorization: Bearer $LP_TOKEN"
```

```json
{
  "account": { "id": 1, "name": "liveadmin", "role": "admin", "main_admin": true,
               "permissions": { "sites": true, "files": true, "services": true } },
  "scopes": ["sites:read", "sites:write", "databases:write"],
  "expires_at": 1795593600,
  "version": "2026.11.25.0545"
}
```

## Sun’iy intellekt (AI) bilan ishlash

API hujjati AI yordamchilar (ChatGPT, Claude, Gemini, Copilot va boshqalar) ham tushunadigan qilib berilgan. AI’ga quyidagilardan birini bering — u to‘g‘ri endpoint, maydon va ruxsatlarni o‘zi topib, PHP, Node.js, Python yoki Bash’da kod yozadi:

| Nima | Manzil |
|---|---|
| OpenAPI 3.1 spetsifikatsiyasi (eng aniq) | `https://wiki.livepanel.uz/openapi.json` |
| Shu sahifa Markdown’da | `https://wiki.livepanel.uz/uz/api-reference.md` |
| Butun qo‘llanma bitta faylda | `https://wiki.livepanel.uz/llms-full.txt?lang=uz` |
| AI uchun indeks ([llms.txt](https://llmstxt.org)) | `https://wiki.livepanel.uz/llms.txt` |

Har bir wiki sahifasidagi **«AI uchun nusxalash»** tugmasi sahifani Markdown ko‘rinishida nusxalaydi — AI chatiga joylashtirish kifoya.

Namunaviy so‘rov:

```text
https://wiki.livepanel.uz/openapi.json dagi LivePanel API v2 asosida PHP skript yoz:
yangi akkaunt yaratsin, unga 2 ta sayt va 3 ta baza limitini qo‘ysin,
shop.example.uz saytini PHP 8.3 da yaratib, Let’s Encrypt SSL olsin.
Token LP_TOKEN muhit o‘zgaruvchisida, panel manzili https://panel.example.uz:6563.
Har bir xatoni {"error": "..."} kodidan tushunarli xabar qilib chiqarsin.
```

Kod yozuvchi AI uchun asosiy qoidalar:

- Asosiy manzil `https://<panel>:6563/api/v2`, sarlavha `Authorization: Bearer lp_…`.
- So‘rov tanasi JSON; noma’lum maydon yuborilsa — `400 invalid_input`.
- Javobda xato bo‘lsa — `{"error": "kod"}`; `402 upgrade_required` — panel Premium emas.
- Sozlamani o‘zgartirishdan oldin uni `GET` bilan o‘qing va o‘zgartirilgan obyektni qaytaring (`/sites/settings`, `/dns` `save`).
- Firewall `apply` dan keyin bir daqiqada `confirm` yuboring.
- Fayl yo‘llari sayt foydalanuvchisining uy papkasiga nisbatan: `www/<domen>/…`.

## Mijoz kodi (PHP, Node.js, Bash)

Quyidagi misollarning hammasi shu kichik yordamchilardan foydalanadi. Tokenni kodga yozmang — muhit o‘zgaruvchisida (`LP_TOKEN`) saqlang.

**Bash** (curl va jq):

```bash
#!/usr/bin/env bash
set -euo pipefail
PANEL="https://panel.example.uz/api/v2"
: "${LP_TOKEN:?LP_TOKEN o‘rnatilmagan}"

# lp METHOD PATH [JSON]
lp() {
  local method=$1 path=$2 body=${3:-}
  if [ -n "$body" ]; then
    curl -sS --fail-with-body -X "$method" "$PANEL$path" \
      -H "Authorization: Bearer $LP_TOKEN" -H "Content-Type: application/json" -d "$body"
  else
    curl -sS --fail-with-body -X "$method" "$PANEL$path" -H "Authorization: Bearer $LP_TOKEN"
  fi
}

lp GET /sites | jq -r '.[].domain'
```

**PHP** (7.4+, curl kengaytmasi):

```php
<?php
const PANEL = 'https://panel.example.uz/api/v2';

function lp(string $method, string $path, ?array $body = null)
{
    $ch = curl_init(PANEL . $path);
    $headers = ['Authorization: Bearer ' . getenv('LP_TOKEN'), 'Accept: application/json'];
    if ($body !== null) {
        $headers[] = 'Content-Type: application/json';
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($body));
    }
    curl_setopt_array($ch, [
        CURLOPT_CUSTOMREQUEST  => $method,
        CURLOPT_HTTPHEADER     => $headers,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT        => 300,
    ]);
    $raw  = curl_exec($ch);
    $code = curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
    curl_close($ch);
    $data = json_decode((string) $raw, true);
    if ($code >= 400) {
        throw new RuntimeException($data['error'] ?? "http_$code", $code);
    }
    return $data;
}

foreach (lp('GET', '/sites') as $site) {
    echo $site['domain'], PHP_EOL;
}
```

**Node.js** (18+, o‘rnatilgan `fetch`):

```js
const PANEL = "https://panel.example.uz/api/v2";

async function lp(method, path, body) {
  const res = await fetch(PANEL + path, {
    method,
    headers: {
      Authorization: `Bearer ${process.env.LP_TOKEN}`,
      ...(body ? { "Content-Type": "application/json" } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  const data = await res.json().catch(() => null);
  if (!res.ok) throw new Error(data?.error ?? `http_${res.status}`);
  return data;
}

const sites = await lp("GET", "/sites");
console.log(sites.map((s) => s.domain));
```

## Ruxsatlar (scopes)

Har bir bo‘limning `:read` (faqat `GET`) va `:write` (o‘zgartirish) ruxsati bor:

| Bo‘lim | Nimani boshqaradi | Kim bera oladi |
|---|---|---|
| `sites` | Saytlar, sozlamalar, SSL, ilova o‘rnatish, sayt xizmati va loglari, skanerlash, trafik | Saytlar ruxsati bor akkaunt |
| `files` | Fayl menejeri: ro‘yxat, o‘qish, saqlash, yuklash, amallar | Fayllar ruxsati bor akkaunt |
| `databases` | MySQL/PostgreSQL bazalari, foydalanuvchilar, import/eksport | Saytlar ruxsati bor akkaunt |
| `dns` | DNS zonalar va yozuvlar | Saytlar ruxsati bor akkaunt |
| `mail` | Pochta domenlari va qutilar | Saytlar ruxsati bor akkaunt |
| `ftp` | FTP akkauntlar | Saytlar ruxsati bor akkaunt |
| `cron` | Rejalashtirilgan vazifalar | Saytlar ruxsati bor akkaunt |
| `backups` | Zaxira nusxalar, tiklash, Google Drive/Dropbox | Saytlar ruxsati bor akkaunt |
| `git` | Git deploy | Saytlar ruxsati bor akkaunt |
| `users` | Panel akkauntlari, 2FA’ni o‘chirish, amallar tarixi | Administrator, reseller |
| `limits` | Akkaunt limitlari (`limits:read` — hamma, `limits:write` — administrator, reseller) | — |
| `branding` | Panel nomi, logotipi, rangi | Administrator, reseller |
| `system` | Xizmatlar, ilovalar, firewall, login himoyasi, kvotalar, panel SSL va manzillari, litsenziya | Faqat asosiy administrator |

API orqali **qilib bo‘lmaydigan** ishlar (xavfsizlik uchun): panelga kirish/chiqish, o‘z parolini, 2FA va tiklash emailini o‘zgartirish, API tokenlarini yaratish yoki bekor qilish, veb-terminal.

## Xatolar

Xato javobi doim bir xil: `{"error": "kod"}`.

| HTTP | Kod | Ma’nosi |
|---|---|---|
| 400 | `invalid_input` | JSON noto‘g‘ri, maydon yetishmaydi yoki ortiqcha |
| 401 | `unauthorized` | Token yo‘q, noto‘g‘ri, muddati o‘tgan, bekor qilingan yoki akkaunt o‘chirilgan |
| 402 | `license_required` | Panel litsenziyasi faol emas |
| 402 | `upgrade_required` | Tarif Premium emas |
| 403 | `scope_denied` | Tokenda bu amal uchun ruxsat yo‘q |
| 403 | `forbidden` | Akkaunt bu ob’ektni boshqara olmaydi (boshqa akkauntning sayti va h.k.) |
| 404 | `site_not_found`, `database_not_found`, … | Ob’ekt topilmadi |
| 409 | `domain_limit_reached`, `database_limit_reached`, … | Limit yoki holat ziddiyati |
| 429 | `too_many_attempts` | Juda ko‘p so‘rov — biroz kuting |
| 503 | `hosting_unavailable` | Server agenti vaqtincha javob bermayapti — qayta urining |

Xato kodlari panel interfeysidagi xabarlar bilan bir xil; ularni dasturda tekshirish qulay.

## Endpointlar

Quyida barcha marshrutlar `https://…/api/v2` ga nisbatan yozilgan. `domain` — sayt domeni, `path` — sayt foydalanuvchisining uy papkasiga nisbatan yo‘l (`www/example.uz/index.php`).

### Hisob

| Metod | Yo‘l | Ruxsat | Vazifasi |
|---|---|---|---|
| GET | `/me` | istalgan | Token egasi, ruxsatlari, muddati va panel versiyasi |

### Saytlar — `sites`

| Metod | Yo‘l | Ruxsat | Vazifasi |
|---|---|---|---|
| GET | `/sites` | read | Saytlar ro‘yxati |
| POST | `/sites` | write | Sayt yaratish |
| POST | `/sites/lifecycle` | write | `{"domain","action"}` — `enable`, `disable`, `delete` |
| GET | `/sites/settings?domain=` | read | Sayt va uning sozlamalari |
| POST | `/sites/settings` | write | Sozlamalarni saqlash, backend turini almashtirish |
| POST | `/sites/ssl` | write | SSL: `issue`, `remove` va HTTPS yo‘naltirishi |
| GET | `/sites/scan?domain=` | read | Oxirgi antivirus skanerlash natijasi |
| POST | `/sites/scan` | write | `{"domain"}` — skanerlashni boshlash |
| POST | `/sites/scan/action` | write | `{"domain","action","path"\|"id"}` — `quarantine`, `delete`, `restore`, `purge` |
| GET | `/site-service?domain=&log=` | read | Sayt xizmati holati va loglari (`log`: `access`, `error`, Node.js/Python’da `backend`) |
| POST | `/site-service` | write | `{"domain","action":"restart"}` |
| GET | `/traffic?domain=&month=YYYY-MM` | read | Oylik trafik va kunlik grafik (`domain` siz — akkauntlar bo‘yicha) |
| GET | `/sites/stats-report?domain=` | read | GoAccess tashriflar hisoboti (HTML) |
| GET | `/apps/install?domain=` | read | Ilova o‘rnatish holati |
| POST | `/apps/install` | write | CMS/framework o‘rnatish |
| GET | `/get-site-photo/{domain}` | read | Sayt ko‘rinishi (rasm) |
| GET | `/owners` | read | Saytlar egalari (Linux foydalanuvchilari) |
| GET | `/php`, `/node`, `/python` | read | O‘rnatilgan versiyalar |

**Sayt yaratish** — `POST /sites`:

| Maydon | Izoh |
|---|---|
| `domain` | Majburiy, masalan `shop.example.uz` |
| `runtime` | Majburiy: `php`, `node`, `python`, `static`, `proxy` |
| `php`, `handler` | PHP versiyasi (`8.3`) va ishlovchi: `fpm`, `fastcgi`, `apache`, `cgi` |
| `node` | Node.js asosiy versiyasi (`22`), bo‘sh — tizimdagi |
| `python` | Python versiyasi (`3.12`) — serverda o‘rnatilgan bo‘lishi kerak |
| `proxy` | `runtime: proxy` uchun manzil (`http://127.0.0.1:3000`) |
| `account_id` | Sayt qaysi akkauntga tegishli (standart — token egasi) |
| `owner`, `new_owner`, `owner_name` | Linux foydalanuvchisi: mavjudi (`owner`), yoki yangi (`new_owner: true`, `owner_name`) |

Javobdagi `state`: `provisioning`, `active`, `disabled`, `failed` (sababi `error` maydonida). Mavjud saytning subdomeni avtomatik o‘sha saytning foydalanuvchisiga qo‘shiladi.

**Sozlamalarni o‘zgartirish** — avval `GET /sites/settings?domain=…`, kerakli maydonlarni o‘zgartirib `POST /sites/settings` ga yuboring:

```json
{
  "domain": "shop.example.uz",
  "settings": { "...GET javobidagi settings obyekti, o‘zgartirilgan holda...": "" },
  "auth_password": "",
  "runtime": "", "handler": "fpm", "php": "8.4", "node": "", "python": "", "proxy": "",
  "force_https": true
}
```

`settings` ichida: `aliases`, `gzip`, `gzip_level`, `nginx_static`, `static_ext`, `cache_days`, `hsts`, `http2`, `redirects`, `access_log`, `error_log`, `auth_on`, `auth_user`, `rate_on`, `rate`, `rate_unit`, `burst_on`, `burst`, `no_delay`, `env`, `access_mode`, `access_list`, `php_ini`. `runtime` ni bo‘sh qoldirsangiz, backend turi o‘zgarmaydi; boshqa qiymat — turini almashtiradi ([Sayt sozlamalari](site-settings.md)).

**SSL** — `POST /sites/ssl`:

```json
{ "domain": "shop.example.uz", "action": "issue", "type": "letsencrypt", "email": "admin@example.uz", "force_https": true }
```

`type`: `letsencrypt` yoki `selfsigned`.

**Ilova o‘rnatish** — `POST /apps/install`:

```json
{ "domain": "blog.example.uz", "app": "wordpress", "title": "Blog",
  "admin_user": "admin", "admin_password": "Uzun-va-murakkab-parol-2026", "admin_email": "admin@example.uz" }
```

`app`: `wordpress`, `joomla`, `drupal`, `laravel`, `symfony`, `codeigniter`, `strapi`, `ghost`, `express`, `nextjs`, `nestjs`, `wagtail`, `django`, `flask`, `fastapi`. Sayt bo‘sh va mos turda bo‘lishi kerak. O‘rnatish fonda ketadi — holatini `GET /apps/install?domain=` bilan kuzating.

### Fayllar — `files`

| Metod | Yo‘l | Ruxsat | Vazifasi |
|---|---|---|---|
| GET | `/files?domain=&path=` | read | Papka ro‘yxati; fayl matni uchun `&action=read` (javobdagi `hash` — saqlashda `expected` sifatida) |
| POST | `/files` | write | `{"domain","path","action","content","expected"}` — `save`, `mkdir`, `create` |
| POST | `/files/op` | write | Amallar: `rename`, `move`, `copy`, `chmod`, `archive`, `extract`, `delete` |
| POST | `/files/upload?domain=&path=` | write | Fayl yuklash: so‘rov tanasi — faylning o‘zi, `path` — saqlanadigan to‘liq yo‘l. Mavjud faylni almashtirish uchun `&overwrite=1` (aks holda `409 file_exists`) |
| GET | `/files/download?domain=&path=` | read | Faylni yuklab olish |
| GET | `/files/stats?domain=&path=` | read | Disk statistikasi: eng katta papka va fayllar |

`/files/op` misollari. `rename` da `target` — faqat yangi nom; `archive` da — arxiv nomi (o‘sha papkada yaratiladi); `copy`, `move`, `extract` da — papka yo‘li. Mavjud nom yoki papka `409 file_exists` qaytaradi.

```json
{ "domain": "shop.example.uz", "action": "rename", "path": "www/shop.example.uz/old.php", "target": "new.php" }
{ "domain": "shop.example.uz", "action": "copy", "path": "www/shop.example.uz/new.php", "target": "www/shop.example.uz/backup" }
{ "domain": "shop.example.uz", "action": "chmod", "paths": ["www/shop.example.uz/storage"], "mode": "755", "recursive": true }
{ "domain": "shop.example.uz", "action": "archive", "path": "www/shop.example.uz/public", "target": "public.zip" }
{ "domain": "shop.example.uz", "action": "extract", "path": "www/shop.example.uz/site.zip", "target": "www/shop.example.uz" }
{ "domain": "shop.example.uz", "action": "delete", "paths": ["www/shop.example.uz/tmp"] }
```

Fayl yuklash (Bash):

```bash
curl -sS --fail-with-body -X POST \
  "$PANEL/files/upload?domain=shop.example.uz&path=www/shop.example.uz/site.zip&overwrite=1" \
  -H "Authorization: Bearer $LP_TOKEN" --data-binary @site.zip
```

### Ma’lumotlar bazalari — `databases`

| Metod | Yo‘l | Ruxsat | Vazifasi |
|---|---|---|---|
| GET | `/databases` | read | Bazalar ro‘yxati |
| POST | `/databases` | write | Amallar (pastda) |
| GET | `/databases/engines` | read | MySQL/PostgreSQL mavjudligi |
| POST | `/databases/import` | write | `{"name","path"}` — sayt papkasidagi `.sql`/`.sql.gz` ni import qilish |
| GET | `/databases/import?name=` | read | Import holati |
| GET | `/databases/export?name=` | read | Bazani `.sql.gz` qilib yuklab olish |
| POST | `/databases/phpmyadmin`, `/databases/adminer` | write | `{"name"}` — parolsiz kirish havolasi |

`POST /databases` amallari:

| `action` | Maydonlar |
|---|---|
| `create` | `name`, `user`, `password`, `site`, `charset` (`utf8mb4`), `engine` (`mysql` yoki `postgresql`) |
| `password` | `name`, `password` |
| `delete` | `name` |
| `user_add` | `name`, `user`, `password`, `privileges` (`all`, `readwrite`, `readonly`) |
| `user_update` | `name`, `user`, `privileges` |
| `user_remove` | `name`, `user` |
| `hosts` | `name`, `user`, `hosts` (IP/tarmoqlar ro‘yxati — tashqi ulanish), `password` |

Bo‘sh maydonlarni ham yuboring: `{"action":"delete","name":"shop_db","user":"","password":"","site":"","charset":""}` ko‘rinishi ham qabul qilinadi.

### DNS — `dns`

| Metod | Yo‘l | Ruxsat | Vazifasi |
|---|---|---|---|
| GET | `/dns` | read | Zonalar, server IP, BIND holati |
| GET | `/dns/zone?zone=` | read | Zona yozuvlari |
| POST | `/dns` | write | `create` (`zone`), `save` (`zone`, `records`), `delete` (`zone`) |

`records` — to‘liq ro‘yxat (`GET /dns/zone` javobidagi `zone.records`, NS yozuvlari bilan birga): `{"name":"www","type":"A","ttl":3600,"value":"203.0.113.10","priority":0}`. `save` zonaning barcha yozuvlarini almashtiradi — avval `GET /dns/zone` bilan oling.

### Pochta — `mail`

| Metod | Yo‘l | Ruxsat | Vazifasi |
|---|---|---|---|
| GET | `/mail` | read | Domenlar, qutilar, ulanish ma’lumotlari, DNS yozuvlari |
| POST | `/mail` | write | Amallar (pastda) |

| `action` | Maydonlar |
|---|---|
| `domain_add` | `domain`, `site` |
| `domain_update` | `domain`, `catch_all`, `disabled` |
| `domain_remove` | `domain` |
| `box_add` | `address` (`info@example.uz`), `password`, `quota_mb`, `aliases`, `forwards` |
| `box_update` | `address`, ixtiyoriy `password`, `quota_mb`, `aliases`, `forwards`, `disabled` |
| `box_remove` | `address` |

### FTP — `ftp`

| Metod | Yo‘l | Ruxsat | Vazifasi |
|---|---|---|---|
| GET | `/accounts` | read | FTP akkauntlar |
| POST | `/accounts` | write | `create`, `update`, `toggle`, `delete` |

Maydonlar: `action`, `name`, `site`, `password`, `home`, `read_only`, `enabled`.

### Rejalashtiruvchi — `cron`

| Metod | Yo‘l | Ruxsat | Vazifasi |
|---|---|---|---|
| GET | `/cron` | read | Vazifalar va keyingi ishga tushish vaqti |
| POST | `/cron` | write | `create`, `update`, `toggle`, `run`, `delete` |

Maydonlar: `action`, `id`, `site`, `schedule` (`*/5 * * * *`), `command`, `comment`, `enabled`. `run` — darhol bajaradi va natijani qaytaradi.

### Zaxira — `backups`

| Metod | Yo‘l | Ruxsat | Vazifasi |
|---|---|---|---|
| GET | `/backups?domain=` | read | `copies` — nusxalar, `job` — joriy jarayon (`state`: `running`, `done`, `failed`), `plan` — jadval |
| POST | `/backups` | write | `create`, `restore`, `delete`, `plan` |
| GET | `/backups/download?domain=&id=` | read | Nusxani `.tar` qilib yuklab olish |
| GET | `/backups/remote?domain=` | read | Saytning Google Drive/Dropbox holati va ombordagi nusxalar |
| POST | `/backups/remote` | write | `enable`, `disable`, `keep`, `sync`, `fetch`, `delete` |
| GET | `/remote` | read | Ulangan omborlar va ulardagi joy |
| POST | `/remote` | write | `connect` — kirish havolasini oladi: `{"provider","action":"connect","origin":"https://<panel manzili>"}`, javobdagi `redirect` ni brauzerda oching (`origin` — so‘rov yuborilgan panel manzilining o‘zi, boshqasi `400 invalid_origin`; `origin` siz — kod bilan ulanish, `pending.user_code`); `cancel`, `disconnect` |

`POST /backups` misollari:

```json
{ "domain": "shop.example.uz", "action": "create" }
{ "domain": "shop.example.uz", "action": "restore", "id": "<GET /backups javobidagi id>", "files": true, "databases": true }
{ "domain": "shop.example.uz", "action": "plan", "plan": { "schedule": "daily", "hour": 3, "weekday": 0, "keep": 7, "files": true, "databases": true } }
```

`schedule`: `off`, `daily`, `weekly`; `weekday` 0–6 (0 — yakshanba). `POST /backups/remote`: `{"domain","provider":"gdrive"|"dropbox","action","keep","file"}`.

### Git — `git`

| Metod | Yo‘l | Ruxsat | Vazifasi |
|---|---|---|---|
| GET | `/git?domain=` | read | Repozitoriy, deploy kaliti, webhook manzili, oxirgi deploy logi |
| POST | `/git` | write | `save` (`repo`, `branch`, `command`), `deploy`, `token` (yangi webhook), `disconnect`. `save` faqat sozlaydi — fayllarni olish uchun keyin `deploy` yuboring; natija `GET /git` dagi `last.state` (`running`, `done`, `failed`) |

CI’dan deploy:

```bash
lp POST /git '{"domain":"api.example.uz","action":"deploy"}'
```

### Akkauntlar — `users`

| Metod | Yo‘l | Ruxsat | Vazifasi |
|---|---|---|---|
| GET | `/users` | read | Akkauntlar ro‘yxati |
| POST | `/users` | write | Akkaunt yaratish (`201`) |
| PATCH | `/users/{id}` | write | O‘zgartirish: rol, ruxsatlar, SSH, parol, `disabled` (bloklash) |
| DELETE | `/users/{id}` | write | O‘chirish (saytlari bo‘lsa — `409 account_has_sites`) |
| POST | `/users/2fa-reset` | write | `{"id"}` — akkaunt 2FA’sini o‘chirish |
| GET | `/audit` | read | Amallar tarixi (oxirgi 50 ta) |

Akkaunt maydonlari: `name` (3–64 belgi, keyin o‘zgarmaydi), `role` (`user`, `reseller`, `admin`), `password` (6–72; `PATCH` da bo‘sh — o‘zgarmaydi), `creator_id`, `permissions` (`{"sites","files","services"}`), `ssh`, `disabled`. `PATCH` da `name` va `role` ni ham yuboring.

### Limitlar — `limits` (Pro va Premium)

| Metod | Yo‘l | Ruxsat | Vazifasi |
|---|---|---|---|
| GET | `/limits?account_id=` | read | Limitlar |
| PUT | `/limits` | write | Limitlarni saqlash |
| GET | `/limits/usage?account_id=` | read | Hozir ishlatilayotgani (disk, RAM, saytlar, bazalar) |

`PUT /limits`: `account_id`, `memory_mib` (0 yoki ≥32), `disk_mib` (0 yoki ≥64, kvotalar yoqilgan bo‘lsin), `domains`, `databases`, `users` (faqat reseller), `cpu_percent` (hozircha `0`). `0` — cheklanmagan.

### Brending — `branding`

| Metod | Yo‘l | Ruxsat | Vazifasi |
|---|---|---|---|
| GET | `/settings/branding` | read | Nom, rang, logotip |
| POST | `/settings/branding` | write | `name`, `color` (`#2563eb`), `logo` (data URL), `remove_logo`, `reset` |

### Server — `system` (faqat asosiy administrator)

| Metod | Yo‘l | Vazifasi |
|---|---|---|
| GET | `/license` | Litsenziya holati va tarif |
| POST | `/license/activate` | Litsenziyani faollashtirish |
| GET | `/metrics`, `/stats?range=` | Server yuklamasi (`range`: `live`, `1h`, `24h`, `7d`, `30d`) |
| GET / POST | `/system/services` | Xizmatlar; `{"unit","action"}` — `start`, `stop`, `restart`, `enable`, `disable` |
| GET / POST | `/applications` | Ilovalar; `{"name","action"}` — `install`, `remove` |
| GET / POST | `/firewall` | Qoidalar; `apply` (`enabled`, `rules`), keyin `confirm` (`token`) |
| GET | `/security` | Login himoyasi, bloklangan IP’lar, fail2ban |
| POST | `/security/settings`, `/security/unblock` | Sozlamalar; `{"ip","jail"}` — blokdan chiqarish |
| GET / POST | `/quota` | Disk kvotalari; `{"action":"enable"}` |
| GET / POST | `/panel-tls` | Panel IP sertifikati: `issue` (olish yoki yangilash; Panel SSL xizmati to‘lanmagan bo‘lsa — `400 service_not_paid`), `self` (o‘z sertifikatiga qaytish; allaqachon o‘zida bo‘lsa ham xatosiz) |
| GET / POST | `/panel-addresses` | Panel domenlari: `add` (`domain`, `cert`, `email`, `cert_pem`, `key_pem`), `cert`, `remove` |

> Firewall’ni API orqali qo‘llaganda `apply` javobidagi `token` bilan bir daqiqa ichida `confirm` yuboring — aks holda panel avvalgi qoidalarni tiklaydi (o‘zingizni bloklab qo‘ymaslik uchun).

## To‘liq misol: to‘lovdan keyin mijozga hosting ochish

Token ruxsatlari: `users:write`, `limits:write`, `sites:write`, `databases:write`.

**Bash:**

```bash
ID=$(lp POST /users '{"name":"client1","role":"user","password":"Mijoz-paroli-2026","permissions":{"sites":true,"files":true,"services":true}}' | jq -r .id)
lp PUT /limits "{\"account_id\":$ID,\"memory_mib\":1024,\"disk_mib\":10240,\"domains\":3,\"databases\":5}"
lp POST /sites "{\"domain\":\"client1.example.uz\",\"runtime\":\"php\",\"php\":\"8.3\",\"handler\":\"fpm\",\"account_id\":$ID}"
lp POST /sites/ssl '{"domain":"client1.example.uz","action":"issue","type":"letsencrypt","email":"","force_https":true}'
lp POST /databases '{"action":"create","name":"client1_db","user":"client1_user","password":"Baza-paroli-2026","site":"client1.example.uz","charset":"utf8mb4","engine":"mysql"}'
```

**PHP:**

```php
$acc = lp('POST', '/users', [
    'name' => 'client1', 'role' => 'user', 'password' => 'Mijoz-paroli-2026',
    'permissions' => ['sites' => true, 'files' => true, 'services' => true],
]);
lp('PUT', '/limits', ['account_id' => $acc['id'], 'memory_mib' => 1024, 'disk_mib' => 10240, 'domains' => 3, 'databases' => 5]);
lp('POST', '/sites', ['domain' => 'client1.example.uz', 'runtime' => 'php', 'php' => '8.3', 'handler' => 'fpm', 'account_id' => $acc['id']]);
lp('POST', '/sites/ssl', ['domain' => 'client1.example.uz', 'action' => 'issue', 'type' => 'letsencrypt', 'email' => '', 'force_https' => true]);
lp('POST', '/databases', ['action' => 'create', 'name' => 'client1_db', 'user' => 'client1_user', 'password' => 'Baza-paroli-2026',
    'site' => 'client1.example.uz', 'charset' => 'utf8mb4', 'engine' => 'mysql']);
```

**Node.js:**

```js
const acc = await lp("POST", "/users", {
  name: "client1", role: "user", password: "Mijoz-paroli-2026",
  permissions: { sites: true, files: true, services: true },
});
await lp("PUT", "/limits", { account_id: acc.id, memory_mib: 1024, disk_mib: 10240, domains: 3, databases: 5 });
await lp("POST", "/sites", { domain: "client1.example.uz", runtime: "php", php: "8.3", handler: "fpm", account_id: acc.id });
await lp("POST", "/sites/ssl", { domain: "client1.example.uz", action: "issue", type: "letsencrypt", email: "", force_https: true });
await lp("POST", "/databases", {
  action: "create", name: "client1_db", user: "client1_user", password: "Baza-paroli-2026",
  site: "client1.example.uz", charset: "utf8mb4", engine: "mysql",
});
```

Muddati tugaganda bloklash va to‘lovdan keyin ochish:

```bash
lp PATCH /users/$ID '{"name":"client1","role":"user","disabled":true}'    # bloklash
lp PATCH /users/$ID '{"name":"client1","role":"user","disabled":false}'   # qayta ochish
```

## API v1

`/api/v1` endi faqat tizim uchun: `GET /api/v1/check/is-live-panel` (token talab qilmaydi; server LivePanel ekanini va versiyasini qaytaradi) va litsenziya xizmati ishlatadigan `POST /api/v1/activate-license`. Avvalgi `/api/v1/users`, `/api/v1/sites`, `/api/v1/limits` olib tashlangan — ularning o‘rniga `/api/v2` dagi xuddi shu yo‘llarni ishlating; tokenlar o‘zgarmaydi.
