import pandas as pd
df = pd.read_csv(r'../1getData/yp.csv', encoding='ISO-8859–1')
df = df[pd.notnull(df['name'])]

df['company'] = list(map(lambda x: ' '.join(x.split()).lower(), df['name'].astype(str)))
#replace '.' and triling white space

df['web'].replace('http://www.', "", regex=True, inplace=True)
df['web'].replace('https://', "", regex=True, inplace=True)
df['web'].replace('http://', "", regex=True, inplace=True)

newaddress = df['addressLocality'].str.split(",", n=1, expand=True)
df['city'] = newaddress[0]
df['tempstatezip'] = newaddress[1].str.lstrip()
statezip = df['tempstatezip'].str.split(" ", n=1, expand=True)
df['state'] = statezip[0]
df['zip'] = statezip[1]
df['zip'].fillna(df['postalCode'], inplace=True)

df.drop(['addressLocality', 'addressRegion', 'postalCode', 'tempstatezip'], axis=1, inplace=True)

df.to_csv(r'../2cleanData/readyDedupYp.csv')
