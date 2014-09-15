PgbarLoader: cmdline exec
argv[0]	: exec name
argv[1]	: title (default: Loader)
argv[2]	: event name (default: Loader.Event)

in the following situations, the behaviors are undefined:
1. more than 1 loader has the same event name

note:
wndclass name: PGBARLOADER

caution:

please call ctypes.windll.kernel32.CloseHandle(hEvt) in python after done.
unless all handles to the event are closed, the event won't be released, which could lead to an undefined situation (1).

use '\x1f' to replace all spaces in the title (BUT NOT IN THE EVENT_NAME)
title = title.replace(" ", "\x1f")

_xp vs2013