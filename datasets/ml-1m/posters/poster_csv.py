import numpy as np
import os
import csv
from glob import glob

csv_path = "/Users/liuweiwei06/Desktop/Paddle_book/dataset/ml-1m/data.csv"

rating_path = "/Users/liuweiwei06/Desktop/Paddle_book/dataset/ml-1m/ratings.dat"

user_path = "/Users/liuweiwei06/Desktop/Paddle_book/dataset/ml-1m/users.dat"

movies_path = "/Users/liuweiwei06/Desktop/Paddle_book/dataset/ml-1m/movies.dat"

# csv_header = ['movieId', 'imdbId', 'tmdbId', 'imdbImgLink']
def wget_poster():
    csv_dict = {}
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        csv_header = next(reader)
        for idx, line in enumerate(reader):

            if line[3] == '':
                print(line)
                continue
            csv_dict[line[0]] = os.path.join(*line[3:])
            if idx % 100 == 0:
                print(line[0], csv_dict[line[0]])

    count = 0
    mov_ids = []
    with open(rating_path, 'r') as f:
        rating_data = f.readlines()
        os.system("cd posters")
        for line in rating_data:
            mov_id = line.split('::')[1]

            if mov_id not in mov_ids:
                mov_ids.append(mov_id)
            else:
                continue

            if mov_id not in csv_dict.keys():
                count += 1
                print(mov_id, "has not poster!!")
                continue
            if not os.path.exists('mov_id' + mov_id + '.jpg'):
                mov_poster_url = csv_dict[mov_id]
                os.system("wget {} -O {}".format(mov_poster_url, "mov_id"+mov_id+".jpg"))
            print(mov_id, "get done!!!")
        print("no poster movies number: ", count, "num movs:", len(mov_ids))


def data_collect():

    # read mov info
    with open(movies_path, 'r', encoding="ISO-8859-1") as f:
        mov_data = f.readlines()
    mov_dict = {}
    for line in mov_data:
        tmp = line.strip().split('::')
        mov_dict[int(tmp[0])] = tmp[1:]

    # read usr info
    with open(user_path, 'r') as f:
        usr_data = f.readlines()
    usr_dict = {}
    for line in usr_data:
        tmp = line.strip().split('::')
        usr_dict[int(tmp[0])] = tmp[1:-1]

    # read rating info
    # with open(rating_path, 'r') as f:
    #     rating_data = f.readlines()
    # rating_dict = {}
    # for line in rating_data:
    #     tmp = line.strip().split('::')
    #     rating_dict[int(tmp[0])] = {int(tmp[1]):int(tmp[2])}

    posters = glob("/Users/liuweiwei06/Desktop/Paddle_book/Code/posters/mov_id*.jpg")

    poster_id = []
    for key in posters:
        poster_id.append(int(key.split('/')[-1][6:-4]))

    # build new_data
    new_rate_file = open('/Users/liuweiwei06/Desktop/Paddle_book/Code/new_rating.txt', 'a')
    new_rate_data = []
    with open(rating_path, 'r') as f:
        rating_data = f.readlines()
    for idx, rate in enumerate(rating_data):
        tmp = rate.strip().split('::')[:-1]
        usr_id, mov_id, score = list(map(int, tmp))
        if mov_id in poster_id:
            new_rate_data.append(rate)
    new_rate_data[-1] = new_rate_data[-1].strip()
    new_rate_file.writelines(new_rate_data)
    print("Done")

# data_collect()
wget_poster()