# hpctool

## A list of primary components

### dorunrun
A function that subprocesses in a consistent way. Also contains an `enum` named `ExitCode` that names all the Linux exit codes.

### fileutils
A collection of functions to enhance the use of Python file objects.

### linuxutils
A collection of functions that provide interfaces to common (and uncommon) interactions with the Linux OS.

### sloppytree
A tree for Python. Also includes a SloppyDict and functions to convert built-in Python types to the new, `slop.py` types.

### sqlitedb
A class that represents a database connection to SQLite3. Supports locking.

### urdecorators
Really, there is only one, `@trap`. It creates a nicely formatted dump of all local and global symbols at the time an exception is raised.

### urlogger
A simple wrapper around the functions in Python's built-in `logging`.


