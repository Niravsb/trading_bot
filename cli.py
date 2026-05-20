import argparse
from dotenv import load_dotenv
from bot.client import get_binance_client
from bot.validators import validate_order_inputs
from bot.orders import place_order
from bot.logging_config import logger

def main():
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")
    parser.add_argument('--symbol', required=True, type=str, help="Trading pair symbol (e.g., BTCUSDT)")
    parser.add_argument('--side', required=True, type=str, choices=['BUY', 'SELL'], help="Order side: BUY or SELL")
    # ADDED 'STOP' to the choices
    parser.add_argument('--type', required=True, type=str, choices=['MARKET', 'LIMIT', 'STOP'], dest='order_type', help="Order type: MARKET, LIMIT, or STOP")
    parser.add_argument('--qty', required=True, type=float, help="Quantity to trade")
    parser.add_argument('--price', type=float, help="Limit Price (Required for LIMIT and STOP orders)")
    # ADDED new argument for stop price
    parser.add_argument('--stop-price', type=float, dest='stop_price', help="Trigger Price (Required for STOP orders)")

    args = parser.parse_args()
    load_dotenv()

    try:
        logger.info("--- New Order Request Summary ---")
        logger.info(f"Symbol: {args.symbol.upper()}, Side: {args.side}, Type: {args.order_type}, Qty: {args.qty}, Price: {args.price}, Stop Price: {args.stop_price}")
        
        # 1. Validate Input (passing the new stop_price)
        validate_order_inputs(args.symbol.upper(), args.side, args.order_type, args.qty, args.price, args.stop_price)
        
        # 2. Get Client
        client = get_binance_client()
        
        # 3. Place Order (passing the new stop_price)
        place_order(client, args.symbol.upper(), args.side, args.order_type, args.qty, args.price, args.stop_price)
        
    except ValueError as e:
        logger.error(f"Order failed due to validation error: {e}")
    except Exception as e:
        logger.error(f"Order failed due to an unexpected application error: {e}")

if __name__ == "__main__":
    main()