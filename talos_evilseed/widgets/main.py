# vim: set sts=4 sw=4 et :

from typing import Callable
from typing import List
from typing import Optional
from typing import Sequence

import tkinter
from tkinter import Frame

from talos_evilseed import schema
from talos_evilseed.widgets.puzzle_row import PuzzleRow


class MainWindow(Frame):
    __slots__ = (
        "_puzzle_row_groups",
        "_puzzle_row_frames",
    )

    def __init__(self, master: Optional[Frame]=None) -> None:
        super().__init__(master)
        self.grid()
        self._build_puzzle_rows()

    def _build_puzzle_rows(self) -> None:
        self._puzzle_row_groups: List[List[PuzzleRow]] = []
        self._puzzle_row_frames: List[Frame] = []

        MATCHERS: Sequence[Callable[[str], bool]] = [
            lambda name: name.startswith("A") or name.startswith("B"),
            lambda name: name.startswith("C") or name.startswith("N"),
        ]

        for frame_idx, f_matcher in enumerate(MATCHERS):
            frame = Frame(self)
            frame.grid(row=0, column=frame_idx, sticky=tkinter.N)
            self._puzzle_row_frames.append(frame)

            puzzle_rows = [
                PuzzleRow(
                    frame,
                    level_name=level_name,
                    level=level,
                    row=i,
                )
                for i, (level_name, level,) in enumerate(sorted(list(schema.PUZZLES.items())))
                if level_name != "ADev" and f_matcher(level_name)
            ]

            self._puzzle_row_groups.append(puzzle_rows)

