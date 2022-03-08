#MaxThreadsPerHotkey, 2
Toggle = 0

F10::
Toggle = !Toggle
If Toggle
   Click, Down
else
   Click, Up
return