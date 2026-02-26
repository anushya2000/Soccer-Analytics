"""
Created on Wed Feb 25 12:29:44 2026

@author: Anushya
"""

# =============================================================================
# Plotting shots on the pitch for the Women's World Cup 2019 - England Vs Sweden 
# If a goal was scored, we use scatter method to plot a circle and annotate method to mark scorer's name.
# If not, we use scatter method to draw a translucent circle. 
# =============================================================================

from mplsoccer import Pitch, Sbopen, VerticalPitch

# using StatsBomb data and filtering for the specific match datasets
parser = Sbopen()
competition_df = parser.competition()
match_df=parser.match(72, 30)

df, related, freeze, tactics = parser.event(69301)
team1, team2 = df.team_name.unique()
shots = df.loc[df['type_name'] == 'Shot'].set_index('id')
    
# plotting a standard-size pitch
pitch = Pitch(line_color='black')
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0, endnote_space=0)
pitchLengthX=120
pitchWidthY=80

# iterating through each row to plot the shot
for i, row in shots.iterrows():
    x, y=row['x'], row['y']
    goal=row['outcome_name']=='Goal'
    team_name = row['team_name']
    
    # goals are plotted in dark colour while missed shots are translucent
    if (team_name==team1):
        if goal:
            pitch.scatter(x, y, alpha = 1, s = 500, color = "red", ax=ax['pitch']) 
            pitch.annotate(row["player_name"], (x + 1, y - 2), ax=ax['pitch'], fontsize = 12)
        else: 
            pitch.scatter(x, y, alpha = 0.2, s = 500, color = "red", ax=ax['pitch']) 
            
    else:
        if goal:
            pitch.scatter(pitchLengthX-x, pitchWidthY-y, alpha = 1, s = 500, color = "blue", ax=ax['pitch']) 
            pitch.annotate(row["player_name"], (pitchLengthX-x + 1, pitchWidthY-y - 2), ax=ax['pitch'], fontsize = 12)
        else: 
            pitch.scatter(pitchLengthX-x, pitchWidthY-y, alpha = 0.2, s = 500, color = "blue", ax=ax['pitch']) 
            

fig.suptitle("England (red) and Sweden (blue) shots", fontsize = 24)     
fig.set_size_inches(10, 7)



# =============================================================================
# Plotting shots on one half using VerticalPitch() class by setting half=True
# =============================================================================


df_england = df[(df['type_name']=='Shot') & (df['team_name'].str.contains('England'))][['x', 'y', 'outcome_name', 'player_name']]
# df_sweden = df[(df['type_name']=='Shot') & (df['team_name'].str.contains('Sweden'))][['x', 'y', 'outcome_name', 'player_name']]

pitch = VerticalPitch(line_color='black', half = True)
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0, endnote_space=0)
#plotting all shots
pitch.scatter(df_england.x, df_england.y, alpha = 1, s = 500, color = "red", ax=ax['pitch'], edgecolors="black") 
fig.suptitle("England shots against Sweden", fontsize = 30)           

