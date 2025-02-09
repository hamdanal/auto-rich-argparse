from __future__ import annotations

import functools
from argparse import ArgumentParser, HelpFormatter

import rich_argparse
from rich_argparse import RichHelpFormatter


def make_rich_formatter_class(formatter_class: type[HelpFormatter]) -> type[HelpFormatter]:
    for cls in formatter_class.mro():
        if cls.__module__ == "argparse":
            try:
                # Find the corresponding rich formatter class
                rich_formatter_class: type[RichHelpFormatter] = getattr(
                    rich_argparse, cls.__name__.replace("HelpFormatter", "RichHelpFormatter")
                )
                if formatter_class.__module__ == "argparse":
                    # If the formatter class itself is from argparse, replace it
                    formatter_class = type(
                        rich_formatter_class.__name__, (rich_formatter_class,), {}
                    )
                else:
                    # Otherwise, inject the rich formatter class into its bases
                    # This is necessary because we can't inherit from classes compiled with mypyc
                    formatter_class.__bases__ = (rich_formatter_class,) + formatter_class.__bases__

                # Disable rich-argparse's options that might have undesirable effects
                setattr(formatter_class, "help_markup", False)
                setattr(formatter_class, "text_markup", False)
                setattr(formatter_class, "group_name_formatter", str)

                return formatter_class
            except Exception:
                break
    return formatter_class


def patch_argument_parser_formatter_class() -> None:
    original_init = ArgumentParser.__init__

    @functools.wraps(original_init, updated=())
    def __init__(*args, **kwargs):
        formatter_class = kwargs.get("formatter_class", HelpFormatter)
        if (
            isinstance(formatter_class, type)
            and issubclass(formatter_class, HelpFormatter)
            and not issubclass(formatter_class, RichHelpFormatter)
        ):
            kwargs["formatter_class"] = make_rich_formatter_class(formatter_class)
        return original_init(*args, **kwargs)

    setattr(ArgumentParser, "__init__", __init__)
