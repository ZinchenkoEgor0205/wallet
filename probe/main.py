
import okx.Account as Account
import okx.Earning as Earn
from keys import api_key, secret_key, passphrase

if __name__ == '__main__':
    flag = '0'
    account_api = Account.AccountAPI(api_key, secret_key, passphrase, flag=flag)

    balance = account_api.get_account_balance()
    # print(balance)

    earn_api = Earn.EarningAPI(api_key, secret_key, passphrase, flag=flag)
    earn = earn_api.get_activity_orders()
    print(earn)