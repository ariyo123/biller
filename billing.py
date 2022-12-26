# import the necessary libraries
import csv

# define the data that needs to be included in the report
data = [
    {"service": "Consultation", "date": "2022-01-01", "cost": 100.00, "discount": 0.10},
    {"service": "Training", "date": "2022-01-02", "cost": 200.00, "discount": 0.00},
    {"service": "Support", "date": "2022-01-03", "cost": 150.00, "discount": 0.05},
]

# calculate the total cost and total discount
total_cost = 0
total_discount = 0
for entry in data:
    total_cost += entry["cost"]
    total_discount += entry["cost"] * entry["discount"]

# output the report to a CSV file
with open("billing_report.csv", "w", newline="") as csvfile:
    fieldnames = ["service", "date", "cost", "discount"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for entry in data:
        writer.writerow(entry)

    writer.writerow({"service": "Total", "date": "", "cost": total_cost, "discount": total_discount})
