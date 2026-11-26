# Server commands

On the server, over SSH as root, the `livepanel` command is available. The list of commands:

```bash
livepanel --help
```

| Command | What it does |
|---|---|
| `livepanel ip-access on` | Turn on access to the panel by IP — port 6563 is open to everyone |
| `livepanel ip-access off` | The panel opens only through its panel addresses — port 6563 is closed to the outside |
| `livepanel ip-access status` | Show whether the panel opens by IP |
| `livepanel passwd NAME` | Set a new password for a panel account |
| `livepanel remove` | Remove LivePanel and everything installed through it |
| `livepanel --help` | The list of commands |

For an unknown command the terminal says so and points to `livepanel --help` for the list.

## Access by IP

```bash
livepanel ip-access off
```

Port 6563 is closed to the outside and the panel opens only through its address, e.g. `https://panel.example.uz`. Access from the server itself (`127.0.0.1`) stays open. The command works only with a [panel address](panel-access.md) that has a Let’s Encrypt or your own certificate — without one, access by IP stays on.

If the panel address stops working (DNS, an expired domain and so on), turn access by IP back on:

```bash
livepanel ip-access on
```

The same setting is in the panel: **Settings → Panel addresses → Access by IP**.

## Panel password

```bash
livepanel passwd liveadmin
```

The command asks for the new password. Leave it empty and the panel makes one and prints it.

## Removing the panel

```bash
livepanel remove
```

This removes the sites and their files, databases, mail, SSL certificates, backups, the web, database, FTP and mail servers, and the programs from **Applications**. The command asks for confirmation three times: “Yes”, a one-time code shown on the screen, and one more “Yes”.

> This cannot be undone. Back up the data you need first — [Backups](backups.md).
