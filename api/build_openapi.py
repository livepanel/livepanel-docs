#!/usr/bin/env python3
"""Builds openapi-v2.json — the OpenAPI 3.1 description of LivePanel API v2.

The route list mirrors internal/app/api_v2.go in the panel. Run after changing
it:  python3 api/build_openapi.py
"""
import json
import os

S = lambda **kw: dict(type='string', **kw)
I = lambda **kw: dict(type='integer', **kw)
B = lambda **kw: dict(type='boolean', **kw)
ARR = lambda items, **kw: dict(type='array', items=items, **kw)


def obj(props, required=(), **kw):
    o = dict(type='object', properties=props, additionalProperties=False, **kw)
    if required:
        o['required'] = list(required)
    return o


def q(name, desc, required=False, schema=None):
    return dict(name=name, **{'in': 'query'}, required=required, description=desc, schema=schema or S())


def p(name, desc, schema=None):
    return dict(name=name, **{'in': 'path'}, required=True, description=desc, schema=schema or S())


DOMAIN = q('domain', 'Site domain, e.g. shop.example.uz', True)
PATHQ = q('path', 'Path relative to the site user’s home folder, e.g. www/shop.example.uz/index.php', True)

schemas = {
    'Error': obj({'error': S(description='Error code, e.g. scope_denied, site_not_found, upgrade_required')}, ['error']),
    'Permissions': obj({'sites': B(), 'files': B(), 'services': B()}),
    'Account': dict(type='object', properties={
        'id': I(), 'name': S(), 'role': S(enum=['admin', 'reseller', 'user']), 'creator_id': I(),
        'disabled': B(), 'permissions': {'$ref': '#/components/schemas/Permissions'}, 'created': I(description='Unix time'),
        'ssh': B(), 'ssh_logins': ARR(S()), 'two_factor': B(),
        'memory_block': dict(type='object', description='Present while the account is blocked for its RAM limit'),
        'creator': B(description='true for the main administrator'),
    }),
    'AccountInput': obj({
        'name': S(pattern='^[a-zA-Z0-9][a-zA-Z0-9_.-]{2,63}$', description='Cannot change after creation; send it in PATCH too'),
        'role': S(enum=['user', 'reseller', 'admin'], description='admin only by the main administrator; resellers create user only'),
        'password': S(minLength=6, maxLength=72, description='Required on create; empty in PATCH keeps it'),
        'creator_id': I(description='Parent account (default: the token owner)'),
        'disabled': B(description='true blocks sign-in and the account’s sites stay as they are'),
        'permissions': {'$ref': '#/components/schemas/Permissions'},
        'ssh': B(description='SSH/SFTP with the panel password'),
    }, ['name', 'role']),
    'Site': dict(type='object', properties={
        'id': S(), 'domain': S(), 'owner': S(description='Linux user'), 'parent': S(),
        'runtime': S(enum=['php', 'node', 'python', 'static', 'proxy']), 'handler': S(enum=['fpm', 'fastcgi', 'apache', 'cgi']),
        'php': S(), 'node': S(), 'python': S(), 'proxy': S(), 'root': S(),
        'state': S(enum=['provisioning', 'active', 'disabled', 'failed']), 'error': S(), 'port': I(), 'created': I(),
        'ssl': S(enum=['', 'letsencrypt', 'selfsigned']), 'force_https': B(), 'account_id': I(), 'account_name': S(),
    }),
    'SiteCreate': obj({
        'domain': S(examples=['shop.example.uz']), 'runtime': S(enum=['php', 'node', 'python', 'static', 'proxy']),
        'handler': S(enum=['fpm', 'fastcgi', 'apache', 'cgi'], description='PHP only'), 'php': S(examples=['8.3']),
        'node': S(description='Node.js major, empty = system'), 'python': S(examples=['3.12'], description='Must be installed'),
        'proxy': S(examples=['http://127.0.0.1:3000']), 'account_id': I(description='Default: the token owner'),
        'owner': S(description='Existing Linux user'), 'new_owner': B(), 'owner_name': S(description='Name of a new Linux user'),
        'parent': S(),
    }, ['domain', 'runtime']),
    'Limits': obj({
        'memory_mib': I(description='0 or >= 32'), 'disk_mib': I(description='0 or >= 64; disk quotas must be on'),
        'cpu_percent': I(description='Must be 0 for now'), 'domains': I(), 'databases': I(), 'users': I(description='Resellers only'),
    }),
}
schemas['LimitsPut'] = obj(dict(account_id=I(), **schemas['Limits']['properties']), ['account_id'])


def action_body(actions, props, required=('action',)):
    pr = {'action': S(enum=actions)}
    pr.update(props)
    return obj(pr, required)


routes = [
    # tag, method, path, scope, summary, params, body
    ('Account', 'GET', '/me', None, 'The token’s account, scopes, expiry and the panel version', [], None),

    ('Sites', 'GET', '/sites', 'sites:read', 'List sites', [], None),
    ('Sites', 'POST', '/sites', 'sites:write', 'Create a site', [], {'$ref': '#/components/schemas/SiteCreate'}),
    ('Sites', 'GET', '/owners', 'sites:read', 'Site owners (Linux users)', [], None),
    ('Sites', 'POST', '/sites/lifecycle', 'sites:write', 'Enable, disable or delete a site', [],
     obj({'domain': S(), 'action': S(enum=['enable', 'disable', 'delete'])}, ['domain', 'action'])),
    ('Sites', 'GET', '/sites/settings', 'sites:read', 'A site and its settings', [DOMAIN], None),
    ('Sites', 'POST', '/sites/settings', 'sites:write', 'Save settings or switch the backend type. Send the settings object from GET with your changes.', [],
     obj({'domain': S(), 'settings': dict(type='object', description='aliases, gzip, gzip_level, nginx_static, static_ext, cache_days, hsts, http2, redirects, access_log, error_log, auth_on, auth_user, rate_on, rate, rate_unit, burst_on, burst, no_delay, env, access_mode, access_list, php_ini'),
          'auth_password': S(), 'runtime': S(description='Empty keeps the type'), 'handler': S(), 'php': S(), 'node': S(), 'python': S(), 'proxy': S(), 'force_https': B()},
         ['domain', 'settings'])),
    ('Sites', 'POST', '/sites/ssl', 'sites:write', 'Issue or remove an SSL certificate, set the HTTPS redirect', [],
     obj({'domain': S(), 'action': S(enum=['issue', 'remove']), 'type': S(enum=['letsencrypt', 'selfsigned', '']), 'email': S(), 'force_https': B()}, ['domain', 'action'])),
    ('Sites', 'GET', '/sites/scan', 'sites:read', 'Last antivirus scan of a site', [DOMAIN], None),
    ('Sites', 'POST', '/sites/scan', 'sites:write', 'Start an antivirus scan (ClamAV)', [], obj({'domain': S()}, ['domain'])),
    ('Sites', 'POST', '/sites/scan/action', 'sites:write', 'Quarantine, delete, restore or purge a found file', [],
     obj({'domain': S(), 'action': S(enum=['quarantine', 'delete', 'restore', 'purge']), 'path': S(), 'id': S()}, ['domain', 'action'])),
    ('Sites', 'GET', '/sites/stats-report', 'sites:read', 'GoAccess visitor report (HTML)', [DOMAIN, q('fresh', 'Rebuild now when set')], None),
    ('Sites', 'GET', '/traffic', 'sites:read', 'Monthly traffic and daily chart (without domain: per account)', [q('domain', 'Site domain'), q('month', 'YYYY-MM')], None),
    ('Sites', 'GET', '/site-service', 'sites:read', 'Site service state and logs', [DOMAIN, q('log', 'access, error, or backend (Node.js/Python)')], None),
    ('Sites', 'POST', '/site-service', 'sites:write', 'Restart the site service', [], obj({'domain': S(), 'action': S(enum=['restart'])}, ['domain', 'action'])),
    ('Sites', 'GET', '/apps/install', 'sites:read', 'Application install state', [DOMAIN], None),
    ('Sites', 'POST', '/apps/install', 'sites:write', 'Install a CMS or framework on an empty site (runs in the background)', [],
     obj({'domain': S(), 'app': S(enum=['wordpress', 'joomla', 'drupal', 'laravel', 'symfony', 'codeigniter', 'strapi', 'ghost', 'express', 'nextjs', 'nestjs', 'wagtail', 'django', 'flask', 'fastapi']),
          'title': S(), 'admin_user': S(), 'admin_password': S(minLength=12), 'admin_email': S()}, ['domain', 'app'])),
    ('Sites', 'GET', '/get-site-photo/{domain}', 'sites:read', 'Site preview image', [p('domain', 'Site domain')], None),
    ('Sites', 'GET', '/php', 'sites:read', 'Installed PHP versions', [], None),
    ('Sites', 'GET', '/node', 'sites:read', 'Installed Node.js versions', [], None),
    ('Sites', 'GET', '/python', 'sites:read', 'Installed Python versions', [], None),

    ('Files', 'GET', '/files', 'files:read', 'List a folder, or with action=read the text of a file (its hash goes into expected when saving)', [DOMAIN, PATHQ, q('action', 'read — return the file text', schema=S(enum=['read'])), q('encoding', 'Text encoding for action=read, default utf-8')], None),
    ('Files', 'POST', '/files', 'files:write', 'Save a file, create a file or a folder', [],
     obj({'domain': S(), 'path': S(), 'action': S(enum=['save', 'create', 'mkdir']), 'content': S(), 'expected': S(description='Hash from the read, protects from overwriting newer changes'), 'encoding': S()}, ['domain', 'path', 'action'])),
    ('Files', 'POST', '/files/op', 'files:write', 'File actions', [],
     obj({'domain': S(), 'action': S(enum=['rename', 'move', 'copy', 'chmod', 'archive', 'extract', 'delete']), 'path': S(), 'paths': ARR(S()),
          'target': S(description='rename: the new name only; archive: the archive name (made in the same folder); copy, move, extract: a folder path'), 'mode': S(examples=['644', '755']), 'recursive': B()}, ['domain', 'action'])),
    ('Files', 'POST', '/files/upload', 'files:write', 'Upload a file: the request body is the file itself (Content-Length required, up to 2 GB)', [DOMAIN, q('path', 'Full destination path including the file name', True), q('overwrite', '1 replaces an existing regular file; otherwise an existing file gives 409 file_exists', schema=S(enum=['1']))], 'binary'),
    ('Files', 'GET', '/files/download', 'files:read', 'Download a file', [DOMAIN, PATHQ], None),
    ('Files', 'GET', '/files/stats', 'files:read', 'Disk usage: largest folders and files', [DOMAIN, PATHQ], None),

    ('Databases', 'GET', '/databases', 'databases:read', 'List databases', [], None),
    ('Databases', 'POST', '/databases', 'databases:write', 'Create, delete, change password, manage extra users and outside access', [],
     obj({'action': S(enum=['create', 'password', 'delete', 'user_add', 'user_update', 'user_remove', 'hosts']), 'name': S(), 'user': S(), 'password': S(),
          'site': S(), 'charset': S(examples=['utf8mb4']), 'engine': S(enum=['mysql', 'postgresql']), 'privileges': S(enum=['all', 'readwrite', 'readonly']),
          'hosts': ARR(S(), description='IPs or networks allowed to connect from outside')}, ['action', 'name'])),
    ('Databases', 'GET', '/databases/engines', 'databases:read', 'Available database engines', [], None),
    ('Databases', 'GET', '/databases/import', 'databases:read', 'Import state', [q('name', 'Database name', True)], None),
    ('Databases', 'POST', '/databases/import', 'databases:write', 'Import a .sql or .sql.gz file from the site folder', [], obj({'name': S(), 'path': S()}, ['name', 'path'])),
    ('Databases', 'GET', '/databases/export', 'databases:read', 'Download the database as .sql.gz', [q('name', 'Database name', True)], None),
    ('Databases', 'POST', '/databases/phpmyadmin', 'databases:write', 'One-time phpMyAdmin sign-in link', [], obj({'name': S()}, ['name'])),
    ('Databases', 'POST', '/databases/adminer', 'databases:write', 'One-time Adminer (PostgreSQL) sign-in link', [], obj({'name': S()}, ['name'])),

    ('DNS', 'GET', '/dns', 'dns:read', 'DNS zones, server IP and BIND state', [], None),
    ('DNS', 'GET', '/dns/zone', 'dns:read', 'Records of a zone', [q('zone', 'Zone name', True)], None),
    ('DNS', 'POST', '/dns', 'dns:write', 'Create or delete a zone, save all its records. save replaces the whole list: start from zone.records of GET /dns/zone (NS records are required)', [],
     obj({'action': S(enum=['create', 'save', 'delete']), 'zone': S(), 'records': ARR(obj({'name': S(), 'type': S(enum=['A', 'AAAA', 'CNAME', 'MX', 'TXT', 'NS', 'SRV', 'CAA']), 'ttl': I(), 'value': S(), 'priority': I()})), 'ttl': I()}, ['action', 'zone'])),

    ('Mail', 'GET', '/mail', 'mail:read', 'Mail domains, mailboxes, connection details and DNS records', [], None),
    ('Mail', 'POST', '/mail', 'mail:write', 'Manage mail domains and mailboxes', [],
     obj({'action': S(enum=['domain_add', 'domain_update', 'domain_remove', 'box_add', 'box_update', 'box_remove']), 'domain': S(), 'site': S(), 'address': S(),
          'password': S(), 'targets': ARR(S()), 'catch_all': S(), 'disabled': B(), 'quota_mb': I(), 'aliases': ARR(S()), 'forwards': ARR(S()), 'ip': S()}, ['action'])),

    ('FTP', 'GET', '/accounts', 'ftp:read', 'FTP accounts', [], None),
    ('FTP', 'POST', '/accounts', 'ftp:write', 'Create, update, toggle or delete an FTP account', [],
     obj({'action': S(enum=['create', 'update', 'toggle', 'delete']), 'name': S(), 'site': S(), 'password': S(), 'home': S(), 'read_only': B(), 'enabled': B()}, ['action', 'name'])),

    ('Cron', 'GET', '/cron', 'cron:read', 'Scheduled tasks', [], None),
    ('Cron', 'POST', '/cron', 'cron:write', 'Create, update, toggle, run now or delete a task', [],
     obj({'action': S(enum=['create', 'update', 'toggle', 'run', 'delete']), 'id': S(), 'site': S(), 'schedule': S(examples=['*/5 * * * *']), 'command': S(), 'comment': S(), 'enabled': B()}, ['action'])),

    ('Backups', 'GET', '/backups', 'backups:read', 'Backups of a site: copies, the current job (state running/done/failed) and plan', [DOMAIN], None),
    ('Backups', 'POST', '/backups', 'backups:write', 'Back up now, restore, delete a copy or set the schedule', [],
     obj({'domain': S(), 'action': S(enum=['create', 'restore', 'delete', 'plan']), 'id': S(), 'files': B(), 'databases': B(),
          'plan': obj({'schedule': S(enum=['off', 'daily', 'weekly']), 'hour': I(minimum=0, maximum=23), 'weekday': I(minimum=0, maximum=6, description='0 = Sunday'), 'keep': I(), 'files': B(), 'databases': B()})}, ['domain', 'action'])),
    ('Backups', 'GET', '/backups/download', 'backups:read', 'Download a copy (.tar)', [DOMAIN, q('id', 'Copy id', True)], None),
    ('Backups', 'GET', '/backups/remote', 'backups:read', 'Google Drive / Dropbox state of a site and the copies in storage', [DOMAIN], None),
    ('Backups', 'POST', '/backups/remote', 'backups:write', 'Turn sending on/off, set copies kept, send now, fetch to the server, delete in storage', [],
     obj({'domain': S(), 'provider': S(enum=['gdrive', 'dropbox']), 'action': S(enum=['enable', 'disable', 'keep', 'sync', 'fetch', 'delete']), 'keep': I(minimum=1, maximum=60), 'file': S()}, ['domain', 'provider', 'action'])),
    ('Backups', 'GET', '/remote', 'backups:read', 'Connected backup storages and their space', [], None),
    ('Backups', 'POST', '/remote', 'backups:write', 'connect: get a sign-in link (open redirect in a browser); origin must be the panel address the request went to, otherwise 400 invalid_origin; without origin the code flow starts (pending.user_code). cancel, disconnect', [],
     obj({'provider': S(enum=['gdrive', 'dropbox']), 'action': S(enum=['connect', 'cancel', 'disconnect']), 'origin': S(description='https://<panel address>, the same the request goes to')}, ['provider', 'action'])),

    ('Git', 'GET', '/git', 'git:read', 'Repository, deploy key, webhook address and the last deploy log', [DOMAIN], None),
    ('Git', 'POST', '/git', 'git:write', 'Save the repository (save only sets it up), deploy (takes the files; follow last.state in GET /git), make a new webhook address or disconnect', [],
     obj({'domain': S(), 'action': S(enum=['save', 'deploy', 'token', 'disconnect']), 'repo': S(), 'branch': S(), 'command': S()}, ['domain', 'action'])),

    ('Accounts', 'GET', '/users', 'users:read', 'Panel accounts', [], None),
    ('Accounts', 'POST', '/users', 'users:write', 'Create an account', [], {'$ref': '#/components/schemas/AccountInput'}),
    ('Accounts', 'PATCH', '/users/{id}', 'users:write', 'Change an account (also block it with disabled: true)', [p('id', 'Account id', I())], {'$ref': '#/components/schemas/AccountInput'}),
    ('Accounts', 'DELETE', '/users/{id}', 'users:write', 'Delete an account (it must have no sites)', [p('id', 'Account id', I())], None),
    ('Accounts', 'POST', '/users/2fa-reset', 'users:write', 'Turn an account’s two-factor sign-in off', [], obj({'id': I()}, ['id'])),
    ('Accounts', 'GET', '/audit', 'users:read', 'Activity log (last 50 entries)', [], None),

    ('Limits', 'GET', '/limits', 'limits:read', 'Limits of an account (Pro and Premium)', [q('account_id', 'Account id (default: the token owner)', schema=I())], None),
    ('Limits', 'PUT', '/limits', 'limits:write', 'Set limits of an account; 0 = unlimited', [], {'$ref': '#/components/schemas/LimitsPut'}),
    ('Limits', 'GET', '/limits/usage', 'limits:read', 'Current usage of an account', [q('account_id', 'Account id', schema=I())], None),

    ('Branding', 'GET', '/settings/branding', 'branding:read', 'Panel name, color and logo', [], None),
    ('Branding', 'POST', '/settings/branding', 'branding:write', 'Set the panel name, color and logo', [],
     obj({'name': S(maxLength=40), 'color': S(examples=['#2563eb']), 'logo': S(description='data: URL, PNG/JPEG/WebP/GIF up to 1 MB'), 'remove_logo': B(), 'reset': B()})),

    ('Server', 'GET', '/license', 'system:read', 'License state and plan', [], None),
    ('Server', 'POST', '/license/activate', 'system:write', 'Activate a license', [], dict(type='object')),
    ('Server', 'GET', '/metrics', 'system:read', 'Live server load', [], None),
    ('Server', 'GET', '/stats', 'system:read', 'Server load history', [q('range', 'live, 1h, 24h, 7d or 30d')], None),
    ('Server', 'GET', '/system/services', 'system:read', 'System services', [], None),
    ('Server', 'POST', '/system/services', 'system:write', 'Start, stop, restart, enable or disable a service', [],
     obj({'unit': S(), 'action': S(enum=['start', 'stop', 'restart', 'enable', 'disable'])}, ['unit', 'action'])),
    ('Server', 'GET', '/applications', 'system:read', 'Server applications (PHP, Node.js, Python versions and tools)', [], None),
    ('Server', 'POST', '/applications', 'system:write', 'Install or remove an application', [], obj({'name': S(), 'action': S(enum=['install', 'remove'])}, ['name', 'action'])),
    ('Server', 'GET', '/firewall', 'system:read', 'Firewall state and rules', [], None),
    ('Server', 'POST', '/firewall', 'system:write', 'Apply rules, then confirm with the returned token within a minute (otherwise the old rules come back)', [],
     obj({'action': S(enum=['apply', 'confirm']), 'enabled': B(), 'rules': ARR(obj({'action': S(enum=['allow', 'deny']), 'proto': S(), 'ports': S(), 'source': S(), 'comment': S()})), 'token': S()}, ['action'])),
    ('Server', 'GET', '/security', 'system:read', 'Sign-in protection, blocked IPs and fail2ban', [], None),
    ('Server', 'POST', '/security/settings', 'system:write', 'Sign-in protection settings', [], dict(type='object')),
    ('Server', 'POST', '/security/unblock', 'system:write', 'Unblock an IP', [], obj({'ip': S(), 'jail': S()}, ['ip'])),
    ('Server', 'GET', '/quota', 'system:read', 'Disk quota state', [], None),
    ('Server', 'POST', '/quota', 'system:write', 'Turn disk quotas on', [], obj({'action': S(enum=['enable'])}, ['action'])),
    ('Server', 'GET', '/panel-tls', 'system:read', 'The panel’s IP certificate', [], None),
    ('Server', 'POST', '/panel-tls', 'system:write', 'issue: get/renew the IP certificate (400 service_not_paid without the paid Panel SSL service); self: back to the own certificate (fine when it already is)', [], obj({'action': S(enum=['issue', 'self'])}, ['action'])),
    ('Server', 'GET', '/panel-addresses', 'system:read', 'Panel domains', [], None),
    ('Server', 'POST', '/panel-addresses', 'system:write', 'Add a panel domain, change its certificate or remove it', [],
     obj({'action': S(enum=['add', 'cert', 'remove']), 'domain': S(), 'cert': S(enum=['letsencrypt', 'selfsigned', 'custom']), 'email': S(), 'cert_pem': S(), 'key_pem': S()}, ['action', 'domain'])),
]

err = lambda d: {'description': d, 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/Error'}}}}
common = {
    '400': err('invalid_input and other validation errors'),
    '401': err('unauthorized: no, wrong, expired or revoked token'),
    '402': err('license_required, or upgrade_required when the panel is not on the Premium plan'),
    '403': err('scope_denied (token scope) or forbidden (the account cannot manage this object)'),
    '503': err('hosting_unavailable: the server agent is busy, retry'),
}
responses_of = {
    ('GET', '/sites'): {'schema': ARR({'$ref': '#/components/schemas/Site'})},
    ('POST', '/sites'): {'schema': {'$ref': '#/components/schemas/Site'}},
    ('GET', '/users'): {'schema': ARR({'$ref': '#/components/schemas/Account'})},
    ('POST', '/users'): {'schema': {'$ref': '#/components/schemas/Account'}, 'status': '201'},
    ('PATCH', '/users/{id}'): {'schema': {'$ref': '#/components/schemas/Account'}},
    ('GET', '/limits'): {'schema': obj({'account_id': I(), 'limits': {'$ref': '#/components/schemas/Limits'}})},
    ('PUT', '/limits'): {'schema': obj({'account_id': I(), 'limits': {'$ref': '#/components/schemas/Limits'}})},
    ('GET', '/me'): {'schema': obj({'account': obj({'id': I(), 'name': S(), 'role': S(), 'permissions': {'$ref': '#/components/schemas/Permissions'}, 'main_admin': B()}),
                                    'scopes': ARR(S()), 'expires_at': I(), 'version': S()})},
}

paths = {}
for tag, method, path, scope, summary, params, body in routes:
    opid = (method.lower() + '_' + path.strip('/').replace('/', '_').replace('-', '_').replace('{', '').replace('}', '')) or method.lower()
    op = {'tags': [tag], 'operationId': opid, 'summary': summary}
    if scope:
        op['description'] = 'Scope: `%s`.' % scope
        op['security'] = [{'bearer': [scope]}]
        op['x-scope'] = scope
    else:
        op['description'] = 'Any valid token.'
        op['security'] = [{'bearer': []}]
    if params:
        op['parameters'] = params
    if body == 'binary':
        op['requestBody'] = {'required': True, 'content': {'application/octet-stream': {'schema': S(format='binary')}}}
    elif body is not None:
        op['requestBody'] = {'required': True, 'content': {'application/json': {'schema': body}}}
    ok = responses_of.get((method, path))
    status = (ok or {}).get('status', '200')
    content = {'application/json': {'schema': ok['schema']}} if ok else {'application/json': {'schema': dict(type='object')}}
    op['responses'] = {status: {'description': 'OK', 'content': content}, **common}
    paths.setdefault(path, {})[method.lower()] = op

scopes = {}
for tag, method, path, scope, *_ in routes:
    if scope:
        scopes[scope] = scope.split(':')[0] + (' — read' if scope.endswith(':read') else ' — change')

spec = {
    'openapi': '3.1.0',
    'info': {
        'title': 'LivePanel API v2',
        'version': '2',
        'summary': 'Everything the LivePanel web interface does, for programs.',
        'description': (
            'Works only on panels with the **Premium** plan; other plans answer `402 upgrade_required`.\n\n'
            'Authenticate with an API token from System → API tokens: `Authorization: Bearer lp_…`. '
            'A token acts as its account (role and permissions are enforced as in the browser) and only within its scopes.\n\n'
            'Request bodies are JSON (up to 16 KB) and unknown fields are rejected. Errors are `{"error": "code"}`. '
            'Paths of files are relative to the site user’s home folder (site files: `www/<domain>/…`).\n\n'
            'Human documentation: https://wiki.livepanel.uz/en/api-reference'),
        'license': {'name': 'Proprietary'},
    },
    'servers': [{'url': 'https://{host}:{port}/api/v2', 'variables': {'host': {'default': 'panel.example.uz'}, 'port': {'default': '6563'}}}],
    'security': [{'bearer': []}],
    'tags': [{'name': t} for t in dict.fromkeys(r[0] for r in routes)],
    'paths': paths,
    'components': {
        'securitySchemes': {'bearer': {'type': 'http', 'scheme': 'bearer', 'bearerFormat': 'lp_<token>', 'description': 'Scopes: ' + ', '.join(sorted(scopes))}},
        'schemas': schemas,
    },
}

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'openapi-v2.json')
with open(out, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(spec, f, ensure_ascii=False, indent=2)
    f.write('\n')
print(out, len(routes), 'operations')
