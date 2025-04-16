import requests
import time
import hmac
import hashlib
import urllib.parse

# ==== GANTI DENGAN API KAMU ====
API_KEY = 'API_KEY_KAMU'
API_SECRET = 'SECRET_API_KEY_KAMU'
API_URL = 'https://indodax.com/tapi/'
PAIR = 'elf_idr' # Ganti dengan Coin yang kamu beli
STOP_LOSS_PERCENT = 5  # Turun 5% dari harga tertinggi
BUY_PRICE = 25000      # Harga beli

MANUAL_TIMESTAMP = 1578304294000
MANUAL_RECVWINDOW = 1578303937000

def generate_signature(params, secret):
    postdata = urllib.parse.urlencode(params)
    return hmac.new(
        secret.encode('utf-8'),
        postdata.encode('utf-8'),
        hashlib.sha512
    ).hexdigest()

def indodax_api(method, params={}):
    params['method'] = method
    params['timestamp'] = MANUAL_TIMESTAMP
    params['recvWindow'] = MANUAL_RECVWINDOW

    headers = {
        'Key': API_KEY,
        'Sign': generate_signature(params, API_SECRET)
    }

    try:
        response = requests.post(API_URL, headers=headers, data=params)
        return response.json()
    except Exception as e:
        print("API Error:", e)
        return {}

def get_current_price():
    ticker = requests.get(f'https://indodax.com/api/{PAIR}/ticker').json()
    return float(ticker['ticker']['last'])

def show_realtime_balance():
    balance = indodax_api('getInfo')
    if 'return' not in balance:
        print("Gagal mengambil saldo.")
        return

    idr = float(balance['return']['balance'].get('idr', 0))
    coin = PAIR.split('_')[0]
    coin_balance = float(balance['return']['balance'].get(coin, 0))
    current_price = get_current_price()
    coin_value = coin_balance * current_price
    total_value = idr + coin_value

    print(f"[Saldo] {coin.upper()}: {coin_balance:.8f} (~Rp {coin_value:,.0f}) | IDR: Rp {idr:,.0f} | Total: Rp {total_value:,.0f}")

def sell_all():
    balance = indodax_api('getInfo')
    coin = PAIR.split('_')[0]
    amount = float(balance['return']['balance'].get(coin, 0))
    if amount > 0:
        price = get_current_price()
        total_sell = amount * price
        total_buy = amount * BUY_PRICE
        profit = total_sell - total_buy
        profit_percent = (profit / total_buy) * 100 if total_buy != 0 else 0

        print(f"Menjual {amount:.8f} {coin.upper()} di harga Rp {price:,.0f}")
        print(f"Modal: Rp {total_buy:,.0f} | Hasil Jual: Rp {total_sell:,.0f}")
        print(f"Keuntungan: Rp {profit:,.0f} ({profit_percent:.2f}%)")

        params = {
            'pair': PAIR,
            'type': 'sell',
            'price': str(price),
            coin: str(amount)
        }
        result = indodax_api('trade', params)

        if 'return' in result:
            ret = result['return']
            sold_key = f'sold_{coin}'
            remain_key = f'remain_{coin}'

            print("\n📦 Hasil Penjualan:")
            print(f"  - Jumlah terjual    : {ret.get(sold_key, 0)} {coin.upper()}")
            print(f"  - Diterima (IDR)    : Rp {int(ret.get('receive_rp', 0)):,}")
            print(f"  - Fee               : {ret.get('fee', 0)}")
            print(f"  - Sisa saldo koin   : {ret.get(remain_key, ret.get('remain', '0'))}")
            print(f"  - Order ID          : {ret.get('order_id')}")
            print(f"  - Client Order ID   : {ret.get('client_order_id', '-')}")
        else:
            print("❌ Gagal melakukan penjualan:", result)
    else:
        print("Tidak ada saldo untuk dijual.")

def main():
    print("Bot Trailing Stop-Loss dimulai...")
    peak_price = get_current_price()
    print(f"Harga awal: Rp {peak_price:,.0f}")

    while True:
        try:
            current_price = get_current_price()
            stop_price = peak_price * (1 - STOP_LOSS_PERCENT / 100)

            print(f"\nHarga Sekarang: Rp {current_price:,.0f} | Peak: Rp {peak_price:,.0f} | Stop-Loss: Rp {stop_price:,.0f}")
            show_realtime_balance()

            if current_price > peak_price:
                peak_price = current_price
                print("📈 Harga naik - Peak price diperbarui.")

            elif current_price <= stop_price:
                print("🚨 Harga turun ke bawah batas trailing stop-loss. Menjual...")
                sell_all()
                break

            time.sleep(5)
        except KeyboardInterrupt:
            print("\n⛔ Bot dihentikan manual.")
            break

if __name__ == '__main__':
    main()
