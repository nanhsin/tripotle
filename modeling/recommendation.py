import random
import pandas as pd

def get_random_songs(num_songs=1):
    df = pd.read_csv('billboard_lyrics_1960-2024.csv')
    return df.sample(n=num_songs).to_dict(orient='records')

if __name__ == '__main__':
    num_songs = int(input("How many songs would you like? "))
    recommendations = get_random_songs(num_songs)
    for song in recommendations:
        print(f"{song['title']} by {song['artist']} ({song['year']})")