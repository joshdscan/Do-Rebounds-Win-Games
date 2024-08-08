# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# %%
# Data Loading Section
NumContestedRebounding = pd.read_csv("/Users/joshuascantlebury/WeekendProjects/NBA-Project/Playoff Rebound Analysis/Dataframes/NumContestedRebounding.csv")
OverallRebounding = pd.read_csv("/Users/joshuascantlebury/WeekendProjects/NBA-Project/Playoff Rebound Analysis/Dataframes/OverallRebounding.csv")
RebDistanceRebounding = pd.read_csv("/Users/joshuascantlebury/WeekendProjects/NBA-Project/Playoff Rebound Analysis/Dataframes/RebDistanceRebounding.csv")
ShotDistanceRebounding = pd.read_csv("/Users/joshuascantlebury/WeekendProjects/NBA-Project/Playoff Rebound Analysis/Dataframes/ShotDistanceRebounding.csv")
ShotTypeRebounding = pd.read_csv("/Users/joshuascantlebury/WeekendProjects/NBA-Project/Playoff Rebound Analysis/Dataframes/ShotTypeRebounding.csv")

# %%
# Initial Data Manipulation
rebdataframes = [NumContestedRebounding, OverallRebounding, RebDistanceRebounding, ShotDistanceRebounding, ShotTypeRebounding]
for df in rebdataframes:
    df['Win_Loss'] = df.duplicated('TEAM_NAME').map({False: 'W', True: 'L'})

# %%
# Modify Win/Loss status for specific teams
for df in rebdataframes:
    df.loc[df['TEAM_ID'] == 1610612756, 'Win_Loss'] = 'L'  # Phoenix
    df.loc[df['TEAM_ID'] == 1610612740, 'Win_Loss'] = 'L'  # NOLA

# %%
# Normalizing Rebound Data by Games Played
for col in NumContestedRebounding.columns[4:]:
    if not NumContestedRebounding[col].dtype == 'object':  
        NumContestedRebounding[col] = round((NumContestedRebounding[col] / NumContestedRebounding["G"]), 2)

# %%
# Preview Adjusted DataFrame
print(NumContestedRebounding.head())

# %%
# Dropping Unnecessary Columns
columns_to_drop = ["REB_FREQUENCY", "C_REB_PCT", "UC_REB_PCT"]
NumContestedRebounding.drop(columns=columns_to_drop, inplace=True)

# %%
# Rebound Distribution Analysis - Melt DataFrame for Visualization
df = NumContestedRebounding.copy()
df_melted = df.melt(id_vars=['TEAM_NAME', 'Win_Loss'], value_vars=['OREB', 'DREB', 'REB'], var_name='Rebound Type', value_name='Average Rebounds')

# %%
# Visualizing Rebound Distribution for Wins and Losses
fig, axes = plt.subplots(1, 2, figsize=(16, 8), sharey=True)
sns.violinplot(ax=axes[0], data=df_melted[df_melted['Win_Loss'] == 'W'], x='Rebound Type', y='Average Rebounds', palette='coolwarm')
axes[0].set_title('Distribution of Rebounds in Wins')
sns.violinplot(ax=axes[1], data=df_melted[df_melted['Win_Loss'] == 'L'], x='Rebound Type', y='Average Rebounds', palette='coolwarm')
axes[1].set_title('Distribution of Rebounds in Losses')
plt.tight_layout()
plt.show()

# %%
# Statistical Analysis - Standard Deviation and Mean
std_devs = NumContestedRebounding.groupby('Win_Loss')[['OREB', 'DREB', 'REB']].std().reset_index()
print("Standard Deviations:")
print(std_devs)

avgs = NumContestedRebounding.groupby('Win_Loss')[['OREB', 'DREB', 'REB']].mean().reset_index()
print("Averages:")
print(avgs)

# %%
# Variation in Rebound Activity - Data Preparation
df_melted_rebounds = NumContestedRebounding.melt(id_vars=['TEAM_NAME', 'Win_Loss'], value_vars=['OREB', 'DREB', 'REB'], 
                                                 var_name='Rebound Type', value_name='Average Rebounds')

# %%
# Visualizing Variation in Rebound Activity Amongst Teams
plt.figure(figsize=(14, 8))
sns.violinplot(data=df_melted_rebounds, x='TEAM_NAME', y='Average Rebounds', hue='Win_Loss', palette='coolwarm')
plt.title('Variation in Rebound Activity Amongst Teams in Wins and Losses')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Win/Loss', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# %%
# Function to Modify Win/Loss Column Based on Custom Rules
def modify_win_loss(df):
    # Group by TEAM_ID and apply modifications
    def assign_win_loss(group):
        n = len(group)
        return ['L'] * min(2, n) + ['W'] * max(0, n - 2)
    
    df['Win_Loss'] = df.groupby('TEAM_ID')['Win_Loss'].transform(assign_win_loss)
    return df

# %%
# Apply Win/Loss Modification Function and Display Results
OverallRebounding = modify_win_loss(OverallRebounding)
print(OverallRebounding)

# %%
# Assuming 'modified_df' is your DataFrame
plt.figure(figsize=(18, 6))
sns.violinplot(x='Win_Loss', y='C_REB_PCT', data=modified_df).set_title('C_REB_PCT by Win/Loss')
sns.violinplot(x='Win_Loss', y='UC_REB_PCT', data=modified_df).set_title('UC_REB_PCT by Win/Loss')
sns.violinplot(x='Win_Loss', y='REB_FREQUENCY', data=modified_df).set_title('REB_FREQUENCY by Win/Loss')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()

# %%
# Adjust Rebounds per Game
list_to_change = ['OREB', 'DREB', 'REB', 'C_OREB', 'C_DREB', 'C_REB', 'UC_OREB', 'UC_DREB', 'UC_REB']
for column in RebDistanceRebounding.columns:
    if column in list_to_change:
        RebDistanceRebounding[column] = round(RebDistanceRebounding[column] / RebDistanceRebounding["G"], 2)

# %%
# Separating Contested and Uncontested Rebounds
uncontestedRebounding = RebDistanceRebounding[RebDistanceRebounding["REB_NUM_CONTESTING_RANGE"] == "0 Contesting Rebounders"]
contestedRebounding = RebDistanceRebounding[RebDistanceRebounding["REB_NUM_CONTESTING_RANGE"] != "0 Contesting Rebounders"]

# %%
# Plotting Uncontested Rebounds Distribution by Win/Loss
plt.figure(figsize=(14, 8))
plt.subplot(1, 3, 1)
sns.violinplot(x='Win_Loss', y='UC_OREB', data=uncontestedRebounding).set_title('Uncontested Offensive Rebounds by Win/Loss')
plt.xlabel('Win/Loss')
plt.ylabel('Uncontested Offensive Rebounds')

plt.subplot(1, 3, 2)
sns.violinplot(x='Win_Loss', y='UC_DREB', data=uncontestedRebounding).set_title('Uncontested Defensive Rebounds by Win/Loss')
plt.xlabel('Win/Loss')
plt.ylabel('Uncontested Defensive Rebounds')

plt.subplot(1, 3, 3)
sns.violinplot(x='Win_Loss', y='UC_REB', data=uncontestedRebounding).set_title('Uncontested Total Rebounds by Win/Loss')
plt.xlabel('Win/Loss')
plt.ylabel('Uncontested Total Rebounds')

plt.tight_layout()
plt.show()

# %%
# Plotting Contested Rebounds Distribution by Win/Loss and Contesting Rebounders
plt.figure(figsize=(18, 8))
plt.subplot(1, 3, 1)
sns.violinplot(x='Win_Loss', y='OREB', hue='REB_NUM_CONTESTING_RANGE', data=contestedRebounding, split=True).set_title('Offensive Rebounds by Win/Loss and Contesting Rebounders')
plt.xlabel('Win/Loss')
plt.ylabel('Offensive Rebounds')

plt.subplot(1, 3, 2)
sns.violinplot(x='Win_Loss', y='DREB', hue='REB_NUM_CONTESTING_RANGE', data=contestedRebounding, split=True).set_title('Defensive Rebounds by Win/Loss and Contesting Rebounders')
plt.xlabel('Win/Loss')
plt.ylabel('Defensive Rebounds')

plt.subplot(1, 3, 3)
sns.violinplot(x='Win_Loss', y='REB', hue='REB_NUM_CONTESTING_RANGE', data=contestedRebounding, split=True).set_title('Total Rebounds by Win/Loss and Contesting Rebounders')
plt.xlabel('Win/Loss')
plt.ylabel('Total Rebounds')

plt.tight_layout()
plt.show()

# %%
# Implementing a Custom Win/Loss Assignment Based on Team Performance
def modify_win_loss_by_team_performance(df):
    def assign_win_loss(group):
        n = len(group)
        return ['W'] * min(4, n) + ['L'] * max(0, n - 4)
    
    df['Win_Loss'] = df.groupby('TEAM_ID')['TEAM_ID'].transform(assign_win_loss)
    return df

# %%
# Modifying Win/Loss in ShotTypeRebounding DataFrame
ShotTypeRebounding = modify_win_loss_by_team_performance(ShotTypeRebounding)

# %%
# Normalizing Rebound Counts in ShotTypeRebounding DataFrame
for column in list_to_change:
    ShotTypeRebounding[column] = round(ShotTypeRebounding[column] / ShotTypeRebounding["G"], 2)

# %%
# Exploratory Analysis: Influence of Shot Distance on Rebound Contesting
plt.figure(figsize=(18, 8))
plt.subplot(1, 3, 1)
sns.violinplot(x='Win_Loss', y='C_REB', hue='REB_DIST_RANGE', data=ShotTypeRebounding, split=True).set_title('Contested Rebounds by Win/Loss and Shot Distance')
plt.xlabel('Win/Loss')
plt.ylabel('Contested Rebounds')

plt.subplot(1, 3, 2)
sns.violinplot(x='Win_Loss', y='C_DREB', hue='REB_DIST_RANGE', data=ShotTypeRebounding, split=True).set_title('Contested Defensive Rebounds by Win/Loss and Shot Distance')
plt.xlabel('Win/Loss')
plt.ylabel('Contested Defensive Rebounds')

plt.subplot(1, 3, 3)
sns.violinplot(x='Win_Loss', y='C_OREB', hue='REB_DIST_RANGE', data=ShotTypeRebounding, split=True).set_title('Contested Offensive Rebounds by Win/Loss and Shot Distance')
plt.xlabel('Win/Loss')
plt.ylabel('Contested Offensive Rebounds')

plt.tight_layout()
plt.show()

# %%
