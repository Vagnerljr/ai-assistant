import requests
import streamlit as st 
import pandas as pd 




url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3ZDU0MTUwMzE3Y2U5ODgxMmQ0YzJhMDAwYTIzYTRlMCIsIm5iZiI6MTc1Njc0MTI2OC45LCJzdWIiOiI2OGI1YmU5NGMwZmI0YjYwOWJiNGZhODAiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.iyH3QLjdgrIqb_Bvrm-7hTYVT9lZedOiQS7EIj3b44o"
}
yearSearch = st.text_input('Year of the movie')
if yearSearch:
    url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&primary_release_year={yearSearch}&sort_by=popularity.desc"

response = requests.get(url, headers=headers)
data = response.json()

movieData = []

for item in data['results']:
    movieTitle = item['original_title']
    imdbRate = item['vote_average']
    description = item['overview']
    movieData.append({'Title':movieTitle, 'Rating':imdbRate, 'Sinopse':description, })

df = pd.DataFrame(movieData)
df = df.sort_values(by="Rating", ascending=False)





movieTable = st.dataframe(df, use_container_width=True, hide_index= True)


