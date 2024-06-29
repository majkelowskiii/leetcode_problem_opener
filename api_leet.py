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

import json
from pathlib import Path
from typing import Any, Dict

import pandas as pd
import requests
from model import Model
from requests import Response

url = "https://leetcode.com/api/problems/algorithms/"
ratings_url = "https://raw.githubusercontent.com/zerotrac/leetcode_problem_rating/main/ratings.txt"
data_dir: Path = Path.cwd() / "data"
data_dir.mkdir(parents=True, exist_ok=True)
cookie_path: Path = data_dir / "cookie.txt"
ratings_path: Path = data_dir / "ratings.txt"
clean_ratings_path: Path = data_dir / "ratings_clean.txt"
problem_list_path: Path = data_dir / "problem_list.txt"
data_output_path: Path = data_dir / "data.txt"

headers = {}
try:
    with open(cookie_path, "r", encoding="utf-8") as file:
        cookie: str = file.read().strip()
    headers = {"cookie": cookie}
except OSError as e:
    print(f"Error reading cookie: {e}")

try:
    req: Response = requests.get(ratings_url, timeout=5)
    with open(ratings_path, "w+", encoding="utf-8") as file:
        file.write(req.text)

    with open(ratings_path, "r", encoding="utf-8") as original_file, open(
        clean_ratings_path, "w+", encoding="utf-8"
    ) as clean_file:
        lines: list[str] = original_file.readlines()[1:]
        clean_file.write("Rating,ID,Title,Title Slug\n")
        clean_lines: list[str] = [
            f'{components[0]},{components[1]},"{components[2]}",{components[4]}\n'
            for line in lines
            if (components := line.strip().split("\t"))
        ]
        clean_file.writelines(clean_lines)
except requests.RequestException as e:
    print(f"Error fetching ratings data: {e}")


try:
    response: Response = requests.get(url, headers=headers, timeout=5)
    data: Model = Model.model_validate_json(response.text)
    data_dict: Dict[str, Any] = data.model_dump()
except (requests.RequestException, json.JSONDecodeError, AttributeError) as e:
    print(f"Error fetching problem data: {e}")
    data_dict = {}

try:
    df1: pd.DataFrame = pd.json_normalize(data_dict, record_path=["stat_status_pairs"])
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

    #'status' = {'ac':'accomplished', 'notac':'submitted but not done', 'None':'not tried'}

    headers: list[str] = [
        "stat.frontend_question_id",
        "stat.question__title",
        "stat.question__title_slug",
        "difficulty.level",
        "paid_only",
        "status",
    ]
    df2: pd.DataFrame = df1[headers].rename(
        columns={
            "stat.frontend_question_id": "ID",
            "stat.question__title": "Title",
            "stat.question__title_slug": "Title Slug",
            "difficulty.level": "Difficulty",
            "paid_only": "premium",
        }
    )

    diff_dict: Dict[int, str] = {1: "Easy", 2: "Medium", 3: "Hard"}
    df2 = df2.sort_values(by="ID").replace({"Difficulty": diff_dict})

    df2.to_csv(problem_list_path, index=False)
except KeyError as e:
    print(f"Error processing problem data: {e}")


try:
    response: Response = requests.get(url, headers=headers, timeout=5)
    data: Model = Model.model_validate_json(response.text)
    data_dict: Dict[str, Any] = data.model_dump()
except (requests.RequestException, json.JSONDecodeError, AttributeError) as e:
    print(f"Error fetching problem data: {e}")
    data_dict = {}


try:
    df1: pd.DataFrame = pd.json_normalize(data_dict, record_path=["stat_status_pairs"])
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

    #'status' = {'ac':'accomplished', 'notac':'submitted but not done', 'None':'not tried'}

    headers: list[str] = [
        "stat.frontend_question_id",
        "stat.question__title",
        "stat.question__title_slug",
        "difficulty.level",
        "paid_only",
        "status",
    ]
    df2: pd.DataFrame = df1[headers].rename(
        columns={
            "stat.frontend_question_id": "ID",
            "stat.question__title": "Title",
            "stat.question__title_slug": "Title Slug",
            "difficulty.level": "Difficulty",
            "paid_only": "premium",
        }
    )

    diff_dict: Dict[int, str] = {1: "Easy", 2: "Medium", 3: "Hard"}
    df2 = df2.sort_values(by="ID").replace({"Difficulty": diff_dict})

    df2.to_csv(problem_list_path, index=False)
except KeyError as e:
    print(f"Error processing problem data: {e}")


df3 = pd.read_csv(clean_ratings_path)

df4 = df3.merge(df2, how="left", on="ID")

# 6 or so rows have different title by one hyphen, so we need to filter that out
headers = ["Rating", "ID", "Title_x", "Title Slug_x", "Difficulty", "premium", "status"]
df4 = pd.DataFrame(df4, columns=headers)
df4 = df4.rename(columns={"Title_x": "Title", "Title Slug_x": "Title Slug"})

df4.to_csv(path_or_buf=data_output_path, index=False)
