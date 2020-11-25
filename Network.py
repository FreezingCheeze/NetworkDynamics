import json
import os
import matplotlib.pyplot as plt

SLASH = "/"
DIR_YT = "youtube_top100"
DIR_SPOT = "spotify_top100"
DIR_3FM = "radio3fm_megahit"
DIR_538 = "radio538_alarmschijf"

def load_json(filename):
    # load json file as dictionary
    with open(filename) as json_file: return json.load(json_file)


def get_views(songname):
    # corresponding to the given songname, for a year
    views = []
    for filename in os.listdir(DIR_YT):
        for song in load_json(DIR_YT + SLASH + filename):
            if songname in song['snippet']['title']:
                views.append(int(song['statistics']['viewCount']))

    return views

def plot_views(songname):
    views = get_views(songname)
    plt.plot(views)
    plt.xlabel('days')
    plt.ylabel('views')
    plt.title('songname')
    plt.show()

plot_views('Hello')