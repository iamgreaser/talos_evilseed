#!/usr/bin/env python3 --
# vim: set sts=4 sw=4 et :

#
# Do a version check and on failure report here.
#

import sys

try:
    import tkinter
except ImportError:
    try:
        import Tkinter as tkinter # type: ignore
    except ImportError:
        raise Exception("This version of Python has no Tk support!")

if sys.version_info < (3, 6,):
    try:
        from tkMessageBox import showerror
    except ImportError:
        try:
            from tkinter.messagebox import showerror
        except ImportError:
            raise Exception("This version of Python has no tkMessageBox support!")

    # Don't show the root window
    root = tkinter.Tk()
    root.withdraw()

    if sys.version_info < (3, 0,):
        showerror(
            "Talos evilseed",
            "This program requires Python 3.6 or higher.\n"
            + "\n"
            + "Stop being a Python 2 pleb.\nGet Python 3.",
        )
    else:
        showerror(
            "Talos evilseed",
            "This program requires Python 3.6 or higher."
        )

    raise Exception("Update Python dammit")

#
# And now we return to your usual imports.
#

import talos_evilseed.app


if __name__ == "__main__":
    talos_evilseed.app.main(
        appname=sys.argv[0],
        args=list(sys.argv[1:]),
    )

