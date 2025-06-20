import RPi.GPIO as GPIO
import time
from BattleshipModel import Game, Player
from BattleshipCellState import CellState as goop

buzzer = 15
green = [27, 22, 17, 5, 12, 25, 4, 23, 18]
red   = [6, 13,14, 26, 21, 24, 19, 16, 20]
all = green + red


def pIndex(x:int, y:int) -> int:
    return x*3+y
## 012/345/678

def initPins():
    GPIO.setmode(GPIO.BCM)
    for pin in all:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        GPIO.setup(buzzer, GPIO.LOW)
        GPIO.output(buzzer, GPIO.LOW)

def resetLeds():
    for indx in range(len(green)):
        GPIO.output(green[indx], GPIO.LOW)
        GPIO.output(red[indx], GPIO.LOW)

class BattleshipViewModel:
    def __init__(self):
        initPins()
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

    def updateAllLeds(self, board, player):
        print(f"Updating LEDs to show {player.name}'s board:")
        for row in board:
            print(row)

        for q in range(3):
            for r in range(3):
                indx = pIndex(q, r)
                GPIO.output(green[indx], GPIO.LOW)
                GPIO.output(red[indx], GPIO.LOW)

                state = board[q][r]

                if state == goop.HIT:
                    print(f"LED at ({q},{r}) set to RED (hit)") #debug
                    GPIO.output(red[indx], GPIO.HIGH)
                elif board[q][r] == goop.MISS:
                    print(f"LED at ({q},{r}) set to GREEN (miss)") #debug
                    GPIO.output(green[indx], GPIO.HIGH)
                elif board[q][r] == goop.SUNK:
                    print(f"LED at ({q},{r}) set to ORANGE (sunk)") #debug
                    GPIO.output(buzzer, GPIO.HIGH)
                    GPIO.output(green[indx], GPIO.HIGH)
                    GPIO.output(red[indx], GPIO.HIGH)
                    time.sleep(0.5)
                    GPIO.output(buzzer, GPIO.LOW)                       



    def play(self):
        for player in (self.player1, self.player2):
            self.placeShips(player)

        while True:
            attacker = self.game.players[self.game.turn]
            defender = self.game.players[1 - self.game.turn]

            ## show DEFENDER board / start turn
            print(f"\n{attacker.name} Turn | Showing {defender.name} board")
            self.updateAllLeds(defender.board, defender)

            ## shoot
            coords = input(f"{attacker.name}, enter target as 'x y': ")
            x, y = map(int, coords.split())
            hit, win = self.game.guess(x, y) ## update backend board state / switch turn no.

            if hit:
                print(f"RESULT: {attacker.name} HIT {defender.name} @ ({x}, {y})")
            else:
                print(f"RESULT: {attacker.name} MISSED {defender.name} @ ({x}, {y})")
            self.updateAllLeds(defender.board, defender)

            if win:
                print(f"{attacker.name} wins")  
                break

            ##debug
            print(f"D: {defender.name}\nA: {attacker.name}")

            newAttacker = self.game.players[self.game.turn]
            waitTime = 5
            print(f"switch turns | showing {newAttacker.name} board in {waitTime} seconds")
            time.sleep(waitTime)


    def cleanup(self):
        GPIO.cleanup()

def main():
    vm = BattleshipViewModel()
    try:
        vm.play()
    except KeyboardInterrupt:
        vm.cleanup()
    except Exception as genException: 
        print("allan broke something", genException.__traceback__)
        raise
    finally:
        vm.cleanup()

main()
 