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

import re
import os
import sys
from docopt import docopt
from pivvy import __VERSION__
from subprocess import call


def main():
    """
    Usage: pivvy [-h|--help] [-v|--version]
                   <command> [<args>...]

    Commands:
        startproject <name>  Creates a new project

    Options:
        -h --help     Show this message
        -v --version  Show version information
    """
    version = "pivvy " + ".".join(str(n) for n in __VERSION__)
    args = docopt(main.__doc__, version=version, options_first=True)
    command = args["<command>"]
    command_args = args["<args>"]
    # argv = [sys.argv[0], command] + command_args
    if command == "startproject":
        if len(command_args) == 0:
            sys.exit("No project name specified")
        package_dir = os.path.dirname(os.path.abspath(__file__))
        name = command_args[0]
        snake_case_name = re.sub(
            r"[^a-z0-9_]", "", name.lower().replace("-", "_"), flags=re.UNICODE)
        doc_name = snake_case_name.replace("_", "")
        sys.exit(
            call(["pivvy-startproject.sh", package_dir, name, snake_case_name, doc_name]))
    else:
        sys.exit("%r is not a pivvy command. 'See pivvy --help'." % command)
