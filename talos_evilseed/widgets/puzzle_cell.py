# vim: set sts=4 sw=4 et :

from typing import TYPE_CHECKING
from typing import Dict
from typing import Optional

import tkinter
from tkinter import Frame
from tkinter import Label

from talos_evilseed.widgets.sigil import SigilWidget

if TYPE_CHECKING:
    from talos_evilseed.app import Application


class PuzzleCell:
    __slots__ = (
        "_active",
        "_app",
        "_column",
        "_frame",
        "_level_name",
        "_master",
        "_puzzle_label",
        "_puzzle_name",
        "_puzzle_sigil",
        "_puzzle_sigil_widget",
        "_row",
    )

    def __init__(self, master: Frame, *, app: "Application", level_name: str, puzzle_name: str, puzzle: Dict[str, str], row: int, column: int) -> None:
        #super().__init__(master)
        self._master = master
        self._app = app
        self._active = False
        self._row = row
        self._column = column
        self._level_name = level_name
        self._puzzle_name = puzzle_name
        self._puzzle_sigil = app.get_sigil_for_puzzle(level_name, puzzle_name)
        self._build_frame()

    def on_lmb_click(self, ev: object) -> None:
        #print("Click!", self, ev)
        self._app.on_puzzle_lmb_click(puzzle=self)

    def _build_frame(self) -> None:
        self._frame: Frame = Frame(
            self._master,
            relief=tkinter.RAISED,
            borderwidth=2,
        )
        self._frame.grid(
            row=self._row,
            column=self._column,
            sticky=tkinter.W+tkinter.E+tkinter.N+tkinter.S,
        )
        self._frame.bind("<ButtonRelease-1>", self.on_lmb_click)

        self._puzzle_label: Label = Label(
            self._frame,
            text=self._puzzle_name,
        )
        self._puzzle_label.grid(sticky=tkinter.N+tkinter.W+tkinter.E)
        self._puzzle_label.bind("<ButtonRelease-1>", self.on_lmb_click)

        self._puzzle_sigil_widget: SigilWidget = SigilWidget(
            self._frame,
            sigil_name=self._puzzle_sigil,
        )
        # FIXME: KLUDGE - violates encapsulation
        self._puzzle_sigil_widget._sigil_frame.bind("<ButtonRelease-1>", self.on_lmb_click)
        self._puzzle_sigil_widget._sigil_icon.bind("<ButtonRelease-1>", self.on_lmb_click)

    def set_sigil(self, sigil_name: str) -> None:
        self._puzzle_sigil = sigil_name
        self._puzzle_sigil_widget.set_sigil(sigil_name)

    def get_sigil(self) -> str:
        return self._puzzle_sigil

    def get_name(self) -> str:
        return self._puzzle_name

    def get_level_name(self) -> str:
        return self._level_name

    def set_active(self, active: bool) -> None:
        self._active = active
        color: str
        color = ("#AAAAFF" if self._active else self._master.cget("bg")) # type: ignore
        self._frame["bg"] = color
        self._puzzle_label["bg"] = color
        # FIXME: KLUDGE - violates encapsulation
        self._puzzle_sigil_widget._sigil_frame["bg"] = color
        self._puzzle_sigil_widget._sigil_icon["bg"] = color

