import json
import os
import matplotlib.pyplot as plt

SLASH = "/"
DIR_YT = "youtube_top100"
DIR_SPOT = "spotify_top100"
DIR_3FM = "radio3fm_megahit"
DIR_538 = "radio538_alarmschijf"

snippet = 'snippet'
title = 'title'
statistics = 'statistics'

tracks = 'tracks'
items = 'items'
track = 'track'
name = 'name'
popularity = 'popularity'

likeCount = 'likeCount'
dislikeCount = 'dislikeCount'
viewCount = 'viewCount'

def load_json(filename):
    # load json file as dictionary
    with open(filename) as json_file: return json.load(json_file)


def print_all_songs():
    #overview of all songs from the 4 datasets
    print("Youtube's Top 100 Songs:")
    dummy_file = load_json("youtube_top100/20151109_1800_data.json")
    for song in dummy_file:
        print(song['snippet']['title'])
    print()

    print("Spotify's Top 100 Songs:")
    dummy_file = load_json("spotify_top100/20151109_1800_data.json")
    for song in dummy_file['tracks']['items']:
        print(song['track']['name'])
    print()

    print("Radio 3FM megahit's songs")
    dummy_file = load_json("radio3fm_megahit/20161028_1800_data.json")
    for song in dummy_file:
        print(song['snippet']['title'])
    print()

    print("Radio 538 alarmschijf's songs")
    dummy_file = load_json("radio538_alarmschijf/20161028_1800_data.json")
    for song in dummy_file:
        print(song['snippet']['title'])
    print()


def get_statistics(songname, dir, *args):
    if dir == DIR_SPOT:
        raise ValueError("Don't use the Spotify dataset with this function")

    temp = []
    for filename in os.listdir(dir):
        for song in load_json(dir + SLASH + filename):
            if songname in song[snippet][title]:
                res = []
                for arg in args:
                    res.append(int(song[statistics][arg]))
                temp.append(res)

    result = []
    for i in range(len(args)):
        res = []
        for j in range(len(temp)):
            res.append(temp[j][i])
        result.append(res)

    return result

def get_differences(songname, dir):
    results = get_statistics(songname, dir, likeCount, dislikeCount)
    differences = []

    for i in range(len(results[0])):
        likes = results[0][i]
        dislikes = results[1][i]
        differences.append(abs(likes - dislikes))

    results.append(differences)
    return results

def get_popularity(songname):
    res = []
    for filename in os.listdir(DIR_SPOT):
        if filename.endswith('.json'):
            for song in load_json(DIR_SPOT + SLASH + filename)[tracks][items]:
                if song  and songname in song[track][name]:
                    res.append(song[track][popularity])
    return res

# This function was copied from last weeks files
def plot_differences(songname, dir):
    '''
    Plots a graph with the days throughout a year on the x-axis and (dis)like count on the y-axis
    '''
    results = get_differences(songname, dir)

    types = ['likes', 'dislikes', 'difference']
    for i in range(len(results)):
        plt.plot(results[i], label=types[i])

    plt.xlabel('days')
    plt.legend()
    plt.title(songname)
    plt.show()
    return None

def plot_views(songname, dir):
    results = get_statistics(songname, dir, viewCount)
    plt.plot(results[0])

    plt.xlabel('days')
    plt.ylabel('views')
    plt.title(songname)
    plt.show()

def plot_popularity(songname):
    results = get_popularity(songname)
    plt.plot(results)
    plt.xlabel('days')
    plt.ylabel('popularity')
    plt.title(songname)
    plt.show()

def plot_all_differences(songs):
    for song in songs:
        plot_differences(song, DIR_YT)


def plot_all_views(songs):
    for song in songs:
        plot_views(song, DIR_YT)


def plot_all_popularity(songs):
    for song in songs:
        plot_popularity(song)


def plot_all(songs):
    for song in songs:
        plot_differences(song, DIR_YT)
        plot_views(song, DIR_YT)
        plot_popularity(song)

print_all_songs()

SONGS_538 = [
    'Fais & Afrojack - Used To Have It All (Official Video)'
]

SONGS_YT = [
    'Hello'
    , 'Sorry'
    , 'Hotline Bling'
    , 'What Do You Mean?'
    , 'Stitches'
    , 'On My Mind'
    , 'Focus'
    , 'How Deep Is Your Love'
    , 'The Hills'
    , 'Same Old Love'
         ]

#plot_all_views(SONGS_YT)
