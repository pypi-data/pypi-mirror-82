# multi-tldr

Yet another python client for [tldr-pages/tldr](https://github.com/tldr-pages/tldr). View tldr pages in multi repo, multi platform, any language at the same time.

Forked from [lord63/tldr.py](https://github.com/lord63/tldr.py), whose original idea is very good. Modified a large proportion of code.

## Intro

Instead of the long man pages, tldr will give you several simple yet powerful examples:

![tar-tldr-page](screenshots/screenshot1.png)

The command examples are not good? Don't worry, you can set up your own `tldr`! They are just [simplified markdown files](https://github.com/tldr-pages/tldr/blob/master/contributing-guides/style-guide.md) and you can create your own pages. You can contribute to [tldr-pages/tldr](https://github.com/tldr-pages/tldr), or keep them private.

One more thing, `tldr` is just a simple version for the man page, it's **NOT** an alternative. Sometimes, you should read the man pages patiently.

## Features

- Use local file, fast without network delay. tldr pages are managed and updated by `git`.
- Support custom output color.

### Differences with `lord63/tldr.py`

- No need to use `tldr find some_command` or create an alias of `tldr find`, just type `tldr some_command` ([related issue](https://github.com/lord63/tldr.py/issues/47))
- No need to rebuild `index.json` index file.
- Support display multi repo and multi platform at the same time. You can create your own private tldr pages repo.
- Support display tlgr pages in any languages, by specify repo dir path items in `repo_directory_list` to the `pages/` level.
- New feature: compact output, not output empty lines.
- Advanced parser: render nested `` ` `` inline code, `{{` and `}}` arguments ([related issue](https://github.com/lord63/tldr.py/issues/25)).
- Config file format `YAML` --> `JSON`, because I hate `YAML`.
- Drop support for Python 2.
- Simplify (just delete) tests code

## Requirements

- Python >= `3.6`, with `pip` installed

### Recommend

- Git: if you do not have `git`, you can still download `.zip` file from [tldr-pages/tldr](https://github.com/tldr-pages/tldr), extract it, and add it when run `tldr --init`, most things still work, but `tldr --update` will NOT work.

### For Windows users

A better terminal is recommended, which must support [ANSI escape sequences](https://en.wikipedia.org/wiki/ANSI_escape_code), and make sure `git` command is available. Try (combine) these: [Cmder](https://cmder.net/), [Cygwin](https://www.cygwin.com/), [Windows Terminal](https://github.com/microsoft/terminal), [WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10), [Git for Windows](https://gitforwindows.org/), [scoop](https://github.com/lukesampson/scoop), [Chocolatey](https://chocolatey.org/), etc.

Test your environment with Python 3:

```python
#!/usr/bin/env python3
# encoding: utf-8

import os
import sys
import shutil

print(f'sys.stdout.isatty() -> {sys.stdout.isatty()}')
print(f'env TERM = {os.environ.get("TERM")!r}')
print('Test ANSI escape sequences: \x1b[31mred \x1b[1mbold\x1b[0m')
print(f'git command is: {shutil.which("git")!r}')
```

If you are using Windows 10, you can import this to the Windows Registry to enable color output of `cmd` and `PowerShell`:

```registry
Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\Console]
"VirtualTerminalLevel"=dword:00000001
```

If output is not colored, try set `color_output` in the config file to `always`.

## Install

Use `pip` to install:

```bash
python3 -m pip install -U multi-tldr
```

## Initialize manually

### Clone [tldr-pages/tldr](https://github.com/tldr-pages/tldr)

First, clone the [tldr-pages/tldr](https://github.com/tldr-pages/tldr) to somewhere (e.g. `~/code/tldr`). We will use it when we look for a command usage.

```bash
git clone --depth=1 https://github.com/tldr-pages/tldr.git
```

### Create config file

Then, run this command to interactively generate configuration file:

```bash
tldr --init
```

Your configuration file should look like this:

```json
{
    "repo_directory_list": [
        "/home/user/code/tldr/pages/",
        "/home/user/code/tldr-private/pages.zh"
    ],
    "color_output": "auto",
    "colors": {
        "description": "bright_yellow",
        "usage": "green",
        "command": "white",
        "param": "cyan"
    },
    "platform_list": [
        "common",
        "osx",
        "linux"
    ],
    "compact_output": false
}
```

The `colors` option is for the output when you look for a command, you can custom it by yourself. (Note that the color should be in `'black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white', 'bright_black', 'bright_red', 'bright_green', 'bright_yellow', 'bright_blue', 'bright_magenta', 'bright_cyan', 'bright_white'`)

The default location for the config file is `~/.config/multi-tldr/.tldr.config.json`. You can use `TLDR_CONFIG_DIR` and `XDG_CONFIG_HOME` environment variable to point it to another path. If `TLDR_CONFIG_DIR` is `/a/b/c`, config file is `/a/b/c/.tldr.config.json`. If `XDG_CONFIG_HOME` is `/a/b/c`, config file is `/a/b/c/multi-tldr/.tldr.config.json`.

## Usage

You can run `tldr --help` to get the help message.

### Look for a command usage

By default, only pages in `platform_list` are output:

```bash
tldr tar
```

You can specify a platform using `-p` argument:

```bash
tldr -p osx airport
```

### Check for updates

`git pull` will be run in all dir paths of `repo_directory_list`, so that we can get the latest tldr pages.

```console
$ tldr --update
Check for updates in '/home/user/code/tldr' ...
Already up to date.
Check for updates in '/home/user/code/tldr-private' ...
Already up to date.
```

### List tldr page files path

List all:

```bash
tldr --list
```

Specify a platform and/or a command:

```bash
tldr --list tar
tldr --list -p linux
tldr --list -p common du
```

## FAQ

**Q: I want to add some custom command usages to a command, how to do it?**

**Q: I want to add some custom command pages, how?**

A: You can contribute to [tldr-pages/tldr](https://github.com/tldr-pages/tldr), or create your own Git repo, or just create a private directory, and add it to `repo_directory_list`.

**Q: I want a short command like `tldr COMMAND`, not `tldr find COMMAND`.**

A: This problem not exists any more.

**Q: Do I need to rebuild any index after `git pull` or create new `.md` files?**

A: You don't any more. Local file is fast enough, and I added a cache decorator.

**Q: I want fuzzy find command usage.**

A: `tldr --list | grep KEYWORD`

**Q: I don't like the default color theme, how to change it?**

A: Edit the tldr configuration file, modify the color until you're happy with it.

**Q: I faided to update the tldr pages, why?**

A: Actually, This program just tries to pull the latest tldr pages for you, no magic behinds it. So the reason why you faided to update is that this program failed to pull the latest upstream, check the failing output and you may know the reason, e.g. you make some changes and haven't commit them yet. You can pull the pages by hand so you can have a better control on it.

**Q: Why use the git repo instead of the assets packaged by the official?**

A: In fact, you can use the offical assets if you want, download the assets and extract it somewhere, but this program don't support update it using `tldr --update`.

Use a `git` repo, you can:

- do the version control, yeah, use `git`.
- better for customization, just edit the pages and add new pages, they belongs to you. You can even maintain your own 'tldr'. If use the official assets, you'll always get the latest pages.

## Contributing

- It sucks? Why not help me improve it? Let me know the bad things.
- Want a new feature? Feel free to file an issue for a feature request.
- Find a bug? Open an issue please, or it's better if you can send me a pull request.

Contributions are always welcome at any time!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for the full license text.
