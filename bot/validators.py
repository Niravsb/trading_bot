from bot.logging_config import logger

# Added stop_price to parameters with a default of None
def validate_order_inputs(symbol, side, order_type, quantity, price=None, stop_price=None):
    if side not in ['BUY', 'SELL']:
        logger.error(f"Validation Error: Invalid side '{side}'. Must be BUY or SELL.")
        raise ValueError("Side must be BUY or SELL")
        
    # Added 'STOP' to valid types
    if order_type not in ['MARKET', 'LIMIT', 'STOP']:
        logger.error(f"Validation Error: Invalid order type '{order_type}'.")
        raise ValueError("Order type must be MARKET, LIMIT, or STOP")
        
    if quantity <= 0:
        logger.error("Validation Error: Quantity must be greater than 0.")
        raise ValueError("Quantity must be greater than 0")
        
    if order_type == 'LIMIT' and (price is None or price <= 0):
        logger.error("Validation Error: Price is required and must be > 0 for LIMIT orders.")
        raise ValueError("Price is required for LIMIT orders")

    # ADDED logic for STOP order validation
    if order_type == 'STOP':
        if price is None or price <= 0:
            logger.error("Validation Error: Limit Price is required for STOP orders.")
            raise ValueError("Limit Price is required for STOP orders")
        if stop_price is None or stop_price <= 0:
            logger.error("Validation Error: Stop Price (trigger) is required for STOP orders.")
            raise ValueError("Stop Price is required for STOP orders")
        
    return True