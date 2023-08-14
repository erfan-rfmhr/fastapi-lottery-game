import random


async def perform_lottery():
    prizes = ['A', 'B', 'C', 'D', 'E']
    weights = [0.1, 0.3, 0.2, 0.15, 0.25]
    return random.choices(prizes, weights=weights, k=1)[0]
