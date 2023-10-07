start_sum = 600
increase_per_month = 360
annual_income_percent = 0.12
month_income_percent = annual_income_percent / 12
period_in_month = 24
current_sum = start_sum

for month in range(1, period_in_month+1):
    # current_sum += current_sum*month_income_percent
    current_sum += increase_per_month
print(current_sum)
