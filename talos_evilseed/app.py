# vim: set sts=4 sw=4 et :

import argparse
from typing import Optional
from typing import Sequence
import tkinter

from talos_evilseed import schema
from talos_evilseed.widgets.main import MainWindow
from talos_evilseed.widgets.puzzle_cell import PuzzleCell


class Application:
    """Main application state."""
    __slots__ = (
        "_active_puzzle",
        "_arg_parser",
        "_arg_map",
        "_main_window",
    )

    def __init__(self, *, appname: str, args: Sequence[str]) -> None:
        self._active_puzzle: Optional[PuzzleCell] = None
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

    def on_puzzle_lmb_click(self, puzzle: PuzzleCell) -> None:
        if self._active_puzzle is not None:
            # We have an active cell, does it match?
            if puzzle is self._active_puzzle:
                # Yes - deactivate the cell and DO NOT SWAP.
                self._active_puzzle.set_active(False)
                self._active_puzzle = None
            else:
                # No - swap! and then deactivate.
                s0 = puzzle.get_sigil()
                s1 = self._active_puzzle.get_sigil()
                puzzle.set_sigil(s1)
                self._active_puzzle.set_sigil(s0)
                self._active_puzzle.set_active(False)
                self._active_puzzle = None
        else:
            # Activate this cell.
            self._active_puzzle = puzzle
            self._active_puzzle.set_active(True)

    def _build_main_window(self) -> None:
        self._main_window: MainWindow = MainWindow(app=self)

    def _run_main_window(self) -> None:
        self._main_window.mainloop()


def main(*, appname: str, args: Sequence[str]) -> None:
    """Application entry point."""
    Application(
        appname=appname,
        args=args,
    ).run()

