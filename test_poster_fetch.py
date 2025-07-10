#!/usr/bin/env python3
"""
Test script to verify poster fetching functionality
"""

import pickle
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import fetch_poster, test_poster_fetch

def test_multiple_movies():
    """Test poster fetching for multiple movies"""
    print("Loading movie data...")
    movies = pickle.load(open('movie_list.pkl','rb'))
    
    # Test first 5 movies
    print("\n=== Testing first 5 movies ===")
    for i in range(5):
        movie_id = movies.iloc[i].movie_id
        title = movies.iloc[i].title
        print(f"\nTesting: {title} (ID: {movie_id})")
        result = test_poster_fetch(movie_id)
        print(f"Result: {result}")
        print("-" * 50)

if __name__ == "__main__":
    test_multiple_movies()
