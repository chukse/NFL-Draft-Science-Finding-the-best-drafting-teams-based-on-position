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

#Formatting Dataframes
pd.options.display.float_format = "{:,.2f}".format
pd.set_option('display.precision', 2)

#Years we will evaluating NFL Draft Picks 
years = range(2000,2023)

#initiate dataframe
df_all = pd.DataFrame()
df_pbp_all = pd.DataFrame()

#pull team logos from library
logo = nfl.import_team_desc()
logo = logo[['team_abbr', 'team_logo_espn']]

#initiate logos list and paths of logos 
logo_paths = []
team_abbr = []

#if not already there, make a 'logos' folder to store logos
if not os.path.exists("logos"):
    os.makedirs("logos")

#loop that pulls all logos and paths and stores them in respective list 
for team in range(len(logo)):
    urllib.request.urlretrieve(logo['team_logo_espn'][team], f"logos/{logo['team_abbr'][team]}.tif")
    logo_paths.append(f"logos/{logo['team_abbr'][team]}.tif")
    team_abbr.append(logo['team_abbr'][team])


    
# Create a dictionary to put logo_paths and team_abbr lists 
data = {'Team Abbr' : team_abbr, 'Logo Path' : logo_paths}

# Create a DataFrame from the dictionary
logo_df = pd.DataFrame(data)


#loop to pull all draft picks from years range and merge into one dataframe 
for year in years:
    df_draft = nfl.import_draft_picks([year])
    #df_pbp = nfl.import_pbp_data([year])
    
    df_all = pd.concat([df_all,df_draft], ignore_index=True)

#only select all draft picks that were categroized as "DL"
a = df_all.query("category == 'DL'")

#print this dataframe to csv file 
a.to_csv('C:/kaggle/working/dataframe_before.csv',index=False,header=True)

#from the dataframe select all draft picks that ended up starting atleast 2 games
sorted_df = a.loc[(a['seasons_started'] > 2)]



#rename "team" column in dataframe in prep for merging dataframes
sorted_df2 = sorted_df.rename(columns={'team':'Team Abbr'})
print(type(sorted_df2))

#change teem abbr in the logo dataframe, to latest teams 
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




#combines logo dataframe and draft picks dataframes 
draft_info = pd.merge(sorted_df2, logo_df, on='Team Abbr')

#stores paths in list 
paths = draft_info['Logo Path']
#print(draft_info)

#if same pick, group them together to get the best picks to draft a particular position
draft_info = draft_info.groupby("pick").sum().reset_index()


#function to pass image path and create plot images
def getImage(path):
    return OffsetImage(plt.imread(path, format="tif"), zoom=.07)



# Define plot size and autolayout
plt.rcParams["figure.figsize"] = [100, 70]
plt.rcParams["figure.autolayout"] = True

# Define the x and y variables
x = draft_info['pick']
y = draft_info['seasons_started']




# Define the plot
fig, ax = plt.subplots()
fig.subplots_adjust( left=None, bottom=None,  right=None, top=None, wspace=None, hspace=None)
# Load the data into the plot
for x0, y0, path in zip(x, y, paths):
   ab = AnnotationBbox(getImage(path), (x0, y0), frameon=False)
   ax.add_artist(ab)

# Plot parameters
plt.xlim(1, 200);
plt.ylim(1, 20);
plt.title("Draft Analysis: Pick vs Seasons Started", fontdict={'fontsize':35});
plt.xlabel("pick", fontdict={'fontsize':21});
plt.ylabel("Seasons Started", fontdict={'fontsize':21});


#print updated logo dataframe to csv 
sorted_df2.to_csv('C:/kaggle/working/NFLDraftHistory1.csv',index=False,header=True)

#print updated draft dataframe to csv 
draft_info.to_csv('C:/kaggle/working/draft_info.csv',index=False,header=True)

#print(sorted_df)
#sorted_df.plot(x="pick", y=["pfr_player_name", "probowls" ],
#        kind="bar", figsize=(10, 10))

plt.show()
