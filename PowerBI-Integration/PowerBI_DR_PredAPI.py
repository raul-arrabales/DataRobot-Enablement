
import requests 
import pandas
from pandas.io.json import json_normalize

def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

API_TOKEN = '*** MY PowerBI API Token - Generated in DataRobot Platform ***'
USERNAME = 'raul.******@datarobot.com'

DEPLOYMENT_ID = '*** My Deployment ID ***'

# Set HTTP headers
# Note: The charset should match the contents of the file.
# The 'datarobot-key' is only needed for Cloud users.  Remove for on-prem installs.
headers = {'Content-Type': 'application/json; charset=UTF-8', 'datarobot-key': '*** DataRobot Cloud Key ***'}

# Convert dataset to JSON
data = dataset.to_json(orient='records')

# Make predictions on your data
# Using DataRobot's EU managed cloud (eu.datarobot.com):
predictions_response = requests.post('https://cfds.orm.eu.datarobot.com/predApi/v1.0/deployments/%s/predictions' % (DEPLOYMENT_ID),
                                     auth=(USERNAME, API_TOKEN), data=data, headers=headers)

predictions_response.raise_for_status()

# store the JSON response from the prediction API
response_json = predictions_response.json()

results_df = pandas.DataFrame()
for row in response_json['data']:
   new_row = json_normalize(data=flatten_json(row))
   results_df = pandas.concat([results_df, new_row])

print(results_df)

