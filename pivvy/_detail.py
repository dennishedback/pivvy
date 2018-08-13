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

try:
    # setup.py goes bananas if we don't catch this during installation
    import vim
    _vim, vim = vim, None
except ImportError:
    pass
except NameError:
    pass


class _Command:
    def __init__(self, name):
        name = name.split("_")
        if (name[-1] == "bang"):
            name = "_".join(name[:-1]) + "!"
        else:
            name = "_".join(name)
        self._name = name

    def __call__(self, *args, **kwargs):
        args = " ".join(str(x) for x in args)
        if len(kwargs):
            args += " " + " ".join("{0}={1}".format(k, str(v))
                                   for k, v in kwargs.items())
        _vim.command("{0} {1}".format(self._name, args))


class _Commands:
    def __getattr__(self, name):
        return _Command(name)


class _Vars:
    def _process_name(self, name):
        name = name.split("_")
        if name[0] in ('g', 's', 'w', 't', 'b', 'l', 'a', 'v'):
            return "{0}:{1}".format(name[0], "_".join(name[1:]))
        else:
            return "_".join(name)

    def __setattr__(self, name, value):
        name = self._process_name(name)
        command = "let {0}='{1}'".format(name, value)
        _vim.command(command)

    def __getattr__(self, name):
        name = self._process_name(name)
        return _vim.eval(name)
