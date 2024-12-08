from policy import Policy

class Policy2210xxx(Policy):
    def __init__(self):
        super().__init__()
        

    def get_action(self, observation, info):
        """
        Implements the improved Greedy algorithm to maximize the filled ratio.
        Args:
            observation: Dictionary with current state of stocks and demands.
            info: Additional environment details.
        Returns:
            Dictionary representing the action to take.
        """
        stocks = observation['stocks']
        demands = observation['products']

        
        for demand_idx, demand in enumerate(demands):
            demand_size = demand['size']  
            quantity = demand['quantity']

            
            if quantity <= 0:
                continue

            
            best_stock_idx, best_position = None, None
            for stock_idx, stock in enumerate(stocks):
                position = self.find_position(stock, demand_size)
                if position:
                    best_stock_idx = stock_idx
                    best_position = position
                    break  

            
            if best_stock_idx is not None:
                return {
                    "stock_idx": best_stock_idx,
                    "size": demand_size,
                    "position": best_position
                }

        
        return {"stock_idx": 0, "size": (0, 0), "position": (0, 0)}

    def find_position(self, stock, demand_size):
        """
        Find the first available position in the stock where the demand can fit.
        Args:
            stock: 2D numpy array representing the stock.
            demand_size: Tuple (length, width) of the demand.
        Returns:
            Tuple (x, y) indicating the position, or None if no position is available.
        """
        stock_length, stock_width = stock.shape
        demand_length, demand_width = demand_size

        for i in range(stock_length - demand_length + 1):
            for j in range(stock_width - demand_width + 1):
                if self.can_place(stock, (i, j), demand_size):
                    return (i, j)
        return None

    def can_place(self, stock, position, demand_size):
        """
        Check if the demand can be placed at the given position in the stock.
        Args:
            stock: 2D numpy array representing the stock.
            position: Tuple (x, y) indicating the top-left corner.
            demand_size: Tuple (length, width) of the demand.
        Returns:
            Boolean indicating whether the demand can be placed.
        """
        x, y = position
        demand_length, demand_width = demand_size

        for i in range(demand_length):
            for j in range(demand_width):
                if stock[x + i][y + j] != -1:  
                    return False
        return True
