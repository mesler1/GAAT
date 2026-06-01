#!/usr/bin/env python3
"""
gaat.py — GAAT entry point.

GAAT is a refactoring of CheetahClaws into a capable, lean AI coding CLI.
This module is the primary entry point; cheetahclaws.py is the legacy runner
and will be removed once the refactor is complete.
"""


def main():
    from cheetahclaws import main as _cc_main
    _cc_main()


if __name__ == "__main__":
    main()
