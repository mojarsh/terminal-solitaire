from terminal_solitaire.deck import Card, Deck

class Hand:
    def __init__(self) -> None:
        self._cards: list[Card] = []

    @property
    def is_empty(self) -> bool:
        return len(self._cards) == 0

    @property
    def cards(self) -> list[Card]:
        return self._cards

    def draw(self, cards: list[Card]) -> None:
        """Accept newly drawn cards and make the top one visible."""
        self._cards = cards
        self._update_display()

    def pop(self) -> Card:
        """Remove and return the top card."""
        card = self._cards.pop(0)
        self._update_display()
        return card

    def return_to_deck(self, deck: Deck) -> None:
        """Cycle remaining cards back into the bottom of the deck."""
        for card in self._cards[::-1]:
            deck.cards.insert(0, card)
        self._cards = []

    def top(self) -> Card | None:
        """Return the top card without removing it."""
        return self._cards[0] if self._cards else None

    def _update_display(self) -> None:
        """Show only the top card; hide all others."""
        for idx, card in enumerate(self._cards):
            card.display_status = idx == 0

    def display(self) -> str:
        """Return a display string of all cards for the status bar."""
        return " ".join(card.display_value for card in self._cards)
