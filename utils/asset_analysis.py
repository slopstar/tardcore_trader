from typing import Optional

def check_dillution(market_cap: float, fully_diluted_market_cap: Optional[float]) -> bool:
    """
    Check if an asset shows signs of value dilution.
    
    Args:
        market_cap: Current market capitalization
        fully_diluted_market_cap: Fully diluted market capitalization (can be None)
    
    Returns:
        True if dilution detected, False otherwise
    """
    # Check if fully diluted market cap is significantly higher than current
    if fully_diluted_market_cap and market_cap:
        dilution_ratio: float = fully_diluted_market_cap / market_cap
        if dilution_ratio > 1.5:  # More than 50% potential dilution
            return True
    
    return False