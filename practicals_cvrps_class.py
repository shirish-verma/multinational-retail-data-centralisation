import random
import time

class RockPaperScissors():
    def __init__(self):
        self.user_wins = 0
        self.computer_wins = 0
        self.rounds_played = 0
        pass

    def get_user_choice(self):
        # user_choice = self.get_prediction()
        rps_choices = ['Rock', 'Paper', 'Scissors']
        while True:
            user_choice = input("User Choice: Rock, Paper or Scissors? >> ").title()
            if user_choice in rps_choices:
                return user_choice
            else:
                print('Invalid input. Please enter either rock, paper or scissors. Input is not case sensitive.')

    def get_prediction(self):
        pass
    
    def get_computer_choice(self):
        rps_choices = ['Rock', 'Paper', 'Scissors']
        computer_choice = random.choice(rps_choices)
        return computer_choice
    
    def get_winner(self, user_choice, computer_choice):
        if user_choice == 'Nothing':
            print('You didnt make a choice. Round forfeited.')
            self.computer_wins += 1
        elif computer_choice == user_choice:
            print('This round is a tie!')
        elif (computer_choice == 'Rock' and user_choice == 'Scissors') or (computer_choice == 'Paper' and user_choice == 'Rock') or (computer_choice == 'Scissors' and user_choice == 'Paper'):
            print('You lost this round.')
            self.computer_wins += 1
        else:
            print('You won this round!')
            self.user_wins +=1

    def play_round(self):
        user_choice = self.get_user_choice()
        computer_choice = self.get_computer_choice()
        self.get_winner(user_choice, computer_choice)
        self.rounds_played += 1


def play_rock_paper_scissors():
    rps_game = RockPaperScissors()
    while True:
        if (rps_game.rounds_played == 5) or (rps_game.computer_wins == 3) or ((rps_game.user_wins == 3)):
            break
        input(f'Round {rps_game.rounds_played + 1}: Ready to proceed? Press enter to continue or CTRL+C to exit.')
        rps_game.play_round()
    if rps_game.computer_wins > rps_game.user_wins:
        print(f'You lost the match. Computer : {rps_game.computer_wins}, User: {rps_game.user_wins}')
    elif rps_game.computer_wins < rps_game.user_wins:
        print(f'You won the match! Computer : {rps_game.computer_wins}, User: {rps_game.user_wins}')
    else:
        print(f'The match is a tie. Computer: {rps_game.computer_wins}, User: {rps_game.user_wins}')

play_rock_paper_scissors()
