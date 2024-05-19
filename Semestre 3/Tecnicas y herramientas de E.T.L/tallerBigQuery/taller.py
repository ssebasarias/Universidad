import requests
import pandas as pd
import json

response = requests.get('http://universities.hipolabs.com/search?country=United+States')
data = response.json()

df = pd.read_json(json.dumps(data))
print(df)