"""
Robinhood Trading API Client using robin-stocks

A simplified wrapper around the robin-stocks library for easier usage.
This module provides a clean interface for common trading operations.
"""

import os
import robin_stocks as r
from loguru import logger
from dotenv import load_dotenv
from typing import Dict, List, Optional, Any

# Load environment variables
load_dotenv()


class RobinhoodTrader:
    """Simplified wrapper for robin-stocks library"""
    
    def __init__(self):
        """Initialize the Robinhood trader client"""
        self.username = os.getenv('ROBINHOOD_USERNAME')
        self.password = os.getenv('ROBINHOOD_PASSWORD')
        self.mfa_code = os.getenv('ROBINHOOD_MFA_CODE')
        
        self.is_authenticated = False
        
        logger.info("RobinhoodTrader initialized with robin-stocks")

    def login(self) -> bool:
        """
        Authenticate with Robinhood API using robin-stocks
        
        Returns:
            bool: True if login successful, False otherwise
        """
        if not self.username or not self.password:
            logger.error("Username and password must be set in environment variables")
            return False
            
        try:
            # Login using robin-stocks
            if self.mfa_code:
                login_response = r.login(self.username, self.password, mfa_code=self.mfa_code)
            else:
                login_response = r.login(self.username, self.password)
            
            if login_response:
                self.is_authenticated = True
                logger.info("Successfully authenticated with Robinhood using robin-stocks")
                return True
            else:
                logger.error("Authentication failed")
                return False
                
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return False

    def get_account(self) -> Optional[Dict[str, Any]]:
        """
        Get account information
        
        Returns:
            Dict: Account information or None if failed
        """
        if not self.is_authenticated:
            logger.error("Must be authenticated to get account info")
            return None
            
        try:
            account_info = r.account.build_user_profile()
            logger.info("Successfully retrieved account information")
            return account_info
        except Exception as e:
            logger.error(f"Error getting account info: {str(e)}")
            return None

    def get_portfolio(self) -> List[Dict[str, Any]]:
        """
        Get current portfolio positions
        
        Returns:
            List[Dict]: List of current positions
        """
        if not self.is_authenticated:
            logger.error("Must be authenticated to get portfolio")
            return []
            
        try:
            positions = r.account.get_open_stock_positions()
            logger.info(f"Retrieved {len(positions)} positions")
            return positions
        except Exception as e:
            logger.error(f"Error getting portfolio: {str(e)}")
            return []

    def get_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Get current quote for a symbol
        
        Args:
            symbol (str): Stock symbol
            
        Returns:
            Dict: Quote data or None if failed
        """
        if not self.is_authenticated:
            logger.error("Must be authenticated to get quotes")
            return None
            
        try:
            quote = r.stocks.get_latest_price(symbol, includeExtendedHours=True)
            if quote:
                return quote[0] if isinstance(quote, list) else quote
            return None
        except Exception as e:
            logger.error(f"Error getting quote for {symbol}: {str(e)}")
            return None

    def get_stock_info(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed stock information
        
        Args:
            symbol (str): Stock symbol
            
        Returns:
            Dict: Stock information or None if failed
        """
        if not self.is_authenticated:
            logger.error("Must be authenticated to get stock info")
            return None
            
        try:
            stock_info = r.stocks.get_instruments_by_symbols(symbol)
            if stock_info:
                return stock_info[0] if isinstance(stock_info, list) else stock_info
            return None
        except Exception as e:
            logger.error(f"Error getting stock info for {symbol}: {str(e)}")
            return None

    def place_market_order(self, symbol: str, quantity: int, side: str) -> Optional[Dict[str, Any]]:
        """
        Place a market order
        
        Args:
            symbol (str): Stock symbol
            quantity (int): Number of shares
            side (str): 'buy' or 'sell'
            
        Returns:
            Dict: Order response or None if failed
        """
        if not self.is_authenticated:
            logger.error("Must be authenticated to place orders")
            return None
            
        try:
            order = r.orders.order_buy_market(symbol, quantity) if side.lower() == 'buy' else r.orders.order_sell_market(symbol, quantity)
            if order:
                logger.info(f"Market {side} order placed successfully for {quantity} shares of {symbol}")
                return order
            return None
        except Exception as e:
            logger.error(f"Error placing market order: {str(e)}")
            return None

    def place_limit_order(self, symbol: str, quantity: int, side: str, price: float) -> Optional[Dict[str, Any]]:
        """
        Place a limit order
        
        Args:
            symbol (str): Stock symbol
            quantity (int): Number of shares
            side (str): 'buy' or 'sell'
            price (float): Limit price
            
        Returns:
            Dict: Order response or None if failed
        """
        if not self.is_authenticated:
            logger.error("Must be authenticated to place orders")
            return None
            
        try:
            order = r.orders.order_buy_limit(symbol, quantity, price) if side.lower() == 'buy' else r.orders.order_sell_limit(symbol, quantity, price)
            if order:
                logger.info(f"Limit {side} order placed successfully for {quantity} shares of {symbol} at ${price}")
                return order
            return None
        except Exception as e:
            logger.error(f"Error placing limit order: {str(e)}")
            return None

    def get_order_history(self) -> List[Dict[str, Any]]:
        """
        Get order history
        
        Returns:
            List[Dict]: List of past orders
        """
        if not self.is_authenticated:
            logger.error("Must be authenticated to get order history")
            return []
            
        try:
            orders = r.orders.get_all_stock_orders()
            logger.info(f"Retrieved {len(orders)} orders")
            return orders
        except Exception as e:
            logger.error(f"Error getting order history: {str(e)}")
            return []

    def get_open_orders(self) -> List[Dict[str, Any]]:
        """
        Get open orders
        
        Returns:
            List[Dict]: List of open orders
        """
        if not self.is_authenticated:
            logger.error("Must be authenticated to get open orders")
            return []
            
        try:
            orders = r.orders.get_all_open_stock_orders()
            logger.info(f"Retrieved {len(orders)} open orders")
            return orders
        except Exception as e:
            logger.error(f"Error getting open orders: {str(e)}")
            return []

    def cancel_order(self, order_id: str) -> bool:
        """
        Cancel an order
        
        Args:
            order_id (str): Order ID to cancel
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.is_authenticated:
            logger.error("Must be authenticated to cancel orders")
            return False
            
        try:
            result = r.orders.cancel_stock_order(order_id)
            if result:
                logger.info(f"Order {order_id} cancelled successfully")
                return True
            return False
        except Exception as e:
            logger.error(f"Error cancelling order {order_id}: {str(e)}")
            return False

    def get_watchlist(self) -> List[Dict[str, Any]]:
        """
        Get watchlist
        
        Returns:
            List[Dict]: List of watchlist items
        """
        if not self.is_authenticated:
            logger.error("Must be authenticated to get watchlist")
            return []
            
        try:
            watchlist = r.account.get_watchlist_by_name('Default')
            logger.info(f"Retrieved {len(watchlist)} items from watchlist")
            return watchlist
        except Exception as e:
            logger.error(f"Error getting watchlist: {str(e)}")
            return []

    def add_to_watchlist(self, symbol: str) -> bool:
        """
        Add symbol to watchlist
        
        Args:
            symbol (str): Stock symbol to add
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.is_authenticated:
            logger.error("Must be authenticated to modify watchlist")
            return False
            
        try:
            result = r.account.add_symbol_to_watchlist(symbol)
            if result:
                logger.info(f"Added {symbol} to watchlist")
                return True
            return False
        except Exception as e:
            logger.error(f"Error adding {symbol} to watchlist: {str(e)}")
            return False

    def get_historical_data(self, symbol: str, interval: str = 'day', span: str = 'year') -> Optional[List[Dict[str, Any]]]:
        """
        Get historical price data
        
        Args:
            symbol (str): Stock symbol
            interval (str): '5minute', '10minute', 'hour', 'day', 'week'
            span (str): 'day', 'week', 'month', '3month', 'year', '5year', 'all'
            
        Returns:
            List[Dict]: Historical data or None if failed
        """
        if not self.is_authenticated:
            logger.error("Must be authenticated to get historical data")
            return None
            
        try:
            data = r.stocks.get_stock_historicals(symbol, interval=interval, span=span)
            logger.info(f"Retrieved historical data for {symbol}")
            return data
        except Exception as e:
            logger.error(f"Error getting historical data for {symbol}: {str(e)}")
            return None

    def logout(self):
        """Logout and clear authentication"""
        try:
            r.logout()
            self.is_authenticated = False
            logger.info("Logged out successfully")
        except Exception as e:
            logger.error(f"Error during logout: {str(e)}")