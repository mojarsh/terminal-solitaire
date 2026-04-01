import json
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class Stats:
    games_played: int = 0
    games_won: int = 0
    fastest_win_seconds: float | None = None
    total_win_seconds: float = 0


def _load_stats(stats_path: Path) -> dict:
    if not stats_path.exists():
        return asdict(Stats())
    with open(stats_path, "r") as f:
        return json.load(f)


def _save_stats(stats_path: Path, stats: dict) -> None:
    stats_path.parent.mkdir(parents=True, exist_ok=True)
    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=2)


def create_or_update_stats_file(
    stats_path: Path, game_won: bool, game_elapsed_time: float
) -> None:
    stats = _load_stats(stats_path)
    stats["games_played"] += 1
    if game_won:
        stats["games_won"] += 1
        stats["total_win_seconds"] += round(game_elapsed_time, 2)
        if (
            stats["fastest_win_seconds"] is None
            or game_elapsed_time < stats["fastest_win_seconds"]
        ):
            stats["fastest_win_seconds"] = round(game_elapsed_time, 2)
    _save_stats(stats_path, stats)


def show_stats_summary(stats_path: Path) -> None:
    if not stats_path.exists():
        print("No terminal solitaire stats available!")

    else:
        stats = _load_stats(stats_path)

        try:
            win_percentage = round(stats["games_won"] / stats["games_played"] * 100, 1)
            average_win = round(stats["total_win_seconds"] / stats["games_won"], 2)

        except ZeroDivisionError:
            win_percentage = 0
            average_win = None

        print(
            "\n",
            f"Games played: {stats['games_played']}\n",
            f"Games won: {stats['games_won']}\n",
            f"Win percentage: {win_percentage}%\n",
            f"Fastest win (s): {stats['fastest_win_seconds']}\n",
            f"Average win (s): {average_win}\n",
        )
