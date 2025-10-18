def calculate_pv(fv, r, n):
    """Calculates the Present Value of a single future cash flow."""
    # Fix: Correct parentheses for order of operations
    return fv / (1 + r) ** n
