# LivePanel documentation

The knowledge base of [LivePanel](https://livepanel.uz), the hosting control panel. The articles are published at **[wiki.livepanel.uz](https://wiki.livepanel.uz)**.

| Language | Folder |
|---|---|
| O‘zbekcha | [`uz/`](uz/) |
| Русский | [`ru/`](ru/) |
| English | [`en/`](en/) |

## Layout

- `{lang}/{slug}.md` — one article; the first `# heading` is its title.
- `toc.json` — the sections and the order of the articles, with their titles in every language.
- `api/openapi-v2.json` — the OpenAPI 3.1 description of API v2, built by `api/build_openapi.py` (keep its route list in step with the panel’s `internal/app/api_v2.go`). Served at https://wiki.livepanel.uz/openapi.json.
- `images/` — the pictures (taken from the English interface), shared by all languages. An article links them as `../images/name.png`.

## Contributing

Corrections are welcome: open a pull request against `main`. Keep the same article in all three languages in step, and use the names the panel shows on its buttons and menus.
