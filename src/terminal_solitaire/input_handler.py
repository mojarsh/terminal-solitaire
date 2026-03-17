class InputHandler:
    def get_action(self) -> str:
        return str(input("\nSelect an action for this turn: ")).strip()

    def get_column(self, prompt: str) -> int:
        return int(input(prompt))

    def get_hand_movement(self) -> str:
        return str(input("Enter 'f' to move to foundations, 't' to move to tableau: ")).strip()

    def get_quit_confirmation(self) -> str:
        return input("Are you sure you want to quit (y/n): ")
