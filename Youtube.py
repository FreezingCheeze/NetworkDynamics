from googleapiclient.discovery import build
import matplotlib.pyplot as plt
import random as rand
import ast

api_key = 'AIzaSyDGbY8PRfEKNJRoQci4Pjx5id-0I5lm5SA' # Gies' API key
bas_key = 'AIzaSyCiv00E35N5wnqTNcp8CAXmkICSXraG0-w'
video_id = 'Vh_vi8qN4Cs'

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

def read_data_from_file():
    with open("YoutubeData.txt", encoding="utf8") as f:
        content = f.read()
        dictionary = ast.literal_eval(content)
        f.close()

    return dictionary

def plot_data(data):

    views = sorted([int(y) for (x, y) in data.values()], reverse=True)

    plt.plot(views)

    plt.xlabel('Number of Videos')
    plt.ylabel('Views')
    plt.title("Views of Videos")
    plt.show()


def plot_normal_distribution():
    dictionary = read_data_from_file()
    views = [int(y) for (x, y) in dictionary.values()]
    min_views = min(views)
    max_views = max(views)
    step = int((max_views - min_views) / 100)
    intervals = [x for x in range(min_views, max_views, step)]

    vals = dict()
    for count in views:
        for val in intervals:
            if val <= count <= val + step:
                if vals.get(val) is not None:
                    vals[val] = vals[val] + 1
                else:
                    vals[val] = 1

    for val in intervals:
        if vals.get(val) is None:
            vals[val] = 0

    vals = sorted(vals.items())
    print(vals)
    plt.plot([x for (x, y) in vals], [y for (x, y) in vals] )

    plt.xlabel('Views')
    plt.ylabel('number of videos')
    plt.title("Views of Videos")
    plt.show()


plot_data(read_data_from_file())
#plot_data(generate_data(video_id))