class Board:
    def __init__(self, columns: int, rows: int):
        self.columns = columns
        self.rows = rows
        self.tableau = self.generate_tableau_board()
        self.foundations = self.generate_foundations_board()

    def generate_tableau_board(self) -> dict:
        tableau = {}
        for row in range(self.rows):
            for col in range(self.columns):
                tableau[(col, row)] = "  "

        return tableau

    def generate_foundations_board(self) -> dict:
        foundations = {}
        for row in range(1):
            for col in range(self.columns):
                foundations[(col, row)] = "  "

        return foundations

    def draw_board(self) -> None:
        print("+ -------------------- +")
        for i in range(1):
            print("|", end=" ")
            for k, v in self.foundations.items():
                if k[1] == i:
                    print(v, end=" ")
            print("|\r")
        print("+ -------------------- +")
        for i in range(self.rows):
            print("|", end=" ")
            for k, v in self.tableau.items():
                if k[1] == i:
                    print(v, end=" ")
            print("|\r")
        print("+ -------------------- +")
