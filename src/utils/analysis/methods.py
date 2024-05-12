import csv

"""
Manually include arrays for each flexible and inflexible methods
"""

# Implementation methods
inflexible_50 = ["inflexible_50", 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
inflexible_60 = ["inflexible_60", 60, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
flexible_30_0 = ["flexible_30_0", 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
flexible_30_10 = ["flexible_30_10", 30, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
flexible_30_20 = ["flexible_30_20", 30, 0, 0, 0, 0, 0, 0, 0, 0, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
flexible_40_0 = ["flexible_40_0", 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
flexible_40_10 = ["flexible_40_10", 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
flexible_40_20 = ["flexible_40_20", 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

data = [
    inflexible_50,
    inflexible_60,
    flexible_30_0,
    flexible_30_10,
    flexible_30_20,
    flexible_40_0,
    flexible_40_10,
    flexible_40_20
]

filename = "src/utils/data/raw/implementation_methods.csv"

with open(filename, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)