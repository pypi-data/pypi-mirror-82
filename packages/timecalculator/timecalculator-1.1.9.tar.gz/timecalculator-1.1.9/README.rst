1.1.9
*****
| Timecalculator is a my first library, so do not await to much.
| It is used to calculate with time.

:code:`sys_time()`
"""""""""""""""""""""""""""""""""
| This function returns the system time.
| An example output would be:
| :code:`Wed, 14 Oct 2020 17:01:06`

:code:`mintosec(minutes)`
""""""""""""""""""""""""""""""""
| This function returns the the minutes * 60, because 1 * 60 are 60 seconds.

:code:`htosec(hours)`
""""""""""""""""""""""""""""""""
| This function works just like the last, but hours * 60 * **60**

:code:`daytosec(days)`
""""""""""""""""""""""""""""""""
| This function is the same again, just days * 24 * 60 * 60

:code:`work_week()`
"""""""""""""""""""""""""""""""""
| This function is something else, it always returns :code:`432.000`
| because it isn´t like one day - one day - one day, it´s work week - weekend - work week

:code:`weekend()`
"""""""""""""""""""""""""""""""""
| same problem, but this time returns :code:`172.800`

:code:`weektosec(weeks)`
"""""""""""""""""""""""""""""""""
| This time the old one again, 7 * 24 * 60 * 60

:code:`monthtosec(months)`
"""""""""""""""""""""""""""""""""""
| 30 * 7 * 24 * 60 * 60

:code:`yeartosek(years)`
"""""""""""""""""""""""""""""""""""
| 365 * 7 * 24 * 60 * 60