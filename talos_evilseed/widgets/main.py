# vim: set sts=4 sw=4 et :

from typing import TYPE_CHECKING
from typing import Callable
from typing import List
from typing import Optional
from typing import Sequence

import tkinter
from tkinter import Button
from tkinter import Frame

from talos_evilseed import schema
from talos_evilseed.widgets.puzzle_row import PuzzleRow

if TYPE_CHECKING:
    from talos_evilseed.app import Application


class MainWindow(Frame):
    __slots__ = (
        "_app",
        "_ctrl_frame",
        "_ctrl_new_button",
        "_ctrl_export_button",
        "_master",
        "_puzzle_row_groups",
        "_puzzle_row_frames",
    )

    def __init__(self, master: Optional[tkinter.Tk]=None, *, app: "Application") -> None:
        if master is None:
            self._master = tkinter.Tk()
        else:
            self._master = master
        super().__init__(self._master)
        self._app = app
        self._master.title("Talos EvilSeed - randomizer full control configurator")
        self.grid()
        self._build_puzzle_rows()
        self._build_control_pane()

    def _build_puzzle_rows(self) -> None:
        self._puzzle_row_groups: List[List[PuzzleRow]] = []
        self._puzzle_row_frames: List[Frame] = []

        MATCHERS: Sequence[Callable[[str], bool]] = [
            lambda name: (name.startswith("A") or name.startswith("B")) and name != "ADev",
            lambda name: (name.startswith("C") or name.startswith("N")) or  name == "ADev",
        ]

        for frame_idx, f_matcher in enumerate(MATCHERS):
            frame = Frame(self)
            frame.grid(row=0, padx=20, ipady=20, column=frame_idx, sticky=tkinter.N)
            self._puzzle_row_frames.append(frame)

            puzzle_rows = [
                PuzzleRow(
                    frame,
                    app=self._app,
                    level_name=level_name,
                    level=level,
                    row=i,
                )
                for i, (level_name, level,) in enumerate(sorted(list(schema.PUZZLES.items())))
                if f_matcher(level_name)
            ]

            self._puzzle_row_groups.append(puzzle_rows)

    def _build_control_pane(self) -> None:
        self._control_pane_frame = Frame(self)
        self._control_pane_frame.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky=tkinter.S+tkinter.W+tkinter.E,
        )

        self._ctrl_new_button = Button(
            self._control_pane_frame,
            text="New seed",
        )
        self._ctrl_new_button.grid(column=0, row=0, ipadx=20, ipady=10)

        self._ctrl_export_button = Button(
            self._control_pane_frame,
            text="Export",
        )
        self._ctrl_export_button.grid(column=2, row=0, ipadx=20, ipady=10)

