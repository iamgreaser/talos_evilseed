# vim: set sts=4 sw=4 et :

from contextlib import contextmanager
import json
import random
from typing import Any
from typing import Dict
from typing import Generator
from typing import List
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
            self.export()
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

    def export(self) -> None:
        self._export_to_fname(fname=f"{self._fname}.lua")

    def _export_to_fname(self, *, fname: str) -> None:
        print(f"Exporting {fname!r}")
        code6_1 = random.randint(4,9)
        code6_2 = random.randint(4,9)
        code6_3 = random.randint(4,9)

        data: Dict[str, Any] = {
            "Randomizer_ExtraSeed": random.randint(0,(1<<31)-1),
            "Randomizer_Generated": 1,
            "Randomizer_Mode": "Default",
            "Randomizer_Mobius": None,
            "Randomizer_Moody": None,
            "Randomizer_Scavenger": None,
            "Randomizer_Seed": -42069,
            "PaintItemSeed": random.randint(0,(1<<31)-1),
            "Code_Floor4": random.randint(0,999),
            "Code_Floor5": random.randint(0,999),
            "Code_Floor61": code6_1,
            "Code_Floor62": code6_2,
            "Code_Floor63": code6_3,
            "Code_Floor6": code6_1*100 + code6_2*10 + code6_3*1,
            "Code_Floor6DigitSeen1": 1,
            "Code_Floor6DigitSeen2": 1,
            "Code_Floor6DigitSeen3": 1,
        }

        # Random sigils
        for idx, name in enumerate(schema.PORTAL_ORDER):
            for level_name, level in schema.PUZZLES.items():
                for puzzle_name, puzzle in level.items():
                    data[puzzle["talosProgress"]] = self._puzzle_to_sigil_map[level_name][puzzle_name]

        # Random portals
        # TODO: add support for this
        for idx, name in enumerate(schema.PORTAL_ORDER):
            data[name] = idx+1

        # TODO: Randomizer_Hints
        # TODO: Randomizer_LastColour
        # TODO: Randomizer_LastShape
        # TODO: Randomizer_ScavengerEnding

        with open(fname, "w") as luafp:
            for base_key in ["prj_strCustomOccasion", "ser_strBanList",]:
                luafp.write(f"{base_key}=[===[")
                luafp.write("Randomizer_AutoStart={")
                sl: List[str] = []
                for key, rawvalue in data.items():
                    if isinstance(rawvalue, str):
                        escvalue: str = rawvalue.replace("\\", "\\\\").replace("'", "\\'")
                        svalue: str = f"'{escvalue}'"
                    elif isinstance(rawvalue, float):
                        svalue = f"{rawvalue:f}"
                    elif isinstance(rawvalue, int):
                        svalue = f"{rawvalue:d}"
                    elif rawvalue is True:
                        svalue = f"1"
                    elif rawvalue is False:
                        svalue = f"0"
                    elif rawvalue is None:
                        svalue = f"0"
                    else:
                        raise Exception(f"TODO: make Lua type for {rawvalue!r} ({type(rawvalue)!r})")

                    sl.append(f"'{key}'={svalue}")
                s: str = ",".join(sl)
                luafp.write(s)
                luafp.write("}")
                luafp.write("]===]\n")

