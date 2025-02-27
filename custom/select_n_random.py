import random

def select_n_random(n_items, n):
    """Return n integers randomly selected from n_items. Starts from 0, without duplicate values."""
    if n > n_items:
        raise ValueError("n cannot be bigger than n_items!")
    return random.sample(range(n_items), n)