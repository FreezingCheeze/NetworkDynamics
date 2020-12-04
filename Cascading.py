# Bas Kool 			-	s2176386
# Gies den Broeder 	-	s2161168

import json
import os
import matplotlib.pyplot as plt

# region Constants

SLASH = "/"
DIR_YT = "youtube_top100"
DIR_SPOT = "spotify_top100"
DIR_3FM = "radio3fm_megahit"
DIR_538 = "radio538_alarmschijf"

DATA = "20151109_1800_data.json"

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

# endregion

# region Tools

def load_json(filename):
    # load json file as dictionary
    with open(filename) as json_file: return json.load(json_file)


# Converts a list of tuples to a list of len(tuple) lists containing the values of the tuples
def tuples_to_list(tuples):
    result = []
    for i in range(len(tuples[0])):
        res = []
        for j in range(len(tuples)):
            res.append(tuples[j][i])
        result.append(res)

    return result

# endregion

# region Stats

# Returns a list of len(arg)-lists containing the values for the given statistics(args) for the given song from the given dataset
def get_statistics(songname, dir, *args):
    if dir == DIR_SPOT:
        raise ValueError("Don't use the Spotify dataset with this function")

    # Temp will be a list of len(arg)-tuples,
    # where each tuple will contain the values requested in args of the requested song,
    # at all time points in the data set
    # Examples of args are: likeCount, dislikeCount, viewCount
    temp = []
    for num, filename in enumerate(os.listdir(dir), start=1):
        for song in load_json(dir + SLASH + filename):
            if songname in song[snippet][title]:
                res = []
                for arg in args:
                    res.append(int(song[statistics][arg]))
                temp.append(res)

        if len(temp) != num:
            res = []
            for arg in args:
                res.append(0)
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

    for num, filename in enumerate(os.listdir(DIR_SPOT), start=1):
        if filename.endswith('.json'):
            for song in load_json(DIR_SPOT + SLASH + filename)[tracks][items]:
                if songname == song[track][name]:
                    res.append(song[track][popularity])

            if len(res) != num: # if song was not found in timeslot, add 0 for its place
                res.append(0)

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


# Produces a list of 2 lists, containing the rankings over time for youtube views, and popularity on spotify
def song_rankings(song):
    res = []
    for filename in os.listdir(DIR_SPOT):
        if filename in os.listdir(DIR_YT) and filename.endswith(".json"):
            spotify_rankings = rank_spotify(filename)
            youtube_rankings = rank_youtube(filename)

            temp = []
            for i in range(len(spotify_rankings)): # Check which entry the song is in spotify
                entry = spotify_rankings[i]
                if song == entry[0]:
                    temp.append(i)

            if len(temp) == 0: # put a 100 if there is no entry for this song in this timeslot
                temp.append(100)

            for j in range(len(youtube_rankings)): # check which entry the song is in youtube
                entry = youtube_rankings[j]
                if song in entry[0]:
                    temp.append(j)

            if len(temp) == 1: # put a 100 if there is no entry for this song in this timeslot
                temp.append(100)

            res.append(temp)

    return tuples_to_list(res)


# Computes the average distance between youtube and spotify ranking for the given dataset
def average_distance(rankings):
    length = len(rankings[0])
    total = 0

    for i in range(length):
        spot_rank = rankings[0][i]
        yt_rank = rankings[1][i]
        total += abs(spot_rank - yt_rank)

    total = total / length
    return total


#endregion

# region Plots

# Plots the differences (likes, dislikes and difference between them), for the given song, in the given directory over time
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


# Plots the views for the given song, in the given directory over time
def plot_views(songname, dir):
    results = get_statistics(songname, dir, viewCount)
    plt.plot(results[0])

    plt.xlabel('days')
    plt.ylabel('views')
    plt.title(songname)
    plt.show()


# Plots the popularity of the given song in the spotify dataset
def plot_popularity(songname):
    results = get_popularity(songname)
    plt.plot(results)

    plt.xlabel('days')
    plt.ylabel('popularity')
    plt.title(songname)
    plt.show()


# Plots the rankings in the spotify and youtube dataset over time, for the given song
def plot_rankings(songname):
    results = song_rankings(songname)

    types = ['Spotify Ranking', 'Youtube Ranking']
    for i in range(len(results)):
        plt.plot([100 - x for x in results[i]], label=types[i]) # invert the results to have higher values be better in the plot
    plt.xlabel('days')
    plt.legend()
    plt.title(songname)
    plt.show()
    return average_distance(results)


# Plots the views of the songs on a given day in the youtube dataset, sorted from high to low
def plot_view_distribution(filename):
    data = rank_youtube(filename)
    views = sorted([int(y) for (x, y) in data], reverse=True)
    plt.plot(views)

    plt.xlabel('Number of Videos')
    plt.ylabel('Views')
    plt.title(filename)
    plt.show()


# endregion

# region Plot All

# Plots the differences of all songs in the given list of songs, from the given directory
def plot_all_differences(songs, dir):
    for song in songs:
        plot_differences(song, dir)


# Plots the views of all songs in the given list of songs, from the given directory
def plot_all_views(songs, dir):
    for song in songs:
        plot_views(song, dir)


# Plots the popularity of all songs in the given list of songs over time from the spotify dataset
def plot_all_popularity(songs):
    for song in songs:
        plot_popularity(song)


# Plots the rankings on youtube and spotify, of all songs in the given list of songs, over time
def plot_all_rankings(songs):
    total_distance = 0
    for song in songs:
        song_average = plot_rankings(song)
        total_distance += song_average
        print(song, "Average Distance:", song_average)
    average = total_distance / len(songs)
    print("Average Distance over songs:", average)


# Calls all plot_all functions on the given list of (youtube/spotify) songs
def plot_all(songs):
    for song in songs:
        plot_differences(song, DIR_YT)
        plot_views(song, DIR_YT)
        plot_popularity(song)
        plot_rankings(song)


# Plot the view distribution for all files in the youtube dataset
def plot_all_view_distributions():
    for file in os.listdir(DIR_YT):
        plot_view_distribution(file)


# endregion

# region Songs

# Songs in 3FM dataset
SONGS_3FM = ['Bastille - Send Them Off!']

# Songs in 538 dataset
SONGS_538 = [
    'Fais & Afrojack - Used To Have It All (Official Video)'
    , "DIT IS 4U MET 'BITTER TASTE' – The Next Boy/Girl Band"
    , 'Kensington - Sorry (official audio)'
            ]

# Smaller set of songs for youtube and spotify to be able to quickly see some plots
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


# These songs should not be used, because
# The song name is also found in another song name, or
# it is entirely not in 1 of the 2 datasets, or
# theres only like 50 days of data, which is not a lot
DONT_USE = [
    'Where Are Ü Now (with Justin Bieber)'
    , 'Easy Love - Original Mix'
    , 'Marvin Gaye (feat. Meghan Trainor)'
    , 'Lay It All On Me (feat. Ed Sheeran)'
    , 'Downtown (feat. Eric Nally, Melle Mel, Kool Moe Dee & Grandmaster Caz)'
    , 'Cheerleader - Felix Jaehn Remix Radio Edit'
    , 'Lean On (feat. MØ & DJ Snake)'
    , 'Here'
    , 'Again'
    , '679 (feat. Remy Boyz)'
    , "Ain't Nobody (Loves Me Better)"
    , 'Reality - Radio Edit'
    , 'See You Again (feat. Charlie Puth)'
    , 'Sugar'
    , 'Are You with Me - Radio Edit'
    , "I Don't Like It, I Love It (feat. Robin Thicke & Verdine White)"
    , 'Alive'
    , 'Hey Mama (feat. Nicki Minaj, Bebe Rexha & Afrojack)'
    , 'I Took A Pill In Ibiza - SeeB Remix'
    , 'Powerful (feat. Ellie Goulding & Tarrus Riley)'
    , 'My Way (feat. Monty)'
    , 'Often'
    , "That's How You Know (feat. Kid Ink & Bebe Rexha)"
    , 'Five More Hours - Deorro x Chris Brown'
    , 'Fight Song'
    , 'Black Magic'
    , 'Ghost Town'
    , "Runnin' (Lose It All)"
    , 'Watch Me (Whip / Nae Nae)'
    , 'Cool for the Summer'
    , 'Back To Back'
    , 'No Role Modelz'
    , 'Rolling in the Deep'
    , 'Love Me Like You'
    , '7 Years'
    , 'Love Me Like You Do - From "Fifty Shades Of Grey"'
    , 'Shut up and Dance'
        ]


# Returns a list of all spotify songs, excluding the ones that should not be used
def spotify_songs():
    res = []
    for item in load_json(DIR_SPOT + SLASH + DATA)[tracks][items]:
        res.append(item[track][name])

    to_remove = []
    for s1 in DONT_USE: # select the songs from DONT_USE, because they shouldn't be used
        for s2 in res:
            if s1 == s2:
                to_remove.append(s2)

    for songname in to_remove: # remove the songs
        if songname in res:
            res.remove(songname)

    return res

# endregion


plot_all_differences(SONGS_3FM, DIR_3FM)
plot_all_differences(SONGS_538, DIR_538)

#plot_all_differences(spotify_songs(), DIR_YT)
#plot_all_views(spotify_songs(), DIR_YT)
#plot_all_popularity(spotify_songs())
#plot_all_rankings(spotify_songs())

plot_all_differences(SONGS_YT, DIR_YT)
plot_all_views(SONGS_YT, DIR_YT)
plot_all_popularity(SONGS_YT)
plot_all_rankings(SONGS_YT)

plot_all_view_distributions()



