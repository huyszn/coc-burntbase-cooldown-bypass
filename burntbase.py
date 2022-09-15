import requests, json, scan_number_and_access_token
from datetime import datetime
import pandas as pd

# Returns a dictionary of all results and their attributes
def results_dict(results_items):
    r_date = [datetime.fromtimestamp(results_items[item]['date']).strftime('%B %d, %Y') for item in range(len(results_items))]
    r_img_name = [(results_items[item]['IMG_NAME']).replace('\\','') for item in range(len(results_items))]
    r_burn_factor = [f"{int(results_items[item]['burn_factor']*100)}%" for item in range(len(results_items))]
    r_transformation = [results_items[item]['transformation'] for item in range(len(results_items))]
    r_yt_channel_id = [f"https://www.youtube.com/channel/{results_items[item]['yt_channel_id']}" for item in range(len(results_items))]
    r_yt_channel_name = [results_items[item]['yt_channel_name'] for item in range(len(results_items))]

    base_results = {'Date': r_date, 'Image': r_img_name, 'Burn Factor': r_burn_factor, 'Transformation': r_transformation, 'YouTube Channel Link': r_yt_channel_id, 'YouTube Channel Name': r_yt_channel_name}
    
    return base_results

scan_number = scan_number_and_access_token.scan_number
url = f"https://app.burntbase.com/api/auth/scans/{scan_number}"

access_token = scan_number_and_access_token.access_token
headers = {"accesstoken": access_token}

response = requests.request("GET", url, headers=headers)

json_r = response.json()

#with open('response.json', 'w') as f:
#    json.dump(response.json(), f)

#json_r = json.load(open('./response.json'))

results = json_r['results']
# match_results are results where burn factor > 80%
match_results = results['match_results']
# no_match_results are results where burn factor < 80%
no_match_results =  results['no_match_results']

match_df = pd.DataFrame(results_dict(match_results))
no_match_df = pd.DataFrame(results_dict(no_match_results))

# Combine all results into one dataframe
all_matches_df = pd.concat([match_df, no_match_df],axis=0)
#print(all_matches_df)

# Change values under Transformation column to make it easier to understand
all_matches_df.loc[all_matches_df['Transformation'] == 'original', 'Transformation'] = 'Original'
all_matches_df.loc[all_matches_df['Transformation'] == 'rotate90', 'Transformation'] = '90° Rotation'
all_matches_df.loc[all_matches_df['Transformation'] == 'rotate180', 'Transformation'] = '180° Rotation'
all_matches_df.loc[all_matches_df['Transformation'] == 'rotate270', 'Transformation'] = '270° Rotation'
all_matches_df.loc[all_matches_df['Transformation'] == 'vertical_reflection', 'Transformation'] = 'Vertical Reflection'
all_matches_df.loc[all_matches_df['Transformation'] == 'horizontal_reflection', 'Transformation'] = 'Horizontal Reflection'

# Save results to a CSV file
all_matches_df.to_csv(f'./Burntbase Scan Results.csv', index=False)