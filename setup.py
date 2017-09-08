"""setup file of hexabot"""

from cx_Freeze import setup, Executable

setup(
    name = "hexabot",
    version = "0.1",
    description = "A minimal irc bot",
    executables = [Executable("/hexabot/my_irc_bot.py")],
)
