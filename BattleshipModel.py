from typing import List, Tuple


class Ship:
    def __init__(self, positions: List[Tuple[int,int]]):
        self.positions = set(positions)
        self.hits = set()

    def takeHit(self, pos: Tuple[int,int]) -> bool:
        if pos in self.positions:
            self.hits.add(pos)
            return True
        return False

    def isSunk(self) -> bool:
        return self.hits == self.positions


class Player:
    def __init__(self, name: str):
        self.name = name
        self.ships: List[Ship] = []
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        # 0-empty, 1-ship, -1-hit, 2-miss
        self.hits = 0
        self.misses = 0

    def addShip(self, positions: List[Tuple[int,int]]):
        ship = Ship(positions)
        self.ships.append(ship)
        for x, y in positions:
            self.board[x][y] = 1


def registerHit(opponent: Player, x: int, y: int) -> bool:
    for ship in opponent.ships:
        if ship.takeHit((x, y)):
            opponent.board[x][y] = -1
            if ship.isSunk():
                opponent.ships.remove(ship)
            return True
    opponent.board[x][y] = 2
    return False


class Game:
    def __init__(self, player1: Player, player2: Player):
        self.players = [player1, player2]
        self.turn = 0

    def guess(self, x: int, y: int) -> Tuple[bool, bool]:
        attacker = self.players[self.turn]
        defender = self.players[1 - self.turn]
        hit = registerHit(defender, x, y)
        if hit:
            attacker.hits += 1
        else:
            attacker.misses += 1
        win = (len(defender.ships) == 0)
        self.turn = 1 - self.turn
        return hit, win