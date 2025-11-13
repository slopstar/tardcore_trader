from typing import Dict, Any, List

def check_dillution(log_data: Dict[str, Any]) -> bool:
    """
    Check if holdings show signs of value dilution.
    
    Args:
        log_data: Deserialized JSON log containing holdings and market data
    
    Returns:
        True if dilution detected, False otherwise
    """
    holdings: List[Dict[str, Any]] = log_data.get("holdings", [])
    
    for holding in holdings:
        symbol = holding["symbol"]
        market_cap = holding["usd_quote"]["market_cap"]
        fully_diluted_cap = holding["usd_quote"]["fully_diluted_market_cap"]
        
        # Check if fully diluted market cap is significantly higher than current
        if fully_diluted_cap and market_cap:
            dilution_ratio: float = fully_diluted_cap / market_cap
            if dilution_ratio > 1.5:  # More than 50% potential dilution
                print(f"{symbol}: {dilution_ratio:.2f}x dilution potential")
                return True
    
    return False