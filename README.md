# csv_file_data_collector
This is small CLI app for parse, collect, filter and aggregate data from file

## Instruction:

use next command to work with application:

```
$ python main.py --file example.csv --where="brand=xiaomi" --aggregate="rating=min"
```

example.csv - you can change it to your own csv file
--where and --aggregate is optional

### for --where use column names:
"brand=samsung", "rating<5", "price=1999", etc.

### for --aggregate use column names and next values:
min, max, avg.

"rating=avg", "price=min", etc.

## Examples of running:

<div align="center">
    <img src="/screenshots/ex-1.png" width="400px"</img> 
</div>

<div align="center">
    <img src="/screenshots/ex-2.png" width="400px"</img> 
</div>

<div align="center">
    <img src="/screenshots/ex-3.png" width="400px"</img> 
</div>

<div align="center">
    <img src="/screenshots/ex-4.png" width="400px"</img> 
</div>

