import ccxt
import yaml


CONFIG_FILE_PATH = 'config/config.yaml'

def load_config(config_file_path: str) -> dict:
    with open(config_file_path, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

config = load_config(CONFIG_FILE_PATH)

exchange_class = getattr(ccxt, config['EXCHANGE'])
exchange = exchange_class({
    'apiKey': config['CREDENTIAL']['API_KEY'],
    'secret': config['CREDENTIAL']['API_SECRET']
})


pairs = config['GRID']

for pair in pairs:
    ticker = exchange.fetch_ticker(pair['SYMBOL'])
    initial_price = ticker['bid']

    # Set up
    buy_order_tracker = []
    sell_order_tracker = []

    # Place buy grid lines
    for i in range(pair['NUM_BUY_GRID_LINES']):
        response = exchange.create_order(
            symbol=pair['SYMBOL'],
            type='limit',
            side='buy',
            amount=pair['POSITION_SIZE'],
            price=initial_price - (pair['GRID_SIZE'] * (i+1)),
            params={
                'postOnly': True
            }
        )
        print(response)

    # Place sell grid lines
    for i in range(pair['NUM_SELL_GRID_LINES']):
        response = exchange.create_order(
            symbol=pair['SYMBOL'],
            type='limit',
            side='sell',
            amount=pair['POSITION_SIZE'],
            price=initial_price + (pair['GRID_SIZE'] * (i+1)),
            params={
                'postOnly': True
            }
        )
        print(response)

    # print(ticker)