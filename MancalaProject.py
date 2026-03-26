import random
random.seed(109)


class Mancala:
    def __init__(self, pits_per_player=6, stones_per_pit = 4):
        """
        The constructor for the Mancala class defines several instance variables:

        pits_per_player: This variable stores the number of pits each player has.
        stones_per_pit: It represents the number of stones each pit contains at the start of any game.
        board: This data structure is responsible for managing the Mancala board.
        current_player: This variable takes the value 1 or 2, as it's a two-player game, indicating which player's turn it is.
        moves: This is a list used to store the moves made by each player. It's structured in the format (current_player, chosen_pit).
        p1_pits_index: A list containing two elements representing the start and end indices of player 1's pits in the board data structure.
        p2_pits_index: Similar to p1_pits_index, it contains the start and end indices for player 2's pits on the board.
        p1_mancala_index and p2_mancala_index: These variables hold the indices of the Mancala pits on the board for players 1 and 2, respectively.
        """
        self.pits_per_player = pits_per_player
        self.board = [stones_per_pit] * ((pits_per_player+1) * 2)  # Initialize each pit with stones_per_pit number of stones 
        self.players = 2
        self.current_player = 1
        self.moves = []
        self.p1_pits_index = [0, self.pits_per_player-1]
        self.p1_mancala_index = self.pits_per_player
        self.p2_pits_index = [self.pits_per_player+1, len(self.board)-1-1]
        self.p2_mancala_index = len(self.board)-1
        
        # Zeroing the Mancala for both players
        self.board[self.p1_mancala_index] = 0
        self.board[self.p2_mancala_index] = 0

    def display_board(self):
        """
        Displays the board in a user-friendly format
        """
        player_1_pits = self.board[self.p1_pits_index[0]: self.p1_pits_index[1]+1]
        player_1_mancala = self.board[self.p1_mancala_index]
        player_2_pits = self.board[self.p2_pits_index[0]: self.p2_pits_index[1]+1]
        player_2_mancala = self.board[self.p2_mancala_index]

        print('P1               P2')
        print('     ____{}____     '.format(player_2_mancala))
        for i in range(self.pits_per_player):
            if i == self.pits_per_player - 1:
                print('{} -> |_{}_|_{}_| <- {}'.format(i+1, player_1_pits[i], 
                        player_2_pits[-(i+1)], self.pits_per_player - i))
            else:    
                print('{} -> | {} | {} | <- {}'.format(i+1, player_1_pits[i], 
                        player_2_pits[-(i+1)], self.pits_per_player - i))
            
        print('         {}         '.format(player_1_mancala))
        turn = 'P1' if self.current_player == 1 else 'P2'
        print('Turn: ' + turn)
        
    def valid_move(self, pit):
        """
        Function to check if the pit chosen by the current_player is a valid move.
        """
        
        # write your code here

        if pit < 1 or pit > self.pits_per_player:
            return False
        
        if self.current_player==1:
            x = pit-1

        else: 
            x = self.p2_pits_index[0] + (pit -1 )
        
        return self.board[x] > 0

        
    def random_move_generator(self):
        """
        Function to generate random valid moves with non-empty pits for the random player
        """
        
        # write your code here
        valid = [pit for pit in range(1, self.pits_per_player +1) if self.valid_move(pit)]

        if valid: 
            return random.choice(valid)
        
        return None
    
    def play(self, pit):
        """
        This function simulates a single move made by a specific player using their selected pit. It primarily performs three tasks:
        1. It checks if the chosen pit is a valid move for the current player. If not, it prints "INVALID MOVE" and takes no action.
        2. It verifies if the game board has already reached a winning state. If so, it prints "GAME OVER" and takes no further action.
        3. After passing the above two checks, it proceeds to distribute the stones according to the specified Mancala rules.

        Finally, the function then switches the current player, allowing the other player to take their turn.
        """
        
        # write your code here
        print(f"Player {self.current_player} chose pit: {pit}")

        if not self.valid_move(pit):
            print("INVALID MOVE")
            return self.board

        if self.winning_eval():
            print("GAME OVER")
            return self.board

        self.moves.append((self.current_player, pit))

        if self.current_player == 1:
            start = pit - 1

        else:
            start = self.p2_pits_index[0] + (pit - 1)

        stones = self.board[start]
        self.board[start] = 0

        if self.current_player == 1:

            skip = self.p2_mancala_index
            manIdx = self.p1_mancala_index
            pitsStart = self.p1_pits_index[0]
            pitsEnd = self.p1_pits_index[1]

        else:

            skip = self.p1_mancala_index
            manIdx = self.p2_mancala_index
            pitsStart = self.p2_pits_index[0]
            pitsEnd = self.p2_pits_index[1]

        curr = start
        lastIdx = -1


        while stones > 0:

            curr = (curr + 1) % len(self.board)

            if curr == skip:
                continue

            self.board[curr] += 1
            stones -= 1
            lastIdx = curr

        if (pitsStart <= lastIdx <= pitsEnd and self.board[lastIdx] == 1):

            opposite_index = 2 * self.pits_per_player - lastIdx

            if self.board[opposite_index] > 0:

                captured = self.board[lastIdx] + self.board[opposite_index]
                self.board[lastIdx] = 0
                self.board[opposite_index] = 0
                self.board[manIdx] += captured

        self.current_player = 3 - self.current_player

        if self.winning_eval():

            for i in range(self.p1_pits_index[0], self.p1_pits_index[1] + 1):

                self.board[self.p1_mancala_index] += self.board[i]
                self.board[i] = 0

            for i in range(self.p2_pits_index[0], self.p2_pits_index[1] + 1):
                
                self.board[self.p2_mancala_index] += self.board[i]
                self.board[i] = 0

        return self.board
    
    def winning_eval(self):
        """
        Function to verify if the game board has reached the winning state.
        Hint: If either of the players' pits are all empty, then it is considered a winning state.
        """
        
        
        # write your code here
        a = all(self.board[i]==0 for i in range(self.p1_pits_index[0], self.p1_pits_index[1] + 1))
        b = all(self.board[i]==0 for i in range(self.p2_pits_index[0], self.p2_pits_index[1] + 1))
        return a or b

 
def randPlayeTest(numGames=100, seed=1400):

    random.seed(seed)
    p1Wins = 0
    p2Wins = 0
    ties = 0
    tot_Turns = 0

    p1_tot_Turns = 0
    p2_tot_Turns = 0

    for _ in range(numGames):

        game = Mancala()
        turn_count = 0
        p1_turns = 0
        p2_turns = 0


        while not game.winning_eval():
            p = game.random_move_generator()

            if p is not None:

                if game.current_player == 1:
                    p1_turns += 1

                else:
                    p2_turns += 1
                    
                game.play(p)
                turn_count += 1


        p1_score = game.board[game.p1_mancala_index]
        p2_score = game.board[game.p2_mancala_index]
        tot_Turns += turn_count

        p1_tot_Turns += p1_turns
        p2_tot_Turns += p2_turns

        if p1_score > p2_score: 
            p1Wins += 1

        elif p2_score > p1_score:
            p2Wins += 1

        else:
            ties += 1

    return  p1Wins, p2Wins, ties, (tot_Turns / numGames), (p1_tot_Turns / numGames), (p2_tot_Turns / numGames)

p1Wins, p2Wins, ties, avg_turns, p1_avg_turns, p2_avg_turns = randPlayeTest()

N = 100


print("P1 win %:", p1Wins/N*100)
print("P1 loss %:", p2Wins/N*100)

print("P2 win %:", p2Wins/N*100)
print("P2 loss %:", p1Wins/N*100)

print("Tie %:", ties/N*100)

print("Average total turns per game:", avg_turns)
print("Average number of turns per game P1:", p1_avg_turns)
print("Average number of turns per game P2:", p2_avg_turns)
