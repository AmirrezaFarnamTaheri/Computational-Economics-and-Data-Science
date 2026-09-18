def calculate_pv(fv, r, n):
    """Return the present value of a future cash flow after n periods."""
    return fv / (1 + r) ** n
