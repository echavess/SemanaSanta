import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta

def easter_date(year):
    "Return Easter as a date object."
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19*a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2*e + 2*i - h - k) % 7
    m = (a + 11*h + 22*l) // 451
    month = (h + l - 7*m + 114) // 31
    day = ((h + l - 7*m + 114) % 31) + 1
    return date(year, month, day)

# Load and parse the earthquake catalog
file_path = 'generalseismicity.event.cat'
earthquake_data_initial = pd.read_csv(file_path, header=None)
earthquake_data_parsed = earthquake_data_initial[0].str.extract(r'(?P<Date>\d{8}) (?P<Time>\d{6})\d{2}')
earthquake_data_parsed['Date'] = pd.to_datetime(earthquake_data_parsed['Date'], format='%Y%m%d')
earthquake_data_parsed['Time'] = earthquake_data_parsed['Time'].str.slice(start=0, stop=2) + ':' + earthquake_data_parsed['Time'].str.slice(start=2, stop=4) + ':' + earthquake_data_parsed['Time'].str.slice(start=4, stop=6)

def count_earthquakes_during_holy_week_fixed(year, earthquake_data):
    easter = pd.to_datetime(easter_date(year))
    palm_sunday = easter - pd.to_timedelta(7, unit='days')
    holy_saturday = easter - pd.to_timedelta(1, unit='days')
    earthquakes_during_holy_week = earthquake_data[(earthquake_data['Date'] >= palm_sunday) & (earthquake_data['Date'] <= holy_saturday)]
    return len(earthquakes_during_holy_week)

# Calculate earthquake counts for Holy Weeks from 2010 to 2024
years = range(2010, 2025)
earthquake_counts = {year: count_earthquakes_during_holy_week_fixed(year, earthquake_data_parsed) for year in years}

# Convert to DataFrame for plotting
earthquake_counts_df = pd.DataFrame(list(earthquake_counts.items()), columns=['Year', 'Earthquake Count']).sort_values(by='Year')

# Plotting with annotations
fig = plt.figure(figsize=(12, 6))
plt.plot(earthquake_counts_df['Year'], earthquake_counts_df['Earthquake Count'], marker='o', linestyle='-', color='blue')
plt.title('Conteo de Sismos Durante la Semana Santa en Costa Rica (2010-2024)',fontsize=25)
plt.xlabel('Año',fontsize=30)
plt.ylabel('Número de Sismos',fontsize=30)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.xticks(earthquake_counts_df['Year'], rotation=45)

for i, txt in enumerate(earthquake_counts_df['Earthquake Count']):
    plt.annotate(txt, (earthquake_counts_df['Year'].iloc[i], earthquake_counts_df['Earthquake Count'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center')


# Define a function to compare earthquake counts during Holy Week, the week before, and the week after
def compare_earthquakes_around_holy_week(year, earthquake_data):
    easter = pd.to_datetime(easter_date(year))
    palm_sunday = easter - pd.to_timedelta(7, unit='days')
    holy_saturday = easter - pd.to_timedelta(1, unit='days')
    
    # Define the period for the week before and after Holy Week
    week_before_start = palm_sunday - pd.to_timedelta(7, unit='days')
    week_before_end = palm_sunday - pd.to_timedelta(1, unit='days')
    week_after_start = holy_saturday + pd.to_timedelta(1, unit='days')
    week_after_end = holy_saturday + pd.to_timedelta(7, unit='days')
    
    # Count earthquakes during these periods
    earthquakes_during_holy_week = len(earthquake_data[(earthquake_data['Date'] >= palm_sunday) & (earthquake_data['Date'] <= holy_saturday)])
    earthquakes_week_before = len(earthquake_data[(earthquake_data['Date'] >= week_before_start) & (earthquake_data['Date'] <= week_before_end)])
    earthquakes_week_after = len(earthquake_data[(earthquake_data['Date'] >= week_after_start) & (earthquake_data['Date'] <= week_after_end)])
    
    return earthquakes_week_before, earthquakes_during_holy_week, earthquakes_week_after

# Calculate the comparison for each year from 2010 to 2023
earthquake_comparison = {year: compare_earthquakes_around_holy_week(year, earthquake_data_parsed) for year in range(2010, 2024)}

# Convert to DataFrame for easier handling
earthquake_comparison_df = pd.DataFrame.from_dict(earthquake_comparison, orient='index', columns=['Week Before', 'Holy Week', 'Week After'])

# Plotting the comparison using a bar plot
fig2 = plt.figure(figsize=(14, 8))

# Position of the bars on the x-axis
ind = list(range(len(earthquake_comparison_df)))

# Width of a bar 
width = 0.25       

plt.bar(ind, earthquake_comparison_df['Week Before'], width, label='Semana previa', color='blue')
plt.bar([p + width for p in ind], earthquake_comparison_df['Holy Week'], width, label='Semana Santa', color='red')
plt.bar([p + width*2 for p in ind], earthquake_comparison_df['Week After'], width, label='Semana posterior', color='green')

plt.xlabel('Año', fontsize=30)
plt.ylabel('Número de sismos',fontsize=30)
plt.title('Cantidad de sismos una semana antes, Durante, and una semana después de semana santa (2010-2023)',fontsize=25)

# Adding the legend and setting the position of the x-ticks
plt.legend(loc='upper left')
plt.xticks([p + width for p in ind], earthquake_comparison_df.index)




plt.tight_layout()
plt.show()
fig.savefig("Sismos_Semanas_Santas.png", format='png', dpi=800)
fig2.savefig("Sismos_Semanas_Santas_comparasion.png", format='png', dpi=800)
