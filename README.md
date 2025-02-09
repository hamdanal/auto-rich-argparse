# auto-rich-argparse

Automatically use [rich-argparse](https://github.com/hamdanal/rich-argparse) help formatters with
argparse command line tools.

## Usage

Install auto-rich-argparse in the same environment as your command line tool.

_Try it out with your favorite tool using `uvx --with auto-rich-argparse <YOUR_FAVORITE_TOOL> --help`_

### Tools installed with `pipx`

If your tool is installed with `pipx`, use the `pipx inject` command to add auto-rich-argparse to
the tool's environment. For example, to use rich-argparse with `pre-commit`:

```bash
pipx inject pre-commit auto-rich-argparse
```

### Tools installed with `uv tool`

If your tool is installed with `uv tool`, use the `--with` flag to install auto-rich-argparse:

```bash
uv tool install pre-commit --with auto-rich-argparse
```

### Tools in the current project

You can also install auto-rich-argparse in you project's environment and it will be used by all
tools that use argparse in that environment:

```bash
python -m pip install auto-rich-argparse
```

## How it works

auto-rich-argparse works by monkey patching the `argparse.ArgumentParser` class to use a subclass of
`RichHelpFormatter` from rich-argparse instead of the default `argparse.HelpFormatter`. The formatter
tries to be compatible with the tool's formatter by setting the following options:

```python
FormatterClass.help_markup = False
FormatterClass.text_markup = False
FormatterClass.group_name_formatter = str
```

## Known limitations

This doesn't currently work if the tool passes a function as the `formatter_class` argument to
`ArgumentParser` instead of a class.
