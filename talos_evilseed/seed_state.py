# vim: set sts=4 sw=4 et :

from contextlib import contextmanager
import json
from typing import Any
from typing import Dict
from typing import Generator
from typing import IO

from talos_evilseed import schema


class SeedState:
    """The state for the given seed."""
    __slots__ = (
        "_fname",
        "_has_active_atomic",
        "_puzzle_to_sigil_map",
    )

    def __init__(self, *, fname: str="default.evilseed") -> None:
        self._fname = fname
        self._has_active_atomic = False
        self._puzzle_to_sigil_map: Dict[str, Dict[str, str]] = {}

        # If the file exists, load it. Otherwise, reset the state.
        try:
            self._load_from_fname(fname=self._fname)
        except FileNotFoundError:
            print(f"Load failed, doing a clean slate")
            self._reset_to_clean_state()

    @contextmanager
    def atomic(self) -> Generator[None, None, None]:
        had_active_atomic = self._has_active_atomic
        self._has_active_atomic = True
        try:
            yield
        finally:
            self._has_active_atomic = had_active_atomic
            self._sync()

    def get_sigil_for_puzzle(self, level_name: str, puzzle_name: str) -> str:
        assert isinstance(level_name, str)
        assert isinstance(puzzle_name, str)
        sigil_name = self._puzzle_to_sigil_map[level_name][puzzle_name]
        assert isinstance(sigil_name, str)
        return sigil_name

    def set_sigil_for_puzzle(self, level_name: str, puzzle_name: str, sigil_name: str) -> None:
        assert isinstance(level_name, str)
        assert isinstance(puzzle_name, str)
        assert isinstance(sigil_name, str)
        self._puzzle_to_sigil_map[level_name][puzzle_name] = sigil_name
        self._sync()

    def _reset_to_clean_state(self) -> None:
        self._reset_puzzle_to_sigil_map()

    def _reset_puzzle_to_sigil_map(self) -> None:
        for level_name, level in schema.PUZZLES.items():
            self._puzzle_to_sigil_map[level_name] = {}
            for puzzle_name, puzzle in level.items():
                sigil = puzzle["sigil"]
                self._puzzle_to_sigil_map[level_name][puzzle_name] = sigil

    def _load_from_fname(self, *, fname: str) -> None:
        print(f"Loading {fname!r}")
        with open(fname, "r") as fp:
            self._load_from_fp(fp=fp)

    def _load_from_fp(self, *, fp: IO[str]) -> None:
        data: Dict[str, Any] = json.loads(fp.read())

        try:
            self._puzzle_to_sigil_map = data["puzzle_to_sigil_map"]
        except LookupError:
            self._reset_puzzle_to_sigil_map()

    def _sync(self) -> None:
        if not self._has_active_atomic:
            self._save_to_fname(fname=self._fname)

    def _save_to_fname(self, *, fname: str) -> None:
        print(f"Saving {fname!r}")
        with open(fname, "w") as fp:
            self._save_to_fp(fp=fp)

    def _save_to_fp(self, *, fp: IO[str]) -> None:
        data: Dict[str, Any] = {
            "puzzle_to_sigil_map": self._puzzle_to_sigil_map,
        }
        fp.write(json.dumps(data))
