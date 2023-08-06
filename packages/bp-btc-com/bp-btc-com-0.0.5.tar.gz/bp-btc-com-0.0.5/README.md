## bp-btc-com
A python 3 api wrapper for btc.com block explorer.
Forked from [psqnt/btc-com](https://github.com/psqnt/btc-com)

docs: https://github.com/qlbnb/btc-com/blob/master/docs.md

api docs: https://btc.com/api-doc

block explorer: https://btc.com/block


## Install
```
pip install bp-btc-com
```
must be python3 so if not in a python3 virtualenv use
```
pip3 install bp-btc-com
```

## Usage
```python
import datetime

from bp_btc_com.explorer import Explorer
from time import sleep

sleep_time = .5  # don't overstep rate limits
# get latest block
print(Explorer("btc").get_block())
sleep(sleep_time)

print(Explorer("bch").get_block())
sleep(sleep_time)

print(Explorer("bsv").get_block())
```

## Examples
https://github.com/qlbnb/btc-com/blob/master/examples.py

## Common Issues
API changes may break the sdk. Please refer to the official btc.com api documentation and update accordingly.
```
'https://chain.api.btc.com/v3/'
'https://bch-chain.api.btc.com/v3/'
'https://bsv-chain.api.btc.com/v3/'
```
