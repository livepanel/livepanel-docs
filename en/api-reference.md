# API v2 reference

> **The API works only on panels with a Premium subscription.** On the Free and Pro plans every request returns `402 upgrade_required`. To upgrade — [License and plans](license.md).

API v2 opens **everything the panel’s web interface does** to programs: sites, files, databases, DNS, mail, FTP, cron, backups, Git, accounts, limits, branding and server settings. A billing system, a Telegram bot, CI/CD or your own script can do every job a person does in the panel.

Every API request goes through exactly the same code the panel pages use: a token can never do what its account cannot do in the panel, and the token’s scopes narrow it further.

## Getting started

1. In the panel open **System → API tokens**, create a token and tick **Read** and/or **Write** for the areas you need ([API tokens and activity log](api-tokens.md)).
2. Save the token right away — it is shown only once (it starts with `lp_`).
3. Send it with every request:

```text
Authorization: Bearer lp_XXXXXXXXXXXXXXXX
```

| | |
|---|---|
| Address | `https://SERVER:6563/api/v2/…` or the panel domain `https://panel.example.uz/api/v2/…` |
| Format | JSON requests and responses. `POST`, `PUT`, `PATCH` need `Content-Type: application/json` |
| Unknown fields | Rejected (`400 invalid_input`) — send only the documented fields |
| JSON size | Up to 16 KB (file uploads are separate, up to 2 GB) |
| Certificate | If the panel uses its own self-signed certificate, give it a trusted one — [Panel address and SSL](panel-access.md) |

Check whom the token belongs to and what it may do:

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

## Client code (PHP, Node.js, Bash)

All examples below use these small helpers. Do not put the token in the code — keep it in an environment variable (`LP_TOKEN`).

**Bash** (curl and jq):

```bash
#!/usr/bin/env bash
set -euo pipefail
PANEL="https://panel.example.uz/api/v2"
: "${LP_TOKEN:?LP_TOKEN is not set}"

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

**PHP** (7.4+, curl extension):

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

**Node.js** (18+, built-in `fetch`):

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

## Scopes

Every area has a `:read` (`GET` only) and a `:write` (changes) scope:

| Area | What it controls | Who can grant it |
|---|---|---|
| `sites` | Sites, settings, SSL, application installer, site service and logs, scanning, traffic | An account with the Sites permission |
| `files` | File manager: list, read, save, upload, actions | An account with the Files permission |
| `databases` | MySQL/PostgreSQL databases, users, import/export | An account with the Sites permission |
| `dns` | DNS zones and records | An account with the Sites permission |
| `mail` | Mail domains and mailboxes | An account with the Sites permission |
| `ftp` | FTP accounts | An account with the Sites permission |
| `cron` | Scheduled tasks | An account with the Sites permission |
| `backups` | Backups, restore, Google Drive/Dropbox | An account with the Sites permission |
| `git` | Git deploy | An account with the Sites permission |
| `users` | Panel accounts, turning 2FA off, activity log | Administrator, reseller |
| `limits` | Account limits (`limits:read` — everyone, `limits:write` — administrator, reseller) | — |
| `branding` | Panel name, logo, color | Administrator, reseller |
| `system` | Services, applications, firewall, sign-in protection, quotas, panel SSL and addresses, license | Main administrator only |

What the API **cannot** do (for security): sign in or out, change the account’s own password, 2FA and recovery email, create or revoke API tokens, the web terminal.

## Errors

An error response always looks the same: `{"error": "code"}`.

| HTTP | Code | Meaning |
|---|---|---|
| 400 | `invalid_input` | Bad JSON, a missing or an extra field |
| 401 | `unauthorized` | No token, a wrong, expired or revoked token, or the account is disabled |
| 402 | `license_required` | The panel license is not active |
| 402 | `upgrade_required` | The plan is not Premium |
| 403 | `scope_denied` | The token has no scope for this action |
| 403 | `forbidden` | The account cannot manage this object (another account’s site etc.) |
| 404 | `site_not_found`, `database_not_found`, … | The object was not found |
| 409 | `domain_limit_reached`, `database_limit_reached`, … | A limit or state conflict |
| 429 | `too_many_attempts` | Too many requests — wait a little |
| 503 | `hosting_unavailable` | The server agent is not answering for a moment — retry |

The error codes are the same as the panel interface messages, so they are easy to handle in code.

## Endpoints

All routes below are relative to `https://…/api/v2`. `domain` is the site domain, `path` is a path relative to the site user’s home folder (`www/example.uz/index.php`).

### Account

| Method | Path | Scope | Purpose |
|---|---|---|---|
| GET | `/me` | any | The token’s owner, scopes, expiry and the panel version |

### Sites — `sites`

| Method | Path | Scope | Purpose |
|---|---|---|---|
| GET | `/sites` | read | List of sites |
| POST | `/sites` | write | Create a site |
| POST | `/sites/lifecycle` | write | `{"domain","action"}` — `enable`, `disable`, `delete` |
| GET | `/sites/settings?domain=` | read | The site and its settings |
| POST | `/sites/settings` | write | Save settings, switch the backend type |
| POST | `/sites/ssl` | write | SSL: `issue`, `remove` and the HTTPS redirect |
| GET | `/sites/scan?domain=` | read | Result of the last antivirus scan |
| POST | `/sites/scan` | write | `{"domain"}` — start a scan |
| POST | `/sites/scan/action` | write | `{"domain","action","path"\|"id"}` — `quarantine`, `delete`, `restore`, `purge` |
| GET | `/site-service?domain=&log=` | read | Site service state and logs (`log`: `access`, `error`, `backend` for Node.js/Python) |
| POST | `/site-service` | write | `{"domain","action":"restart"}` |
| GET | `/traffic?domain=&month=YYYY-MM` | read | Monthly traffic and a daily chart (without `domain` — per account) |
| GET | `/sites/stats-report?domain=` | read | GoAccess visitor report (HTML) |
| GET | `/apps/install?domain=` | read | Application install state |
| POST | `/apps/install` | write | Install a CMS/framework |
| GET | `/get-site-photo/{domain}` | read | Site preview (image) |
| GET | `/owners` | read | Site owners (Linux users) |
| GET | `/php`, `/node`, `/python` | read | Installed versions |

**Creating a site** — `POST /sites`:

| Field | Notes |
|---|---|
| `domain` | Required, e.g. `shop.example.uz` |
| `runtime` | Required: `php`, `node`, `python`, `static`, `proxy` |
| `php`, `handler` | PHP version (`8.3`) and handler: `fpm`, `fastcgi`, `apache`, `cgi` |
| `node` | Node.js major version (`22`); empty — the system one |
| `python` | Python version (`3.12`) — must be installed on the server |
| `proxy` | Target for `runtime: proxy` (`http://127.0.0.1:3000`) |
| `account_id` | Which account the site belongs to (default — the token’s owner) |
| `owner`, `new_owner`, `owner_name` | The Linux user: an existing one (`owner`) or a new one (`new_owner: true`, `owner_name`) |

`state` in the response: `provisioning`, `active`, `disabled`, `failed` (the reason is in `error`). A subdomain of an existing site joins that site’s user automatically.

**Changing settings** — first `GET /sites/settings?domain=…`, change the fields you need and send it to `POST /sites/settings`:

```json
{
  "domain": "shop.example.uz",
  "settings": { "...the settings object from GET, changed...": "" },
  "auth_password": "",
  "runtime": "", "handler": "fpm", "php": "8.4", "node": "", "python": "", "proxy": "",
  "force_https": true
}
```

Inside `settings`: `aliases`, `gzip`, `gzip_level`, `nginx_static`, `static_ext`, `cache_days`, `hsts`, `http2`, `redirects`, `access_log`, `error_log`, `auth_on`, `auth_user`, `rate_on`, `rate`, `rate_unit`, `burst_on`, `burst`, `no_delay`, `env`, `access_mode`, `access_list`, `php_ini`. An empty `runtime` keeps the backend type; another value switches it ([Site settings](site-settings.md)).

**SSL** — `POST /sites/ssl`:

```json
{ "domain": "shop.example.uz", "action": "issue", "type": "letsencrypt", "email": "admin@example.uz", "force_https": true }
```

`type`: `letsencrypt` or `selfsigned`.

**Installing an application** — `POST /apps/install`:

```json
{ "domain": "blog.example.uz", "app": "wordpress", "title": "Blog",
  "admin_user": "admin", "admin_password": "A-long-and-strong-password-2026", "admin_email": "admin@example.uz" }
```

`app`: `wordpress`, `joomla`, `drupal`, `laravel`, `symfony`, `codeigniter`, `strapi`, `ghost`, `express`, `nextjs`, `nestjs`, `wagtail`, `django`, `flask`, `fastapi`. The site must be empty and of the matching type. The install runs in the background — follow it with `GET /apps/install?domain=`.

### Files — `files`

| Method | Path | Scope | Purpose |
|---|---|---|---|
| GET | `/files?domain=&path=` | read | A folder listing or a file’s text |
| POST | `/files` | write | `{"domain","path","action","content","expected"}` — `save`, `mkdir`, `create` |
| POST | `/files/op` | write | Actions: `rename`, `move`, `copy`, `chmod`, `archive`, `extract`, `delete` |
| POST | `/files/upload?domain=&path=` | write | Upload: the request body is the file itself, `path` is the full destination path |
| GET | `/files/download?domain=&path=` | read | Download a file |
| GET | `/files/stats?domain=&path=` | read | Disk statistics: the largest folders and files |

`/files/op` examples:

```json
{ "domain": "shop.example.uz", "action": "rename", "path": "www/shop.example.uz/old.php", "target": "www/shop.example.uz/new.php" }
{ "domain": "shop.example.uz", "action": "chmod", "paths": ["www/shop.example.uz/storage"], "mode": "755", "recursive": true }
{ "domain": "shop.example.uz", "action": "archive", "paths": ["www/shop.example.uz"], "target": "site.zip" }
{ "domain": "shop.example.uz", "action": "extract", "path": "www/shop.example.uz/site.zip", "target": "www/shop.example.uz" }
{ "domain": "shop.example.uz", "action": "delete", "paths": ["www/shop.example.uz/tmp"] }
```

Uploading a file (Bash):

```bash
curl -sS --fail-with-body -X POST \
  "$PANEL/files/upload?domain=shop.example.uz&path=www/shop.example.uz/site.zip" \
  -H "Authorization: Bearer $LP_TOKEN" --data-binary @site.zip
```

### Databases — `databases`

| Method | Path | Scope | Purpose |
|---|---|---|---|
| GET | `/databases` | read | List of databases |
| POST | `/databases` | write | Actions (below) |
| GET | `/databases/engines` | read | Whether MySQL/PostgreSQL are available |
| POST | `/databases/import` | write | `{"name","path"}` — import a `.sql`/`.sql.gz` from the site folder |
| GET | `/databases/import?name=` | read | Import state |
| GET | `/databases/export?name=` | read | Download the database as `.sql.gz` |
| POST | `/databases/phpmyadmin`, `/databases/adminer` | write | `{"name"}` — a password-less sign-in link |

`POST /databases` actions:

| `action` | Fields |
|---|---|
| `create` | `name`, `user`, `password`, `site`, `charset` (`utf8mb4`), `engine` (`mysql` or `postgresql`) |
| `password` | `name`, `password` |
| `delete` | `name` |
| `user_add` | `name`, `user`, `password`, `privileges` (`all`, `readwrite`, `readonly`) |
| `user_update` | `name`, `user`, `privileges` |
| `user_remove` | `name`, `user` |
| `hosts` | `name`, `user`, `hosts` (list of IPs/networks — outside access), `password` |

Sending the empty fields too is accepted: `{"action":"delete","name":"shop_db","user":"","password":"","site":"","charset":""}`.

### DNS — `dns`

| Method | Path | Scope | Purpose |
|---|---|---|---|
| GET | `/dns` | read | Zones, the server IP, BIND state |
| GET | `/dns/zone?zone=` | read | Records of a zone |
| POST | `/dns` | write | `create` (`zone`), `save` (`zone`, `records`), `delete` (`zone`) |

`records` is the full list: `{"name":"www","type":"A","ttl":3600,"value":"203.0.113.10","priority":0}`. `save` replaces all records of the zone — read them first with `GET /dns/zone`.

### Mail — `mail`

| Method | Path | Scope | Purpose |
|---|---|---|---|
| GET | `/mail` | read | Domains, mailboxes, connection details, DNS records |
| POST | `/mail` | write | Actions (below) |

| `action` | Fields |
|---|---|
| `domain_add` | `domain`, `site` |
| `domain_update` | `domain`, `catch_all`, `disabled` |
| `domain_remove` | `domain` |
| `box_add` | `address` (`info@example.uz`), `password`, `quota_mb`, `aliases`, `forwards` |
| `box_update` | `address`, optional `password`, `quota_mb`, `aliases`, `forwards`, `disabled` |
| `box_remove` | `address` |

### FTP — `ftp`

| Method | Path | Scope | Purpose |
|---|---|---|---|
| GET | `/accounts` | read | FTP accounts |
| POST | `/accounts` | write | `create`, `update`, `toggle`, `delete` |

Fields: `action`, `name`, `site`, `password`, `home`, `read_only`, `enabled`.

### Scheduler — `cron`

| Method | Path | Scope | Purpose |
|---|---|---|---|
| GET | `/cron` | read | Tasks and their next run |
| POST | `/cron` | write | `create`, `update`, `toggle`, `run`, `delete` |

Fields: `action`, `id`, `site`, `schedule` (`*/5 * * * *`), `command`, `comment`, `enabled`. `run` executes the task right away and returns the result.

### Backups — `backups`

| Method | Path | Scope | Purpose |
|---|---|---|---|
| GET | `/backups?domain=` | read | Copies and the automatic backup schedule |
| POST | `/backups` | write | `create`, `restore`, `delete`, `plan` |
| GET | `/backups/download?domain=&id=` | read | Download a copy as `.tar` |
| GET | `/backups/remote?domain=` | read | The site’s Google Drive/Dropbox state and the copies in storage |
| POST | `/backups/remote` | write | `enable`, `disable`, `keep`, `sync`, `fetch`, `delete` |
| GET | `/remote` | read | Connected storages and their space |
| POST | `/remote` | write | `disconnect` (connecting goes through the browser) |

`POST /backups` examples:

```json
{ "domain": "shop.example.uz", "action": "create" }
{ "domain": "shop.example.uz", "action": "restore", "id": "<id from GET /backups>", "files": true, "databases": true }
{ "domain": "shop.example.uz", "action": "plan", "plan": { "schedule": "daily", "hour": 3, "weekday": 0, "keep": 7, "files": true, "databases": true } }
```

`schedule`: `off`, `daily`, `weekly`; `weekday` 0–6 (0 — Sunday). `POST /backups/remote`: `{"domain","provider":"gdrive"|"dropbox","action","keep","file"}`.

### Git — `git`

| Method | Path | Scope | Purpose |
|---|---|---|---|
| GET | `/git?domain=` | read | Repository, deploy key, webhook address, the last deploy log |
| POST | `/git` | write | `save` (`repo`, `branch`, `command`), `deploy`, `token` (a new webhook), `disconnect` |

Deploying from CI:

```bash
lp POST /git '{"domain":"api.example.uz","action":"deploy"}'
```

### Accounts — `users`

| Method | Path | Scope | Purpose |
|---|---|---|---|
| GET | `/users` | read | List of accounts |
| POST | `/users` | write | Create an account (`201`) |
| PATCH | `/users/{id}` | write | Change: role, permissions, SSH, password, `disabled` (block) |
| DELETE | `/users/{id}` | write | Delete (with sites — `409 account_has_sites`) |
| POST | `/users/2fa-reset` | write | `{"id"}` — turn an account’s 2FA off |
| GET | `/audit` | read | Activity log (the last 50 entries) |

Account fields: `name` (3–64 characters, cannot change later), `role` (`user`, `reseller`, `admin`), `password` (6–72; empty in `PATCH` — unchanged), `creator_id`, `permissions` (`{"sites","files","services"}`), `ssh`, `disabled`. Send `name` and `role` in `PATCH` too.

### Limits — `limits` (Pro and Premium)

| Method | Path | Scope | Purpose |
|---|---|---|---|
| GET | `/limits?account_id=` | read | Limits |
| PUT | `/limits` | write | Save limits |
| GET | `/limits/usage?account_id=` | read | Current usage (disk, RAM, sites, databases) |

`PUT /limits`: `account_id`, `memory_mib` (0 or ≥32), `disk_mib` (0 or ≥64, quotas must be on), `domains`, `databases`, `users` (resellers only), `cpu_percent` (`0` for now). `0` means unlimited.

### Branding — `branding`

| Method | Path | Scope | Purpose |
|---|---|---|---|
| GET | `/settings/branding` | read | Name, color, logo |
| POST | `/settings/branding` | write | `name`, `color` (`#2563eb`), `logo` (data URL), `remove_logo`, `reset` |

### Server — `system` (main administrator only)

| Method | Path | Purpose |
|---|---|---|
| GET | `/license` | License state and plan |
| POST | `/license/activate` | Activate a license |
| GET | `/metrics`, `/stats?range=` | Server load (`range`: `live`, `1h`, `24h`, `7d`, `30d`) |
| GET / POST | `/system/services` | Services; `{"unit","action"}` — `start`, `stop`, `restart`, `enable`, `disable` |
| GET / POST | `/applications` | Applications; `{"name","action"}` — `install`, `remove` |
| GET / POST | `/firewall` | Rules; `apply` (`enabled`, `rules`), then `confirm` (`token`) |
| GET | `/security` | Sign-in protection, blocked IPs, fail2ban |
| POST | `/security/settings`, `/security/unblock` | Settings; `{"ip","jail"}` — unblock |
| GET / POST | `/quota` | Disk quotas; `{"action":"enable"}` |
| GET / POST | `/panel-tls` | The panel’s IP certificate: `issue` (get or renew), `self` (back to its own certificate) |
| GET / POST | `/panel-addresses` | Panel domains: `add` (`domain`, `cert`, `email`, `cert_pem`, `key_pem`), `cert`, `remove` |

> When applying the firewall through the API, send `confirm` with the `token` from the `apply` response within a minute — otherwise the panel restores the previous rules (so you cannot lock yourself out).

## Full example: open hosting for a customer after payment

Token scopes: `users:write`, `limits:write`, `sites:write`, `databases:write`.

**Bash:**

```bash
ID=$(lp POST /users '{"name":"client1","role":"user","password":"Customer-pass-2026","permissions":{"sites":true,"files":true,"services":true}}' | jq -r .id)
lp PUT /limits "{\"account_id\":$ID,\"memory_mib\":1024,\"disk_mib\":10240,\"domains\":3,\"databases\":5}"
lp POST /sites "{\"domain\":\"client1.example.uz\",\"runtime\":\"php\",\"php\":\"8.3\",\"handler\":\"fpm\",\"account_id\":$ID}"
lp POST /sites/ssl '{"domain":"client1.example.uz","action":"issue","type":"letsencrypt","email":"","force_https":true}'
lp POST /databases '{"action":"create","name":"client1_db","user":"client1_user","password":"Db-pass-2026","site":"client1.example.uz","charset":"utf8mb4","engine":"mysql"}'
```

**PHP:**

```php
$acc = lp('POST', '/users', [
    'name' => 'client1', 'role' => 'user', 'password' => 'Customer-pass-2026',
    'permissions' => ['sites' => true, 'files' => true, 'services' => true],
]);
lp('PUT', '/limits', ['account_id' => $acc['id'], 'memory_mib' => 1024, 'disk_mib' => 10240, 'domains' => 3, 'databases' => 5]);
lp('POST', '/sites', ['domain' => 'client1.example.uz', 'runtime' => 'php', 'php' => '8.3', 'handler' => 'fpm', 'account_id' => $acc['id']]);
lp('POST', '/sites/ssl', ['domain' => 'client1.example.uz', 'action' => 'issue', 'type' => 'letsencrypt', 'email' => '', 'force_https' => true]);
lp('POST', '/databases', ['action' => 'create', 'name' => 'client1_db', 'user' => 'client1_user', 'password' => 'Db-pass-2026',
    'site' => 'client1.example.uz', 'charset' => 'utf8mb4', 'engine' => 'mysql']);
```

**Node.js:**

```js
const acc = await lp("POST", "/users", {
  name: "client1", role: "user", password: "Customer-pass-2026",
  permissions: { sites: true, files: true, services: true },
});
await lp("PUT", "/limits", { account_id: acc.id, memory_mib: 1024, disk_mib: 10240, domains: 3, databases: 5 });
await lp("POST", "/sites", { domain: "client1.example.uz", runtime: "php", php: "8.3", handler: "fpm", account_id: acc.id });
await lp("POST", "/sites/ssl", { domain: "client1.example.uz", action: "issue", type: "letsencrypt", email: "", force_https: true });
await lp("POST", "/databases", {
  action: "create", name: "client1_db", user: "client1_user", password: "Db-pass-2026",
  site: "client1.example.uz", charset: "utf8mb4", engine: "mysql",
});
```

Blocking when the term ends, and opening again after payment:

```bash
lp PATCH /users/$ID '{"name":"client1","role":"user","disabled":true}'    # block
lp PATCH /users/$ID '{"name":"client1","role":"user","disabled":false}'   # open again
```

## API v1

`/api/v1` is now for the system only: `GET /api/v1/check/is-live-panel` (no token; tells that the server is LivePanel and its version) and `POST /api/v1/activate-license`, used by the license service. The former `/api/v1/users`, `/api/v1/sites` and `/api/v1/limits` are removed — use the same paths under `/api/v2`; tokens stay the same.
