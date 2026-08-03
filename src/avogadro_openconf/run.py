#  This source file is part of the Avogadro project
#  This source code is released under the 3-Clause BSD License, (see "LICENSE").
#  https://github.com/ghutchis/avogadro-openconf/

"""Dispatch feature identifier to the appropriate handler."""

import json
import sys


def run(args):
    avo_input = json.load(sys.stdin)
    output = None

    from .conformers import PRESETS

    if args.feature in PRESETS:
        from .conformers import generate
        output = generate(avo_input, args.feature)

    if output is not None:
        print(json.dumps(output))
