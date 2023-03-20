import numpy as np

def fetch_Metal_Tally(df,year,country):
    medal_df =df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag=0
    if year== 'Overall' and country  == 'Overall':
        temp_df=medal_df
    if year =='Overall' and country!='Overall':
        flag=1
        temp_df=medal_df[medal_df['region']==country]
    if year !='Overall' and country=='Overall':
        temp_df=medal_df[medal_df['Year']==int(year)]
    if year!='Overall' and country != 'Overall':
        temp_df=medal_df[(medal_df['Year']==int(year)) & (medal_df['region']==country)]
    if flag  ==1:
        x=temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
        x=temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    x['Total']= x['Gold']+x['Silver']+x['Bronze']
    return x


def Medal_Tally(df):
    Medal_Tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    Medal_Tally=Medal_Tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    Medal_Tally['Total'] = Medal_Tally['Gold'] + Medal_Tally['Silver'] + Medal_Tally['Bronze']


    Medal_Tally['Gold']= Medal_Tally['Gold'].astype('int')
    Medal_Tally['Silver'] = Medal_Tally['Silver'].astype('int')
    Medal_Tally['Bronze'] = Medal_Tally['Bronze'].astype('int')
    Medal_Tally['Total'] = Medal_Tally['Total'].astype('int')

    return Medal_Tally


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')
    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')
    return years,country

def data_over_time(df,col):
    # Participating nation over time :
    data_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('index')
    data_over_time.rename(columns={'index': 'Edition', 'Year': col}, inplace=True)
    return data_over_time


def most_sucessful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    pt = ((new_df.pivot_table(index='Sport',columns='Year',aggfunc='count').fillna(0)))

    return pt

def most_sucessful_countrywise(df,country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='index', right_on='Name', how='left')[
            ['index', 'Name_x', 'Sport']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport!= 'Overall':
     temp_df = athlete_df[athlete_df['Sport'] == sport]
    else:
     return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final.fillna(0, inplace=True)
    return final


def athlete_info(df, name):
    temp_df = df.dropna(subset=[ 'Medal','Team', ])

    if name != 'Overall':
        temp_df = temp_df[temp_df['Name'] == name]
    x = temp_df['Name'].value_counts().reset_index().merge(df, left_on='index', right_on='Name', how='left')[
    ['index', 'Name_x', 'Sex', 'Age', 'Height', 'Weight', 'Team', 'Sport', 'region']]


    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)

    return x


def filter_by_name(df, name):
    if name != 'Overall':
        df[df['Name'] == name][
            ['Name', 'Sex', 'Age', 'Height', 'Weight', 'Team', 'Year', 'Season', 'City', 'Sport', 'Event', 'region',
             'Gold', 'Silver', 'Bronze']]
    else:
        print('error found')
    return df[df['Name'] == name][
        ['Name', 'Sex', 'Age', 'Height', 'Weight', 'Team', 'Year', 'Season', 'City', 'Sport', 'Event', 'region', 'Gold',
         'Silver', 'Bronze']]

