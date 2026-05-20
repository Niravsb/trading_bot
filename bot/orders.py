from binance.exceptions import BinanceAPIException, BinanceRequestException
from bot.logging_config import logger

# Added stop_price parameter
def place_order(client, symbol, side, order_type, quantity, price=None, stop_price=None):
    logger.info(f"Preparing to place {order_type} order to {side} {quantity} {symbol}.")
    
    try:
        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity
        }
        
        if order_type == 'LIMIT':
            params['timeInForce'] = 'GTC'
            params['price'] = price
            
        # ADDED payload construction for STOP orders
        elif order_type == 'STOP':
            params['timeInForce'] = 'GTC'
            params['price'] = price
            params['stopPrice'] = stop_price
            
        logger.info(f"API Request Payload: {params}")
        response = client.futures_create_order(**params)
        
        logger.info("Order successfully placed!")
        logger.info(f"Order ID: {response.get('orderId')}")
        logger.info(f"Status: {response.get('status')}")
        logger.info(f"Executed Qty: {response.get('executedQty')}")
        
        return response
        
    except BinanceAPIException as e:
        logger.error(f"Binance API Exception: {e.status_code} - {e.message}")
    except BinanceRequestException as e:
        logger.error(f"Network/Request Exception: {e}")
    except Exception as e:
        logger.error(f"Unexpected Error: {e}")