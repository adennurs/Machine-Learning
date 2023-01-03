import flask
import pandas as pd
import numpy as np
import math
from sklearn.cluster import KMeans

app = flask.Flask(__name__, template_folder='templates')
df = pd.read_csv('track.csv') 
all_titles = [df['name'][i] for i in range(len(df['name']))]
def get_recommendations(name_of_song): 
    
    #Reading our data 
    df = pd.read_csv('track.csv') 
    pd.set_option('display.max_colwidth', 400)
   
    #Saving coluns  
    columns_to_cluster = ['energy', 'loudness','acousticness'] 
     
    #Taking top 100000 songs for wasting less time 
    df=df.head(10000) 
     
    #the  main dataset 
    x=df[['energy','loudness','acousticness']].values 
     
    #deviding dataset to clusters 
    kmeans = KMeans(n_clusters=10, init='k-means++', random_state=0).fit(x) 
     
    #training dataset 
    df['cluster'] = kmeans.fit_predict(df[df.columns[9:12]]) 
     
    #finding centroids 
    centroids = kmeans.cluster_centers_  
     
    #Saving the centers 
    center_df = pd.DataFrame(centroids, columns = ['centerX','centerY', 'centerZ'])   
     
     
    # finding the cluster of our song  
    energy = '' 
    loudness = '' 
    cluster_of_song = 0; 
    df.iloc[0]['name'] 
    for i in range(0,len(df)): 
        if name_of_song == df.iloc[i]['name']: 
            cluster_of_song = df.iloc[i]['cluster'] 
            energy = df.iloc[i]['energy'] 
            loudness = df.iloc[i]['loudness'] 
            acousticness = df.iloc[i]['acousticness'] 
            break 

    #finding the songs in this cluster, and saving them in to songs_in_cluster 
    songs_in_cluster = [] 
    for i in range(0,len(df)): 
        if cluster_of_song == df.iloc[i]['cluster']: 
            songs_in_cluster.append(df.iloc[i]) 

    #finding the distance between song and other songs 
     
    distances = [] 
    for i in range(0,len(songs_in_cluster)): 
        distances.append(math.sqrt(pow(energy-songs_in_cluster[i]['energy'] , 2) + pow( loudness-songs_in_cluster[i]['loudness'] , 2) +  pow(acousticness-songs_in_cluster[i]['acousticness'] , 2))) 
     
    #Embeding songs to pandas      
    x = np.array(songs_in_cluster)  
    data_pan = pd.DataFrame(x)  
     
    #Adding distances to pandas 
    data_pan['distances'] = distances 
     
    #Sorting pandas by a distances  
    data_pan.sort_values(by=['distances']) 
    resa = [] 
    resa1 = [] 
    resa2 = []  
    res = [] 
     
    #Getting top 10 best songs in pandas 
    for i in range(0,11): 
        if(i!=0): 
            resa.append(data_pan.iloc[i][3]) 
            resa1.append(data_pan.iloc[i][6]) 
            resa2.append(data_pan.iloc[i][13]) 
    res.append(resa) 
    res.append(resa1) 
    res.append(resa2) 
    res = pd.DataFrame() 
    res['name'] = resa 
    res['years'] = resa1
    res['url'] = resa2 
    return res
@app.route('/', methods=['GET', 'POST'])

    
def main():
    if flask.request.method == 'GET':
        return(flask.render_template('index.html'))
            
    if flask.request.method == 'POST':
        m_name = " ".join(flask.request.form['music_name'].split())
        if m_name not in all_titles:
            return(flask.render_template('notFound.html',name=m_name))
        elif m_name in all_titles:
            result_final = get_recommendations(m_name)
            names = []
            releaseDate = []
            homepage = []
            for i in range(len(result_final)):
                names.append(result_final.iloc[i][0])
                releaseDate.append(result_final.iloc[i][1])
                # url.append(result_final.iloc[i][2])
                if(len(str(result_final.iloc[i][2]))>3):
                    homepage.append(result_final.iloc[i][2])
                else:
                    homepage.append("#")
            return flask.render_template('found.html',music_names=names,search_name=m_name,music_releaseDate=releaseDate,music_homepage=homepage)

@app.route('/about/')
def about():
    return flask.render_template('about.html')

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
    #app.run()
