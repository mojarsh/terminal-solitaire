from dataclasses import dataclass, field
from terminal_solitaire.rules import (
    Rule,
    same_suit_foundation_rule,
    alternating_colour_rule,
    higher_value_foundation_rule,
    king_to_empty_space_rule,
    lower_value_rule,
)


def _default_rules() -> dict[str, list[Rule]]:
    return {
        "foundation": [same_suit_foundation_rule, higher_value_foundation_rule],
        "tableau": [
            alternating_colour_rule,
            lower_value_rule,
            king_to_empty_space_rule,
        ],
    }


@dataclass
class GameConfig:
    draw_count: int = 3
    pass_limit: int | None = None
    allow_undo: bool = True
    seed: int | None = None
    rules: dict[str, list[Rule]] = field(default_factory=_default_rules)
