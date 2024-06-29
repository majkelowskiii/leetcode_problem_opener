# <div role="rowgroup">
# <div role="row">
#
# <div role="cell"> (status) </div>
# <div role="cell"> (title)
# ....
# <a href="/problems/{title-slug}/">
# "{Number of problem}"
# "{.}"
# "{Title}"
# ....
# </div>
# <div role="cell"> (solution) </div>
# <div role="cell"> (acceptance) </div>
# <div role="cell"> (difficulty) </div>
# <div role="cell"> (frequency) </div>
# </div> (row)
# </div> (rowgroup)


# no of pages
# <nav role="navigation">
# <button class="flex [...]">
# {last button with text contains no of pages}
# </button>
# </nav>

# https://leetcode.com/problemset/all/?page=1

# ^ all this but leetcode gets calls from API/JS so it doesnt work :(

# TODO: call with current username

import json
import os

import pandas as pd
import requests

url = "https://leetcode.com/api/problems/algorithms/"

try:
    path = os.getcwd() + "/data/" + "cookie.txt"
    with open(path, "r") as file:
        cookie = file.read()

    # cookie expired after few weeks
    # needs to make sure that after copying cookie it contains no trailing whitespaces

    headers = {"cookie": cookie}
    r = requests.get(url, headers=headers)
except:
    r = requests.get(url)


data = json.loads(r.text)
df = pd.read_json(r.text)
df1 = pd.json_normalize(data, record_path=["stat_status_pairs"])

# df1.columns Index(['status', 'paid_only', 'is_favor', 'frequency', 'progress',
#       'stat.question_id', 'stat.question__article__live',
#       'stat.question__article__slug',
#       'stat.question__article__has_video_solution', 'stat.question__title',
#       'stat.question__title_slug', 'stat.question__hide', 'stat.total_acs',
#       'stat.total_submitted', 'stat.frontend_question_id',
#       'stat.is_new_question', 'difficulty.level'],
#      dtype='object')

# stat.frontend_question_id -> index order
# stat.question_id -> ???

# stat.question_id                                           2500
# stat.question__title_slug    minimum-costs-using-the-train-line
# stat.frontend_question_id                                  2361


headers = [
    "stat.frontend_question_id",
    "stat.question__title",
    "stat.question__title_slug",
    "difficulty.level",
    "paid_only",
    "status",
]
#'status' = {'ac':'accomplished', 'notac':'submitted but not done', 'None':'not tried'}


df2 = pd.DataFrame(df1, columns=headers)

df2 = df2.rename(
    columns={
        "stat.frontend_question_id": "ID",
        "stat.question__title": "Title",
        "stat.question__title_slug": "Title Slug",
        "difficulty.level": "Difficulty",
        "paid_only": "premium",
    }
)

df2 = df2.sort_values(by="ID")

diff_dict = {1: "Easy", 2: "Medium", 3: "Hard"}
df2["Difficulty"].replace(diff_dict, inplace=True)

path = os.getcwd() + "/data/" + "problem_list.txt"
df2.to_csv(path_or_buf=path, index=False)

path = os.getcwd() + "/data/" + "ratings_clean.txt"
df3 = pd.read_csv(path)

df4 = df3.merge(df2, how="left", on="ID")

# 6 or so rows have different title by one hyphen, so we need to filter that out
headers = ["Rating", "ID", "Title_x", "Title Slug_x", "Difficulty", "premium", "status"]
df4 = pd.DataFrame(df4, columns=headers)
df4 = df4.rename(columns={"Title_x": "Title", "Title Slug_x": "Title Slug"})

path = os.getcwd() + "/data/" + "data.txt"
df4.to_csv(path_or_buf=path, index=False)
