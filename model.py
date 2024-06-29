from __future__ import annotations

from typing import Sequence

from pydantic import BaseModel, ConfigDict


class Stat(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
        frozen=True,
    )
    question_id: int
    question__article__live: bool | None = None
    question__article__slug: str | None = None
    question__article__has_video_solution: bool | None = None
    question__title: str
    question__title_slug: str
    question__hide: bool
    total_acs: int
    total_submitted: int
    frontend_question_id: int
    is_new_question: bool


class Difficulty(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
        frozen=True,
    )
    level: int


class StatStatusPair(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
        frozen=True,
    )
    stat: Stat
    status: str | None = None
    difficulty: Difficulty
    paid_only: bool
    is_favor: bool
    frequency: int
    progress: int


class Model(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
        frozen=True,
    )
    user_name: str
    num_solved: int
    num_total: int
    ac_easy: int
    ac_medium: int
    ac_hard: int
    stat_status_pairs: Sequence[StatStatusPair]
    frequency_high: int
    frequency_mid: int
    category_slug: str
