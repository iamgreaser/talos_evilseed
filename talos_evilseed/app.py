# vim: set sts=4 sw=4 et :

import argparse
from typing import Optional
from typing import Sequence
import tkinter

from talos_evilseed import schema
from talos_evilseed.seed_state import SeedState
from talos_evilseed.widgets.main import MainWindow
from talos_evilseed.widgets.portal_cell import PortalCell
from talos_evilseed.widgets.puzzle_cell import PuzzleCell


class Application:
    """Main application state."""
    __slots__ = (
        "_active_portal",
        "_active_puzzle",
        "_arg_parser",
        "_arg_map",
        "_main_window",
        "_seed_state",
    )

    def __init__(self, *, appname: str, args: Sequence[str]) -> None:
        self._active_portal: Optional[PortalCell] = None
        self._active_puzzle: Optional[PuzzleCell] = None
        self._build_arg_parser()
        self._parse_args(args=list(args))

    def _build_arg_parser(self) -> None:
        self._arg_parser: argparse.ArgumentParser = argparse.ArgumentParser()

    def _parse_args(self, *, args: Sequence[str]) -> None:
        self._arg_map: argparse.Namespace = self._arg_parser.parse_args(args)

    def run(self) -> None:
        """Run the application."""
        self._seed_state = SeedState()
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

                # Save the new swap
                with self._seed_state.atomic():
                    self._seed_state.set_sigil_for_puzzle(
                        puzzle.get_level_name(),
                        puzzle.get_name(),
                        puzzle.get_sigil(),
                    )
                    self._seed_state.set_sigil_for_puzzle(
                        self._active_puzzle.get_level_name(),
                        self._active_puzzle.get_name(),
                        self._active_puzzle.get_sigil(),
                    )

                self._active_puzzle.set_active(False)
                self._active_puzzle = None
        else:
            # Activate this cell.
            self._active_puzzle = puzzle
            self._active_puzzle.set_active(True)

    def on_portal_lmb_click(self, portal: PortalCell) -> None:
        if self._active_portal is not None:
            # We have an active cell, does it match?
            if portal is self._active_portal:
                # Yes - deactivate the cell and DO NOT SWAP.
                self._active_portal.set_active(False)
                self._active_portal = None
            else:
                # No - swap! and then deactivate.
                s0 = portal.get_portal()
                s1 = self._active_portal.get_portal()
                portal.set_portal(s1)
                self._active_portal.set_portal(s0)

                # Save the new swap
                with self._seed_state.atomic():
                    self._seed_state.set_portal_for_level(
                        portal.get_level_name(),
                        portal.get_portal(),
                    )
                    self._seed_state.set_portal_for_level(
                        self._active_portal.get_level_name(),
                        self._active_portal.get_portal(),
                    )

                self._active_portal.set_active(False)
                self._active_portal = None
        else:
            # Activate this cell.
            self._active_portal = portal
            self._active_portal.set_active(True)

    def get_sigil_for_puzzle(self, level_name: str, puzzle_name: str) -> str:
        return self._seed_state.get_sigil_for_puzzle(level_name, puzzle_name)

    def get_portal_for_level(self, level_name: str) -> str:
        return self._seed_state.get_portal_for_level(level_name)

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

