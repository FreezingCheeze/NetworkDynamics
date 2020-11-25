import json
import os
import matplotlib.pyplot as plt

DIR_YT = "youtube_top100"
DIR_SPOT = "spotify_top100"
DIR_3FM = "radio3fm_megahit"
DIR_538 = "radio538_alarmschijf"

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


def likes_dislikes(songname):
    # returns a tuple containing a list with likes and a list with dislikes,
    # corresponding to the given songname, for a year
    likes = []
    dislikes = []
    differences = []
    for filename in os.listdir("youtube_top100"):
        for song in load_json("youtube_top100/" + filename):
            if songname in song['snippet']['title']:
                like = int(song['statistics']['likeCount'])
                dislike = int(song['statistics']['dislikeCount'])
                likes.append(like)
                dislikes.append(dislike)
                differences.append(abs(like - dislike))
    return likes, dislikes, differences


def differences(likes_dislikes):
    res = []
    for entry in zip(likes_dislikes[0], likes_dislikes[1]):
        res.append(abs(int(entry[0]) - int(entry[1])))
    return res


def print_differences(data):
    for song in data:
        name = song['snippet']['title']
        difference = abs(int(song['statistics']['likeCount']) - int(song['statistics']['dislikeCount']))
        print(str(difference) + "\t\t" + name)


# This function was copied from last weeks files
def plot_graph(songname, type):
    '''
    Plots a graph with the days throughout a year on the x-axis and (dis)like count on the y-axis
    '''

    types = ['likes', 'dislikes', 'difference']
    if type not in types:
        raise ValueError("Invalid type, expected: ", types)
    else:
        index = types.index(type)

    results = likes_dislikes(songname)

    plt.plot(results[index])

    plt.xlabel('days')
    plt.ylabel(type)
    plt.title(songname)
    plt.show()
    return None


plot_graph('Hello', 'likes')
plot_graph('Hello', 'dislikes')
plot_graph('Hello', 'difference')

