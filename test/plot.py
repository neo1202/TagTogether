import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('checkin_log.csv')

# Calculate the cumulative sum of the count
df['cumulative_count'] = df['count'].cumsum()

# Convert timestamp to a more readable format if needed
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(df['timestamp'], df['cumulative_count'], marker='o')
plt.title('Total Count of User Checkin Over Time')
plt.xlabel('Timestamp')
plt.ylabel('Cumulative Count')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()