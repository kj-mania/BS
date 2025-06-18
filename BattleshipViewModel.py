import RPi.GPIO as GPIO
from BattleshipModel import Game, Player

green = [27, 22, 17, 5, 12, 25, 4, 23, 18]
red   = [6, 13,14, 26, 21, 24, 19, 16, 20]
all = green + red


def pIndex(x:int, y:int) -> int:
    return x*3+y


class BattleshipViewModel:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        for pin in all:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")
        self.game = Game(self.player1, self.player2)

    def placeShips(self, player: Player):
        coords = input(f"{player.name}, enter 1×1 ship position as 'x,y': ")
        parts = coords.split(",")
        x = int(parts[0])
        y = int(parts[1])
        player.addShip([(x, y)])

        coords = input(f"{player.name}, enter 1×2 ship positions as 'x1,y1 x2,y2': ")
        spots = []
        for pair in coords.split():
            stringX, stringY = pair.split(',')
            spots.append((int(stringX), int(stringY)))
        player.addShip(spots)

    def resetLeds(self):
        for idx in range(len(green)):
            GPIO.output(green[idx], GPIO.LOW)
            GPIO.output(red[idx], GPIO.LOW)

    def updateAllLeds(self, board, player):
        if player.name:
            print(f"Updating LEDs to show {player.name}'s board:")
        else:
            print("Updating LEDs to show board:")
        for row in board:
            print(row)
        for q in range(3):
            for r in range(3):
                idx = pIndex(q, r)
                GPIO.output(green[idx], GPIO.LOW)
                GPIO.output(red[idx], GPIO.LOW)
                if board[q][r] == -1:
                    print(f"LED at ({q},{r}) set to RED (hit)") #debug
                    GPIO.output(red[idx], GPIO.HIGH)
                elif board[q][r] == 2:
                    print(f"LED at ({q},{r}) set to GREEN (miss)") #debug
                    GPIO.output(green[idx], GPIO.HIGH)

    def updateLed(self, x: int, y: int, hit: bool):
        idx = pIndex(x, y)
        GPIO.output(green[idx], GPIO.LOW)
        GPIO.output(red[idx], GPIO.LOW)
        if hit:                                   
            pin = red[idx]
        else:
            pin = green[idx]
        GPIO.output(pin, GPIO.HIGH)


    def play(self):
        for player in (self.player1, self.player2):
            self.placeShips(player)

        while True:
            attacker = self.game.players[self.game.turn]
            defender = self.game.players[1 - self.game.turn]
            self.updateAllLeds(defender.board, defender)
            coords = input(f"{attacker.name}, enter target as 'x y': ")
            x, y = map(int, coords.split())
            hit, win = self.game.guess(x, y)

            if hit:
                print(f"{attacker.name} hit {defender.name} at ({x}, {y})")

            self.updateLed(x, y, hit)

            if win:
                print(f"{attacker.name} wins")  
                break

    def cleanup(self):
        GPIO.cleanup()

def main():
    vm = BattleshipViewModel()
    try:
        vm.play()
    except:
        raise Exception("allan broke something")
    finally:
        vm.cleanup()

main()
 