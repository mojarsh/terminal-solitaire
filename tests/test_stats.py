from dataclasses import asdict
from src.terminal_solitaire.stats import (
    Stats,
    _load_stats,
    _save_stats,
    create_or_update_stats_file,
    show_stats_summary,
)


def test_stats_file_created_if_not_exists(tmp_path) -> None:
    stats_path = tmp_path / "stats.json"
    stats = _load_stats(stats_path)
    assert stats["games_played"] == 0
    assert stats["games_won"] == 0
    assert stats["fastest_win_seconds"] is None
    assert stats["total_win_seconds"] == 0


def test_load_stats_from_existing_file(tmp_path, stats) -> None:
    stats_path = tmp_path / "stats.json"
    _save_stats(stats_path, stats)
    loaded = _load_stats(stats_path)
    assert loaded == stats


def test_stats_saved_correctly(tmp_path, stats) -> None:
    stats_path = tmp_path / "stats.json"
    _save_stats(stats_path, stats)

    new_stats = _load_stats(stats_path)

    assert new_stats["games_played"] == 42
    assert new_stats["games_won"] == 30
    assert new_stats["fastest_win_seconds"] == 342.60
    assert new_stats["total_win_seconds"] == 4800.54


def test_stats_updated_game_won(tmp_path, stats) -> None:

    stats_path = tmp_path / "stats.json"
    _save_stats(stats_path, stats)
    create_or_update_stats_file(stats_path, True, 400.0)

    new_stats = _load_stats(stats_path)
    assert new_stats["games_played"] == 43
    assert new_stats["games_won"] == 31
    assert new_stats["fastest_win_seconds"] == 342.60
    assert new_stats["total_win_seconds"] == 5200.54


def test_stats_updated_game_lost(tmp_path, stats) -> None:
    stats_path = tmp_path / "stats.json"
    _save_stats(stats_path, stats)
    create_or_update_stats_file(stats_path, False, 400.0)
    new_stats = _load_stats(stats_path)
    assert new_stats["games_played"] == 43
    assert new_stats["games_won"] == 30  # unchanged
    assert new_stats["fastest_win_seconds"] == 342.60  # unchanged
    assert new_stats["total_win_seconds"] == 4800.54  # unchanged


def test_fastest_win_updated_if_faster(tmp_path, stats) -> None:
    stats_path = tmp_path / "stats.json"
    _save_stats(stats_path, stats)
    create_or_update_stats_file(stats_path, True, 100.0)
    new_stats = _load_stats(stats_path)
    assert new_stats["fastest_win_seconds"] == 100.0


def test_fastest_win_not_updated_when_slower(tmp_path, stats) -> None:
    stats_path = tmp_path / "stats.json"
    _save_stats(stats_path, stats)
    create_or_update_stats_file(stats_path, True, 500.0)
    new_stats = _load_stats(stats_path)
    assert new_stats["fastest_win_seconds"] == 342.60


def test_fastest_win_set_on_first_win(tmp_path) -> None:
    stats_path = tmp_path / "stats.json"
    create_or_update_stats_file(stats_path, True, 250.0)
    stats = _load_stats(stats_path)
    assert stats["fastest_win_seconds"] == 250.0


def test_stats_file_created_on_first_update(tmp_path) -> None:
    stats_path = tmp_path / "stats.json"
    assert not stats_path.exists()
    create_or_update_stats_file(stats_path, False, 0.0)
    assert stats_path.exists()
    stats = _load_stats(stats_path)
    assert stats["games_played"] == 1


def test_save_stats_creates_parent_directory(tmp_path) -> None:
    stats_path = tmp_path / "nested" / "dir" / "stats.json"
    _save_stats(stats_path, asdict(Stats()))
    assert stats_path.exists()


def test_show_stats_summary_no_file(tmp_path, capsys) -> None:
    stats_path = tmp_path / "stats.json"
    show_stats_summary(stats_path)
    captured = capsys.readouterr()
    assert "No terminal solitaire stats available" in captured.out


def test_show_stats_summary_zero_wins(tmp_path, capsys) -> None:
    stats_path = tmp_path / "stats.json"
    create_or_update_stats_file(stats_path, False, 0.0)
    show_stats_summary(stats_path)
    captured = capsys.readouterr()
    assert "0%" in captured.out
    assert "Games played: 1" in captured.out


def test_show_stats_summary_with_wins(tmp_path, stats, capsys) -> None:
    stats_path = tmp_path / "stats.json"
    _save_stats(stats_path, stats)
    show_stats_summary(stats_path)
    captured = capsys.readouterr()
    assert "Games played: 42" in captured.out
    assert "Games won: 30" in captured.out
    assert "342.6" in captured.out  # fastest win
