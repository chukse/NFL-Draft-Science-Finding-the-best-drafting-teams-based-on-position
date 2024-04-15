import pandas as pd
import nfl_data_py as nfl
import matplotlib.pyplot as plt
import urllib.request
import os
import time
import numpy as np
import seaborn as sns
from datetime import datetime
from datetime import date
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


pd.options.display.float_format = "{:,.2f}".format
pd.set_option('display.precision', 2)

years = range(2000,2023)
df_all = pd.DataFrame()
df_pbp_all = pd.DataFrame()
logo = nfl.import_team_desc()
logo = logo[['team_abbr', 'team_logo_espn']]
logo_paths = []
team_abbr = []


if not os.path.exists("logos"):
    os.makedirs("logos")

for team in range(len(logo)):
    urllib.request.urlretrieve(logo['team_logo_espn'][team], f"logos/{logo['team_abbr'][team]}.tif")
    logo_paths.append(f"logos/{logo['team_abbr'][team]}.tif")
    team_abbr.append(logo['team_abbr'][team])


    
# Create a dictionary to put logo_paths and team_abbr in
data = {'Team Abbr' : team_abbr, 'Logo Path' : logo_paths}

# Create a DataFrame from the dictionary
logo_df = pd.DataFrame(data)

logo_df.head()


logo_df = pd.DataFrame(data)

logo_df.head()


for year in years:
    df_draft = nfl.import_draft_picks([year])
    #df_pbp = nfl.import_pbp_data([year])
    
    df_all = pd.concat([df_all,df_draft], ignore_index=True)
    #df_pbp_all = pd.concat([df_pbp_all,df_pbp], ignore_index=True)
    #print(df_all)

a = df_all.query("category == 'DB'")
#a = pd.concat([df_all.query("position == 'CB'"), df_all.query("position == 'S'")])
a.to_csv('C:/kaggle/working/dataframe_before.csv',index=False,header=True)
#df_value = nfl.import_draft_values()
#df_all.query("position == 'QB'").to_csv('C:/kaggle/working/NFLDraftHistory.csv',index=False,header=True)

#a.sort_values("pass_yards",ascending=False)

sorted_df = a.loc[(a['seasons_started'] > 2)]


#sorted_df.rename(columns = {'team':'Team Abbr'}, inplace = True)

sorted_df2 = sorted_df.rename(columns={'team':'Team Abbr'})
print(type(sorted_df2))

#print(len(sorted_df2['Team Abbr']))

for i in range(len(sorted_df2['Team Abbr'])):
    if(sorted_df2['Team Abbr'].iloc[i] == 'GNB'):
        sorted_df2['Team Abbr'] = sorted_df2['Team Abbr'].replace(['GNB'], 'GB')
    elif(sorted_df2['Team Abbr'].iloc[i] == 'SFO'):
        sorted_df2['Team Abbr'] = sorted_df2['Team Abbr'].replace(['SFO'], 'SF')
    elif(sorted_df2['Team Abbr'].iloc[i] == 'KAN'):
        sorted_df2['Team Abbr'] = sorted_df2['Team Abbr'].replace(['KAN'], 'KC')
    elif(sorted_df2['Team Abbr'].iloc[i] == 'LVR'):
        sorted_df2['Team Abbr'] = sorted_df2['Team Abbr'].replace(['LVR'], 'LV')
    elif(sorted_df2['Team Abbr'].iloc[i] == 'NWE'):
        sorted_df2['Team Abbr'] = sorted_df2['Team Abbr'].replace(['NWE'], 'NE')
    elif(sorted_df2['Team Abbr'].iloc[i] == 'NOR'):
        sorted_df2['Team Abbr'] = sorted_df2['Team Abbr'].replace(['NOR'], 'NO')
    elif(sorted_df2['Team Abbr'].iloc[i] == 'SDG'):
        sorted_df2['Team Abbr'] = sorted_df2['Team Abbr'].replace(['SDG'], 'SD')
    elif(sorted_df2['Team Abbr'].iloc[i] == 'TAM'):
        sorted_df2['Team Abbr'] = sorted_df2['Team Abbr'].replace(['TAM'], 'TB')





draft_info = pd.merge(sorted_df2, logo_df, on='Team Abbr')

paths = draft_info['Logo Path']
#print(draft_info)
#draft_info = draft_info.groupby("pick").sum().reset_index()



def getImage(path):
    return OffsetImage(plt.imread(path, format="tif"), zoom=.07)



# Define plot size and autolayout
plt.rcParams["figure.figsize"] = [100, 70]
plt.rcParams["figure.autolayout"] = True

# Define the x and y variables
x = draft_info['pick']
y = draft_info['seasons_started']

# Define the image paths


# Define the plot
fig, ax = plt.subplots()
fig.subplots_adjust( left=None, bottom=None,  right=None, top=None, wspace=None, hspace=None)
# Load the data into the plot
for x0, y0, path in zip(x, y, paths):
   #print(getImage(path))
   ab = AnnotationBbox(getImage(path), (x0, y0), frameon=False)
   ax.add_artist(ab)

# Plot parameters
plt.xlim(1, 200);
plt.ylim(1, 20);
plt.title("Draft Analysis: Pick vs Seasons Started", fontdict={'fontsize':35});
plt.xlabel("pick", fontdict={'fontsize':21});
plt.ylabel("Seasons Started", fontdict={'fontsize':21});



sorted_df2.to_csv('C:/kaggle/working/NFLDraftHistory1.csv',index=False,header=True)
#df_value.to_csv('C:/kaggle/working/NFLDraftvalue.csv',index=False,header=True)
#df_pbp_all.to_csv('C:/kaggle/working/playbyplay.csv',index=False,header=True)
draft_info.to_csv('C:/kaggle/working/draft_info.csv',index=False,header=True)

#print(sorted_df)
#sorted_df.plot(x="pick", y=["pfr_player_name", "probowls" ],
#        kind="bar", figsize=(10, 10))

plt.show()
