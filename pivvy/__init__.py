# Copyright (c) 2018, Dennis Hedback
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#     1. Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#
#     2. Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in
#        the documentation and/or other materials provided with the
#        distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

__VERSION__ = (0, 1, 1)

command = None

import sys
try:
    # setup.py goes bananas if we don't catch this during installation
    import vim
    import pivvy._detail
    from vim import *
    _vim, vim = vim, None
    command = pivvy._detail._Commands()
    vars = pivvy._detail._Vars()
except ImportError:
    pass
except NameError:
    pass

PREFIX = ""
_callbacks = []


def _reload():
    import importlib
    importlib.reload(pivvy._detail)


def confirm(text, choices=["Yes", "No"], default=1):
    print(text)
    choices_str = "[{0}]".format(
        ", ".join("'{0}. {1}'".format(i + 1, x) for i, x in enumerate(choices)))
    choice = int(_vim.eval("inputlist({0})".format(choices_str)))
    print(" ")
    print(" ")
    return choice


def _run_callb(i, args):
    if len(args) < len(_callbacks[i][1]):
        print("Too few arguments for command", file=sys.stderr)
        return
    d = {}
    for j, item in enumerate(_callbacks[i][1].items()):
        k, v = item
        d[k] = args[j]
    _callbacks[i][0](**d)


def define_command(name, callb):
    from inspect import signature
    params = signature(callb).parameters
    nargs = len(params)
    _callbacks.append((callb, params))
    i = len(_callbacks) - 1
    nargs = "*" if nargs > 1 else str(nargs)
    command.command_bang(
        "-nargs={0}".format(nargs),
        name,
        "call",
        "s:{0}_pivvy_run_callb({1}, <f-args>)".format(PREFIX, i)
    )
