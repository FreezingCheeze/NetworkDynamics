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
    # overview of all songs from the 4 datasets
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


def tuples_to_list(tuples):
    result = []
    for i in range(len(tuples[0])):
        res = []
        for j in range(len(tuples)):
            res.append(tuples[j][i])
        result.append(res)

    return result

# region Stats


def get_statistics(songname, dir, *args):
    if dir == DIR_SPOT:
        raise ValueError("Don't use the Spotify dataset with this function")

    # Temp will be a list of len(arg)-tuples,
    # where each tuple will contain the values requested in args at that time point in the data set
    # Examples of args are: likeCount, dislikeCount, viewCount
    temp = []
    for filename in os.listdir(dir):
        for song in load_json(dir + SLASH + filename):
            if songname in song[snippet][title]:
                res = []
                for arg in args:
                    res.append(int(song[statistics][arg]))
                temp.append(res)

    return tuples_to_list(temp)


def get_differences(songname, dir):
    # Get the lists of likes and dislikes for the given song in the given directory/dataset
    results = get_statistics(songname, dir, likeCount, dislikeCount)

    # Calculate the differences
    differences = []
    for i in range(len(results[0])):
        likes = results[0][i]
        dislikes = results[1][i]
        differences.append(abs(likes - dislikes))

    # Append the differences list to the result,
    # creating a list of 3 lists with likes, dislikes and differences respectively
    results.append(differences)
    return results


# Returns a list of popularity values over time for the given song from the spotify dataset
def get_popularity(songname):
    res = []
    for filename in os.listdir(DIR_SPOT):
        if filename.endswith('.json'):
            for song in load_json(DIR_SPOT + SLASH + filename)[tracks][items]:
                if songname in song[track][name]:
                    res.append(song[track][popularity])
    return res


# Creates a dict from a song to its popularity for the 100 top songs in the given spotify dataset
def rank_spotify(filename):
    res = dict()
    for song in load_json(DIR_SPOT + SLASH + filename)[tracks][items]:
        songname = song[track][name]
        index = song[track][popularity]
        res[songname] = index

    return sorted(res.items(), key=lambda x: x[1])


# Creates a dict from a song to its views for the 100 top songs in the given youtube dataset
def rank_youtube(filename):
    res = dict()
    for song in load_json(DIR_YT + SLASH + filename):
        songname = song[snippet][title]
        views = song[statistics][viewCount]
        res[songname] = views

    return sorted(res.items(), key=lambda x: x[1], reverse=True)


def song_rankings(song):
    res = []
    for filename in os.listdir(DIR_SPOT):
        if filename in os.listdir(DIR_YT) and filename.endswith(".json"):
            spotify_rankings = rank_spotify(filename)
            youtube_rankings = rank_youtube(filename)

            for i in range(len(spotify_rankings)): # Check which entry the song is in spotify
                entry = spotify_rankings[i]
                if song in entry[0]:

                    for j in range(len(youtube_rankings)): # check which entry the song is in youtube
                        entry = youtube_rankings[j]
                        if song in entry[0]:
                            res.append((i, j))
                            break

    return tuples_to_list(res)

# endregion

# region Plots


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


def plot_rankings(songname):
    results = song_rankings(songname)
    types = ['Spotify Ranking', 'Youtube Ranking']
    for i in range(len(results)):
        plt.plot(results[i], label=types[i])
    plt.xlabel('days')
    plt.legend()
    plt.title(songname)
    plt.show()

#endregion

# region Plot All


def plot_all_differences(songs, dir):
    for song in songs:
        plot_differences(song, dir)


def plot_all_views(songs, dir):
    for song in songs:
        plot_views(song, dir)


def plot_all_popularity(songs):
    for song in songs:
        plot_popularity(song)


def plot_all_rankings(songs):
    for song in songs:
        plot_rankings(song)


def plot_all(songs):
    for song in songs:
        plot_differences(song, DIR_YT)
        plot_views(song, DIR_YT)
        plot_popularity(song)
        plot_rankings(song)


# endregion

SONGS_3FM = ['Bastille - Send Them Off!']

SONGS_538 = [
    'Fais & Afrojack - Used To Have It All (Official Video)'
    , "DIT IS 4U MET 'BITTER TASTE' – The Next Boy/Girl Band"
    , 'Kensington - Sorry (official audio)'
            ]

# Youtube songs can also be used for spotify datalist
SONGS_YT = [
    'Hello'
    , 'Good For You'
    , 'Hotline Bling'
    , 'Jumpman'
    , 'Stitches'
    , 'On My Mind'
    , '7 Years'
    , 'How Deep Is Your Love'
    , 'The Hills'
    , 'Same Old Love'
         ]


#print_all_songs()

#plot_all_views(SONGS_3FM, DIR_3FM)
#plot_all_views(SONGS_538, DIR_538)
#plot_all_views(SONGS_YT, DIR_YT)
#plot_all_popularity(SONGS_YT)

#plot_all_popularity(SONGS_YT)
plot_all_rankings(SONGS_YT)