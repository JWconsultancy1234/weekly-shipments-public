# weekly-shipments
Made-up shipments export for the AI journey, Builder step 11

## changes.py

Prints the three biggest changes in pallets between the last week in a
shipments export and the week before.

### The rule

1. **Weeks are ISO weeks.** Each row's `date` is put in its ISO week
   (Monday to Sunday, named like `2026-W42`). Around New Year an ISO week can
   belong to the other calendar year: 2025-12-29 falls in `2026-W01`.
2. **Last week** is the latest ISO week that has a row in the file.
   **The week before** is the ISO week directly before it, whether or not
   the file has rows for it. A week with no rows counts as 0 pallets.
3. **Every client and every route is counted, each on its own.** Pallets are
   added up per client and per route for both weeks. Clients and routes are
   then ranked together in one list. A client or route with no shipments in
   one of the two weeks counts as 0 pallets that week.
4. **Change = last week − the week before.** The list is sorted by the size
   of the change, so a drop of 23 ranks the same as a rise of 23. When two
   changes are the same size, they are sorted by name so the output never
   changes between runs. The top three are printed.
5. Every row is counted, whatever its `status`.

Routes collect more shipments than single clients, so they often fill the
top three. In the sample, the biggest client change is Beta Foods (+22), in
4th place, so it is not printed.

### How to run

You need Python 3.8 or newer. Nothing else needs installing.

```
python3 changes.py                         # reads shipments-export-sample.csv
python3 changes.py path/to/export.csv      # reads another export
```

The file needs at least the columns `date` (YYYY-MM-DD), `client`, `route`
and `pallets` (a whole number).

### Output on the sample file

```
Pallet changes, 2026-W41 -> 2026-W42 (clients and routes)
1. route  BE-BE    25 ->   60  +35
2. route  NL-BE    77 ->  101  +24
3. route  BE-FR    71 ->   48  -23
```
