# villaInventorySdk
> read and write inventory in real time


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

    CPU times: user 5.63 ms, sys: 103 µs, total: 5.73 ms
    Wall time: 5.38 ms


## Update inventory 

```python
%%time
sdk.updateWithS3( sampleInput )
```

    CPU times: user 13 ms, sys: 8.05 ms, total: 21.1 ms
    Wall time: 130 ms





    {'body': 'true', 'statusCode': 200, 'header': {}}



## Query single product

```python
%%time
sdk.querySingleProduct('0000002')
```

    CPU times: user 13.7 ms, sys: 0 ns, total: 13.7 ms
    Wall time: 64.3 ms





    {'body': '{"ib_prcode":"0000002","1000":{"ib_cf_qty":35,"new_ib_bs_stock_cv":33,"lastUpdate":1600567810.529301},"1001":{"ib_cf_qty":32,"new_ib_bs_stock_cv":30,"lastUpdate":1600567810.529316},"1002":{"ib_cf_qty":34,"new_ib_bs_stock_cv":30,"lastUpdate":1600567810.529318},"lastUpdate":1600567810.529318}',
     'statusCode': 200,
     'header': {}}



## Query Branch

```python
result = sdk.queryBranch('1000')
#showing the first 2 result
list(iter(result.items()))[:2]
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-30-c8acf849e3da> in <module>
    ----> 1 result = sdk.queryBranch('1000')
          2 #showing the first 2 result
          3 list(iter(result.items()))[:2]


    AttributeError: 'InventorySdk' object has no attribute 'queryBranch'

