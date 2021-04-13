import pandas as pd
import math


songmetadata = pd.read_csv('genre.csv')
songdata = pd.read_csv('songdata.csv')

song_df = pd.merge(songdata, songmetadata.drop_duplicates(['song_id']), on="song_id", how="left")
song_grouped = song_df.groupby(['song_id']).agg({"listen_count":"count"}).sort_values(['listen_count'],ascending = False)

popularsongs = pd.merge(song_grouped, songmetadata.drop_duplicates(['song_id']), on="song_id", how="left")
#popularsongs.to_csv('popularsongs.csv')

def recommend(user):
    personalised = song_df[song_df['user_id']==user].drop(['user_id'],axis=1)
    
    genre_dict = {}
    for i in personalised.genre.unique():
        genre_dict[i] = sum(personalised[personalised['genre']==i]['listen_count'])
    sorted_genre_dict = sorted(genre_dict.items(), key=lambda x: x[1], reverse = True)
    
    listen_sum = sum(personalised['listen_count'])
    recommend = pd.DataFrame(columns = ['song_id', 'listen_count', 'track_href', 'genre', 'song_name'])
    
    for i in sorted_genre_dict:
        per_genre = math.ceil((i[1] / listen_sum ) * 10)
        
        df1 = popularsongs[popularsongs['genre']==i[0]]
        common = df1.merge(personalised,on=['song_id'])
        recommend = recommend.append(df1[~df1.song_id.isin(common.song_id)].head(per_genre), ignore_index = True)
    print(recommend)  
    
#recommend('U0001')