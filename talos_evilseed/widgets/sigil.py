# vim: set sts=4 sw=4 et :

import math
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

import tkinter
from tkinter import Canvas
from tkinter import Frame


COLOR_MAP: Dict[str, str] = {
    # Some of these look kinda bad, but colourblind people do exist
    "D": "#00FF00",
    "M": "#FFFF99",
    "N": "#CC0000",
    "E": "#AAAAAA",
    "*": "#FFFF99",
}

SHAPE_MAP: Dict[str, List[Tuple[int, int]]] = {
    "I": [(0,1), (1,1), (2,1), (3,1)],
    "J": [(0,0), (0,1), (1,1), (2,1)],
    "L": [(2,0), (0,1), (1,1), (2,1)],
    "O": [(0,0), (1,0), (0,1), (1,1)],
    "S": [(1,0), (2,0), (0,1), (1,1)],
    "T": [(1,0), (0,1), (1,1), (2,1)],
    "Z": [(0,0), (1,0), (1,1), (2,1)],
}

class SigilWidget:
    __slots__ = (
        "_master",
        "_shapes",
        "_sigil_frame",
        "_sigil_icon",
        "_sigil_name",
    )

    def __init__(self, master: Frame, *, sigil_name: str) -> None:
        self._master: Frame = master
        self._sigil_name = sigil_name

        self._sigil_frame: Frame = Frame(
            self._master,
        )

        self._sigil_icon: Canvas = Canvas(
            self._sigil_frame,
            width=54,
            height=22,
        )
        self._shapes: List[Any] = []
        self._draw_shape(
            color_name=sigil_name[0],
            shape_name=sigil_name[1],
            bg=True,
        )
        self._draw_shape(
            color_name=sigil_name[0],
            shape_name=sigil_name[1],
            bg=False,
        )
        self._shapes.append(self._sigil_icon.create_text( # type: ignore
            54,
            0,
            anchor=tkinter.NE,
            text=self._sigil_name[:2],
        ))

        # FIXME this layout sucks
        #self._sigil_frame.grid(sticky=tkinter.S+tkinter.W+tkinter.E)
        #self._sigil_icon.grid(sticky=tkinter.W+tkinter.E)
        self._sigil_frame.grid(sticky=tkinter.S+tkinter.W)
        self._sigil_icon.grid(sticky=tkinter.W)

    def _draw_shape(self, *, color_name: str, shape_name: str, bg: bool) -> None:
        color = ("#000000" if bg else COLOR_MAP[color_name])

        if shape_name == "*":
            if not bg:
                POINT_COUNT = 5
                ORADIUS = 11
                IRADIUS = 4
                points: List[int] = []
                for point_idx in range(POINT_COUNT):
                    a0 = point_idx*math.pi*2/POINT_COUNT
                    a1 = (point_idx+0.5)*math.pi*2/POINT_COUNT
                    px0 = round(8+6+ORADIUS*+math.sin(a0))
                    py0 = round(8+3+ORADIUS*-math.cos(a0))
                    px1 = round(8+6+IRADIUS*+math.sin(a1))
                    py1 = round(8+3+IRADIUS*-math.cos(a1))
                    points += [px0, py0, px1, py1]

                self._shapes.append(self._sigil_icon.create_polygon( # type: ignore
                    *points,
                    fill=color,
                    outline="#000000",
                ))
            pass # TODO!
        else:
            radius = (5 if bg else 4)
            for cx, cy, in SHAPE_MAP[shape_name]:
                x = cx*8+6
                y = cy*8+6
                self._shapes.append(self._sigil_icon.create_rectangle( # type: ignore
                    x-radius, y-radius,
                    x+radius, y+radius,
                    fill=color,
                    outline="",
                ))

