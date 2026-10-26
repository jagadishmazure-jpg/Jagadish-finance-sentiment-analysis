"""Cost / budget inputs. Negative amounts are rejected, never clamped.

Clamping a negative to zero would hide an upstream sign error and
understate spend. Raising keeps the error visible at the call site.
"""


class NegativeCostError(ValueError):
    pass


def validate_cost(amount):
    if amount is None:
        raise ValueError("cost must not be None")
    if amount < 0:
        raise NegativeCostError(f"cost must not be negative, got {amount}")
    return amount


class Budget:
    def __init__(self, limit):
        self.limit = validate_cost(limit)
        self.spent = 0.0

    def add(self, amount):
        validate_cost(amount)
        self.spent += amount
        return self.spent

    def remaining(self):
        return self.limit - self.spent

    def over_budget(self):
        return self.spent > self.limit
