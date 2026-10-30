# weekly-shipments
Made-up shipments export for the AI journey, Builder step 11

## changes.py

Prints the three biggest percent changes in pallets between the last week in
a shipments export and the week before.

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
4. **Change = (last week − the week before) ÷ the week before, as a percent.**
   The list is sorted by the size of the change, so a drop of 23% ranks the
   same as a rise of 23%. A client or route going from 0 pallets to any number
   has no percentage: it is printed as `new` and ranks above all percentages.
   When two changes are the same size, they are sorted by name so the output
   never changes between runs. The top three are printed.
5. Every row is counted, whatever its `status`.

Percentages favour small numbers, so a small client can outrank a busy route
on few pallets. In the sample, Epsilon Garden (+11 pallets, +122.2%) ranks
above BE-FR (−23 pallets, −32.4%), which does not make the top three.

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
Pallet changes by percent, 2026-W41 -> 2026-W42 (clients and routes)
1. route  BE-BE                       25 ->   60  +140.0%
2. client Epsilon Garden (example)     9 ->   20  +122.2%
3. client Delta Home (example)        28 ->    9  -67.9%
```
