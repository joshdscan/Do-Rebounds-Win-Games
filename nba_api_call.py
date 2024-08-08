# %%
import pandas as pd
import os
import matplotlib as plt
import seaborn as sns
from nba_api.stats import endpoints 
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.static import teams



# %%
playoff_teams=leaguegamefinder.LeagueGameFinder(season_type_nullable="Playoffs")
playoff_teams=playoff_teams.get_data_frames()[0]
playoff_teams["GAME_DATE"]=pd.to_datetime(playoff_teams["GAME_DATE"])
playoff_teams=playoff_teams[playoff_teams['GAME_DATE'].dt.year == 2024]

# %%
playoff_teams_list=playoff_teams["TEAM_ID"].to_list() # This includes WNBA/G league i think

# %%
nba_teams = teams.get_teams()
team_dict = {team['id']: team['full_name'] for team in nba_teams if team['id'] in playoff_teams_list}
WL = ['W', 'L']
df_range=range(1,5)


# %% [markdown]
# ## NumContestedRebounding

# %%
for i, team_id in enumerate(playoff_teams_list, start=1):
    combined_df = pd.DataFrame()
    team_name = team_dict[team_id]
    for winorloss in WL:
        reboundstats = endpoints.TeamDashPtReb(season_type_all_star="Playoffs", team_id=team_id, outcome_nullable=winorloss)
        df = reboundstats.get_data_frames()[0] 
        combined_df = pd.concat([combined_df, df], ignore_index=True)
    filename = f"{team_name}NumContestedRebounding.csv"
    combined_df.to_csv(filename, index=False)


# %%
data_frames = []

# Directory where the files are located
directory = '/Users/joshuascantlebury/WeekendProjects/NBA-Project/Playoff Rebound Analysis/'

for team in team_dict.values():
    file_path = os.path.join(directory, f'{team}.csv')
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        data_frames.append(df)

# Combine all DataFrames into one
combined_df = pd.concat(data_frames, ignore_index=True)

# Display the combined DataFrame
combined_df.head()

# Save the combined DataFrame to a new CSV file
combined_df.to_csv('/Users/joshuascantlebury/WeekendProjects/NBA-Project/Playoff Rebound Analysis/NumContestedRebounding.csv', index=False)

# %% [markdown]
# ## OverallRebounding

# %%
for i, team_id in enumerate(playoff_teams_list, start=1):
    combined_df = pd.DataFrame()
    team_name = team_dict[team_id]
    for winorloss in WL:
        reboundstats = endpoints.TeamDashPtReb(season_type_all_star="Playoffs", team_id=team_id, outcome_nullable=winorloss)
        df = reboundstats.get_data_frames()[1] 
        combined_df = pd.concat([combined_df, df], ignore_index=True)
    filename = f"{team_name}OverallRebounding.csv"
    combined_df.to_csv(filename, index=False)


# %%
data_frames = []

# Directory where the files are located
directory = '/Users/joshuascantlebury/WeekendProjects/NBA-Project/Playoff Rebound Analysis/'

for team in team_dict.values():
    file_path = os.path.join(directory, f'{team}OverallRebounding.csv')
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        data_frames.append(df)

# Combine all DataFrames into one
combined_df = pd.concat(data_frames, ignore_index=True)

# Display the combined DataFrame
combined_df.head()

# Save the combined DataFrame to a new CSV file
combined_df.to_csv('/Users/joshuascantlebury/WeekendProjects/NBA-Project/Playoff Rebound Analysis/OverallRebounding.csv', index=False)

# %% [markdown]
# ## RebDistanceRebounding

# %%
for i, team_id in enumerate(playoff_teams_list, start=1):
    combined_df = pd.DataFrame()
    team_name = team_dict[team_id]
    for winorloss in WL:
        reboundstats = endpoints.TeamDashPtReb(season_type_all_star="Playoffs", team_id=team_id, outcome_nullable=winorloss)
        df = reboundstats.get_data_frames()[2] 
        combined_df = pd.concat([combined_df, df], ignore_index=True)
    filename = f"{team_name}RebDistanceRebounding.csv"
    combined_df.to_csv(filename, index=False)


# %%
data_frames = []

# Directory where the files are located
directory = '/Users/joshuascantlebury/WeekendProjects/NBA-Project/Playoff Rebound Analysis/'

for team in team_dict.values():
    file_path = os.path.join(directory, f'{team}RebDistanceRebounding.csv')
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        data_frames.append(df)

# Combine all DataFrames into one
combined_df = pd.concat(data_frames, ignore_index=True)

# Display the combined DataFrame
combined_df.head()

# Save the combined DataFrame to a new CSV file
combined_df.to_csv('/Users/joshuascantlebury/WeekendProjects/NBA-Project/Playoff Rebound Analysis/RebDistanceRebounding.csv', index=False)

# %% [markdown]
# ## ShotDistanceRebounding

# %%
for i, team_id in enumerate(playoff_teams_list, start=1):
    combined_df = pd.DataFrame()
    team_name = team_dict[team_id]
    for winorloss in WL:
        reboundstats = endpoints.TeamDashPtReb(season_type_all_star="Playoffs", team_id=team_id, outcome_nullable=winorloss)
        df = reboundstats.get_data_frames()[3] 
        combined_df = pd.concat([combined_df, df], ignore_index=True)
    filename = f"{team_name}ShotDistanceRebounding.csv"
    combined_df.to_csv(filename, index=False)


# %%
data_frames = []

# Directory where the files are located
directory = '/Users/joshuascantlebury/WeekendProjects/NBA-Project/Playoff Rebound Analysis/'

for team in team_dict.values():
    file_path = os.path.join(directory, f'{team}ShotDistanceRebounding.csv')
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        data_frames.append(df)

# Combine all DataFrames into one
combined_df = pd.concat(data_frames, ignore_index=True)

# Display the combined DataFrame
combined_df.head()

# Save the combined DataFrame to a new CSV file
combined_df.to_csv('/Users/joshuascantlebury/WeekendProjects/NBA-Project/Playoff Rebound Analysis/ShotDistanceRebounding.csv', index=False)

# %% [markdown]
# ## ShotTypeRebounding

# %%
for i, team_id in enumerate(playoff_teams_list, start=1):
    combined_df = pd.DataFrame()
    team_name = team_dict[team_id]
    for winorloss in WL:
        reboundstats = endpoints.TeamDashPtReb(season_type_all_star="Playoffs", team_id=team_id, outcome_nullable=winorloss)
        df = reboundstats.get_data_frames()[4] 
        combined_df = pd.concat([combined_df, df], ignore_index=True)
    filename = f"{team_name}ShotTypeRebounding.csv"
    combined_df.to_csv(filename, index=False)


# %%
data_frames = []

# Directory where the files are located
directory = '/Users/joshuascantlebury/WeekendProjects/NBA-Project/Playoff Rebound Analysis/'

for team in team_dict.values():
    file_path = os.path.join(directory, f'{team}ShotTypeRebounding.csv')
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        data_frames.append(df)

# Combine all DataFrames into one
combined_df = pd.concat(data_frames, ignore_index=True)

# Display the combined DataFrame
combined_df.head()

# Save the combined DataFrame to a new CSV file
combined_df.to_csv('/Users/joshuascantlebury/WeekendProjects/NBA-Project/Playoff Rebound Analysis/ShotTypeRebounding.csv', index=False)


