# vim: set sts=4 sw=4 et :

import argparse
from typing import Sequence
import tkinter

from talos_evilseed import schema
from talos_evilseed.widgets.main import MainWindow


class Application:
    """Main application state."""
    __slots__ = (
        "_arg_parser",
        "_arg_map",

        "_main_window",
    )

    def __init__(self, *, appname: str, args: Sequence[str]) -> None:
        self._build_arg_parser()
        self._parse_args(args=list(args))

    def _build_arg_parser(self) -> None:
        self._arg_parser: argparse.ArgumentParser = argparse.ArgumentParser()

    def _parse_args(self, *, args: Sequence[str]) -> None:
        self._arg_map: argparse.Namespace = self._arg_parser.parse_args(args)

    def run(self) -> None:
        """Run the application."""
        self._build_main_window()
        self._run_main_window()

    def _build_main_window(self) -> None:
        self._main_window: MainWindow = MainWindow()

    def _run_main_window(self) -> None:
        self._main_window.mainloop()


def main(*, appname: str, args: Sequence[str]) -> None:
    """Application entry point."""
    Application(
        appname=appname,
        args=args,
    ).run()

