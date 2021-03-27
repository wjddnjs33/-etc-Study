import pyupbit
import sys

access_key = 'REDACTED'
secret_key = 'REDACTED'

# upbit 클래스 생성
upbit = pyupbit.Upbit(access_key, secret_key)
## pyupbit 모듈 연결 확인
if pyupbit.Upbit:
    print("[+] Connected")
else:
    sys.exit()

Name = 'KRW-STORJ'
Price = 50
add_money = 15

first_price = 0
def first_p():
    global first_price
    first_price = pyupbit.get_current_price(Name)
    print("[+] {} 현재 가격 : {}".format(Name, first_price))

## 매수 확인
def my_money():
    result = 0
    c = Name.split('-')[1]
    m = upbit.get_balances()
    for i in range(len(m)):
        if c in m[i]['currency']:
            result = 1
            break
        else:
            pass
    return result

# 시장가 매수 
# name이라는 코인을 price원어치 시장가 매수
def buy(name, price):
    result = 0
    
    try:
        ret = upbit.buy_market_order(name, price)
        if "error" in str(ret):
            e = ret['error']['message']
            print("[+] Error Occur! : {}".format(e))
            result = 0
        else:
            result = 1
    except:
        pass
    return result

# 시장가 매도 
# name이라는 코인을 num 개수만큼 시장가 매도
def sell(name, num):
    result = 0
    try:
        ret = upbit.sell_market_order(name, num)
        if "error" in str(ret):
            e = ret['error']['message']
            print("[+] Error Occur! : {}".format(e))
            result = 0
        else:
            result = 1
    except:
        pass
    return result   

def final_buy():
    if buy(Name, Price):
        print("[+] Buy Success")
    else:
        print("[+] Buy Failed")

def keep():
    while(1):
        f = pyupbit.get_current_price(Name)
        print("[+] {} 현재 가격 : {}".format(Name, f))
        if my_money():
            if f > first_price + add_money:
                print("[+] {} 현재 가격 : {}".format(Name, pyupbit.get_current_price(Name)))
                if sell(Name, 33):
                    print("[+] Sell Success")
                    while(1): 
                        if int(pyupbit.get_current_price(Name)) < condition:
                            first_p()
                            final_buy()
                            break
                        else:
                            pass
                else:
                    print("[+] Sell Failed")
            else:
                pass
        else:
            pass

if __name__ == '__main__':
    # condition 변수에는 특정 코인에 현재 가격이 들어감.
    # 해당 변수는 매수를 하는데 있어서 해당 가격보다 비싼 가격때에는 사지 않기 하기 위함.
    condition = pyupbit.get_current_price(Name)

    first_p()
    final_buy()
    keep()
