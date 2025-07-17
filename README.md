# 🎥 Project: Movie Recommendation System using Machine Learning

## 📌 Project Overview

This project is a **Movie Recommendation System** built using **Machine Learning**, **Python**, and **Streamlit**. It recommends movies similar to the user's choice by leveraging **content-based filtering** based on movie overviews and genres. It uses **cosine similarity** to calculate the similarity score between movies and suggest the most relevant ones. The goal is to enhance user experience by offering intelligent movie suggestions with poster previews using the **TMDB API**.




## 🎥Live Demo
[Click here to watch the demo video](https://drive.google.com/file/d/1WNSKXbmn5a-7CR3hFn33XDZuAj45bQbS/view?usp=sharing)


## ✅ Functionalities

- 🔍 **Content-Based Filtering** using movie overviews and genres
- 📦 Preprocessed dataset of over 5,000 movies (from TMDB)
- 📑 Similarity computation using cosine similarity
- 🎨 User interface built with Streamlit
- 🎞️ Poster images fetched from TMDB API
  
## 📊 Dataset

This project uses the [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) from Kaggle.


## 🔧 Tools & Technologies

| Tool           | Description                                      |
|----------------|--------------------------------------------------|
| Python         | Programming Language                             |
| Pandas         | Data Handling & Manipulation                     |
| Scikit-learn   | Cosine Similarity Computation                    |
| Pickle         | Saving ML Model Artifacts                        |
| Streamlit      | Frontend Framework for Web UI                    |
| TMDB API       | To Fetch Movie Posters & Metadata                |

## 🧠 How It Works

The Movie Recommendation System follows a structured pipeline to deliver personalized movie suggestions based on user input. Below is the process visualized in a flowchart:

```
graph TD
    A[Start: Load TMDB 5000 Dataset] -->|Read CSV| B[Preprocess Metadata]
    B -->|Combine Genres, Overviews| C[Clean and Format Text Data]
    C --> D[Apply TF-IDF Vectorizer]
    D -->|Convert Text to Vectors| E[Compute Cosine Similarity Matrix]
    E --> F[Store Similarity Matrix in Pickle]
    F --> G[User Opens Streamlit App]
    G --> H[Select Movie from Dropdown]
    H --> I[Retrieve Top-N Similar Movies]
    I -->|Query TMDB API| J[Fetch Movie Posters and Metadata]
    J --> K[Display Recommendations with Posters]
    K --> L[End: User Enjoys Suggestions]
```

## 📁 Project Structure

```bash
Movie-Recommendation/
├── main.py                     # Streamlit app
├── MOVIE RECOMMENDER SYSTEM.ipynb  # Jupyter notebook Code
├── movie_list.pkl              # Pickle file of movie names and similarity matrix
├── test_poster_fetch.py        # Poster-fetch testing script
├── tmdb_5000_movies.csv        # Dataset
├── README.md                   # Project documentation

```


## 🙋‍♀️ Author

**Shivangi**  
_Data Science & Analytics Enthusiast_  
[GitHub Profile](https://github.com/vaish-shivangi)



