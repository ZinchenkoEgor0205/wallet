import okx.Earning as Earn
from okx import Funding
from okx import MarketData


def get_crypto_sum(crypto_wallet: dict):
    total_sum = 0
    for source_data in crypto_wallet.values():
        for ccy_data in source_data.values():
            total_sum += ccy_data['cost_USDT']
    return total_sum


async def get_market_data(api_key: str, secret_key: str, passphrase: str, currencies: list) -> dict:
    flag = '0'
    market_api = MarketData.MarketAPI(api_key, secret_key, passphrase, flag=flag, debug=False)
    prices = {}
    for ccy in currencies:
        ccy_data = market_api.get_ticker(f'{ccy}-USDT')
        price = ccy_data['data'][0]['last']
        prices[ccy] = price
    return prices


async def get_okx_balance(api_key, secret_key, passphrase):
    flag = '0'
    assets = {}
    balance_api = Funding.FundingAPI(api_key, secret_key, passphrase, flag=flag, debug=False)
    balance = balance_api.get_balances()
    earn_api = Earn.EarningAPI(api_key, secret_key, passphrase, flag=flag, debug=False)
    earn = earn_api.get_saving_balance()

    for data in balance['data']:
        ccy = data['ccy']
        if assets.get(ccy):
            if assets[ccy].get('amount'):
                assets[ccy]['amount'] += float(data['availBal'])
            else:
                if float(data['availBal']) >= 0.0001:
                    assets[ccy]['amount'] = float(data['availBal'])
        else:
            if float(data['availBal']) >= 0.0001:
                assets[ccy] = {}
                assets[ccy]['amount'] = float(data['availBal'])

    for data in earn['data']:
        ccy = data['ccy']
        if assets.get(ccy):
            if assets[ccy].get('amount'):
                assets[ccy]['amount'] += (float(data['amt']) + float(data['earnings']))
            else:
                assets[ccy]['amount'] = (float(data['amt']) + float(data['earnings']))
        else:
            assets[ccy] = {}
            assets[ccy]['amount'] = (float(data['amt']) + float(data['earnings']))
        assets[ccy]['amount'] = round(assets[ccy]['amount'], 4)
    ccy_prices = await get_market_data(api_key, secret_key, passphrase, assets.keys())
    for ccy in ccy_prices.keys():
        cost = float(ccy_prices[ccy]) * assets[ccy]['amount']
        assets[ccy]['cost_USDT'] = round(cost, 4)
    return assets


async def get_okx_data(okx_api_key, deposits, request):
    okx_phrase = request.cookies.get('okx_phrase')
    okx_key = request.cookies.get('okx_key')
    if okx_phrase and okx_key and okx_api_key:
        okx_balance = await get_okx_balance(okx_api_key, okx_key, okx_phrase)
        deposits['crypto']['OKX'] = okx_balance
        deposits['crypto']['total_cost_USDT'] = get_crypto_sum(deposits['crypto'])
    return deposits


async def get_binance_data(binance_api_key, deposits, request):
    print('!!!')