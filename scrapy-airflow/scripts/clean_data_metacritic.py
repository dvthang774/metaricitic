
df_games = pd.read_csv('desktop/2023-05-08.csv')
df_games.drop('Unnamed: 0', axis = 1, inplace = True)
df_games['year'] = df_games['release_date'].apply(lambda x : x[-4:])
df_games = df_games.loc[~(df_games['user_score']=='tbd')]
df_games['user_score'] = pd.to_numeric(df_games['user_score'], downcast = 'integer')
df_games['user_score'] = df_games['user_score'].apply(lambda x : int(x * 10))
