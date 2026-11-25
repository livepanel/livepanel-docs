# Справочник API v2

> **API работает только на панелях с подпиской Premium.** На тарифах Free и Pro каждый запрос возвращает `402 upgrade_required`. Повысить тариф — [Лицензия и тарифы](license.md).

API v2 открывает программам **всё, что умеет веб-интерфейс панели**: сайты, файлы, базы данных, DNS, почту, FTP, cron, резервные копии, Git, аккаунты, лимиты, брендинг и настройки сервера. Биллинг, Telegram-бот, CI/CD или ваш скрипт могут делать в панели всё, что делает человек.

Каждый запрос API проходит через тот же код, что и страницы панели: токен никогда не сделает того, чего его аккаунт не может сделать в панели, а права токена сужают его ещё сильнее.

## Начало работы

1. В панели откройте **Система → API-токены**, создайте токен и отметьте **Чтение** и/или **Запись** для нужных разделов ([API-токены и журнал действий](api-tokens.md)).
2. Сразу сохраните токен — он показывается только один раз (начинается с `lp_`).
3. Передавайте его в каждом запросе:

```text
Authorization: Bearer lp_XXXXXXXXXXXXXXXX
```

| | |
|---|---|
| Адрес | `https://SERVER:6563/api/v2/…` или домен панели `https://panel.example.uz/api/v2/…` |
| Формат | Запросы и ответы — JSON. Для `POST`, `PUT`, `PATCH` нужен `Content-Type: application/json` |
| Неизвестные поля | Отклоняются (`400 invalid_input`) — отправляйте только описанные поля |
| Размер JSON | До 16 КБ (загрузка файлов — отдельно, до 2 ГБ) |
| Сертификат | Если панель работает с самоподписанным сертификатом, выдайте ей доверенный — [Адрес панели и SSL](panel-access.md) |

Проверка — кому принадлежит токен и что ему разрешено:

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

## Клиентский код (PHP, Node.js, Bash)

Все примеры ниже используют эти небольшие помощники. Не пишите токен в коде — храните его в переменной окружения (`LP_TOKEN`).

**Bash** (curl и jq):

```bash
#!/usr/bin/env bash
set -euo pipefail
PANEL="https://panel.example.uz/api/v2"
: "${LP_TOKEN:?LP_TOKEN не задан}"

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

**PHP** (7.4+, расширение curl):

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

**Node.js** (18+, встроенный `fetch`):

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

## Права (scopes)

У каждого раздела есть право `:read` (только `GET`) и `:write` (изменения):

| Раздел | Что управляет | Кто может выдать |
|---|---|---|
| `sites` | Сайты, настройки, SSL, установка приложений, служба и логи сайта, сканирование, трафик | Аккаунт с правом «Сайты» |
| `files` | Файловый менеджер: список, чтение, сохранение, загрузка, действия | Аккаунт с правом «Файлы» |
| `databases` | Базы MySQL/PostgreSQL, пользователи, импорт/экспорт | Аккаунт с правом «Сайты» |
| `dns` | DNS-зоны и записи | Аккаунт с правом «Сайты» |
| `mail` | Почтовые домены и ящики | Аккаунт с правом «Сайты» |
| `ftp` | FTP-аккаунты | Аккаунт с правом «Сайты» |
| `cron` | Задания по расписанию | Аккаунт с правом «Сайты» |
| `backups` | Резервные копии, восстановление, Google Drive/Dropbox | Аккаунт с правом «Сайты» |
| `git` | Деплой из Git | Аккаунт с правом «Сайты» |
| `users` | Аккаунты панели, отключение 2FA, журнал действий | Администратор, реселлер |
| `limits` | Лимиты аккаунтов (`limits:read` — все, `limits:write` — администратор, реселлер) | — |
| `branding` | Название, логотип, цвет панели | Администратор, реселлер |
| `system` | Службы, приложения, файрвол, защита входа, квоты, SSL и адреса панели, лицензия | Только главный администратор |

Через API **нельзя** (ради безопасности): входить и выходить, менять свой пароль, 2FA и email для восстановления, создавать и отзывать API-токены, пользоваться веб-терминалом.

## Ошибки

Ответ с ошибкой всегда одинаковый: `{"error": "код"}`.

| HTTP | Код | Значение |
|---|---|---|
| 400 | `invalid_input` | Неверный JSON, не хватает поля или есть лишнее |
| 401 | `unauthorized` | Нет токена, он неверный, просрочен, отозван или аккаунт отключён |
| 402 | `license_required` | Лицензия панели не активна |
| 402 | `upgrade_required` | Тариф не Premium |
| 403 | `scope_denied` | У токена нет права на это действие |
| 403 | `forbidden` | Аккаунт не может управлять этим объектом (чужой сайт и т. п.) |
| 404 | `site_not_found`, `database_not_found`, … | Объект не найден |
| 409 | `domain_limit_reached`, `database_limit_reached`, … | Лимит или конфликт состояния |
| 429 | `too_many_attempts` | Слишком много запросов — подождите |
| 503 | `hosting_unavailable` | Агент сервера временно не отвечает — повторите |

Коды ошибок совпадают с сообщениями интерфейса панели, их удобно обрабатывать в коде.

## Методы

Все пути ниже — относительно `https://…/api/v2`. `domain` — домен сайта, `path` — путь относительно домашней папки пользователя сайта (`www/example.uz/index.php`).

### Аккаунт

| Метод | Путь | Право | Назначение |
|---|---|---|---|
| GET | `/me` | любое | Владелец токена, права, срок и версия панели |

### Сайты — `sites`

| Метод | Путь | Право | Назначение |
|---|---|---|---|
| GET | `/sites` | read | Список сайтов |
| POST | `/sites` | write | Создать сайт |
| POST | `/sites/lifecycle` | write | `{"domain","action"}` — `enable`, `disable`, `delete` |
| GET | `/sites/settings?domain=` | read | Сайт и его настройки |
| POST | `/sites/settings` | write | Сохранить настройки, сменить тип бэкенда |
| POST | `/sites/ssl` | write | SSL: `issue`, `remove` и перенаправление на HTTPS |
| GET | `/sites/scan?domain=` | read | Результат последнего сканирования антивирусом |
| POST | `/sites/scan` | write | `{"domain"}` — запустить сканирование |
| POST | `/sites/scan/action` | write | `{"domain","action","path"\|"id"}` — `quarantine`, `delete`, `restore`, `purge` |
| GET | `/site-service?domain=&log=` | read | Состояние службы сайта и логи (`log`: `access`, `error`, для Node.js/Python — `backend`) |
| POST | `/site-service` | write | `{"domain","action":"restart"}` |
| GET | `/traffic?domain=&month=YYYY-MM` | read | Трафик за месяц и график по дням (без `domain` — по аккаунтам) |
| GET | `/sites/stats-report?domain=` | read | Отчёт о посещениях GoAccess (HTML) |
| GET | `/apps/install?domain=` | read | Состояние установки приложения |
| POST | `/apps/install` | write | Установить CMS/фреймворк |
| GET | `/get-site-photo/{domain}` | read | Снимок сайта (изображение) |
| GET | `/owners` | read | Владельцы сайтов (Linux-пользователи) |
| GET | `/php`, `/node`, `/python` | read | Установленные версии |

**Создание сайта** — `POST /sites`:

| Поле | Примечание |
|---|---|
| `domain` | Обязательно, например `shop.example.uz` |
| `runtime` | Обязательно: `php`, `node`, `python`, `static`, `proxy` |
| `php`, `handler` | Версия PHP (`8.3`) и обработчик: `fpm`, `fastcgi`, `apache`, `cgi` |
| `node` | Основная версия Node.js (`22`); пусто — системная |
| `python` | Версия Python (`3.12`) — должна быть установлена на сервере |
| `proxy` | Адрес для `runtime: proxy` (`http://127.0.0.1:3000`) |
| `account_id` | Какому аккаунту принадлежит сайт (по умолчанию — владельцу токена) |
| `owner`, `new_owner`, `owner_name` | Linux-пользователь: существующий (`owner`) или новый (`new_owner: true`, `owner_name`) |

`state` в ответе: `provisioning`, `active`, `disabled`, `failed` (причина — в поле `error`). Поддомен существующего сайта автоматически получает пользователя этого сайта.

**Изменение настроек** — сначала `GET /sites/settings?domain=…`, измените нужные поля и отправьте в `POST /sites/settings`:

```json
{
  "domain": "shop.example.uz",
  "settings": { "...объект settings из GET, с изменениями...": "" },
  "auth_password": "",
  "runtime": "", "handler": "fpm", "php": "8.4", "node": "", "python": "", "proxy": "",
  "force_https": true
}
```

Внутри `settings`: `aliases`, `gzip`, `gzip_level`, `nginx_static`, `static_ext`, `cache_days`, `hsts`, `http2`, `redirects`, `access_log`, `error_log`, `auth_on`, `auth_user`, `rate_on`, `rate`, `rate_unit`, `burst_on`, `burst`, `no_delay`, `env`, `access_mode`, `access_list`, `php_ini`. Пустой `runtime` оставляет тип бэкенда; другое значение меняет его ([Настройки сайта](site-settings.md)).

**SSL** — `POST /sites/ssl`:

```json
{ "domain": "shop.example.uz", "action": "issue", "type": "letsencrypt", "email": "admin@example.uz", "force_https": true }
```

`type`: `letsencrypt` или `selfsigned`.

**Установка приложения** — `POST /apps/install`:

```json
{ "domain": "blog.example.uz", "app": "wordpress", "title": "Blog",
  "admin_user": "admin", "admin_password": "Dlinnyj-i-slozhnyj-parol-2026", "admin_email": "admin@example.uz" }
```

`app`: `wordpress`, `joomla`, `drupal`, `laravel`, `symfony`, `codeigniter`, `strapi`, `ghost`, `express`, `nextjs`, `nestjs`, `wagtail`, `django`, `flask`, `fastapi`. Сайт должен быть пустым и подходящего типа. Установка идёт в фоне — следите за ней через `GET /apps/install?domain=`.

### Файлы — `files`

| Метод | Путь | Право | Назначение |
|---|---|---|---|
| GET | `/files?domain=&path=` | read | Список папки или текст файла |
| POST | `/files` | write | `{"domain","path","action","content","expected"}` — `save`, `mkdir`, `create` |
| POST | `/files/op` | write | Действия: `rename`, `move`, `copy`, `chmod`, `archive`, `extract`, `delete` |
| POST | `/files/upload?domain=&path=` | write | Загрузка: тело запроса — сам файл, `path` — полный путь назначения |
| GET | `/files/download?domain=&path=` | read | Скачать файл |
| GET | `/files/stats?domain=&path=` | read | Статистика диска: самые большие папки и файлы |

Примеры `/files/op`:

```json
{ "domain": "shop.example.uz", "action": "rename", "path": "www/shop.example.uz/old.php", "target": "www/shop.example.uz/new.php" }
{ "domain": "shop.example.uz", "action": "chmod", "paths": ["www/shop.example.uz/storage"], "mode": "755", "recursive": true }
{ "domain": "shop.example.uz", "action": "archive", "paths": ["www/shop.example.uz"], "target": "site.zip" }
{ "domain": "shop.example.uz", "action": "extract", "path": "www/shop.example.uz/site.zip", "target": "www/shop.example.uz" }
{ "domain": "shop.example.uz", "action": "delete", "paths": ["www/shop.example.uz/tmp"] }
```

Загрузка файла (Bash):

```bash
curl -sS --fail-with-body -X POST \
  "$PANEL/files/upload?domain=shop.example.uz&path=www/shop.example.uz/site.zip" \
  -H "Authorization: Bearer $LP_TOKEN" --data-binary @site.zip
```

### Базы данных — `databases`

| Метод | Путь | Право | Назначение |
|---|---|---|---|
| GET | `/databases` | read | Список баз |
| POST | `/databases` | write | Действия (ниже) |
| GET | `/databases/engines` | read | Доступность MySQL/PostgreSQL |
| POST | `/databases/import` | write | `{"name","path"}` — импорт `.sql`/`.sql.gz` из папки сайта |
| GET | `/databases/import?name=` | read | Состояние импорта |
| GET | `/databases/export?name=` | read | Скачать базу как `.sql.gz` |
| POST | `/databases/phpmyadmin`, `/databases/adminer` | write | `{"name"}` — ссылка для входа без пароля |

Действия `POST /databases`:

| `action` | Поля |
|---|---|
| `create` | `name`, `user`, `password`, `site`, `charset` (`utf8mb4`), `engine` (`mysql` или `postgresql`) |
| `password` | `name`, `password` |
| `delete` | `name` |
| `user_add` | `name`, `user`, `password`, `privileges` (`all`, `readwrite`, `readonly`) |
| `user_update` | `name`, `user`, `privileges` |
| `user_remove` | `name`, `user` |
| `hosts` | `name`, `user`, `hosts` (список IP/сетей — внешний доступ), `password` |

Пустые поля тоже можно отправлять: `{"action":"delete","name":"shop_db","user":"","password":"","site":"","charset":""}`.

### DNS — `dns`

| Метод | Путь | Право | Назначение |
|---|---|---|---|
| GET | `/dns` | read | Зоны, IP сервера, состояние BIND |
| GET | `/dns/zone?zone=` | read | Записи зоны |
| POST | `/dns` | write | `create` (`zone`), `save` (`zone`, `records`), `delete` (`zone`) |

`records` — полный список: `{"name":"www","type":"A","ttl":3600,"value":"203.0.113.10","priority":0}`. `save` заменяет все записи зоны — сначала получите их через `GET /dns/zone`.

### Почта — `mail`

| Метод | Путь | Право | Назначение |
|---|---|---|---|
| GET | `/mail` | read | Домены, ящики, данные подключения, DNS-записи |
| POST | `/mail` | write | Действия (ниже) |

| `action` | Поля |
|---|---|
| `domain_add` | `domain`, `site` |
| `domain_update` | `domain`, `catch_all`, `disabled` |
| `domain_remove` | `domain` |
| `box_add` | `address` (`info@example.uz`), `password`, `quota_mb`, `aliases`, `forwards` |
| `box_update` | `address`, по желанию `password`, `quota_mb`, `aliases`, `forwards`, `disabled` |
| `box_remove` | `address` |

### FTP — `ftp`

| Метод | Путь | Право | Назначение |
|---|---|---|---|
| GET | `/accounts` | read | FTP-аккаунты |
| POST | `/accounts` | write | `create`, `update`, `toggle`, `delete` |

Поля: `action`, `name`, `site`, `password`, `home`, `read_only`, `enabled`.

### Планировщик — `cron`

| Метод | Путь | Право | Назначение |
|---|---|---|---|
| GET | `/cron` | read | Задания и время следующего запуска |
| POST | `/cron` | write | `create`, `update`, `toggle`, `run`, `delete` |

Поля: `action`, `id`, `site`, `schedule` (`*/5 * * * *`), `command`, `comment`, `enabled`. `run` выполняет задание сразу и возвращает результат.

### Резервные копии — `backups`

| Метод | Путь | Право | Назначение |
|---|---|---|---|
| GET | `/backups?domain=` | read | Копии и расписание автоматического копирования |
| POST | `/backups` | write | `create`, `restore`, `delete`, `plan` |
| GET | `/backups/download?domain=&id=` | read | Скачать копию как `.tar` |
| GET | `/backups/remote?domain=` | read | Состояние Google Drive/Dropbox для сайта и копии в хранилище |
| POST | `/backups/remote` | write | `enable`, `disable`, `keep`, `sync`, `fetch`, `delete` |
| GET | `/remote` | read | Подключённые хранилища и место в них |
| POST | `/remote` | write | `disconnect` (подключение — через браузер) |

Примеры `POST /backups`:

```json
{ "domain": "shop.example.uz", "action": "create" }
{ "domain": "shop.example.uz", "action": "restore", "id": "<id из GET /backups>", "files": true, "databases": true }
{ "domain": "shop.example.uz", "action": "plan", "plan": { "schedule": "daily", "hour": 3, "weekday": 0, "keep": 7, "files": true, "databases": true } }
```

`schedule`: `off`, `daily`, `weekly`; `weekday` 0–6 (0 — воскресенье). `POST /backups/remote`: `{"domain","provider":"gdrive"|"dropbox","action","keep","file"}`.

### Git — `git`

| Метод | Путь | Право | Назначение |
|---|---|---|---|
| GET | `/git?domain=` | read | Репозиторий, ключ развёртывания, адрес вебхука, лог последнего деплоя |
| POST | `/git` | write | `save` (`repo`, `branch`, `command`), `deploy`, `token` (новый вебхук), `disconnect` |

Деплой из CI:

```bash
lp POST /git '{"domain":"api.example.uz","action":"deploy"}'
```

### Аккаунты — `users`

| Метод | Путь | Право | Назначение |
|---|---|---|---|
| GET | `/users` | read | Список аккаунтов |
| POST | `/users` | write | Создать аккаунт (`201`) |
| PATCH | `/users/{id}` | write | Изменить: роль, права, SSH, пароль, `disabled` (блокировка) |
| DELETE | `/users/{id}` | write | Удалить (если есть сайты — `409 account_has_sites`) |
| POST | `/users/2fa-reset` | write | `{"id"}` — отключить 2FA аккаунта |
| GET | `/audit` | read | Журнал действий (последние 50 записей) |

Поля аккаунта: `name` (3–64 символа, потом не меняется), `role` (`user`, `reseller`, `admin`), `password` (6–72; пустой в `PATCH` — не меняется), `creator_id`, `permissions` (`{"sites","files","services"}`), `ssh`, `disabled`. В `PATCH` передавайте также `name` и `role`.

### Лимиты — `limits` (Pro и Premium)

| Метод | Путь | Право | Назначение |
|---|---|---|---|
| GET | `/limits?account_id=` | read | Лимиты |
| PUT | `/limits` | write | Сохранить лимиты |
| GET | `/limits/usage?account_id=` | read | Текущее использование (диск, RAM, сайты, базы) |

`PUT /limits`: `account_id`, `memory_mib` (0 или ≥32), `disk_mib` (0 или ≥64, квоты должны быть включены), `domains`, `databases`, `users` (только реселлеру), `cpu_percent` (пока `0`). `0` — без ограничений.

### Брендинг — `branding`

| Метод | Путь | Право | Назначение |
|---|---|---|---|
| GET | `/settings/branding` | read | Название, цвет, логотип |
| POST | `/settings/branding` | write | `name`, `color` (`#2563eb`), `logo` (data URL), `remove_logo`, `reset` |

### Сервер — `system` (только главный администратор)

| Метод | Путь | Назначение |
|---|---|---|
| GET | `/license` | Состояние лицензии и тариф |
| POST | `/license/activate` | Активировать лицензию |
| GET | `/metrics`, `/stats?range=` | Нагрузка сервера (`range`: `live`, `1h`, `24h`, `7d`, `30d`) |
| GET / POST | `/system/services` | Службы; `{"unit","action"}` — `start`, `stop`, `restart`, `enable`, `disable` |
| GET / POST | `/applications` | Приложения; `{"name","action"}` — `install`, `remove` |
| GET / POST | `/firewall` | Правила; `apply` (`enabled`, `rules`), затем `confirm` (`token`) |
| GET | `/security` | Защита входа, заблокированные IP, fail2ban |
| POST | `/security/settings`, `/security/unblock` | Настройки; `{"ip","jail"}` — разблокировать |
| GET / POST | `/quota` | Дисковые квоты; `{"action":"enable"}` |
| GET / POST | `/panel-tls` | Сертификат панели на IP: `issue` (получить или обновить), `self` (вернуться к своему) |
| GET / POST | `/panel-addresses` | Домены панели: `add` (`domain`, `cert`, `email`, `cert_pem`, `key_pem`), `cert`, `remove` |

> Применяя файрвол через API, в течение минуты отправьте `confirm` с `token` из ответа `apply` — иначе панель вернёт прежние правила (чтобы вы не заблокировали себя).

## Полный пример: открыть хостинг клиенту после оплаты

Права токена: `users:write`, `limits:write`, `sites:write`, `databases:write`.

**Bash:**

```bash
ID=$(lp POST /users '{"name":"client1","role":"user","password":"Parol-klienta-2026","permissions":{"sites":true,"files":true,"services":true}}' | jq -r .id)
lp PUT /limits "{\"account_id\":$ID,\"memory_mib\":1024,\"disk_mib\":10240,\"domains\":3,\"databases\":5}"
lp POST /sites "{\"domain\":\"client1.example.uz\",\"runtime\":\"php\",\"php\":\"8.3\",\"handler\":\"fpm\",\"account_id\":$ID}"
lp POST /sites/ssl '{"domain":"client1.example.uz","action":"issue","type":"letsencrypt","email":"","force_https":true}'
lp POST /databases '{"action":"create","name":"client1_db","user":"client1_user","password":"Parol-bazy-2026","site":"client1.example.uz","charset":"utf8mb4","engine":"mysql"}'
```

**PHP:**

```php
$acc = lp('POST', '/users', [
    'name' => 'client1', 'role' => 'user', 'password' => 'Parol-klienta-2026',
    'permissions' => ['sites' => true, 'files' => true, 'services' => true],
]);
lp('PUT', '/limits', ['account_id' => $acc['id'], 'memory_mib' => 1024, 'disk_mib' => 10240, 'domains' => 3, 'databases' => 5]);
lp('POST', '/sites', ['domain' => 'client1.example.uz', 'runtime' => 'php', 'php' => '8.3', 'handler' => 'fpm', 'account_id' => $acc['id']]);
lp('POST', '/sites/ssl', ['domain' => 'client1.example.uz', 'action' => 'issue', 'type' => 'letsencrypt', 'email' => '', 'force_https' => true]);
lp('POST', '/databases', ['action' => 'create', 'name' => 'client1_db', 'user' => 'client1_user', 'password' => 'Parol-bazy-2026',
    'site' => 'client1.example.uz', 'charset' => 'utf8mb4', 'engine' => 'mysql']);
```

**Node.js:**

```js
const acc = await lp("POST", "/users", {
  name: "client1", role: "user", password: "Parol-klienta-2026",
  permissions: { sites: true, files: true, services: true },
});
await lp("PUT", "/limits", { account_id: acc.id, memory_mib: 1024, disk_mib: 10240, domains: 3, databases: 5 });
await lp("POST", "/sites", { domain: "client1.example.uz", runtime: "php", php: "8.3", handler: "fpm", account_id: acc.id });
await lp("POST", "/sites/ssl", { domain: "client1.example.uz", action: "issue", type: "letsencrypt", email: "", force_https: true });
await lp("POST", "/databases", {
  action: "create", name: "client1_db", user: "client1_user", password: "Parol-bazy-2026",
  site: "client1.example.uz", charset: "utf8mb4", engine: "mysql",
});
```

Блокировка по окончании срока и открытие после оплаты:

```bash
lp PATCH /users/$ID '{"name":"client1","role":"user","disabled":true}'    # заблокировать
lp PATCH /users/$ID '{"name":"client1","role":"user","disabled":false}'   # открыть снова
```

## API v1

`/api/v1` теперь только для системы: `GET /api/v1/check/is-live-panel` (без токена; сообщает, что сервер — LivePanel, и его версию) и `POST /api/v1/activate-license`, которым пользуется служба лицензий. Прежние `/api/v1/users`, `/api/v1/sites` и `/api/v1/limits` удалены — используйте те же пути в `/api/v2`; токены остаются прежними.
