import streamlit as st
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
font-weight:bolder;
}}

</style>
""",
            unsafe_allow_html=True)

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

if st.button("Recommend"):
    recomended,poster_fetch=recommendation(option)
    col1, col2, col3,col4,col5= st.columns(5)

    with col1:
        st.button(recomended[0],on_click=homepage[0])
        st.image(poster_fetch[0])

    with col2:
        st.text(recomended[1])
        st.image(poster_fetch[1])

    with col3:
        st.text(recomended[2])
        st.image(poster_fetch[2])

    with col4:
        st.text(recomended[3])
        st.image(poster_fetch[3])
    with col5:
        st.text(recomended[4])
        st.image(poster_fetch[4])
