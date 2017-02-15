#
# License: BSD
#   https://raw.githubusercontent.com/stonier/py_trees_suite/devel/LICENSE
#

##############################################################################
# Description
##############################################################################

"""
.. module:: console
   :synopsis: Tools for colourising the console.

Simple colour definitions and syntax highlighting for the console.

----

**Colour Definitions**

The current list of colour definitions include:

 * ``Regular``: black, red, green, yellow, blue, magenta, cyan, white,
 * ``Bold``: bold, bold_black, bold_red, bold_green, bold_yellow, bold_blue, bold_magenta, bold_cyan, bold_white

These colour definitions can be used in the following way:

.. code-block:: python

   import py_trees.console as console
   print(console.cyan + "    Name" + console.reset + ": " + console.yellow + "Dude" + console.reset)

"""

##############################################################################
# Imports
##############################################################################

import fcntl
import os
import sys
import termios


# python2 is raw-input, python3 is input
try:
    input = raw_input
except NameError:
    pass

##############################################################################
# Keypress
##############################################################################


def read_single_keypress():
    """Waits for a single keypress on stdin.

    This is a silly function to call if you need to do it a lot because it has
    to store stdin's current setup, setup stdin for reading single keystrokes
    then read the single keystroke then revert stdin back after reading the
    keystroke.

    :returns: the character of the key that was pressed and raises KeyboardInterrupt
    if CTRL-C was pressed (keycode 0x03)
    """
    fd = sys.stdin.fileno()
    # save old state
    flags_save = fcntl.fcntl(fd, fcntl.F_GETFL)
    attrs_save = termios.tcgetattr(fd)
    # make raw - the way to do this comes from the termios(3) man page.
    attrs = list(attrs_save)  # copy the stored version to update
    # iflag
    attrs[0] &= ~(termios.IGNBRK | termios.BRKINT | termios.PARMRK |
                  termios.ISTRIP | termios.INLCR | termios. IGNCR |
                  termios.ICRNL | termios.IXON)
    # oflag
    attrs[1] &= ~termios.OPOST
    # cflag
    attrs[2] &= ~(termios.CSIZE | termios. PARENB)
    attrs[2] |= termios.CS8
    # lflag
    attrs[3] &= ~(termios.ECHONL | termios.ECHO | termios.ICANON |
                  termios.ISIG | termios.IEXTEN)
    termios.tcsetattr(fd, termios.TCSANOW, attrs)
    # turn off non-blocking
    fcntl.fcntl(fd, fcntl.F_SETFL, flags_save & ~os.O_NONBLOCK)
    # read a single keystroke
    ret = sys.stdin.read(1)  # returns a single character
    if ord(ret) == 3:  # CTRL-C
        termios.tcsetattr(fd, termios.TCSAFLUSH, attrs_save)
        fcntl.fcntl(fd, fcntl.F_SETFL, flags_save)
        raise KeyboardInterrupt("Ctrl-c")
    # restore old state
    termios.tcsetattr(fd, termios.TCSAFLUSH, attrs_save)
    fcntl.fcntl(fd, fcntl.F_SETFL, flags_save)
    return ret

##############################################################################
# Methods
##############################################################################


def console_has_colours(stream):
    """
    Detects if the specified stream has colourising capability.

    :param stream: stream to check (typically sys.stdout)
    """
    if not hasattr(stream, "isatty"):
        return False
    if not stream.isatty():
        return False  # auto color only on TTYs
    try:
        import curses
        curses.setupterm()
        return curses.tigetnum("colors") > 2
    except:
        # guess false in case of error
        return False

has_colours = console_has_colours(sys.stdout)
if has_colours:
    # reset = "\x1b[0;0m"
    reset = "\x1b[0m"
    bold = "\x1b[%sm" % '1'
    black, red, green, yellow, blue, magenta, cyan, white = ["\x1b[%sm" % str(i) for i in range(30, 38)]
    bold_black, bold_red, bold_green, bold_yellow, bold_blue, bold_magenta, bold_cyan, bold_white = ["\x1b[%sm" % ('1;' + str(i)) for i in range(30, 38)]
else:
    reset = ""
    bold = ""
    black, red, green, yellow, blue, magenta, cyan, white = ["" for i in range(30, 38)]
    bold_black, bold_red, bold_green, bold_yellow, bold_blue, bold_magenta, bold_cyan, bold_white = ["" for i in range(30, 38)]

colours = [bold,
           black, red, green, yellow, blue, magenta, cyan, white,
           bold_black, bold_red, bold_green, bold_yellow, bold_blue, bold_magenta, bold_cyan, bold_white
           ]


def pretty_print(msg, colour=white):
    if has_colours:
        seq = colour + msg + reset
        sys.stdout.write(seq)
    else:
        sys.stdout.write(msg)


def pretty_println(msg, colour=white):
    if has_colours:
        seq = colour + msg + reset
        sys.stdout.write(seq)
        sys.stdout.write("\n")
    else:
        sys.stdout.write(msg)


##############################################################################
# Console
##############################################################################


def debug(msg):
    print(green + msg + reset)


def warning(msg):
    print(yellow + msg + reset)


def info(msg):
    print(msg)


def error(msg):
    print(red + msg + reset)


def logdebug(message):
    '''
    Prefixes '[debug]' and colours the message green.

    :param message str: message to log.
    '''
    print(green + "[DEBUG] " + message + reset)


def loginfo(message):
    '''
    Prefixes '[ INFO]' to the message.

    :param message str: message to log.
    '''
    print("[ INFO] " + message)


def logwarn(message):
    '''
    Prefixes '[ WARN]' and colours the message yellow.

    :param message str: message to log.
    '''
    print(yellow + "[ WARN] " + message + reset)


def logerror(message):
    '''
    Prefixes '[ERROR]' and colours the message red.

    :param message str: message to log.
    '''
    print(red + "[ERROR] " + message + reset)


def logfatal(message):
    '''
    Prefixes '[FATAL]' and colours the message bold red.

    :param message str: message to log.
    '''
    print(bold_red + "[FATAL] " + message + reset)


##############################################################################
# Main
##############################################################################

if __name__ == '__main__':
    for colour in colours:
        pretty_print("dude\n", colour)
    logdebug("loginfo message")
    logwarn("logwarn message")
    logerror("logerror message")
    logfatal("logfatal message")
    pretty_print("red\n", red)
    print("some normal text")
    print(cyan + "    Name" + reset + ": " + yellow + "Dude" + reset)
