import streamlit as st
import gdown
import pandas as pd
import pickle
import requests

st.markdown(f""" 
<style>
.stApp
{{
background-image:
url('https://th.bing.com/th/id/OIP.ihRM-KXt4H2VF-EOtESd1gHaHU?pid=ImgDet&rs=1');
background-size:100%;
color:white;
font-size:15px;
background-color: rgb(93 17 17);
font-weight:bolder;
}}
.css-1n543e5
{{
        background-color: rgb(93 17 17);
}}


</style>
""",
            unsafe_allow_html=True)


# URLs for the files on Google Drive
# URLs for the files on Google Drive
movies_url =  'https://drive.google.com/uc?id=1_zb0dEjbBnpoiVAXY1tJ8H3dB4XCMNyr'

similarity_url = 'https://drive.google.com/uc?id=1aN88uWER1DKVOoPnR4ycd2Q9sS-yu8Ln'

movies_file_path = 'movies.pkl'
similarity_file_path = 'similarity.pkl'


# Download the files from Google Drive
gdown.download(movies_url, movies_file_path, quiet=False)
gdown.download(similarity_url, similarity_file_path, quiet=False)


movies=pd.DataFrame(pickle.load(open("movies.pkl","rb")))
similarity=pickle.load(open("similarity.pkl","rb"))

# st.write(similarity[0])

st.title("MOVIE RECOMMENDATION SYSTEM")
option = st.selectbox(
    "Select Movie ",
    (movies["title"]))
st.write('You selected:', option)

def poster(movie_id):
    response =requests.get('http://api.themoviedb.org/3/movie/{}?api_key=d7cbcb8365a3c04b0f5687c726a621cd&language=en-US'.format(movie_id))
    data= response.json()
    return 'https://image.tmdb.org/t/p/w185/'+data["poster_path"]
# st.write(poster(155))

def webpage(movie_id):
    response =requests.get('http://api.themoviedb.org/3/movie/{}?api_key=d7cbcb8365a3c04b0f5687c726a621cd&language=en-US'.format(movie_id))
    data= response.json()
    return data["homepage"]
def recommendation(movie):
    movie_index = movies[movies["title"] == movie].index[0]  # returns movies index in dataframe
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    recomend=[]
    posterlist=[]
    homepage=[]
    for A in movie_list:

        recomend.append(movies.iloc[A[0]].title)
        movie_id = movies.iloc[A[0]].movie_id
        #fetch movie Poster using API of TMBD
        posterlist.append(poster(movie_id))
        homepage.append(webpage(movie_id))
    return recomend,posterlist,homepage

# recomended,poster_fetch, homepage=recommendation(option)
# st.write(homepage[0])


if st.button("Recommend"):

    recomended,poster_fetch, homepage=recommendation(option)
    # st.write(homepage[0])
    col1, col2, col3,col4,col5= st.columns(5)

    with col1:
        # st.button(recomended[0],on_click=homepage[0])
        st.write('''
                 <a href={0}>
                 <p>
                 {1}
                 </p>
                 </a>
                 '''.format("\""+homepage[0]+"\"", recomended[0]),
                 unsafe_allow_html=True)
        st.image(poster_fetch[0])

    with col2:
        st.write('''
                 <a href={0}>
                 <p>
                 {1}
                 </p>
                 </a>
                 '''.format("\""+homepage[1]+"\"", recomended[1]),
                 unsafe_allow_html=True)
        st.image(poster_fetch[1])

    with col3:
        st.write('''
                 <a href={0}>
                 <p>
                 {1}
                 </p>
                 </a>
                 '''.format("\""+homepage[2]+"\"", recomended[2]),
                 unsafe_allow_html=True)
        st.image(poster_fetch[2])

    with col4:
        st.write('''
                 <a href={0}>
                 <p>
                 {1}
                 </p>
                 </a>
                 '''.format("\""+homepage[3]+"\"", recomended[3]),
                 unsafe_allow_html=True)
        st.image(poster_fetch[3])
    with col5:
        st.write('''
                 <a href={0}>
                 <p>
                 {1}
                 </p>
                 </a>
                 '''.format("\""+homepage[4]+"\"", recomended[4]),
                 unsafe_allow_html=True)
        st.image(poster_fetch[4])
