start = 15
income_rate = 0.19
period_length = 21
periods_per_year = 365 / period_length
period_percent = income_rate / periods_per_year
day_percent = income_rate / 365

# for i in range(365 // 21):
#     start += start * period_percent

# for i in range(365):
#     start += start * day_percent

# print(start)
result = (1 + (income_rate / periods_per_year))**(periods_per_year*1) - 1
print(result/1)
