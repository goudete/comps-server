import pickle
from rest_framework.response import Response
from bot.models import Ratings
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class Recommend():

    def get_user_recs(self, ratings_data, user_id):
        # get data from Ratings model & clean it
        ratings_df = pd.DataFrame(ratings_data, columns=['user', 'place', 'rating'])
        
        #Normalizing data
        Mean = ratings_df.groupby(by="user",as_index=False)['rating'].mean()
        Rating_avg = pd.merge(ratings_df,Mean,on='user')
        Rating_avg['adg_rating']=Rating_avg['rating_x']-Rating_avg['rating_y']

        # user-place matrix. Will be used to check if a user has rated a place
        check = pd.pivot_table(Rating_avg,values='rating_x',index='user',columns='place')

        #Create user-item ratings matrix
        final = pd.pivot_table(Rating_avg,values='adg_rating',index='user',columns='place')

        #Replacing NaN values with Place Average
        final_place = final.fillna(final.mean(axis=0))

        #Replacing NaN values by User average
        final_user = final.apply(lambda row: row.fillna(row.mean()), axis=1)

        #Replacing NaN values with Place Average
        final_place = final.fillna(final.mean(axis=0))

        # Calculating user similarity
        cosine = cosine_similarity(final_place)
        np.fill_diagonal(cosine, 0 )
        similarity_with_place = pd.DataFrame(cosine,index=final_place.index)
        similarity_with_place.columns=final_user.index

        #Find top 5 most similar users
        sim_user_5_m = self.find_n_neighbours(similarity_with_place, 5)

        Rating_avg = Rating_avg.astype({"place": str})
        Place_user = Rating_avg.groupby(by = 'user')['place'].apply(lambda x:','.join(x))

        return self.User_item_score1(check, sim_user_5_m, Place_user, final_place, Mean, similarity_with_place, user_id)
        
    # Find n Nearest Neighbors
    def find_n_neighbours(self, df, n):
        order = np.argsort(df.values, axis=1)[:, :n]
        df = df.apply(lambda x: pd.Series(x.sort_values(ascending=False)
            .iloc[:n].index, 
            index=['top{}'.format(i) for i in range(1, n+1)]), axis=1)
        return df

    # Returns top 5 recommendations given a user_id
    def User_item_score1(self, check, sim_user_5_m, Place_user, final_place, Mean, similarity_with_place, user):
        Place_seen_by_user = check.columns[check[check.index==user].notna().any()].tolist()
        a = sim_user_5_m[sim_user_5_m.index==user].values
        b = a.squeeze().tolist()
        d = Place_user[Place_user.index.isin(b)]
        l = ','.join(d.values)
        Place_seen_by_similar_users = l.split(',')
        Places_under_consideration = list(set(Place_seen_by_similar_users)-set(list(map(str, Place_seen_by_user))))
        Places_under_consideration = list(map(int, Places_under_consideration))
        score = []
        for item in Places_under_consideration:
            c = final_place.loc[:,item]
            d = c[c.index.isin(b)]
            f = d[d.notnull()]
            avg_user = Mean.loc[Mean['user'] == user,'rating'].values[0]
            index = f.index.values.squeeze().tolist()
            corr = similarity_with_place.loc[user,index]
            fin = pd.concat([f, corr], axis=1)
            fin.columns = ['adg_score','correlation']
            fin['score']=fin.apply(lambda x:x['adg_score'] * x['correlation'],axis=1)
            nume = fin['score'].sum()
            deno = fin['correlation'].sum()
            final_score = avg_user + (nume/deno)
            score.append(final_score)
        data = pd.DataFrame({'place':Places_under_consideration,'score':score})
        top_5_recommendation = data.sort_values(by='score',ascending=False).head(5)
        top5 = top_5_recommendation.place.values.tolist()

        return top5