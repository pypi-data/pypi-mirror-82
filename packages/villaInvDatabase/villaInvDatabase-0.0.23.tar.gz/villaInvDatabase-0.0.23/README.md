# villa inventory database model
> serverless database to take control of products inventory


This file will become your README and also the index of your documentation.

## Install

`pip install villaInvDatabase`

## How to use

interact with a database hosted in dynamodb

```python
import os
os.environ['DATABASE_TABLE_NAME'] = 'inventory-database-dev-manual'
os.environ['REGION'] = 'ap-southeast-1'
os.environ['INVENTORY_BUCKET_NAME'] = 'inventory-bucket-dev-manual'
os.environ['INPUT_BUCKET_NAME'] = 'input-bucket-dev-manual'
os.environ['DAX_ENDPOINT'] = 'longtermcluster.vuu7lr.clustercfg.dax.apse1.cache.amazonaws.com:8111'
try:
  with open(os.path.expanduser('~/.testbot')) as f: os.environ['SLACK'] =  f.read()
except:
  print('cant load slack key')
# os.environ['DAX_ENDPOINT'] = None
REGION = 'ap-southeast-1'
INVENTORY_BUCKET_NAME = os.environ['INVENTORY_BUCKET_NAME']
INPUT_BUCKET_NAME = os.environ['INPUT_BUCKET_NAME']
```

```python
from villaInvDatabase.database import Database
```

```python
sampleInput = [ 
  { 'ib_prcode': '0000009', 'ib_brcode': '1000', 'ib_cf_qty': '50', 'new_ib_vs_stock_cv': '27' },
  { 'ib_prcode': '0000002', 'ib_brcode': '1000', 'ib_cf_qty': '35', 'new_ib_vs_stock_cv': '33' }
              ]
```

```python
%%time
#update
Database.dumpToS3(user=USER, pw = PW)
```

    CPU times: user 51.8 ms, sys: 4.02 ms, total: 55.9 ms
    Wall time: 1.09 s





    {'newDataSaved': False,
     'numberOfProducts': 0,
     'message': 'no changes to database'}



```python
%%time
Database.splitBranches(bucket = INVENTORY_BUCKET_NAME, user=USER, pw=PW)
```

    CPU times: user 20.7 s, sys: 350 ms, total: 21.1 s
    Wall time: 26.9 s





    {'success': 32, 'failure': 0, 'errorMessage': []}



# Save using Standard

```python
Database.updateLambdaInput(sampleInput)
```




    {'success': 0, 'failure': 0, 'failureMessage': []}



## Save using s3

```python
inputKeyName = 'input-data-name'
saveResult = S3.save(key=inputKeyName, 
                     objectToSave = sampleInput , 
                     bucket = INPUT_BUCKET_NAME,
                     user = USER,
                     pw = PW,
                     accelerate = False)
logging.info('test input data saved to s3')
updateResult = Database.updateS3Input(
  inputBucketName=INPUT_BUCKET_NAME, key= inputKeyName,
  user = USER, pw = PW)

logging.info(f's3 save result is {saveResult} update result is {updateResult}')
```

## Query test

#### Product Query

```python
sampleQueryInput = {
    'ib_prcode': '0000002'
}  
```

```python
Database.singleProductQuery(sampleQueryInput)
```




    {"ib_prcode": "0000002", "1000": {"ib_cf_qty": 35, "new_ib_bs_stock_cv": 33, "lastUpdate": 1600567810.529301}, "1001": {"ib_cf_qty": 32, "new_ib_bs_stock_cv": 30, "lastUpdate": 1600567810.529316}, "1002": {"ib_cf_qty": 34, "new_ib_bs_stock_cv": 30, "lastUpdate": 1600567810.529318}, "lastUpdate": 1600567810.529318}



### Branch Query

```python
from s3bz.s3bz import Requests
branchURL = Database.branchQuery('1000', bucket = INVENTORY_BUCKET_NAME, user=USER, pw=PW)
print(branchURL)
next(iter(Requests.getContentFromUrl(branchURL).items()))
```

    https://inventory-bucket-dev-manual.s3-accelerate.amazonaws.com/1000?AWSAccessKeyId=ASIAVX4Z5TKDYYBW7BXS&Signature=uII2DK3tBfbV46GDRzyxS302%2BXI%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEM7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDmFwLXNvdXRoZWFzdC0xIkcwRQIhAJol46W3ZC%2BXzaPGrfILHCIPxAcnIEnVEylaHYWcsezrAiA3kXDWsY4GS5lgjuEW4dxI3Es84lhAsoCOf%2BkTKFN%2Ffir1AggYEAAaDDM5NDkyMjkyNDY3OSIMAOqC2RZsrFMrb9QbKtICTHSeTcUdEYlGf2FCF7nMC6AbH%2FywuPnY4XrAAHVnm0zDUasRG%2FTfa8d4zhKOdGlXYhfxsiTJyLl3m3tx7J6Nvq4TpdeeoJXcr5GHYi5OUI9cwmcbBs4xqvMXmPLMi%2FiDihKcLFJZEzgMtMhYLI8cyvsvd6If4NdfDVaXivf6PRG7WcI6eBif9d7Buh2HQIh4ZNYp26%2FP2tjc58B5WC%2FneiksTa02VIrUkDzyoC5yEZRaXlPCcyYN6S3mvtRpVwYU2%2F%2BPyxd8YHbDP26OUvj23GLFWBsfyqKOoCdTVIMqwYIIwX3HM7BHR8sKuqRSalZkGlnAWgqBzXG7gPrsau00UZw1ayyBKzkGGqDeiWKbuuE7lBT%2F1O%2F3OmmfTlKxXQbNK8ejQh4f7f2gas%2FN1p%2FcNnWtIcC86Ok%2BCmX5rVJ5SIzwoKFWVlQzanjSCazQURNWOdowmvyr%2FAU6wwEdmHcWYYFV%2BnUT11gnHcp76z2jzByhG3jaQB4xMevo4VmGNzeCB6qBzqUQRNA%2FzOIypslWr7XvVR7Wo26WQK8NW%2FtJGVX870hCii%2BDvavgouwUIeiqs6KMBKRZ04Ntac5t0Uq0fX54LMI9Tbg6kL7eBrEgZ7h%2Ff1KbXkjwBZR7oZ88Fiz%2BncAmaFlS7DKGTHAWdqu4F5bhlM8ygqlLygtp8Os850jZdhpVdDuCF5cSP7l6szic%2BBM%2F6j6kemJqEXrz%2Fak%3D&Expires=1602946927





    ('0000009',
     {'ib_cf_qty': 50, 'new_ib_bs_stock_cv': 27, 'lastUpdate': 1602338504.869655})



### AllQuery

```python
from s3bz.s3bz import Requests
branchURL = Database.allQuery(bucket = INVENTORY_BUCKET_NAME, user=USER, pw=PW)
print(branchURL)
next(iter(Requests.getContentFromUrl(branchURL).items()))
```

    https://inventory-bucket-dev-manual.s3-accelerate.amazonaws.com/allData?AWSAccessKeyId=ASIAVX4Z5TKDYYBW7BXS&Signature=9Q9ES6%2B%2BYmR3Xq%2BND5rzLtLtVyg%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEM7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDmFwLXNvdXRoZWFzdC0xIkcwRQIhAJol46W3ZC%2BXzaPGrfILHCIPxAcnIEnVEylaHYWcsezrAiA3kXDWsY4GS5lgjuEW4dxI3Es84lhAsoCOf%2BkTKFN%2Ffir1AggYEAAaDDM5NDkyMjkyNDY3OSIMAOqC2RZsrFMrb9QbKtICTHSeTcUdEYlGf2FCF7nMC6AbH%2FywuPnY4XrAAHVnm0zDUasRG%2FTfa8d4zhKOdGlXYhfxsiTJyLl3m3tx7J6Nvq4TpdeeoJXcr5GHYi5OUI9cwmcbBs4xqvMXmPLMi%2FiDihKcLFJZEzgMtMhYLI8cyvsvd6If4NdfDVaXivf6PRG7WcI6eBif9d7Buh2HQIh4ZNYp26%2FP2tjc58B5WC%2FneiksTa02VIrUkDzyoC5yEZRaXlPCcyYN6S3mvtRpVwYU2%2F%2BPyxd8YHbDP26OUvj23GLFWBsfyqKOoCdTVIMqwYIIwX3HM7BHR8sKuqRSalZkGlnAWgqBzXG7gPrsau00UZw1ayyBKzkGGqDeiWKbuuE7lBT%2F1O%2F3OmmfTlKxXQbNK8ejQh4f7f2gas%2FN1p%2FcNnWtIcC86Ok%2BCmX5rVJ5SIzwoKFWVlQzanjSCazQURNWOdowmvyr%2FAU6wwEdmHcWYYFV%2BnUT11gnHcp76z2jzByhG3jaQB4xMevo4VmGNzeCB6qBzqUQRNA%2FzOIypslWr7XvVR7Wo26WQK8NW%2FtJGVX870hCii%2BDvavgouwUIeiqs6KMBKRZ04Ntac5t0Uq0fX54LMI9Tbg6kL7eBrEgZ7h%2Ff1KbXkjwBZR7oZ88Fiz%2BncAmaFlS7DKGTHAWdqu4F5bhlM8ygqlLygtp8Os850jZdhpVdDuCF5cSP7l6szic%2BBM%2F6j6kemJqEXrz%2Fak%3D&Expires=1602946928





    ('0000009',
     {'ib_prcode': '0000009',
      '1000': {'ib_cf_qty': 50,
       'new_ib_bs_stock_cv': 27,
       'lastUpdate': 1602338504.869655},
      'lastUpdate': 1602338504.869655})



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


