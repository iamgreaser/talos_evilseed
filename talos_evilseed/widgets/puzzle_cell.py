# vim: set sts=4 sw=4 et :

from typing import Dict
from typing import Optional

import tkinter
from tkinter import Frame
from tkinter import Label


class PuzzleCell:
    __slots__ = (
        "_column",
        "_frame",
        "_master",
        "_row",
        "_puzzle_label",
        "_puzzle_name",
        "_puzzle_sigil",
        "_puzzle_sigil_widget",
    )

    def __init__(self, master: Frame, *, puzzle_name: str, puzzle: Dict[str, str], row: int, column: int) -> None:
        #super().__init__(master)
        self._master = master
        self._row = row
        self._column = column
        self._puzzle_name = puzzle_name
        self._puzzle_sigil = puzzle["sigil"]
        self._build_frame()

    def _build_frame(self) -> None:
        self._frame: Frame = Frame(
            self._master,
            relief=tkinter.RAISED,
            borderwidth=2,
        )
        self._frame.grid(
            row=self._row,
            column=self._column,
            sticky=tkinter.W+tkinter.E,
        )
        self._puzzle_label: Label = Label(self._frame, text=self._puzzle_name)
        self._puzzle_label.grid(sticky=tkinter.N+tkinter.W+tkinter.E)
        self._puzzle_sigil_widget: Label = Label(self._frame, text=self._puzzle_sigil)
        self._puzzle_sigil_widget.grid(sticky=tkinter.S+tkinter.W+tkinter.E)



