from os import PathLike
from typing import TypeAlias

# Adapted from https://stackoverflow.com/questions/53418046/how-do-i-type-hint-a-filename-in-a-function
Filename: TypeAlias = str | bytes | PathLike
