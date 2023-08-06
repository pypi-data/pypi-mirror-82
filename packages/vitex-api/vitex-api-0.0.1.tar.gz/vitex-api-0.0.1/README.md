# Vitex-API-Python

ViteX API enables users to complete trading operations on ViteX decentralized exchange without exposing private keys. ViteX API is categorized into trading API and market trends API. Trading API (also known as private API) requires authentication and authorization, and provides functions such as order placement and cancellation. Market trends API (also known as public API) provides market data, information query, etc. Market trends API can be accessed publicly without authentication.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install vitex_api.

```bash
python -m pip install --index-url https://pypi.org/simple/ --no-deps vitex_api
```

## Usage

```python
from vitex_api_pkg import VitexRestApi
from vitex_api_pkg import VitexWebSocket
```
### Create an Object of Vitex API Class
```
vitexrestapi = VitexRestApi(key, signature)
vitexwebsocket = VitexWebSocket(clientId, opType, topics)
```

### API Response
API response is returned in JSON.

HTTP code:

HTTP **200** API returned successfully

HTTP **4XX** Wrong API request

HTTP **5XX** Service error

Response format:

| Key  |  Value |
| ------------ | ------------ |
| code  | 0 - success. An error code is returned if the API request failed  |
| msg  | Detailed error message  |
| data  | Return data  |

Example:
```
{
  "code": 1,
  "msg": "Invalid symbol",
  "data": {}
}
```
Error code:

**0** API returned successfully

**1** General error - view the specific error message in msg field.

**1001** Too frequent request - request exceeds limit.

**1002** Invalid parameter - this may include invalid timestamp, wrong order price, invalid amount, order too small, invalid market, insufficient permission, symbol not exist, etc.

**1003** Network - network jam, network broken, insufficient quota and so on.

**1004** Other failure - such as attempting to cancel an order of other address, attempting to cancel an order already filled, order status exception

**1005** Service error - unexpected API error

**1006** Minimum order quantity not satisfied - order quantity doesn't reach the minimal requirement in the market

**1007** Insufficient Exchange Balance - user's balance in the exchange is not enough

Data Definition

#Order Status

| Code  | Status  | Description  |
| ------------ | ------------ | ------------ |
| 0  | Unknown  | Status unknown  |
| 1 | Pending Request  | Order submitted. A corresponding request transaction has been created on the blockchain  |
| 2 | Received  |  Order received by ViteX smart contract. Not yet dispatched into matching engine |
| 3 | Open  | Order unfilled  |
| 4  | Filled  | Order completely filled  |
| 5  | Partially Filled  | Order partially filled  |
| 6  | Pending Cancel  | Cancel order request submitted. A corresponding request transaction has been created on the blockchain  |
| 7  | Cancelled  | Order cancelled  |
| 8  | 	Partially Cancelled  | Order partially cancelled (order is partially filled and then cancelled)  |
| 9  | Failed  | Order failed  |
| 10  | Expired  | Order expired  |

#Order Type

| Code  | Status  | Description  |
| ------------ | ------------ | ------------ |
| 0  | Limit Order  | Limit Order  |
| 1 | Market Order  | Market Order (not supported at present)  |

#Side

| Code  | Status  | Description  |
| ------------ | ------------ | ------------ |
| 0  | Buy Order  | Buy  |
| 1 | Sell Order  | Sell  |

#Time In Force

| Code  | Status  | Description  |
| ------------ | ------------ | ------------ |
| 0  | GTC - Good till Cancel  | Place an order and wait for it to be fully filled or cancelled  |
| 1 | IOC - Immediate or Cancel  | Place an order and immediately cancel unfilled (not supported at present)  |
| 2 | FOK - Fill or Kill  | Place an order only when it can be fully filled (not supported at present)  |

### Private REST API

Place Order (test)

Test placing order. The request will not be submitted to exchange. This API is generally used to verify that the signature is correct.
```
res = vitexrestapi.place_order_test(symbol = None, amount = None, price = None, side = None)
```
Parameters:

| Name  | Type  |  Description  |
| ------------ | ------------ | ------------ |
| symbol  | STRING  |Trading pair name. For example, ETH-000_BTC-000  |
| amount | STRING  | Order amount (in trade token)  |
| price  | STRING  | Order price  |
| side  | INT  | Buy - 0 , Sell - 1  |

Response:

```
{
  "code": 0,
  "msg": "ok",
  "data": null
}
```

Place Order

```

res = vitexrestapi.place_order(symbol = None, amount = None, price = None, side = None)

```

Parameters:

| Name  | Type  | Description  |
| ------------ | ------------ | ------------ |
| symbol  | STRING  | Trading pair name. For example, ETH-000_BTC-000  |
| amount | STRING  | Order amount (in trade token)  |
| price  | STRING  | Order price  |
| side  | INT  | uy - 0 , Sell - 1  |

Response:

| Name  | Type  | Description  |
| ------------ | ------------ | ------------ |
| symbol  | STRING  | Trading pair name  |
| orderId | STRING  | Order ID  |
| status  | INTEGER  | Order status  |

```

{
  "code": 0,
  "msg": "ok",
  "data": {
    "symbol": "VX_ETH-000",
    "orderId": "c35dd9868ea761b22fc76ba35cf8357db212736ecb56399523126c515113f19d",
    "status": 1
  }
}

```

Cancel Order

```
res = vitexrestapi.cancel_order(symbol = None, orderId = None)
```

Parameters:

| Name  | Type  | Description  |
| ------------ | ------------ | ------------ |
| symbol  | STRING  | Trading pair name. For example, ETH-000_BTC-000  |
| orderId | STRING  | Order ID  |

Response:

| Name  | Type  | Description  |
| ------------ | ------------ | ------------ |
| symbol  | STRING  | Trading pair name  |
| orderId | STRING  | Order ID  |
| cancelRequest | STRING  | Cancel request ID  |
| status | INTEGER  | Order status  |

```
{
  "code": 0,
  "msg": "ok",
  "data": {
    "symbol": "VX_ETH-000",
    "orderId": "c35dd9868ea761b22fc76ba35cf8357db212736ecb56399523126c515113f19d",
    "cancelRequest": "2d015156738071709b11e8d6fa5a700c2fd30b28d53aa6160fd2ac2e573c7595",
    "status": 6
  }
}
```

Cancel All Order

```
res = vitexrestapi.cancel_all_order(symbol = None)
```

Parameters:

| Name  | Type  | Description  |
| ------------ | ------------ | ------------ |
| symbol  | STRING  | Trading pair name. For example, ETH-000_BTC-000  |

Response:

| Name  | Type  | Description  |
| ------------ | ------------ | ------------ |
| symbol  | STRING  | Trading pair name  |
| orderId | STRING  | Order ID  |
| cancelRequest | STRING  | Cancel request ID  |
| status | INTEGER  | Order status  |

```
{
  "code": 0,
  "msg": "ok",
  "data": [
    {
      "symbol": "VX_ETH-000",
      "orderId": "de185edae25a60dff421c1be23ac298b121cb8bebeff2ecb25807ce7d72cf622",
      "cancelRequest": "355b6fab007d86e7ff09b0793fbb205e82d3880b64d948ed46f88237115349ab",
      "status": 6
    },
    {
      "symbol": "VX_ETH-000",
      "orderId": "7e079d4664791207e082c0fbeee7b254f2a31e87e1cff9ba18c5faaeee3d400a",
      "cancelRequest": "55b80fe42c41fa91f675c04a8423afa85857cd30c0f8878d52773f7096bfac3b",
      "status": 6
    }
  ]
}
```

### Public REST API
Get Order Limit

Get minimum order quantity for all markets
```
res = vitexrestapi.get_order_limit()
```

Response:
```
{
  "code": 0,
  "msg": "ok",
  "data": {
      "minAmount": {
          "BTC-000": "0.0001",
          "USDT-000": "1",
          "ETH-000": "0.01"
      },
      "depthStepsLimit": {}
  }
}
```

Get All Tokens

```
res = vitexrestapi.get_all_tokens(category = None, tokenSymbolLike = None, offset = None, limit = None)
```

Parameters:

| Name  | Type  | Description  |
| ------------ | ------------ | ------------ |
| category  | STRING  | Token category, [ quote , all ], default all  |
| tokenSymbolLike  | STRING  | Token symbol. For example, VITE . Fuzzy search supported. |
| offset  | INTEGER  | Search starting index, starts at 0 , default 0 |
| limit  | INTEGER  | Search limit, max 500 , default 500 |

```
{
  "code": 0,
  "msg": "ok",
  "data": [
    {
      "tokenId": "tti_322862b3f8edae3b02b110b1",
      "name": "BTC Token",
      "symbol": "BTC-000",
      "originalSymbol": "BTC",
      "totalSupply": "2100000000000000",
      "owner": "vite_ab24ef68b84e642c0ddca06beec81c9acb1977bbd7da27a87a",
      "tokenDecimals": 8,
      "urlIcon": null
    }
  ]
}
```

Get Token Detail

```
res = vitexrestapi.get_token_detail(tokenSymbol = None, tokenId = None)
```

Parameters:

| Name  | Type  | Description  |
| ------------ | ------------ | ------------ |
| tokenSymbol  | STRING  | Token symbol. For example, VITE  |
| tokenId  | STRING  | Token id. For example, tti_5649544520544f4b454e6e40 |

Response:
```
{
  "code": 0,
  "msg": "ok",
  "data": {
    "tokenId": "tti_322862b3f8edae3b02b110b1",
    "name": "BTC Token",
    "symbol": "BTC-000",
    "originalSymbol": "BTC",
    "totalSupply": "2100000000000000",
    "publisher": "vite_ab24ef68b84e642c0ddca06beec81c9acb1977bbd7da27a87a",
    "tokenDecimals": 8,
    "tokenAccuracy": "0.00000001",
    "publisherDate": null,
    "reissue": 2,
    "urlIcon": null,
    "gateway": null,
    "website": null,
    "links": null,
    "overview": null
  }
}
```

Get Listed Tokens

Get tokens that are already listed in specific market

```
res = vitexrestapi.get_listed_tokens(quoteTokenSymbol = None)
```

Parameters:

| Name  | Type  | Description  |
| ------------ | ------------ | ------------ |
| quoteTokenSymbol  | STRING  | Quote token symbol. For example, VITE  |

Response:

```
{
  "code": 0,
  "msg": "ok",
  "data": [
    {
      "tokenId": "tti_c2695839043cf966f370ac84",
      "symbol": "VCP"
    }
  ]
}
```

Get Unlisted Tokens

Get tokens that are not yet listed in specific market


```
res = vitexrestapi.get_unlisted_tokens(quoteTokenSymbol = None)
```

Parameters:

| Name  | Type  | Description  |
| ------------ | ------------ | ------------ |
| quoteTokenSymbol  | STRING  | Quote token symbol. For example, VITE  |

Response:
```
{
  "code": 0,
  "msg": "ok",
  "data": [
    {
      "tokenId": "tti_2736f320d7ed1c2871af1d9d",
      "symbol": "VTT"
    }
  ]
}
```

Get Trading Pair

Get trading pair in detail

```
res = vitexrestapi.get_trading_pair(symbol = None)
```

Parameters:

| Name  | Type  | Description  |
| ------------ | ------------ | ------------ |
| symbol  | STRING  | Trading pair name. For example, GRIN-000_BTC-000  |

Response:
```{
   "code": 0,
      "msg": "ok",
      "data": {
          "symbol": "GRIN-000_BTC-000",
          "tradingCurrency": "GRIN-000",
          "quoteCurrency": "BTC-000",
          "tradingCurrencyId": "tti_289ee0569c7d3d75eac1b100",
          "quoteCurrencyId": "tti_b90c9baffffc9dae58d1f33f",
          "tradingCurrencyName": "Grin",
          "quoteCurrencyName": "Bitcoin",
          "operator": "vite_4c2c19f563187163145ab8f53f5bd36864756996e47a767ebe",
          "operatorName": "Vite Labs",
          "operatorLogo": "https://token-profile-1257137467.cos.ap-hongkong.myqcloud.com/icon/f62f3868f3cbb74e5ece8d5a4723abef.png",
          "pricePrecision": 8,
          "amountPrecision": 2,
          "minOrderSize": "0.0001",
          "operatorMakerFee": 5.0E-4,
          "operatorTakerFee": 5.0E-4,
          "highPrice": "0.00007000",
          "lowPrice": "0.00006510",
          "lastPrice": "0.00006682",
          "volume": "1476.37000000",
          "baseVolume": "0.09863671",
          "bidPrice": "0.00006500",
          "askPrice": "0.00006999",
          "openBuyOrders": 27,
          "openSellOrders": 42
      }
}
```

Get All Trading Pairs

```
res = vitexrestapi.get_all_trading_pairs(offset = None, limit = None)
```

Parameters:

| Name  | Type  | Description  |
| ------------ | ------------ | ------------ |
| offset  | INTEGER  | Search starting index, starts at 0 , default 0  |
| limit  | INTEGER  | Search limit, max 500 , default 500  |

Response:

```
{
  "code": 0,
  "msg": "ok",
  "data": [
    {
      "symbol": "BTC-000_USDT",
      "tradeTokenSymbol": "BTC-000",
      "quoteTokenSymbol": "USDT-000",
      "tradeToken": "tti_322862b3f8edae3b02b110b1",
      "quoteToken": "tti_973afc9ffd18c4679de42e93",
      "pricePrecision": 8,
      "quantityPrecision": 8
    }
  ]
}
```

Get Order

```
res = vitexrestapi.get_order(address = None, orderId = None)
```

Parameters:

| Name  | Type  | Description  |
| ------------ | ------------ | ------------ |
| address  | STRING  | User's account address (not delegation address)  |
| orderId  | STRING  | Order id |

Response:
```
{
  "code": 0,
  "msg": "ok",
  "data": {
    "address": "vite_228f578d58842437fb52104b25750aa84a6f8558b6d9e970b1",
    "orderId": "0dfbafac33fbccf5c65d44d5d80ca0b73bc82ae0bbbe8a4d0ce536d340738e93",
    "symbol": "VX_ETH-000",
    "tradeTokenSymbol": "VX",
    "quoteTokenSymbol": "ETH-000",
    "tradeToken": "tti_564954455820434f494e69b5",
    "quoteToken": "tti_06822f8d096ecdf9356b666c",
    "side": 1,
    "price": "0.000228",
    "quantity": "100.0001",
    "amount": "0.02280002",
    "executedQuantity": "100.0000",
    "executedAmount": "0.022800",
    "executedPercent": "0.999999",
    "executedAvgPrice": "0.000228",
    "fee": "0.000045",
    "status": 5,
    "type": 0,
    "createTime": 1586941713
  }
}
```

Get Open Order

Get orders that are unfilled or partially filled.

```
res = vitexrestapi.get_open_order(address = None, symbol = None, quoteTokenSymbol = None, tradeTokenSymbol = None, offset = None, limit = None, total = None)
```

Parameters:

| Name  | Type  | Description  |
| ------------ | ------------ | ------------ |
| address  | STRING  | User's account address (not delegation address)  |
| symbol  | STRING  | Trading pair name. For example, GRIN-000_BTC-000 |
| quoteTokenSymbol  | STRING  | Quote token symbol. For example, BTC-000 |
| tradeTokenSymbol  | STRING  | Trade token symbol. For example, GRIN-000 |
| offset  | INTEGER  | Search starting index, starts at 0 , default 0 |
| limit  | INTEGER  | Search limit, default 30 , max 100 |
| total  | INTEGER  | Include total number searched in result? 0 - not included, 1 - included. Default is 0 , in this case total=-1 in response |

Response:

```
{
  "code": 0,
  "msg": "ok",
  "data": {
    "order": [
      {
        "address": "vite_ff38174de69ddc63b2e05402e5c67c356d7d17e819a0ffadee",
        "orderId": "5379b281583bb17c61bcfb1e523b95a6c153150e03ce9db35f37d652bbb1b321",
        "symbol": "BTC-000_USDT-000",
        "tradeTokenSymbol": "BTC-000",
        "quoteTokenSymbol": "USDT-000",
        "tradeToken": "tti_322862b3f8edae3b02b110b1",
        "quoteToken": "tti_973afc9ffd18c4679de42e93",
        "side": 0,
        "price": "1.2000",
        "quantity": "1.0000",
        "amount": "1.20000000",
        "executedQuantity": "0.0000",
        "executedAmount": "0.0000",
        "executedPercent": "0.0000",
        "executedAvgPrice": "0.0000",
        "confirmations": null,
        "fee": "0.0000",
        "status": 3,
        "type": 0,
        "createTime": 1587906622
      }
    ]
  }
}
```

Get Orders

```
res = vitexrestapi.get_orders(address = None, symbol = None, quoteTokenSymbol = None, tradeTokenSymbol = None, startTime = None, endTime = None, side = None, status = None, offset = None, limit = None, total = None)
```

Parameters:

| Name  | Type  | Description  |
| ------------ | ------------ | ------------ |
| address  | STRING  | User's account address (not delegation address)  |
| symbol  | STRING  | Trading pair name. For example, GRIN-000_BTC-000 |
| quoteTokenSymbol  | STRING  | Quote token symbol. For example, BTC-000 |
| tradeTokenSymbol  | STRING  | Trade token symbol. For example, GRIN-000 |
| startTime  | LONG  | Start time (s) |
| endTime  | LONG  | End time (s) |
| side  | INTEGER  | Order side. 0 - buy, 1 - sell |
| status  | INTEGER  | Order status, valid in [ 0-10 ]. 3 , 5 - returns orders that are unfilled or partially filled; 7 , 8 - returns orders that are cancelled or partially cancelled |
| offset  | INTEGER  | Search starting index, starts at 0 , default 0 |
| limit  | INTEGER  | Search limit, default 30 , max 100 |
| total  | INTEGER  | Include total number searched in result? 0 - not included, 1 - included. Default is 0 , in this case total=-1 in response |

Response:

```
{
  "code": 0,
  "msg": "ok",
  "data": {
    "order": [
      {
        "address": "vite_ff38174de69ddc63b2e05402e5c67c356d7d17e819a0ffadee",
        "orderId": "0dfbafac33fbccf5c65d44d5d80ca0b73bc82ae0bbbe8a4d0ce536d340738e93",
        "symbol": "VX_ETH-000",
        "tradeTokenSymbol": "VX",
        "quoteTokenSymbol": "ETH-000",
        "tradeToken": "tti_564954455820434f494e69b5",
        "quoteToken": "tti_06822f8d096ecdf9356b666c",
        "side": 1,
        "price": "0.000228",
        "quantity": "100.0001",
        "amount": "0.02280002",
        "executedQuantity": "100.0000",
        "executedAmount": "0.022800",
        "executedPercent": "0.999999",
        "executedAvgPrice": "0.000228",
        "fee": "0.000045",
        "status": 5,
        "type": 0,
        "createTime": 1586941713
      }
    ],
    "total": -1
  }
}
```

Get 24hr Ticker Price Changes

```
res = vitexrestapi.get_24hr_ticker_price_changes(symbol = None, quoteTokenSymbol = None)
```

Parameters:

| Name  | Type  | Description  |
| ------------ | ------------ | ------------ |
| symbols  | STRING  | Trading pairs, split by ","  |
| quoteTokenSymbol  | STRING  | Quote token symbol. For example, USDT-000 . Returns all pairs if not present |

Response:
```
{
  "code": 0,
  "msg": "ok",
  "data": [
    {
      "symbol":"BTC-000_USDT-000",
      "tradeTokenSymbol":"BTC-000",
      "quoteTokenSymbol":"USDT-000",
      "tradeToken":"tti_b90c9baffffc9dae58d1f33f",
      "quoteToken":"tti_80f3751485e4e83456059473",
      "openPrice":"7540.0000",
      "prevClosePrice":"7717.0710",
      "closePrice":"7683.8816",
      "priceChange":"143.8816",
      "priceChangePercent":0.01908244,
      "highPrice":"7775.0000",
      "lowPrice":"7499.5344",
      "quantity":"13.8095",
      "amount":"104909.3499",
      "pricePrecision":4,
      "quantityPrecision":4,
      "openTime":null,
      "closeTime":null
    }
  ]
}
```

Get Order Book Ticker

Get current best price/qty on the order book for a trading pair

```
res = vitexrestapi.get_order_book_ticker(symbol = None)
```

Parameters:

| Name  | Type  | Description  |
| ------------ | ------------ | ------------ |
| symbol  | STRING  | Trading pair name. For example, GRIN-000_VITE |

Response:
```
{
  "code": 0,
  "msg": "ok",
  "data": {
    "symbol": "BTC-000_USDT-000",
    "bidPrice": "7600.0000",
    "bidQuantity": "0.7039",
    "askPrice": "7725.0000",
    "askQuantity": "0.0001",
    "height": null
  }
}
```

Get Trade Summary

Get trade records in summary

```
res = vitexrestapi.get_trade_summary(symbol = None, limit = None)
```

Parameters:

| Name  | Type  | Description  |
| ------------ | ------------ | ------------ |
| symbol  | STRING  | Trading pair name. For example, GRIN-000_VITE |
| limit  | INTEGER  | Search limit, default 500 |

Response:
```
{
  "code": 0,
  "msg": "ok",
  "data": [
    {
        "timestamp": 1588214534000,
        "price": "0.024933",
        "amount": "0.0180",
        "side": 0
    },
    {
        "timestamp": 1588214364000,
        "price": "0.024535",
        "amount": "0.0127",
        "side": 0
    }
  ]
}
```

Get Trade Records

Get trade records in detail

```
res = vitexrestapi.get_trade_records(symbol = None, orderId = None, startTime = None, endTime = None, side = None, offset = None, limit = None, total = None)
```

Parameters:

| Name  | Type  | Description  |
| ------------ | ------------ | ------------ |
| symbol  | STRING  | Trading pair name. For example, GRIN-000_VITE |
| orderId  | INTEGER  | Order id |
| startTime  | LONG  | Start time (s) |
| endTime  | LONG  | End time (s) |
| side  | INTEGER  | Order side. 0 - buy, 1 - sell |
| offset  | INTEGER  | Search starting index, starts at 0 , default 0 |
| limit  | INTEGER  | Search limit, default 30 , max 100 |
| total  | INTEGER  | Include total number searched in result? 0 - not included, 1 - included. Default is 0 , in this case total=-1 in response |

Response:
```
{
  "code": 0,
  "msg": "ok",
  "data": {
    "height": null,
    "trade": [
      {
        "tradeId": "d3e7529de05e94d247a4e7ef58a56b069b059d52",
        "symbol": "VX_ETH-000",
        "tradeTokenSymbol": "VX",
        "quoteTokenSymbol": "ETH-000",
        "tradeToken": "tti_564954455820434f494e69b5",
        "quoteToken": "tti_06822f8d096ecdf9356b666c",
        "price": "0.000228",
        "quantity": "0.0001",
        "amount": "0.00000002",
        "time": 1586944732,
        "side": 0,
        "buyFee": "0.00000000",
        "sellFee": "0.00000000",
        "blockHeight": 260
      }
    ],
    "total": -1
  }
}
```

Get Order Book Depth

```
res = vitexrestapi.get_order_book_depth(symbol = None, limit = None, precision = None)
```

Parameters:

| Name  | Type  | Description  |
| ------------ | ------------ | ------------ |
| symbol  | STRING  | Trading pair name. For example, GRIN-000_VITE |
| limit  | INTEGER  | Search limit, max 100 , default 100 |
| precision  | INTEGER  | Price Precision |

```
{
    "code": 0,
    "msg": "ok",
    "data": {
      "timestamp": 1588170501936,
      "asks": [
        [
            "0.025750",
            "0.0323"
        ],
        [
            "0.026117",
            "0.0031"
        ]
      ],
      "bids": [
        [
            "0.024820",
            "0.0004"
        ],
        [
            "0.024161",
            "0.0042"
        ]
      ]
    }
  }
```

Get Klines/Candlestick bars

```
res = vitexrestapi.get_klines_candlestick_bars(symbol = None, interval = None, limit = None, startTime = None, endTime = None)
```

Parameters:

| Name  | Type  | Description  |
| ------------ | ------------ | ------------ |
| symbol  | STRING  | Trading pair name. For example, GRIN-000_VITE |
| interval  | STRING  | Interval, [ minute , hour , day , minute30 , hour6 , hour12 , week ] |
| limit  | INTEGER  | Search limit, max 1500 , default 500 |
| startTime  | LONG  | Start time (s) |
| endTime  | LONG  | End time (s) |

Response:

| Name  | Type  | Description  |
| ------------ | ------------ | ------------ |
| t  | LONG  | Timestamp |
| c  | STRING  | Close price |
| p  | INTEGER  | Open price |
| h  | LONG  | Highest price |
| l  | LONG  | Lowest price |
| v  | LONG  | Trade volume |

```
{
  "code": 0,
  "msg": "ok",
  "data": {
    "t": [
      1554207060
    ],
    "c": [
      1.0
    ],
    "p": [
      1.0
    ],
    "h": [
      1.0
    ],
    "l": [
      1.0
    ],
    "v": [
      12970.8
    ]
  }
}
```

Get Deposit-Withdrawal Records

```
res = vitexrestapi.get_deposit_withdrawal_records(address = None, tokenId = None, offset = None, limit = None)
```

Parameters:

| Name  | Type  | Description  |
| ------------ | ------------ | ------------ |
| address  | STRING  | Account address |
| tokenId  | STRING  | Token id. For example, tti_5649544520544f4b454e6e40 |
| offset  | INTEGER  | Search starting index, starts at 0 , default 0 |
| limit  | INTEGER  | Search limit, max 100 , default 100 |

Response:
```
{
  "code": 0,
  "msg": "ok",
  "data": {
    "record": [
      {
        "time": 1555057049,
        "tokenSymbol": "VITE",
        "amount": "1000000.00000000",
        "type": 1
      }
    ],
    "total": 16
  }
}
```

Get Exchange Rate

```
res = vitexrestapi.get_exchante_rate(tokenSymbols = None, tokenIds = None)
```

Parameters:

| Name  | Type  | Description  |
| ------------ | ------------ | ------------ |
| tokenSymbols  | STRING  | Trading pairs, split by ",". For example, VITE,ETH-000 |
| tokenIds  | STRING  | Token ids, split by ",". For example, tti_5649544520544f4b454e6e40,tti_5649544520544f4b454e6e40 |

Response:
```
{
  "code": 0,
  "msg": "ok",
  "data": [
    {
      "tokenId": "tti_5649544520544f4b454e6e40",
      "tokenSymbol": "VITE",
      "usdRate": 0.03,
      "cnyRate": 0.16
    }
  ]
}
```

Get USD-CNY Rate

```
res = vitexrestapi.get_usd_cny_rate()
```

Parameters: None

Response:
```
{
  "code": 0,
  "msg": "ok",
  "data": 6.849
}
```

Get Exchange Balance

```
res = vitexrestapi.get_exchante_balance(address = None)
```

Parameters:

| Name  | Type  | Description  |
| ------------ | ------------ | ------------ |
| address  | STRING  | Account address |

Response:

| Name  | Type  | Description  |
| ------------ | ------------ | ------------ |
| available  | STRING  | Available balance |
| locked  | STRING  | Balance locked by open order |

```
{
  "code": 0,
  "msg": "ok",
  "data": {
    "VX": {
      "available": "0.00000000",
      "locked": "0.00000000"
    },
    "VCP": {
      "available": "373437.00000000",
      "locked": "0.00000000"
    },
    "BTC-000": {
      "available": "0.02597393",
      "locked": "0.13721639"
    },
    "USDT-000": {
      "available": "162.58284100",
      "locked": "170.40459600"
    },
    "GRIN-000": {
      "available": "0.00000000",
      "locked": "0.00000000"
    },
    "VITE": {
      "available": "30047.62090072",
      "locked": "691284.75633290"
    },
    "ETH-000": {
      "available": "1.79366977",
      "locked": "7.93630000"
    }
  }
}
```

Get Trade Mining Info

Get the current cycle's trade mining pool size and real-time fees accumulated

```
res = vitexrestapi.get_trade_mining_info()
```

Response:
```
{
    "code": 0,
    "msg": "ok",
    "data": {
        "tradePoolVx": {
            "1": "6005.736536774939954301",
            "2": "6005.736536774939954301",
            "3": "6005.736536774939954301",
            "4": "6005.736536774939954301"
        },
        "tradePoolFee": {
            "1": "17769.748909914626699977",
            "2": "1.267967346417481080",
            "3": "0.03045706",
            "4": "299.338260"
        }
    }
}
```

Get Server Time

```
res = vitexrestapi.get_server_time()
res = vitexrestapi.get_server_time_stamp()
```

Response:
```
{
  "code": 0,
  "msg": "ok",
  "data": 1559033445000
}
```

###WebSocket API
```
websocketapi = WebSocketApi(clientId, opType, topics)
res = websocketapi.response()
```

Definition of op_type

**sub**: subscribe

**un_sub**: un-subscribe

**ping**: heartbeat

**pong**: server acknowledgement

**push**: push message to client

Topic List

Support single and multiple topic subscriptions, separated by ",". For example, topic1,topic2


| Topic  | Description  | Message  |
| ------------ | ------------ | ------------ |
| order.$address  | Order update  | Order |
| market.$symbol.depth  | Depth data update  | Depth |
| market.$symbol.trade  | Trade data update  | Trade |
| market.$symbol.tickers  | Market pair statistics update  | TickerStatistics |
| market.quoteToken.$symbol.tickers  | Quote token statistics update  | TickerStatistics |
| market.quoteTokenCategory.VITE.tickers  | Quote token category statistics update  | TickerStatistics |
| market.quoteTokenCategory.ETH.tickers  | Quote token category statistics update  | TickerStatistics |
| market.quoteTokenCategory.USDT.tickers  | Quote token category statistics update  | TickerStatistics |
| market.quoteTokenCategory.BTC.tickers  | Quote token category statistics update  | TickerStatistics |
| market.$symbol.kline.minute  | 1-minute kline update  | Kline |
| market.$symbol.kline.minute30  | 30-minute kline update  | Kline |
| market.$symbol.kline.hour  | 1-hour kline update  | Kline |
| market.$symbol.kline.day  | 1-day kline update | Kline |
| market.$symbol.kline.week  | 1-week kline update | Kline |
| market.$symbol.kline.hour6  | 6-hour kline update | Kline |
| market.$symbol.kline.hour12  | 12-hour kline update | Kline |


JSON Message

#Message Definitions

**Order**

**Definition**

```
// order id
private String oid;
// symbol
private String s;
// trade token symbol
private String ts;
// quote token symbol
private String qs;
// trade tokenId
private String tid;
// quote tokenId
private String qid;
// side
private Integer side;
// price
private String p;
// quantity
private String q;
// amount
private String a;
// executed quantity
private String eq;
// executed amount
private String ea;
// executed percentage
private String ep;
// executed average price
private String eap;
// fee
private String f;
// status
private Integer st;
// type
private Integer tp;
// create time
private Long ct;
// address
private String d;
```

**Example**

Subscribe:

```
{
  "clientId":"test",
  "opType":"sub",
  "topics":"order.vite_cc392cbb42a22eebc9136c6f9ba416d47d19f3be1a1bd2c072"
}
```

Response:

```
{
  "message":{
    "a":"13.72516176",
    "ct":1588142062,
    "d":"vite_cc392cbb42a22eebc9136c6f9ba416d47d19f3be1a1bd2c072",
    "ea":"13.7251",
    "eap":"0.1688",
    "ep":"1.0000",
    "eq":"81.3102",
    "f":"0.0308",
    "oid":"b0e0e20739c570d533679315dbb154201c8367b6e23636b6521e9ebdd9f8fc0a",
    "p":"0.1688",
    "q":"81.3102",
    "qid":"tti_80f3751485e4e83456059473",
    "qs":"USDT-000",
    "s":"VX_USDT-000",
    "side":0,
    "st":2,
    "tid":"tti_564954455820434f494e69b5",
    "tp":0,
    "ts":"VX"
  }
}
```

**Trade**

**Definition**

```
// tradeId
private String id;
// symbol
private String s;
// trade token symbol
private String ts;
// quote token symbol
private String qs;
// trade tokenId
private String tid;
// quote tokenId
private String qid;
// price
private String p;
// quantity
private String q;
// amount
private String a;
// time
private Long t;
// side
private Integer side;
// buyer orderId
private String bid;
//seller orderId
private String sid;
// buyer fee
private String bf;
// seller fee
private String sf;
// block height
private Long bh;
```

**Example**

Subscribe:

```
{
  "clientId":"test",
  "opType":"sub",
  "topics":"market.VX_VITE.trade"
}
```

Response:

```
{
  "message":[
   {
    "a":"6324.77710294",
    "bf":"14.23074848",
    "bh":14526719,
    "bid":"00001f00fffffffff340910fa1ff005e6618cb000030",
    "id":"702d8d5bd6e8d5aa7b40953484acbcfeae6c1fcf",
    "p":"12.8222",
    "q":"493.2677",
    "qid":"tti_5649544520544f4b454e6e40",
    "qs":"VITE",
    "s":"VX_VITE",
    "sf":"14.23074848",
    "sid":"00001f01000000000cbf6ef05e00005e6618cb00002f",
    "side":0,
    "t":1583749346,
    "tid":"tti_564954455820434f494e69b5",
    "ts":"VX"
    }
  ]
}
```

**TickerStatistics**

**Definition**

```
// symbol
private String s;
// trade token symbol
private String ts;
// quote token symbol
private String qs;
// trade tokenId
private String tid;
// quote tokenId
private String qid;
// open price
private String op;
// previous close price
private String pcp;
// close price
private String cp;
// price change 
private String pc;
// price change percentage
private String pCp;
// high price 
private String hp;
// low price
private String lp;
// quantity 
private String q;
// amount 
private String a;
// price precision
private Integer pp;
// quantity precision
private Integer qp;
```

**Example**

Subscribe:

```
{
  "clientId":"test",
  "opType":"sub",
  "topics":"market.VX_VITE.tickers"
}
```

Response:
```
{
  "message":{
    "a":"14932378.5785",
    "cp":"13.3013",
    "hp":"13.5200",
    "lp":"10.9902",
    "op":"11.3605",
    "pc":"1.9408",
    "pcp":"13.2947",
    "pp":4,
    "q":"1207963.7611",
    "qid":"tti_5649544520544f4b454e6e40",
    "qp":4,
    "qs":"VITE",
    "s":"VX_VITE",
    "tid":"tti_564954455820434f494e69b5",
    "ts":"VX"
  }
}
```

**KLine/Candlestick bars**

**Definition**

```
private Long t;
private Double c;
private Double o;
private Double v;
private Double h;
private Double l;
```

**Example**

Subscribe:

```
{
  "clientId":"test",
  "opType":"sub",
  "topics":"market.VX_VITE.kline.minute"
}
```

Response:

```
{
  "message":{
  "c":12.935,
  "h":12.935,
  "l":12.935,
  "o":12.935,
  "t":1583749440,
  "v":415.1729
  }
}
```

**Depth**

**Definition**

```
private List<List<String>> asks; // [[price, quantity],[price, quantity]]
private List<List<String>> bids; // [[price, quantity],[price, quantity]]
```

**Example**

Subscribe:

```
{
  "clientId":"test",
  "opType":"sub",
  "topics":"market.VX_VITE.depth"
}
```

Response:

```
{
  "message":{
  "asks":[
  [
    "12.9320",
    "185.3194"
  ],[
    "13.3300",
    "48.9177"
  ],[
    "13.4959",
    "1305.9508"
  ],[
    "13.5100",
    "466.7237"
  ],[
    "13.8000",
    "134.5858"
  ]],
  "bids":[
  [
    "12.7002",
    "170.2562"
  ],[
    "12.6000",
    "63.6076"
  ],[
    "12.4000",
    "15339.2586"
  ],[
    "12.3010",
    "324.6731"
  ],[
    "12.3000",
    "222.7945"
  ]]
  }
}
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)