# vim: set sts=4 sw=4 et :

from typing import TYPE_CHECKING
from typing import Dict
from typing import Optional

import tkinter
from tkinter import Frame
from tkinter import Label

if TYPE_CHECKING:
    from talos_evilseed.app import Application


class PortalCell:
    __slots__ = (
        "_active",
        "_app",
        "_column",
        "_level_name",
        "_master",
        "_portal_label",
        "_portal_name",
        "_row",
    )

    def __init__(self, master: Frame, *, app: "Application", level_name: str, row: int, column: int) -> None:
        #super().__init__(master)
        self._master = master
        self._app = app
        self._active = False
        self._column = column
        self._row = row
        self._level_name = level_name
        self._portal_name = app.get_portal_for_level(level_name)
        self._portal_label: Label = Label(
            self._master,
            text=self._portal_name[:2],
            relief=tkinter.RAISED,
            borderwidth=2,
        )
        self._portal_label.grid(
            sticky=tkinter.W+tkinter.E+tkinter.N+tkinter.S,
            column=self._column,
            row=self._row,
            padx=20,
            ipadx=10,
        )
        self._portal_label.bind("<ButtonRelease-1>", self.on_lmb_click)

    def on_lmb_click(self, ev: object) -> None:
        #print("Click!", self, ev)
        self._app.on_portal_lmb_click(portal=self)

    def set_portal(self, portal_name: str) -> None:
        self._portal_label["text"] = portal_name[:2]
        self._portal_name = portal_name

    def get_level_name(self) -> str:
        return self._level_name

    def get_portal(self) -> str:
        return self._portal_name

    def set_active(self, active: bool) -> None:
        self._active = active
        color: str
        color = ("#AAAAFF" if self._active else self._master.cget("bg")) # type: ignore
        self._portal_label["bg"] = color

