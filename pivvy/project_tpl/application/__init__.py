#
# This is an example plugin, change it as you see fit :)
#

import pivvy


def on_load():
    pivvy.vars.g___SNAKE_CASE_PLACEHOLDER___message = "Hello, world!"
    pivvy.define_command("HelloWorld", hello_world)
    pivvy.define_command("HelloName", hello_name)


def hello_world():
    print(pivvy.vars.g___SNAKE_CASE_PLACEHOLDER___message)


def hello_name(name):
    pivvy.current.buffer.append("Hello, {0}!".format(name))
