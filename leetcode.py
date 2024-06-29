# leetcode ratings.txt from https://github.com/zerotrac/leetcode_problem_rating

import webbrowser
from os import getcwd
from tkinter import BooleanVar, E, N, S, StringVar, Tk, W, ttk
from typing import Literal

import pandas as pd


class Leetcode:
    def __init__(self, root) -> None:
        self.read_ratings()
        self.df: pd.DataFrame = self.data
        self.set_longest_title()

        root.title("Leetcode problem opener")

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.problem_diff = StringVar()
        ttk.Label(mainframe, textvariable=self.problem_diff, width=7).grid(
            column=3, row=4, sticky=(W, E)
        )
        ttk.Label(mainframe, text="Diff").grid(column=3, row=3, sticky=(W, E))

        self.problem_id = StringVar()
        ttk.Label(mainframe, textvariable=self.problem_id, width=7).grid(
            column=2, row=4, sticky=(W, E)
        )
        ttk.Label(mainframe, text="ID").grid(column=2, row=3, sticky=(W, E))

        self.problem_name = StringVar()
        ttk.Label(
            mainframe, textvariable=self.problem_name, width=self.longest_title
        ).grid(column=4, row=4, sticky=(W, E))
        ttk.Label(mainframe, text="Problem name").grid(column=4, row=3, sticky=(W, E))

        ttk.Button(mainframe, text="Next", command=self.show_next_prob, width=15).grid(
            column=6, row=4, sticky=(W, E)
        )
        ttk.Button(mainframe, text="Prev", command=self.show_prev_prob, width=15).grid(
            column=5, row=4, sticky=(W, E)
        )
        ttk.Button(mainframe, text="Open", command=self.open_problem, width=15).grid(
            column=6, row=5, sticky=(W, E)
        )

        self.problem_progress = StringVar()
        ttk.Label(mainframe, textvariable=self.problem_progress).grid(
            column=5, row=5, sticky=(W, E)
        )

        self.goto_choice = StringVar()
        goto_entry = ttk.Entry(mainframe, textvariable=self.goto_choice, width=15)
        goto_entry.grid(column=5, row=3, sticky=(W, E))

        self.goto_combovar = StringVar()
        self.goto_combovar_values: tuple[Literal["ID"], Literal["Problem index"]] = (
            "ID",
            "Problem index",
        )
        goto_combo = ttk.Combobox(
            mainframe, textvariable=self.goto_combovar, width=15, state="readonly"
        )
        goto_combo.grid(column=6, row=3, sticky=(W, E))
        goto_combo["values"] = self.goto_combovar_values
        goto_combo.current(0)
        # goto_combo.state(["readonly"]) - instead of state="readonly" in ttk.Combobox()

        ttk.Button(mainframe, text="Go To", command=self.goto_problem, width=15).grid(
            column=7, row=3, sticky=(W, E)
        )

        self.show_ac_var = BooleanVar(value=True)
        premium_checkbox = ttk.Checkbutton(
            mainframe, text="Show accomplished", variable=self.show_ac_var
        )
        premium_checkbox.grid(column=1, row=2, sticky=(W, E))

        self.show_premium_var = BooleanVar(value=True)
        premium_checkbox = ttk.Checkbutton(
            mainframe, text="Show premium", variable=self.show_premium_var
        )
        premium_checkbox.grid(column=1, row=3, sticky=(W, E))

        self.show_easy_var = BooleanVar(value=True)
        premium_checkbox = ttk.Checkbutton(
            mainframe, text="Show Easy", variable=self.show_easy_var
        )
        premium_checkbox.grid(column=1, row=4, sticky=(W, E))

        self.show_medium_var = BooleanVar(value=True)
        premium_checkbox = ttk.Checkbutton(
            mainframe, text="Show Medium", variable=self.show_medium_var
        )
        premium_checkbox.grid(column=1, row=5, sticky=(W, E))

        self.show_hard_var = BooleanVar(value=True)
        premium_checkbox = ttk.Checkbutton(
            mainframe, text="Show Hard", variable=self.show_hard_var
        )
        premium_checkbox.grid(column=1, row=6, sticky=(W, E))

        ttk.Button(
            mainframe, text="Apply changes", command=self.set_show_status, width=15
        ).grid(column=1, row=7, sticky=(W, E))

        self.problem_index = 0
        self.set_by_index()

        goto_entry.focus()
        # root.bind("<Return>", self.open_problem())
        # root.bind("<Left>", self.show_prev_prob())
        # root.bind("<Right>", self.show_next_prob())

    def set_by_index(self) -> None:
        self.problem_index: int = max(self.problem_index, 0)
        self.problem_index = min(self.problem_index, len(self.df) - 1)
        self.problem_id.set(self.df["ID"].iloc[self.problem_index])
        self.problem_name.set(self.df["Title"].iloc[self.problem_index])
        self.problem_progress.set(
            f"{str(self.problem_index + 1)} / {len(self.df)}"  # 0-indexed vs 1-indexed
        )
        self.problem_diff.set(self.df["Difficulty"].iloc[self.problem_index])

    def set_by_id(self) -> None:
        number = int(self.goto_choice.get())  # 0-indexed vs 1-indexed

        index: pd.Index = self.df.index[self.df["ID"] == number]

        if not index.empty:
            self.problem_index = index[0]
            self.set_by_index()

    def goto_problem(self) -> None:
        try:
            number: int = int(self.goto_choice.get()) - 1
        except ValueError:
            return

        # todo - validation https://tkdocs.com/tutorial/widgets.html#entry

        label: str = self.goto_combovar.get()

        if label == self.goto_combovar_values[0]:  # self.goto_combovar_values == "ID"
            self.set_by_id()
        elif (
            label
            == self.goto_combovar_values[1]  # self.goto_combovar_values == "Index"
        ):
            if 0 <= number <= len(self.df):
                self.problem_index = number
                self.set_by_index()

    def set_longest_title(self) -> None:
        # get there by index - useful for extracting title itself
        # idx = self.df.Title.str.len().idxmax()
        # longest_title = self.df["Title"][idx]
        # len(longest_title)

        lngst_title: int = self.df.Title.str.len().max()
        # same as self.df["Title"].str.len().max()

        self.longest_title: int = lngst_title

    def read_ratings(self) -> None:
        path: str = getcwd() + "/data/" + "data.txt"
        self.data: pd.DataFrame = pd.read_csv(path)

    def save_ratings(self) -> None:
        # TODO document why this method is empty
        pass

    def open_problem(self) -> None:
        problem_slug = self.df["Title Slug"].iloc[
            self.problem_index
        ]  # 0-indexed vs 1-indexed
        urlpath = "https:/www.leetcode.com/problems/" + problem_slug
        webbrowser.open(urlpath)

    def show_next_prob(self) -> None:
        self.problem_index += 1
        self.set_by_index()

    def show_prev_prob(self) -> None:
        self.problem_index -= 1
        self.set_by_index()

    def set_show_status(self) -> None:
        temp_df: pd.DataFrame = self.data

        if not self.show_ac_var.get():
            temp_df = temp_df.loc[temp_df["status"] != "ac"]

        if not self.show_premium_var.get():
            temp_df = temp_df.loc[~temp_df["premium"]]

        diff = []

        if self.show_easy_var.get():
            diff.append("Easy")

        if self.show_medium_var.get():
            diff.append("Medium")

        if self.show_hard_var.get():
            diff.append("Hard")

        if diff:
            self.df = temp_df.loc[temp_df["Difficulty"].isin(diff)]

        self.df = self.df.reset_index()
        self.set_by_index()


root = Tk()
Leetcode(root)
root.mainloop()
