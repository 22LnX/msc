import pandas as pd

# Load the datasets
blast_df = pd.read_csv('/mnt/shared/home/lxu/sample_data/WeeklyGardenSampling/bubble/top10_Blast_phylum_frequencies_aggregated.csv', header=None, names=['Phylum', 'Season', 'Kingdom', 'FileType', 'Frequency'])
diamond_df = pd.read_csv('/mnt/shared/home/lxu/sample_data/WeeklyGardenSampling/bubble/top10_Diamond_phylum_frequencies_aggregated.csv', header=None, names=['Phylum', 'Season', 'Kingdom', 'FileType', 'Frequency'])

# Convert Frequency to integers
blast_df['Frequency'] = blast_df['Frequency'].astype(int)
diamond_df['Frequency'] = diamond_df['Frequency'].astype(int)

# Group by Phylum and Season, then sum the frequencies
blast_grouped = blast_df.groupby(['Phylum', 'Season'])['Frequency'].sum().reset_index()
diamond_grouped = diamond_df.groupby(['Phylum', 'Season'])['Frequency'].sum().reset_index()

# Add a column to identify the data source
blast_grouped['FileType'] = 'Blast'
diamond_grouped['FileType'] = 'Diamond'

# Combine the two datasets
combined_df = pd.concat([blast_grouped, diamond_grouped])

# Save the combined dataframe to a new CSV file
output_path = '/mnt/shared/home/lxu/sample_data/WeeklyGardenSampling/bubble/combined_phylum_frequencies_by_season.csv'
combined_df.to_csv(output_path, index=False)

print(f"Combined data saved to {output_path}")





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








import os
import pandas as pd
import matplotlib.pyplot as plt

# 文件路径
blast_files = {
    'Spring': '/mnt/shared/projects/nhm/clark-student/WeeklyGardenSampling/WeeklyGardenSampling/taxname_by_season/Spring_kingdom_frequency.csv',
    'Summer': '/mnt/shared/projects/nhm/clark-student/WeeklyGardenSampling/WeeklyGardenSampling/taxname_by_season/Summer_kingdom_frequency.csv',
    'Autumn': '/mnt/shared/projects/nhm/clark-student/WeeklyGardenSampling/WeeklyGardenSampling/taxname_by_season/Autumn_kingdom_frequency.csv',
    'Winter': '/mnt/shared/projects/nhm/clark-student/WeeklyGardenSampling/WeeklyGardenSampling/taxname_by_season/Winter_kingdom_frequency.csv'
}

diamond_files = {
    'Spring': '/mnt/shared/projects/nhm/clark-student/WeeklyGardenSampling/WeeklyGardenSampling/diamond_top_hits_by_season/Spring_kingdom_frequency.csv',
    'Summer': '/mnt/shared/projects/nhm/clark-student/WeeklyGardenSampling/WeeklyGardenSampling/diamond_top_hits_by_season/Summer_kingdom_frequency.csv',
    'Autumn': '/mnt/shared/projects/nhm/clark-student/WeeklyGardenSampling/WeeklyGardenSampling/diamond_top_hits_by_season/Autumn_kingdom_frequency.csv',
    'Winter': '/mnt/shared/projects/nhm/clark-student/WeeklyGardenSampling/WeeklyGardenSampling/diamond_top_hits_by_season/Winter_kingdom_frequency.csv'
}

# 季节列表
seasons = ['Spring', 'Summer', 'Autumn', 'Winter']

# 需要保留的 Kingdom 列表
valid_kingdoms = ['Viridiplantae', 'Fungi', 'Bacteria', 'Metazoa', 'Heunggongvirae', 'Shotokuvirae']

# 初始化字典来存储频数数据
blast_data = {'Season': [], 'Kingdom': [], 'Count': []}
diamond_data = {'Season': [], 'Kingdom': [], 'Count': []}

# 读取blast数据
for season in seasons:
    file_path = blast_files[season]
    df = pd.read_csv(file_path)
    df = df[df['Kingdom'].isin(valid_kingdoms)]  # 仅保留指定的 Kingdom
    for _, row in df.iterrows():
        blast_data['Season'].append(season)
        blast_data['Kingdom'].append(row['Kingdom'])
        blast_data['Count'].append(row['Count'])

# 读取diamond数据
for season in seasons:
    file_path = diamond_files[season]
    df = pd.read_csv(file_path)
    df = df[df['Kingdom'].isin(valid_kingdoms)]  # 仅保留指定的 Kingdom
    for _, row in df.iterrows():
        diamond_data['Season'].append(season)
        diamond_data['Kingdom'].append(row['Kingdom'])
        diamond_data['Count'].append(row['Count'])

# 将字典转换为DataFrame
blast_df = pd.DataFrame(blast_data)
diamond_df = pd.DataFrame(diamond_data)

# 绘制气泡图
plt.figure(figsize=(20, 16))  # 调整图表大小

# 设置气泡的大小
max_blast = blast_df['Count'].max()
max_diamond = diamond_df['Count'].max()

# 调整大小比例，确保两者在图中比例合理
bubble_size_blast = (blast_df['Count'] / max_blast) * 2500  # 调整大小比例
bubble_size_diamond = (diamond_df['Count'] / max_diamond) * 2500  # 调整大小比例

# 季节位置偏移量
season_offset = {
    'Spring': -0.2,
    'Summer': -0.1,
    'Autumn': 0.1,
    'Winter': 0.2
}

# 绘制BLAST气泡
scatter_blast = plt.scatter(
    blast_df['Season'],
    blast_df['Kingdom'].apply(lambda x: valid_kingdoms.index(x)),
    s=bubble_size_blast,
    alpha=0.5,
    label='BLAST',
    color='blue'
)

# 绘制DIAMOND气泡
scatter_diamond = plt.scatter(
    diamond_df['Season'],
    diamond_df['Kingdom'].apply(lambda x: valid_kingdoms.index(x) + 0.3),
    s=bubble_size_diamond,
    alpha=0.5,
    label='DIAMOND',
    color='red'
)

# 添加频数标签，将数字显示在气泡旁边
for i, row in blast_df.iterrows():
    plt.annotate(f'{row["Count"]}', 
                 (row['Season'], valid_kingdoms.index(row['Kingdom'])),
                 textcoords="offset points", 
                 xytext=(0, 10), 
                 ha='center', 
                 fontsize=14, 
                 color='darkblue', 
                 weight='bold')

for i, row in diamond_df.iterrows():
    plt.annotate(f'{row["Count"]}', 
                 (row['Season'], valid_kingdoms.index(row['Kingdom']) + 0.3), 
                 textcoords="offset points", 
                 xytext=(0, 10), 
                 ha='center', 
                 fontsize=14, 
                 color='black', 
                 weight='bold')

# 添加标签和标题
plt.xlabel('Season', fontsize=16, fontweight='bold')
plt.ylabel('Kingdom', fontsize=16, fontweight='bold')
plt.title('Kingdom Frequencies by Season: BLAST vs DIAMOND', fontsize=18, fontweight='bold')

# 调整 x 轴标签旋转角度
plt.xticks(fontsize=18, fontweight='bold')
plt.yticks(ticks=range(len(valid_kingdoms)), labels=valid_kingdoms, fontsize=18, fontweight='bold')
# 调整子图的边距以确保所有气泡都在图表内
plt.subplots_adjust(left=0.2, right=0.8, top=0.9, bottom=0.3)

# 使用颜色的小长方形来表示图例
import matplotlib.patches as mpatches
legend_blast = mpatches.Patch(color='blue', alpha=0.5, label='BLAST')
legend_diamond = mpatches.Patch(color='red', alpha=0.5, label='DIAMOND')
plt.legend(handles=[legend_blast, legend_diamond], loc='center left', bbox_to_anchor=(1, 0.95), fontsize=14)

# 显示网格
plt.grid(True)

# 保存图表到文件
output_path = "/mnt/shared/projects/nhm/clark-student/WeeklyGardenSampling/WeeklyGardenSampling/bubble/kingdom_frequencies_by_season_filtered_inverted_axes.png"
plt.savefig(output_path, format='png', dpi=300)

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 读取更新后的数据文件
file_path = "/mnt/shared/projects/nhm/clark-student/WeeklyGardenSampling/WeeklyGardenSampling/bubble/kingdom_counts.csv"
df = pd.read_csv(file_path)

# 确保 Kingdom 列中的所有值都是字符串
df['Kingdom'] = df['Kingdom'].astype(str)

# 将 nan 项合并到 Unclassified 并删除 Unclassified
df.loc[df['Kingdom'] == 'Unclassified', 'BLAST'] += df.loc[df['Kingdom'] == 'nan', 'BLAST'].sum()
df.loc[df['Kingdom'] == 'Unclassified', 'DIAMOND'] += df.loc[df['Kingdom'] == 'nan', 'DIAMOND'].sum()
df = df[df['Kingdom'] != 'nan']
df = df[df['Kingdom'] != 'Unclassified']

# 重新调整索引
df.reset_index(drop=True, inplace=True)

# 直接使用已有的Genome_percentage数据
df['Genome_percentage'] = (df['BLAST'] / (df['BLAST'] + df['DIAMOND'])) * 100

# 对数变换 Genome_percentage 数据
df['Genome_log'] = np.log10(df['Genome_percentage'] + 1)

# 计算总和以便计算百分比
total_blast = df['BLAST'].sum()
total_diamond = df['DIAMOND'].sum()

# 计算百分比
df['BLAST_percentage'] = (df['BLAST'] / total_blast) * 100
df['DIAMOND_percentage'] = (df['DIAMOND'] / total_diamond) * 100

# 绘制气泡图
plt.figure(figsize=(25, 10))  # 调整图表大小

# 设置气泡的大小
bubble_size_factor = 1750  # 调整这个值以放大气泡大小
bubble_size_blast = df['BLAST_percentage'] * bubble_size_factor  # 调整大小比例
bubble_size_diamond = df['DIAMOND_percentage'] * bubble_size_factor  # 调整大小比例

# 绘制BLAST气泡
scatter_blast = plt.scatter(df['Kingdom'], df['Genome_log'], s=bubble_size_blast, alpha=0.7, label='BLAST', color='blue')

# 绘制DIAMOND气泡
scatter_diamond = plt.scatter(df['Kingdom'], df['Genome_log'], s=bubble_size_diamond, alpha=0.7, label='DIAMOND', color='red')

# 添加百分比标签，BLAST在上方，DIAMOND在下方
for i in range(len(df)):
    plt.text(df['Kingdom'][i], df['Genome_log'][i] + 0.05, f'{df["BLAST_percentage"][i]:.2f}%', 
             ha='center', va='bottom', fontsize=14, color='darkblue', weight='bold')
    plt.text(df['Kingdom'][i], df['Genome_log'][i] - 0.05, f'{df["DIAMOND_percentage"][i]:.2f}%', 
             ha='center', va='top', fontsize=14, color='black', weight='bold')

# 添加标签和标题
plt.xlabel('Kingdom', fontweight='bold',fontsize=14)
plt.ylabel('Log Transformed Genome Percentage', fontweight='bold', fontsize=12)
plt.title('Kingdom: BLAST vs DIAMOND with Genome Percentage (Log Transformed)', fontsize=14, fontweight='bold')

# 设置 x 和 y 轴的范围
plt.ylim(0, max(df['Genome_log']) * 1.1)  # 根据数据调整范围
plt.xlim(-0.5, len(df['Kingdom']) - 0.5)  # 留一些空间以避免气泡超出边界

# 调整子图的边距以确保所有气泡都在图表内
plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.2)
plt.xticks(fontsize=16, fontweight='bold', rotation=45)
# 使用颜色的小长方形来表示图例
import matplotlib.patches as mpatches
legend_blast = mpatches.Patch(color='blue', alpha=0.5, label='BLAST')
legend_diamond = mpatches.Patch(color='red', alpha=0.5, label='DIAMOND')
plt.legend(handles=[legend_blast, legend_diamond], loc='upper left')

# 显示网格
plt.grid(True)

# 保存图表到文件
output_path = "/mnt/shared/projects/nhm/clark-student/WeeklyGardenSampling/WeeklyGardenSampling/bubble/kingdom_frequencies_genome_percentage_log_transformed.png"
plt.savefig(output_path, format='png', dpi=300)


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 读取更新后的数据文件
file_path = "/mnt/shared/projects/nhm/clark-student/WeeklyGardenSampling/WeeklyGardenSampling/bubble/top20_phylum_counts.csv"
df = pd.read_csv(file_path)

# 确保 Phylum 列中的所有值都是字符串
df['Phylum'] = df['Phylum'].astype(str)

# 重新调整索引
df.reset_index(drop=True, inplace=True)

# 直接使用已有的Genome_Percentage数据
df['Genome_Percentage'] = df['Genome_Percentage'] * 100  # 如果需要将百分比转化为0-100的范围

# 对数变换 Genome_Percentage 数据
df['Genome_log'] = np.log10(df['Genome_Percentage'] + 1)

# 给定的总和
total_blast = 16362659
total_diamond = 16362659

# 重新计算百分比
df['BLAST_percentage'] = (df['BLAST'] / total_blast) * 100
df['DIAMOND_percentage'] = (df['DIAMOND'] / total_diamond) * 100

# 绘制气泡图
plt.figure(figsize=(25, 8))  # 调整图表大小

# 设置气泡的大小
bubble_size_factor = 1750  # 调整这个值以放大气泡大小
bubble_size_blast = df['BLAST_percentage'] * bubble_size_factor  # 调整大小比例
bubble_size_diamond = df['DIAMOND_percentage'] * bubble_size_factor  # 调整大小比例

# 绘制BLAST气泡
scatter_blast = plt.scatter(df['Phylum'], df['Genome_log'], s=bubble_size_blast, alpha=0.7, label='BLAST', color='blue')

# 绘制DIAMOND气泡
scatter_diamond = plt.scatter(df['Phylum'], df['Genome_log'], s=bubble_size_diamond, alpha=0.7, label='DIAMOND', color='red')

# 添加百分比标签，BLAST在上方，DIAMOND在下方
for i in range(len(df)):
    plt.text(df['Phylum'][i], df['Genome_log'][i] + 0.05, f'{df["BLAST_percentage"][i]:.2f}%', 
             ha='center', va='bottom', fontsize=14, color='darkblue', weight='bold')
    plt.text(df['Phylum'][i], df['Genome_log'][i] - 0.05, f'{df["DIAMOND_percentage"][i]:.2f}%', 
             ha='center', va='top', fontsize=14, color='black', weight='bold')

# 添加标签和标题
plt.xlabel('Phylum', fontweight='bold', fontsize=14)
plt.ylabel('Log Transformed Genome Percentage', fontweight='bold',fontsize=14)
plt.title('Phylum: BLAST vs DIAMOND with Genome Percentage (Log Transformed)',fontsize=14, fontweight='bold')

# 设置 x 和 y 轴的范围
plt.ylim(0, max(df['Genome_log']) * 1.1)  # 根据数据调整范围
plt.xlim(-0.5, len(df['Phylum']) - 0.5)  # 留一些空间以避免气泡超出边界

# 调整子图的边距以确保所有气泡都在图表内
plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.2)
plt.xticks(fontsize=16, fontweight='bold', rotation=25)
# 使用颜色的小长方形来表示图例
import matplotlib.patches as mpatches
legend_blast = mpatches.Patch(color='blue', alpha=0.5, label='BLAST')
legend_diamond = mpatches.Patch(color='red', alpha=0.5, label='DIAMOND')
plt.legend(handles=[legend_blast, legend_diamond], loc='upper left')

# 显示网格
plt.grid(True)

# 保存图表到文件
output_path = "/mnt/shared/projects/nhm/clark-student/WeeklyGardenSampling/WeeklyGardenSampling/bubble/phylum_frequencies_genome_percentage_log_transformed_corrected.png"
plt.savefig(output_path, format='png', dpi=300)




