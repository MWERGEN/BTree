import csv

data = [
    (1, 1),
    (1, 2),
    (1, 12),
    (1, 13),
    (1, 14),
    (1, 15),
    (1, 16),
    (1, 17),
    (1, 18),
    (1, 19),
    (1, 20),
    (1, 14),
    (1, 15)
]

filename = 'data.csv'

with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

print("CSV file created successfully.")
