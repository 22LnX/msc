import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Load your data
file_path = "/mnt/shared/projects/nhm/clark-student/WeeklyGardenSampling/WeeklyGardenSampling/bubble/combined_phylum_frequencies_by_season.csv"
df = pd.read_csv(file_path)

# Remove 'Chlorophyta' from the data
df = df[df['Phylum'] != 'Chlorophyta']

# Set figure size
plt.figure(figsize=(20, 26))

# Calculate bubble sizes
max_blast = df[df['FileType'] == 'Blast']['Frequency'].max()
max_diamond = df[df['FileType'] == 'Diamond']['Frequency'].max()
bubble_size_blast = (df[df['FileType'] == 'Blast']['Frequency'] / max_blast) * 3000
bubble_size_diamond = (df[df['FileType'] == 'Diamond']['Frequency'] / max_diamond) * 3000

# Phylum position offset
phylum_list = sorted(df['Phylum'].unique())
phylum_offset = {phylum: i for i, phylum in enumerate(phylum_list)}

# Plot BLAST bubbles
blast_df = df[df['FileType'] == 'Blast']
plt.scatter(
    blast_df['Season'],
    blast_df['Phylum'].apply(lambda x: phylum_offset[x]),
    s=bubble_size_blast,
    alpha=0.5,
    label='BLAST',
    color='blue'
)

# Plot DIAMOND bubbles
diamond_df = df[df['FileType'] == 'Diamond']
plt.scatter(
    diamond_df['Season'],
    diamond_df['Phylum'].apply(lambda x: phylum_offset[x] + 0.3),
    s=bubble_size_diamond,
    alpha=0.5,
    label='DIAMOND',
    color='red'
)

# Annotate frequencies
for i, row in blast_df.iterrows():
    plt.annotate(f'{int(row["Frequency"])}', 
                 (row['Season'], phylum_offset[row['Phylum']]),
                 textcoords="offset points", 
                 xytext=(0, 10), 
                 ha='center', 
                 fontsize=14, 
                 color='darkblue', 
                 weight='bold')

for i, row in diamond_df.iterrows():
    plt.annotate(f'{int(row["Frequency"])}', 
                 (row['Season'], phylum_offset[row['Phylum']] + 0.3), 
                 textcoords="offset points", 
                 xytext=(0, 10), 
                 ha='center', 
                 fontsize=14, 
                 color='black', 
                 weight='bold')

# Add labels and title
plt.xlabel('Season', fontsize=16, fontweight='bold')
plt.ylabel('Phylum', fontsize=16, fontweight='bold')
plt.title('Phylum Frequencies by Season: BLAST vs DIAMOND', fontsize=18, fontweight='bold')

# Adjust axis labels
plt.xticks(fontsize=18, fontweight='bold')
plt.yticks(ticks=range(len(phylum_list)), labels=phylum_list, fontsize=18, fontweight='bold',)
plt.subplots_adjust(left=0.2, right=0.8, top=0.9, bottom=0.3)

# Legend
legend_blast = mpatches.Patch(color='blue', alpha=0.5, label='BLAST')
legend_diamond = mpatches.Patch(color='red', alpha=0.5, label='DIAMOND')
plt.legend(handles=[legend_blast, legend_diamond], loc='center left', bbox_to_anchor=(1, 0.95), fontsize=14)

# Display grid
plt.grid(True)

# Save plot
output_path = "/mnt/shared/projects/nhm/clark-student/WeeklyGardenSampling/WeeklyGardenSampling/bubble/phylum_frequencies_by_season_filtered.png"
plt.savefig(output_path, format='png', dpi=300)
plt.show()

