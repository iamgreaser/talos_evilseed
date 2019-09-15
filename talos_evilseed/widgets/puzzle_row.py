# vim: set sts=4 sw=4 et :

from typing import TYPE_CHECKING
from typing import Dict
from typing import List
from typing import Optional

import tkinter
from tkinter import Frame
from tkinter import Label

from talos_evilseed.widgets.puzzle_cell import PuzzleCell

if TYPE_CHECKING:
    from talos_evilseed.app import Application


class PuzzleRow:
    __slots__ = (
        "_app",
        "_level_label",
        "_level_name",
        "_portal_label",
        "_master",
        "_puzzle_cells",
        "_puzzles",
        "_row",
    )

    def __init__(self, master: Frame, *, app: "Application", level_name: str, level: Dict[str, Dict[str, str]], row: int) -> None:
        self._master: Frame = master
        self._app = app
        self._level_name = level_name
        self._puzzles = level
        self._row = row
        self._level_label: Label = Label(master, text=self._level_name[:2].replace("S","*"))
        self._level_label.grid(
            sticky=tkinter.W+tkinter.E+tkinter.N+tkinter.S,
            column=0,
            row=self._row,
        )
        self._portal_label: Label = Label(
            master,
            text=self._level_name[:2].replace("S","*"),
            relief=tkinter.RAISED,
            borderwidth=2,
        )
        self._portal_label.grid(
            sticky=tkinter.W+tkinter.E+tkinter.N+tkinter.S,
            column=1,
            row=self._row,
            padx=20,
            ipadx=10,
        )
        self._build_puzzle_cells()

    def _build_puzzle_cells(self) -> None:
        self._puzzle_cells: List[PuzzleCell] = [
            PuzzleCell(
                self._master,
                app=self._app,
                puzzle_name=puzzle_name,
                puzzle=puzzle,
                row=self._row,
                column=i+2,
            )
            for i, (puzzle_name, puzzle,) in enumerate(sorted(list(self._puzzles.items())))
        ]


