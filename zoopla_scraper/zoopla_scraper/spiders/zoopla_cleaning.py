import pandas as pd

df=pd.read_csv('zoopla_edinburgh.csv')

#Removing the exta headers from the new scraped list
to_drop=df[df['available_from']=='available_from']
df_clean=df.drop(to_drop.index)

#Dropping duplicates
df_single=df_clean.drop_duplicates(subset=['address', 'description', 'features', 'images', 'letting_agent_name', 'number_of_baths',
       'number_of_beds', 'price', 'property_url', 'title'])

#Saving to a file
df_single.to_csv('zoopla_edinburgh.csv',index=False)

print('Script ran succesfully')
print('Number of rows BEFORE cleaning: {}\nNumber of rows AFTER cleaning: {}'.format(df.shape[0],df_single.shape[0]))