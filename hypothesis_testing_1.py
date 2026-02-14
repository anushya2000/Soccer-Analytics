# -*- coding: utf-8 -*-
"""
Created on Wed Feb 11 18:16:49 2026

@author: Anushya
"""

# =============================================================================
# SIGN TEST - non-parametric test to verify if a couple of groups are of equal sizes
# Case study - verify if Heung-Min Son is ambidextrous with shooting (using both feet the same number of times)
# =============================================================================

import os
import json
import pandas as pd
from pathlib import Path


path1 = os.path.join(str(Path().resolve()), 'Wyscout_data', 'events', 'events_England.json')

with open(path1) as f:
    data = json.load(f)
events_df = pd.DataFrame(data)


path2 = os.path.join(str(Path().resolve()), 'Wyscout_data', 'players.json')

with open(path2) as f:
    data1 = json.load(f)
player_df = pd.DataFrame(data1)



# =============================================================================
# exploration
# =============================================================================
player_df.loc[player_df["shortName"] == "Son Heung-Min"].iloc[0].to_dict()
player_df[["foot", "birthArea"]]

player_df.foot.value_counts()

# extract data from a dict column
player_df[player_df["shortName"] == "Son Heung-Min"].birthArea.str["id"]
# =============================================================================
# exploration
# =============================================================================



# getting Heung's shots where the data is coded like: left=401, right=402
Heung_id = player_df[player_df.shortName.str.contains('Heung', na=False)].iloc[0].wyId
shots_df = events_df[(events_df.subEventName =='Shot') & (events_df.playerId == Heung_id)]


# left and right leg shots
left_shots = shots_df[shots_df.tags.apply(lambda tags: {'id':401} in tags)]
right_shots = shots_df[shots_df.tags.apply(lambda tags: {'id':402} in tags)]


#create list with 1 for left foot shots and -1 for right foot shots
lis = [1] * len(left_shots)
lis.extend([-1] * len(right_shots))



# perform sign test with hypothesized median as 0
from statsmodels.stats.descriptivestats import sign_test
test = sign_test(lis, mu0 = 0)

# test[0] = test statistic (number of positives or signed count)
# test[1] = p-value
pvalue = test[1]


if pvalue < 0.05:
    print("P-value amounts to", str(pvalue)[:5], "- We reject null hypothesis - Heung-Min Son is not ambidextrous")
else:
    print("P-value amounts to", str(pvalue)[:5], " - We do not reject null hypothesis - Heung-Min Son is ambidextrous")

