import pickle
import streamlit as st
import requests
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

TMDB_API_KEY = os.getenv('TMDB_API_KEY', '8c2c886a9984022126be0df2b6fcd352')

def test_poster_fetch(movie_id):
    """Debug function to test poster fetching"""
    print(f"\n=== Testing poster fetch for movie_id: {movie_id} ===")
    result = fetch_poster(movie_id)
    print(f"Result: {result}")
    return result

def fetch_poster(movie_id, retries=5):
    if not movie_id:
        print(f"Invalid movie_id: {movie_id}")
        return "https://via.placeholder.com/500x750?text=Invalid+Movie+ID"

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    
    for attempt in range(retries):
        try:
            print(f"Fetching poster for movie ID: {movie_id} (Attempt {attempt + 1}/{retries})")
            
            # Use session for connection reuse
            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            response = session.get(url, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                poster_path = data.get('poster_path')
                if poster_path:
                    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                    print(f"Successfully fetched poster for movie {movie_id}")
                    return poster_url
                else:
                    print(f"No poster available for movie {movie_id}")
                    return "https://via.placeholder.com/500x750?text=No+Poster+Available"
            elif response.status_code == 404:
                print(f"Movie {movie_id} not found")
                return "https://via.placeholder.com/500x750?text=Movie+Not+Found"
            elif response.status_code == 401:
                print(f"API authentication error for movie {movie_id}")
                return "https://via.placeholder.com/500x750?text=API+Error" 
            elif response.status_code == 429:
                print(f"Rate limit exceeded for movie {movie_id}, waiting longer...")
                time.sleep(5 * (attempt + 1))
            else:
                print(f"HTTP {response.status_code} error for movie {movie_id}")
                
        except requests.exceptions.ConnectionError as e:
            print(f"[Retry {attempt+1}/{retries}] Connection error for movie {movie_id}: {e}")
            time.sleep(3 * (attempt + 1)) 
        except requests.exceptions.Timeout as e:
            print(f"[Retry {attempt+1}/{retries}] Timeout error for movie {movie_id}: {e}")
            time.sleep(2 * (attempt + 1))
        except requests.exceptions.RequestException as e:
            print(f"[Retry {attempt+1}/{retries}] Request error for movie {movie_id}: {e}")
            time.sleep(2 * (attempt + 1))
        except Exception as e:
            print(f"[Retry {attempt+1}/{retries}] Unexpected error for movie {movie_id}: {e}")
            time.sleep(2 * (attempt + 1))
    
    print(f"All retries failed for movie {movie_id}")
    return "https://via.placeholder.com/500x750?text=Fetch+Failed"

def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        
        # Get movie details first
        movie_data_list = []
        for i in distances[1:6]:
            movie_data = movies.iloc[i[0]]
            movie_id = movie_data.movie_id
            movie_title = movie_data.title
            movie_data_list.append((movie_id, movie_title))
        

        recommended_movie_names = []
        recommended_movie_posters = []
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_movie = {}
            for movie_id, movie_title in movie_data_list:
                if movie_id and str(movie_id).isdigit():
                    future = executor.submit(fetch_poster, movie_id)
                    future_to_movie[future] = (movie_id, movie_title)
                else:
                    print(f"Invalid movie_id for {movie_title}: {movie_id}")
                    future_to_movie[None] = (movie_id, movie_title)
            
            for movie_id, movie_title in movie_data_list:
                found = False
                for future in future_to_movie:
                    if future_to_movie[future] == (movie_id, movie_title):
                        if future is None:
                            poster_url = "https://via.placeholder.com/500x750?text=Invalid+ID"
                        else:
                            try:
                                poster_url = future.result(timeout=30)
                            except Exception as e:
                                print(f"Error fetching poster for {movie_title}: {e}")
                                poster_url = "https://via.placeholder.com/500x750?text=Fetch+Error"
                        
                        recommended_movie_posters.append(poster_url)
                        recommended_movie_names.append(movie_title)
                        found = True
                        break
                
                if not found:
                    recommended_movie_posters.append("https://via.placeholder.com/500x750?text=Error")
                    recommended_movie_names.append(movie_title)

        return recommended_movie_names, recommended_movie_posters
    except Exception as e:
        print(f"Error in recommend function: {e}")
        return [], []


st.header('Movie Recommender System')
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    # Show loading progress
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text('Finding similar movies...')
        progress_bar.progress(20)
        
        status_text.text('Fetching movie posters...')
        progress_bar.progress(50)
        
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        progress_bar.progress(100)
        status_text.text('Done!')
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        if recommended_movie_names:
            st.subheader(f"Movies similar to '{selected_movie}'")
            col1, col2, col3, col4, col5 = st.columns(5)
            columns = [col1, col2, col3, col4, col5]
            
            for i, (name, poster) in enumerate(zip(recommended_movie_names, recommended_movie_posters)):
                with columns[i]:
                    st.text(name)
                    try:
                        if "placeholder" in poster or "via." in poster:
                            st.image(poster, use_container_width=True, caption="Poster unavailable")
                        else:
                            st.image(poster, use_container_width=True)
                    except Exception as e:
                        st.error(f"Error loading poster")
                        st.image("https://via.placeholder.com/500x750?text=Error+Loading+Poster", use_container_width=True)
        else:
            st.error("Sorry, couldn't fetch recommendations. Please try again.")
    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        st.error(f"An error occurred: {str(e)}")