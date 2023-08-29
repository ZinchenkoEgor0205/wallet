start = 6
day_percent = 0.19 / (365 // 21)

for i in range(365 // 21):
    start += start * day_percent

print(start)