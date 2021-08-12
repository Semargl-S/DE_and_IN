import matplotlib.pyplot as plt
import pandas as pd
import json
import seaborn as sns

country_list = ['CA', 'DE', 'IN', 'FR', 'GB', 'JP', 'KR', 'MX', 'RU', 'US']
for country in country_list:
    json_name = pd.DataFrame(columns=['id', 'category_name'])
    f = open('{}_category_id.json'.format(country))
    data = json.load(f)
    for j, i in enumerate(data['items']):
        json_name.loc[j, 'id'] = int(i['id'])
        json_name.loc[j, 'category_name'] = i['snippet']['title']
    f.close()

    json_name.loc[len(json_name) + 1, 'id'] = 29
    json_name.loc[len(json_name), 'category_name'] = 'Missing category'

    country_df = pd.read_csv('{}videos.csv'.format(country))
    country_df['country'] = country
    country_df = country_df.merge(json_name, how='left', left_on='category_id', right_on='id')
    country_df_grouped = country_df.groupby(['category_name']).count()/len(country_df)
    country_df = country_df_grouped['title']

    fig = plt.figure(figsize=(10, 12))
    plt.subplot(111)
    sns.barplot(data=country_df_grouped, x=country_df_grouped.index, y=country_df_grouped['title'])
    plt.title(country)
    plt.ylabel('percentage')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    fig.savefig(country + '.png')