import okx.Earning as Earn
from okx import Funding
from okx import Account
from okx import MarketData
import binance


def get_crypto_sum(crypto_wallet: dict):
    total_sum = 0
    for source_data in crypto_wallet.values():
        for ccy, ccy_data in zip(source_data.keys(), source_data.values()):
            if ccy != 'USDT':
                total_sum += ccy_data['cost_USDT']
            else:
                total_sum += ccy_data['amount']
    return total_sum


async def get_market_data(api_key: str, secret_key: str, passphrase: str, currencies: list) -> dict:
    flag = '0'
    market_api = MarketData.MarketAPI(api_key, secret_key, passphrase, flag=flag, debug=False)
    prices = {}
    for ccy in currencies:
        if ccy == 'USDT':
            continue
        ccy_data = market_api.get_ticker(f'{ccy}-USDT')
        price = ccy_data['data'][0]['last']
        prices[ccy] = price
    return prices


async def get_okx_balance(api_key, secret_key, passphrase) -> dict:
    flag = '0'
    assets = {}
    balance_api = Funding.FundingAPI(api_key, secret_key, passphrase, flag=flag, debug=False)
    balance = balance_api.get_balances()
    earn_api = Earn.EarningAPI(api_key, secret_key, passphrase, flag=flag, debug=False)
    earn = earn_api.get_saving_balance()
    trade_api = Account.AccountAPI(api_key, secret_key, passphrase, flag=flag, debug=False)
    trade_balance = trade_api.get_account_balance()

    for data in balance['data']:
        ccy = data['ccy']
        amount = round((float(data['availBal'])), 4)
        if amount <= 0.0001:
            continue
        if assets.get(ccy):
            if assets[ccy].get('amount'):
                assets[ccy]['amount'] += amount
            else:
                assets[ccy]['amount'] = amount
        else:
            assets[ccy] = {}
            assets[ccy]['amount'] = amount

    for data in trade_balance['data'][0]['details']:
        amount = round((float(data['availBal'])), 4)
        if amount <= 0.0001:
            continue
        ccy = data['ccy']
        if assets.get(ccy):
            if assets[ccy].get('amount'):
                assets[ccy]['amount'] += amount
            else:
                assets[ccy]['amount'] = amount
        else:
            assets[ccy] = {}
            assets[ccy]['amount'] = amount
        assets[ccy]['amount'] = amount

    for data in earn['data']:
        ccy = data['ccy']
        amount = round((float(data['amt'])), 4)
        earnings = round((float(data['earnings'])), 4)
        if assets.get(ccy):
            if assets[ccy].get('amount'):
                assets[ccy]['amount'] += amount + earnings
            else:
                assets[ccy]['amount'] = amount + earnings
        else:
            assets[ccy] = {}
            assets[ccy]['amount'] = amount + earnings
        assets[ccy]['amount'] = round(assets[ccy]['amount'], 4)
    ccy_prices = await get_market_data(api_key, secret_key, passphrase, assets.keys())
    for ccy in ccy_prices.keys():
        cost = float(ccy_prices[ccy]) * assets[ccy]['amount']
        assets[ccy]['cost_USDT'] = round(cost, 4)
    return assets


async def get_okx_data(okx_api_key, deposits, request) -> dict:
    okx_phrase = request.cookies.get('okx_phrase')
    okx_key = request.cookies.get('okx_key')
    if okx_phrase and okx_key and okx_api_key:
        okx_balance = await get_okx_balance(okx_api_key, okx_key, okx_phrase)
        deposits['crypto']['OKX'] = okx_balance
    return deposits


async def get_binance_data(binance_api_key: str, deposits: dict, request) -> dict:
    binance_key = request.cookies.get('binance_key')
    client = binance.Client(api_key=binance_api_key, api_secret=binance_key)
    futures_balance = client.futures_account_balance()
    binance_assets = {}
    for data in futures_balance:
        if float(data.get('crossWalletBalance')):
            ccy = data['asset']
            current_sum = round(float(data['crossWalletBalance']), 4)
            if not binance_assets.get(ccy):
                binance_assets[ccy] = {}
            binance_assets[ccy]['amount'] = current_sum
    deposits['crypto']['binance'] = binance_assets
    return deposits
