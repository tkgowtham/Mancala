import time
class Palankuzhi:
    def __init__(self):
        self.board = [
                        [5, 5, 5, 5, 5, 5, 5], #player 1 --> 0
                        [5, 5, 5, 5, 5, 5, 5]  #player 2 --> 1
                     ]
        self.player_coins = [0, 0]
        self.player1_coin_on_board = 35
        self.player2_coin_on_board = 35

    def checkForWin(self):
        coin_on_side1 = 0
        coin_on_side2 = 0
        for i in range(7):
            coin_on_side1 += self.board[0][i]
            coin_on_side2 += self.board[1][i]


        if coin_on_side1 == 0 or coin_on_side2 == 0:
            self.player_coins[0] += coin_on_side1
            self.player_coins[1] += coin_on_side2
            winner = None
            if self.player_coins[0] > self.player_coins[1]:
                print("Player 1 Wins !!!")
                winner = 0
            elif self.player_coins[0] < self.player_coins[1]:
                print("Player 2 Wins!!!")
                winner = 1
            else:
                print("Draw!!!")
            
            print("Final Stats: ")
            self.printStats()
            return (True, winner)
        
        return (False, -1)
    
    def validMove(self, row, col):
        if self.board[row][col] == 0:
            return False
        
        return True
    
    def printBoard(self):
        print("P1 --> ", self.board[0])
        print("P2 --> ", self.board[1])

    def printStats(self):
        print("Player 1: ", self.player_coins[0])
        print("Player 2: ", self.player_coins[1])
        print("\n")
            
    
    def __check_for_pasu(self):
        cur_side1 = self.board[0]
        while 4 in cur_side1:
            ind = cur_side1.index(4)
            self.player_coins[0] += 4
            self.board[0][ind] = 0
        cur_side2 = self.board[1]
        while 4 in cur_side2:
            ind = cur_side2.index(4)
            self.player_coins[1] += 4
            self.board[1][ind] = 0

    def __nextIndex(self, row, col):
        if row == 1:
            col += 1
            if col > 6:
                row = 0
                col = 6
        elif row == 0:
            col -= 1
            if col < 0:
                row = 1
                col = 0

        return row, col
    
    def setBoard(self, board, player_coins):
        self.board = board
        self.player_coins = player_coins
    
    def moveCoins(self, player_id, row, col):
        #player_id = player_id - 1
        #index = index - 1

        cur_coins = self.board[row][col]
        self.board[row][col] = 0

        while cur_coins > 0:
            row, col = self.__nextIndex(row, col)
            self.board[row][col] += 1
            cur_coins -= 1

            self.__check_for_pasu()
        #self.printBoard()
        #time.sleep(3)

        row, col = self.__nextIndex(row, col)
        if self.board[row][col] > 0:
            return self.moveCoins(player_id, row, col)
        elif self.board[row][col] == 0:
            row, col = self.__nextIndex(row, col)
            self.player_coins[player_id] += self.board[row][col]
            self.board[row][col] = 0
            return
"""            if row == 0: 
                if col == 0:
                    self.player_coins[player_id] += self.board[1][0]
                    self.board[1][0] = 0
                else:
                    self.player_coins[player_id] += self.board[row][col - 1]
                    self.board[row][col - 1] = 0
            elif row == 1:
                if col == 6:
                    self.player_coins[player_id] += self.board[0][6]
                    self.board[0][6] = 0
                else:
                    self.player_coins[player_id] += self.board[row][col + 1]
                    self.board[row][col + 1] = 0"""

"""
            if cur_coins == 0:
                if row == 0 and col > 0:
                    cur_coins = self.board[row][col - 1]
                elif row == 0 and col == 0:
                    cur_coins = self.board[1][0]
                elif row == 1 and col < 4:
                    cur_coins = self.board[row][col + 1]
                elif row == 1 and col == 4:
                    cur_coins = self.board[0][4]"""



"""     if player_id == 0:
            if row == 0 and col > 0:
                self.player1_coins += self.board[row][col - 1]
            elif row == 0 and col == 0:
                self.player1_coins += self.board[1][0]
        else:
            if row == 1 and col < 4:
                self.player2_coins += self.board[row][col + 1]
            elif row == 1 and col == 4:
                self.player2_coins += self.board[0][4]"""
class state:
    def __init__(self):
        self.board = None
        self.player_coins = [0,0]
        self.no_of_states = 0
        self.no_of_wins = 0
        self.next_state = [None for _ in range(7)]

class Tree:
    def __init__(self, player_id):
        self.game = Palankuzhi()
        self.curr_player = player_id
        self.root = state()
        self.root.board = self.game.board
        self.dfs(root=self.root, player_id=player_id)

    def dfs(self, root, player_id):
        self.game.setBoard(root.board.copy(), root.player_coins[:])
        win, winner = self.game.checkForWin()
        if win:
            if winner == self.curr_player:
                return 1
            return 0
            
        next_id = not player_id
        for i in range(7):
            if self.game.validMove(row=player_id,col=i):
                root.next_state[i] = state()
                self.game.moveCoins(player_id=player_id, row=player_id, col=i)
                self.game.printBoard()
                root.next_state[i].board = self.game.board
                root.next_state[i].player_coins = self.game.player_coins
                root.no_of_states += 1
                root.no_of_wins += self.dfs(root=root.next_state[i], player_id=next_id)
                self.game.setBoard(root.board.copy(), root.player_coins[:])
        
        return root.no_of_wins

    def set_next_state(self,index):
        self.root = self.root.next_state[index]
    
    def next_best_state(self):
        max_avg = float('-inf')
        max_coins = float('-inf')
        best_id = None
        for i in range(7):
            if self.root.next_state[i] is not None:
                avg = self.root.next_state[i].no_of_wins / self.root.next_state[i].no_of_states
                if avg > max_avg:
                    max_avg = avg
                    max_coins = self.root.next_state[i].player_coins[self.curr_player]
                    best_id = i
                elif avg == max_avg:
                    if self.root.next_state[i].player_coins[self.curr_player] > max_coins:
                        max_coins = self.root.next_state[i].player_coins[self.curr_player]
                        best_id = i
        self.set_next_state(i)
        return i


def manual():
    game = Palankuzhi()
    game.printBoard()
    game.printStats()
    player_id = int(input("Player 1 or 2: ")) - 1
    while True:
        print("Current Player: ", player_id + 1)
        index = int(input("Select (1 - 7): ")) - 1
        if not game.validMove(player_id, index):
            print("Not Valid Move")
            continue
        game.moveCoins(player_id, player_id, index)
        game.printBoard()
        game.printStats()
        if game.checkForWin()[0] == True:
            break
        player_id = not player_id

def AIopp():
    game = Palankuzhi()
    game.printBoard()
    game.printStats()
    player_id = int(input("Player 1 or 2: ")) - 1
    ai = Tree(player_id=not player_id)
    while True:
        print("Current Player: ", player_id + 1)
        index = int(input("Select (1 - 7): ")) - 1
        if not game.validMove(player_id, index):
            print("Not Valid Move")
            continue
        game.moveCoins(player_id, player_id, index)
        game.printBoard()
        game.printStats()
        ai.set_next_state(index)
        if game.checkForWin()[0] == True:
            break
        player_id = not player_id
        print("Current Player: ", player_id + 1)
        index = ai.next_best_state()
        game.moveCoins(player_id, player_id, index)
        game.printBoard()
        game.printStats()
        if game.checkForWin()[0] == True:
            break
        player_id = not player_id

if __name__ == '__main__':
    AIopp()