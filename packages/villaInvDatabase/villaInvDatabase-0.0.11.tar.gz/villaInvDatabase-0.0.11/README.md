# Project name here
> Summary description here.


This file will become your README and also the index of your documentation.

## Install

`pip install villaInvDatabase`

## How to use

interact with a database hosted in dynamodb

```python
from villaInvDatabase.database import Database
```

    error, missing environment variables 
    'DATABASE_TABLE_NAME'
    dax endpoint missing
    missing environment variable 'INVENTORY_BUCKET_NAME' in Database s3 NB
    missing environment variable 'INVENTORY_BUCKET_NAME' in query NB
    missing environment variable 'INPUT_BUCKET_NAME' in update NB


```python
sampleinput = [ 
  { 'ib_prcode': '0000009', 'ib_brcode': '1000', 'ib_cf_qty': '50', 'new_ib_vs_stock_cv': '27' },
  { 'ib_prcode': '0000002', 'ib_brcode': '1000', 'ib_cf_qty': '35', 'new_ib_vs_stock_cv': '33' }
              ]
```

```python
costPer100ms = 0.0000016667
costPerMs = costPer100ms / 100
timePerCallS = 40
timePerCallMs = timePerCallS * 1000
costPerCall = costPerMs * timePerCallMs
callsPerDay = 60 * 24 /10
costPerDay = callsPerDay * costPerCall
```

```python
costPerDay * 33
```




    3.16806336


