import pandas as pd
import matplotlib.pyplot as plt

# Load the file
file_path = 'last_events_detected_saved_Enero102024.dat'
df = pd.read_csv(file_path, header=None, names=['Event ID', 'Event Time'])

# Assuming the format is 'Event ID' followed by 'Event Time' in each row, separated by a space
df[['Event ID', 'Event Time']] = df['Event ID'].str.split(' ', expand=True)

# Convert the 'Event Time' to datetime format
df['Event Time'] = pd.to_datetime(df['Event Time'])

# Set 'Event Time' as the index
df.set_index('Event Time', inplace=True)

# Resample to count the number of events per day
events_per_day = df.resample('D').count()

# Define a color map for different years
colors = {2022: 'blue', 2023: 'green', 2024: 'red'}

# Plot the time series of the number of events
fig = plt.figure(figsize=(12, 6))

events_per_day['Event ID'].plot(kind='line', marker='o', linestyle='-', markeredgecolor='k', lw=0.5)

plt.title('Number of automatic events communicated by Earthbeat-OVSICORI\nper Day from January 2022 to January 2024')
plt.xlabel('Date')
plt.ylabel('Number of Events')

# Setting x-axis limits from January 2022 to January 2024
plt.xlim(pd.Timestamp('2022-01-01'), pd.Timestamp('2024-01-31'))

plt.tight_layout()
plt.show()
fig.savefig("Publicaciones_automaticas_sismos.png", format='png', dpi=600)
