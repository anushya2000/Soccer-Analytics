# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 12:33:57 2026

@author: Anushya
"""

# =============================================================================
# One-sample one-sided t-test
# Case study - Assuming that each team typically gets 5 corners per match, let's verify if Manchester City gets more 
#              since they are an attacking team 
# =============================================================================

import pandas as pd
import os
import pathlib
import warnings
import numpy as np
import json
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")

# load events data
path = os.path.join(str(pathlib.Path().resolve()), 'Wyscout_data', 'events', 'Events_england.json')
with open(path) as f:
    data = json.load(f)
events_df = pd.DataFrame(data)

# load teams data
path1 = os.path.join(str(pathlib.Path().resolve()), 'Wyscout_data', 'teams.json')
with open(path1) as f:
    data1 = json.load(f)
teams_df = pd.DataFrame(data1)
teams_df = teams_df.rename(columns={"wyId": "teamId"})


corners_df = events_df[events_df.subEventName == 'Corner']
corner_by_game = corners_df.groupby(['teamId', 'matchId']).size().reset_index(name="counts")
summary = corner_by_game.merge(teams_df[["name", "teamId"]], how = "left", on = ["teamId"])


team_name= 'Manchester City'
city_corners = summary[summary["name"] == 'Manchester City']["counts"]


# plotting a normalized density histogram of the corners taken by Manchester City
def FormatFigure(ax):
    ax.legend(loc='upper left')
    ax.set_ylim(0,0.25) #bar height visibility
    ax.spines['top'].set_visible(False) #removes top border
    ax.spines['right'].set_visible(False) #removes right border
    ax.set_xlabel('Corners')
    ax.set_ylabel('Proportion of games')
    ax.set_xticks(np.arange(0,21,step=1)) #forces ticks every 1 unit, better visibility


fig,ax1=plt.subplots(1,1) #1 row, 1 column for plotting
ax1.hist(city_corners, 
         np.arange(0.01,20.5,1), #Defines bins from 0 to 20 with width = 1 (1 corner interval on X-axis)
         color='lightblue', edgecolor = 'black', linestyle='-', alpha=0.5, #aesthetics
         label=team_name, #legend
         density=True, #Normalized histogram, so total area = 1 (proportion instead of raw counts). False=frequency histogram
         align='right')
FormatFigure(ax1)

# bins = np.arange(0, 21, 1)
# ax1.hist(city_corners, bins=bins, density=True)

mean, std = city_corners.mean(), city_corners.std()
print('City typically had %.2f  plus/minus %.2f corners per match in the 2017/18 season.'%(mean,std))


# We set the significance level at 0.05
from scipy.stats import ttest_1samp
t, pvalue = ttest_1samp(city_corners,popmean=5)

print("The t-staistic is %.2f and the P-value is %.2f."%(t,pvalue))
if pvalue < 0.05:
    print("We reject null hypothesis - " + team_name + " typically take more than 5 corners per match.")
else:
    print("We cannot reject null hypothesis - " + team_name + " do not typically take more than 5 corners per match.")



# =============================================================================
# Two-sample two-sided t-test
# Case study - testing if Liverpool had a different average corners per game than Everton
# =============================================================================

liverpool_corners = summary.loc[summary["name"] == 'Liverpool']["counts"]
everton_corners = summary.loc[summary["name"] == 'Everton']["counts"]

mean, std = liverpool_corners.mean(), liverpool_corners.std()
print('Liverpool typically had %.2f plus/minus %.2f corners per match in the 2017/18 season.'%(mean,std))
std_error=std/np.sqrt(len(liverpool_corners))
print('The standard error in the number of corners per match is %.4f'%std_error)

mean, std = everton_corners.mean(), everton_corners.std()
print('Everton typically had %.2f plus/minus %.2f corners per match in the 2017/18 season.'%(mean,std))
std_error=std/np.sqrt(len(everton_corners))
print('The standard error in the number of corners per match is %.4f'%std_error)



fig,ax=plt.subplots(1,1)
ax.hist(liverpool_corners, np.arange(0.01,15.5,1), color='red', edgecolor = 'white',linestyle='-',alpha=1.0, label="Liverpool", density=True,align='right')
ax.hist(everton_corners, np.arange(0.01,15.5,1), alpha=0.25, color='blue', edgecolor = 'black', label='Everton',  density=True,align='right')
FormatFigure(ax)


# We set the significance level at 0.05
from scipy.stats import ttest_ind
t, pvalue  = ttest_ind(a=liverpool_corners, b=everton_corners, equal_var=True)

print("The t-staistic is %.2f and the P-value is %.2f."%(t,pvalue))
if pvalue < 0.05:
    print("We reject null hypothesis - Liverpool took different number of corners per game than Everton")
else:
    print("We cannot reject the null hypothesis that Liverpool took the same number of corners per game as Everton")
