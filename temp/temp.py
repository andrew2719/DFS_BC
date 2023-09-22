import datetime

# Sample data (you should replace this with your own data)
failure_events = [
    {"timestamp": "2023-09-22 08:00:00", "event_type": "corruption"},
    {"timestamp": "2023-09-23 12:30:00", "event_type": "loss"},
    # Add more failure events here
]

# Calculate the failure rate for a specific time period
def calculate_failure_rate(data, start_date, end_date):
    total_failures = 0
    total_opportunities = 0

    for event in data:
        timestamp = datetime.datetime.strptime(event["timestamp"], "%Y-%m-%d %H:%M:%S")

        # Check if the event falls within the specified time period
        if start_date <= timestamp <= end_date:
            total_failures += 1

        total_opportunities += 1

    failure_rate = (total_failures / total_opportunities) * 100
    return failure_rate

# Specify the time period for which you want to calculate the failure rate
start_date = datetime.datetime.strptime("2023-09-01 00:00:00", "%Y-%m-%d %H:%M:%S")
end_date = datetime.datetime.strptime("2023-09-30 23:59:59", "%Y-%m-%d %H:%M:%S")

# Calculate the failure rate for the specified time period
failure_rate = calculate_failure_rate(failure_events, start_date, end_date)

# Print the failure rate
print(f"Failure Rate for {start_date} to {end_date}: {failure_rate:.2f}%")
