# Given the percentage decrease over a longer period (45 years) and needing to find the equivalent annual rate
total_decrease_45_years = 0.515  # as a decimal
total_years_long = 45

# Calculate the equivalent annual decrease rate using the compound interest formula
equivalent_annual_rate = (1 - total_decrease_45_years) ** (1 / total_years_long) - 1

# Now calculate what the value would be over 10 years using this equivalent annual rate
remaining_effectiveness_10_years_from_45 = (1 + equivalent_annual_rate) ** 10

# Convert the remaining effectiveness to percentage decrease over 10 years
decrease_10_years = 1 - remaining_effectiveness_10_years_from_45
decrease_10_years_percentage = decrease_10_years * 100

print(equivalent_annual_rate, decrease_10_years_percentage)