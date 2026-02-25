"""
Created on Wed Feb 25 12:29:44 2026

@author: Anushya
"""

# =============================================================================
# Plotting shots on the pitch for the Women's World Cup 2019 between England and Sweden 
# =============================================================================

import matplotlib.pyplot as plt
from mplsoccer import Pitch, Sbopen

# using StatsBomb data and filtering for the specific match datasets
parser = Sbopen()
competition_df = parser.competition()
match_df=parser.match(72, 30)

df, related, freeze, tactics = parser.event(69301)
#get team names
team1, team2 = df.team_name.unique()
#A dataframe of shots
shots = df.loc[df['type_name'] == 'Shot'].set_index('id')
    
# plotting a standard-size pitch
pitch = Pitch(line_color='black')
fig, ax = pitch.draw(figsize=(10,7))
pitchLengthX=120
pitchWidthY=80

# iterating through each row to plot the shot on the picth
for i, shot in shots.iterrows():
    x, y=shot['x'], shot['y']
    goal=shot['outcome_name']=='Goal'
    team_name = shot['team_name']
    circleSize=2
    
    # goals are plotted in dark colour while missed shots are light in colour
    if (team_name==team1):
        if goal:
            shotCircle=plt.Circle((x,y),circleSize,color="red")
            plt.text(x+1, y-2, shot['player_name'])
        else:
            shotCircle=plt.Circle((x,y), circleSize,color="red")
            shotCircle.set_alpha(.2)
            
    else:
        if goal:
             shotCircle=plt.Circle((pitchLengthX-x,pitchWidthY - y),circleSize,color="blue") 
             plt.text(pitchLengthX-x+1,pitchWidthY - y - 2 ,shot['player_name'])
        else:
             shotCircle=plt.Circle((pitchLengthX-x,pitchWidthY - y),circleSize,color="blue")      
             shotCircle.set_alpha(.2)
    ax.add_patch(shotCircle)

fig.suptitle("England (red) and Sweden (blue) shots", fontsize = 24)
