#%%
from datetime import datetime

import numpy as np
import pandas as pd
from tqdm import tqdm

# %%
picks = pd.read_csv('gamma_picks.csv', sep=",")
events = pd.read_csv('gamma_events.csv', sep=",")

## 2013
#drop_sta_list = ['HMOB', 'JBNB', 'JBR', 'JECB', 'JELB', 'JLAB','JUM','MOBB']
#drop_cha_list = ['EH','BH']

## 2014
drop_sta_list = ['HAST.*BH','HAST.*HN','SAO.*BH','SAO.*HN','SCZ.*BH','SCZ.*HN',
                 'CADB.*EH','HMOB.*EH','HTU.*EH','JBNB.*EH','JBR.*EH','JECB.*EH','JELB.*EH','JLAB.*EH','JUM.*EH']
                 #'MOBB.*BH']

#drop_cha_list = ['BH','HN','EH']

# %%
#events["match_id"] = events.apply(lambda x: f'{x["event_idx"]}_{x["file_index"]}', axis=1)
#picks["match_id"] = picks.apply(lambda x: f'{x["event_idx"]}_{x["file_index"]}', axis=1)
events["match_id"] = events["event_index"]
picks["match_id"] = picks["event_index"]
# %%
out_file = open("hypoInput.arc", "w")

picks_by_event = picks.groupby("match_id").groups

for i in tqdm(range(len(events))):

    event = events.iloc[i]
    event_time = datetime.strptime(event["time"], "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y%m%d%H%M%S%f")[:-4]
    lat_degree = int(event["latitude"])
    lat_minute = (event["latitude"] - lat_degree) * 60 * 100
    south = "S" if lat_degree <= 0 else " "
    lng_degree = int(event["longitude"])
    lng_minute = (event["longitude"] - lng_degree) * 60 * 100
    east = "E" if lng_degree >= 0 else " "
    #depth = event["depth(m)"] / 1e3 * 100
    depth = event["depth_km"] #* 100

    picks_idx = picks_by_event[event["match_id"]]

    ## take out certain station with certain channels (both)
    tmp_picks = picks.loc[picks_idx]
    ##- Check if any sta from drop_sta_list is present
    condition_sta = ~tmp_picks['station_id'].str.contains('|'.join(drop_sta_list))
    tmp_picks = tmp_picks[condition_sta]
    
    ##- Check if 'EH' is present
    #condition_cha = ~tmp_picks['station_id'].str.contains('|'.join(drop_cha_list))
    ##- Exclude rows where both conditions are true
    #tmp_picks = tmp_picks[condition_sta | condition_cha]
        
    ## Filter out events with only S picks
    phase_type = np.unique(tmp_picks['type'])
    if len(phase_type) == 1:
        if phase_type[0] == 'S':
            continue
    
    event_line = f"{event_time}{abs(lat_degree):2d}{south}{abs(lat_minute):4.0f}{abs(lng_degree):3d}{east}{abs(lng_minute):4.0f}{depth:5.0f}"
    out_file.write(event_line + "\n")

    #for j in picks_idx:
    #    pick = picks.iloc[j]
    for j in range(len(tmp_picks)):
        pick = tmp_picks.iloc[j]
        network_code, station_code, comp_code, channel_code = pick['id'].split('.')
        phase_type = pick['type']
        phase_weight = min(max(int((1 - pick['prob']) / (1 - 0.3) * 4) - 1, 0), 3)

        ## make certain station more important
        # if station_code == 'MOBB':
        #     phase_weight = 0
        
        pick_time = datetime.strptime(pick["timestamp"], "%Y-%m-%dT%H:%M:%S.%f")
        phase_time_minute = pick_time.strftime("%Y%m%d%H%M")
        phase_time_second = pick_time.strftime("%S%f")[:-4]
        tmp_line = f"{station_code:<5}{network_code:<2} {comp_code:<1}{channel_code:<3}"
        if phase_type.upper() == 'P':
            pick_line = f"{tmp_line:<13} P {phase_weight:<1d}{phase_time_minute} {phase_time_second}"
        elif phase_type.upper() == 'S':
            pick_line = f"{tmp_line:<13}   4{phase_time_minute} {'':<12}{phase_time_second} S {phase_weight:<1d}"
        else:
            raise (f"Phase type error {phase_type}")
        out_file.write(pick_line + "\n")

    out_file.write("\n")
    #if i > 1e3:
    #    break

out_file.close()
