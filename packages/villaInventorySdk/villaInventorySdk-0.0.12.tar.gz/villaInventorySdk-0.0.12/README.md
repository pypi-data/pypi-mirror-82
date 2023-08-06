# villaInventorySdk



## Install

`pip install villaInventorySdk`

## How to use

Uploading a large amount of data

## sample input

```python
sampleInput = [ 
  {'ib_brcode': '1023', 'ib_cf_qty': '835', 'ib_prcode': '84621', 'new_ib_vs_stock_cv': '839'},
  {'ib_brcode': '1022', 'ib_cf_qty': '24', 'ib_prcode': '12424', 'new_ib_vs_stock_cv': '21'}
]
```

## Upload data

## init sdk

```python
%%time
sdk = InventorySdk(user=USER, pw=PW, branchName = branch)
```

    CPU times: user 28.5 ms, sys: 12 ms, total: 40.4 ms
    Wall time: 1.05 s


## Update inventory 

```python
%%time
sdk.updateWithS3( sampleInput )
```

    CPU times: user 48.5 ms, sys: 7.17 ms, total: 55.7 ms
    Wall time: 173 ms





    {'body': 'true', 'statusCode': 200, 'header': {}}



## Query single product

```python
%%time
sdk.querySingleProduct('0000002')
```

    CPU times: user 14.4 ms, sys: 0 ns, total: 14.4 ms
    Wall time: 2.05 s





    {'body': '{"ib_prcode":"0000002","1000":{"ib_cf_qty":35,"new_ib_bs_stock_cv":33,"lastUpdate":1600567810.529301},"1001":{"ib_cf_qty":32,"new_ib_bs_stock_cv":30,"lastUpdate":1600567810.529316},"1002":{"ib_cf_qty":34,"new_ib_bs_stock_cv":30,"lastUpdate":1600567810.529318},"lastUpdate":1600567810.529318}',
     'statusCode': 200,
     'header': {}}



## Query Branch

```python
%%time
result = sdk.queryBranch('1000')
#showing the first 2 result
list(iter(result.items()))[:2]
```

    CPU times: user 271 ms, sys: 12.6 ms, total: 283 ms
    Wall time: 507 ms





    [('0000009',
      {'ib_cf_qty': 50,
       'new_ib_bs_stock_cv': 27,
       'lastUpdate': 1602338504.869655}),
     ('0000002',
      {'ib_cf_qty': 35,
       'new_ib_bs_stock_cv': 33,
       'lastUpdate': 1600567810.529301})]



## Query All

```python
%%time
result = sdk.queryAll()
list(iter(result.items()))[:2]
```

    CPU times: user 1.63 s, sys: 48.7 ms, total: 1.67 s
    Wall time: 1.96 s





    [('0000009',
      {'ib_prcode': '0000009',
       '1000': {'ib_cf_qty': 50,
        'new_ib_bs_stock_cv': 27,
        'lastUpdate': 1602338504.869655},
       'lastUpdate': 1602338504.869655}),
     ('0000002',
      {'ib_prcode': '0000002',
       '1000': {'ib_cf_qty': 35,
        'new_ib_bs_stock_cv': 33,
        'lastUpdate': 1600567810.529301},
       '1001': {'ib_cf_qty': 32,
        'new_ib_bs_stock_cv': 30,
        'lastUpdate': 1600567810.529316},
       '1002': {'ib_cf_qty': 34,
        'new_ib_bs_stock_cv': 30,
        'lastUpdate': 1600567810.529318},
       'lastUpdate': 1600567810.529318})]


