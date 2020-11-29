from googleapiclient.discovery import build
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import random as rand
import ast

gies_key = 'AIzaSyDGbY8PRfEKNJRoQci4Pjx5id-0I5lm5SA' # Gies' API key
bas_key = 'AIzaSyCiv00E35N5wnqTNcp8CAXmkICSXraG0-w' # Bas' API key
video_id = 'Vh_vi8qN4Cs'
video_id2 = 'c0SrxSMHDmE'
video_id3 = '9sTQ0QdkN3Q'

service = build('youtube', 'v3', developerKey=bas_key)


# Takes the video id of the video to get data from, as well as the dictionary to put the stats into
def get_video_data(v_id, res):
    request = service.videos().list(  # request the statistics of the chosen video
        part=['statistics', 'snippet'],
        id=v_id
    )
    response = request.execute()  # initial response (in json)

    views = response['items'][0]['statistics']['viewCount']  # gather view count from response
    name = response['items'][0]['snippet']['title']
    res[v_id] = (name, views)  # set the viewcount


# Generates a dictionary of song id to a tuple of (name, views), for 100 songs
def generate_data(v_id):
    res = dict()

    get_video_data(v_id, res)

    for i in range(100):

        request = service.search().list( # Get the recommendations based on the previous looked up video
            part='snippet',
            relatedToVideoId=v_id,
            type="video"
        )
        response = request.execute()

        video = rand.choice(response['items']) # Take a random video out of the first couple recommendations
        print(video)
        v_id = video['id']['videoId'] # get its video id

        get_video_data(v_id, res)
        print("F", res)

    return res


def read_data_from_file(filename):
    with open(filename, encoding="utf8") as f:
        content = f.read()
        dictionary = ast.literal_eval(content)
        f.close()

    return sorted([int(y) for (x, y) in dictionary.values()], reverse=True)


def plot_data(views, title):
    plt.plot(views)

    plt.xlabel('Number of Videos')
    plt.ylabel('Views')
    plt.title(title)
    plt.show()


def plot_normal_distribution(views, title):
    view_mean = np.mean(views) # Mean
    view_std = np.std(views) # Standard Deviation
    pdf = stats.norm.pdf(views, view_mean, view_std) # fit

    plt.plot(views, pdf)
    plt.title("Normal distribution for " + title)
    plt.show()


def gather_data(files):
    all_views = []
    for file in files:
        views = read_data_from_file(file)
        all_views.extend(views)

    return sorted(all_views, reverse=True)


# The data here was copied from internet, so I knew it would yield a nice graph
def plot_actual_normal_distrbution():
    data = sorted([186, 176, 158, 180, 186, 168, 168, 164, 178, 170, 189, 195, 172,
     187, 180, 186, 185, 168, 179, 178, 183, 179, 170, 175, 186, 159,
     161, 178, 175, 185, 175, 162, 173, 172, 177, 175, 172, 177, 180])
    mean = np.mean(data)
    std = np.std(data)
    pdf = stats.norm.pdf(data, mean, std)

    plt.plot(data, pdf)
    plt.show()


Data1 = 'Data1.txt'
Data2 = 'Data2.txt'
Data3 = 'Data3.txt'
Data4 = 'Data4.txt'

FILES = [Data1
        , Data2
        , Data3
        , Data4
        ]


def plot_all_data():
    for data in FILES:
        plot_data(read_data_from_file(data), data)
    plot_data(gather_data(FILES), 'All Files')


def plot_all_normal_distributions():
    for data in FILES:
        plot_normal_distribution(read_data_from_file(data), data)
    plot_normal_distribution(gather_data(FILES), 'All files')


# plot_data(generate_data(video_id3))
plot_all_data()
plot_all_normal_distributions()
plot_actual_normal_distrbution()
