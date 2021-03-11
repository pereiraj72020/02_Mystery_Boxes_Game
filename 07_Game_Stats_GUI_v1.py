from tkinter import *
from functools import partial  # To prevent unwanted windows
import random


class Start:
    def __init__(self, parent):

        # GUI to get starting balance and stakes
        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # Set Initial balance to zero
        self.starting_funds = IntVar()
        self.starting_funds.set(0)

        # Mystery Heading (row 0)
        self.mystery_box_label = Label(self.start_frame, text="Mystery Box Game",
                                       font="Arial 19 bold")
        self.mystery_box_label.grid(row=0)

        # Initial Instructions (row 1)
        self.mystery_instructions = Label(self.start_frame,
                                          font="Arial 10 italic",
                                          text="Please enter a dollar amount "
                                               "(between $5 and $50) in the box "
                                               "below. Then choose the  "
                                               "stakes. The higher the stakes, "
                                               "the more you can win!",
                                          wrap=275, justify=LEFT, padx=10, pady=10)
        self.mystery_instructions.grid(row=1)

        # Entry box, Button & Error Label (row 2)
        self.entry_error_frame = Frame(self.start_frame, width=200)
        self.entry_error_frame.grid(row=2)

        self.start_amount_entry = Entry(self.entry_error_frame,
                                        font="Arial 19 bold", width=10)
        self.start_amount_entry.grid(row=0, column=0)

        self.add_funds_button = Button(self.entry_error_frame,
                                       font="Arial 14 bold",
                                       text="Add Funds",
                                       command=self.check_funds)
        self.add_funds_button.grid(row=0, column=1)

        self.amount_error_label = Label(self.entry_error_frame, fg="maroon",
                                        text="", font="Arial 10 bold", wrap=275,
                                        justify=LEFT)
        self.amount_error_label.grid(row=1, columnspan=2, pady=5)

        # button frame (row 3)
        self.stakes_frame = Frame(self.start_frame)
        self.stakes_frame.grid(row=3)

        # Buttons go here...
        button_font = "Arial 12 bold"
        # Orange low stakes button...
        self.low_stakes_button = Button(self.stakes_frame, text="Low ($5) ",
                                        command=lambda: self.to_game(1),
                                        font=button_font, bg="#FF9933")
        self.low_stakes_button.grid(row=0, column=0, pady=10)

        # Yellow medium stakes button...
        self.medium_stakes_button = Button(self.stakes_frame, text="Medium ($10)",
                                           command=lambda: self.to_game(2),
                                           font=button_font, bg="#FFFF33")
        self.medium_stakes_button.grid(row=0, column=1, padx=5, pady=10)

        # Green high stakes button...
        self.high_stakes_button = Button(self.stakes_frame, text="High ($15)",
                                         command=lambda: self.to_game(3),
                                         font=button_font, bg="#99FF33")
        self.high_stakes_button.grid(row=0, column=2, pady=10)

        # Disabled all stakes buttons at start
        self.low_stakes_button.config(state=DISABLED)
        self.medium_stakes_button.config(state=DISABLED)
        self.high_stakes_button.config(state=DISABLED)

    def check_funds(self):
        starting_balance = self.start_amount_entry.get()

        # Set error background colours (and assume that thare are no
        # errors at the start...
        error_back = "#ffafaf"
        has_errors = "no"
        error_feedback = ""

        # change background to white (for testing purposes) ...
        self.start_amount_entry.config(bg="white")
        self.amount_error_label.config(text="")

        # Disable all stakes buttons in case user changes mind and
        # decreases amount entered.
        self.low_stakes_button.config(state=DISABLED)
        self.medium_stakes_button.config(state=DISABLED)
        self.high_stakes_button.config(state=DISABLED)

        try:
            starting_balance = int(starting_balance)

            if starting_balance < 5:
                has_errors = "yes"
                error_feedback = "Sorry, the least you can play with is $5"
            elif starting_balance > 50:
                has_errors = "yes"
                error_feedback = "Too high! The most you can risk in this " \
                                 "game is $50"

            elif starting_balance >= 15:
                # enable all buttons
                self.low_stakes_button.config(state=NORMAL)
                self.medium_stakes_button.config(state=NORMAL)
                self.high_stakes_button.config(state=NORMAL)
            elif starting_balance >= 10:
                # enable low and medium stakes buttons
                self.low_stakes_button.config(state=NORMAL)
                self.medium_stakes_button.config(state=NORMAL)
            else:
                self.low_stakes_button.config(state=NORMAL)

        except ValueError:
            has_errors = "yes"
            error_feedback = "Please enter a dollar amount (no text / decimals)"

        if has_errors == "yes":
            self.start_amount_entry.config(bg=error_back)
            self.amount_error_label.config(text=error_feedback)
        else:
            # Set starting balance to amount entered by user
            self.starting_funds.set(starting_balance)

    def to_game(self, stakes):

        # retrieve starting balance
        starting_balance = self.starting_funds.get()

        Game(self, stakes, starting_balance)

        # hide start up window
        root.withdraw()


class Game:
    def __init__(self):
        # Formatting variables...
        self.game_stats_list = [50, 6]

        # In actual program this is blank and is populated with user calculations
        self.round_stats_list = ['gold ($5) | silver ($2) | lead ($0) - Cost: $5 | Payback: $7 | Current Balance: $22'
                                 'gold ($5) | silver ($2) | lead ($0) - Cost: $5 | Payback: $7 | Current Balance: $22',
                                 'lead ($0) | silver ($2) | copper ($1) - Cost: $5 | Payback: $3 | Current Balance: $20'
                                 'gold ($5) | silver ($2) | lead ($0) - Cost: $5 | Payback: $7 | Current Balance: $22',
                                 'lead ($0) | silver ($2) | copper ($1) - Cost: $5 | Payback: $3 | Current Balance: $20',
                                 'copper ($1) | copper ($1) | copper ($1) - Cost: $5 | Payback: $3 | Current Balance: $18'
                                 'gold ($5) | silver ($2) | lead ($0) - Cost: $5 | Payback: $7 | Current Balance: $22',
                                 'lead ($0) | silver ($2) | copper ($1) - Cost: $5 | Payback: $3 | Current Balance: $20',
                                 'copper ($1) | copper ($1) | copper ($1) - Cost: $5 | Payback: $3 | Current Balance: $18',
                                 'lead ($0) | copper ($1) | copper ($1) - Cost: $5 | Payback: $2 | Current Balance: $15'
                                 'gold ($5) | silver ($2) | lead ($0) - Cost: $5 | Payback: $7 | Current Balance: $22',
                                 'lead ($0) | silver ($2) | copper ($1) - Cost: $5 | Payback: $3 | Current Balance: $20',
                                 'copper ($1) | copper ($1) | copper ($1) - Cost: $5 | Payback: $3 | Current Balance: $18',
                                 'lead ($0) | copper ($1) | copper ($1) - Cost: $5 | Payback: $2 | Current Balance: $15',
                                 'copper ($1) | lead ($0) | silver ($2) - Cost: $5 | Payback: $3 | Current Balance: $13'
                                 'gold ($5) | silver ($2) | lead ($0) - Cost: $5 | Payback: $7 | Current Balance: $22',
                                 'lead ($0) | silver ($2) | copper ($1) - Cost: $5 | Payback: $3 | Current Balance: $20',
                                 'copper ($1) | copper ($1) | copper ($1) - Cost: $5 | Payback: $3 | Current Balance: $18',
                                 'lead ($0) | copper ($1) | copper ($1) - Cost: $5 | Payback: $2 | Current Balance: $15',
                                 'copper ($1) | lead ($0) | silver ($2) - Cost: $5 | Payback: $3 | Current Balance: $13',
                                 'lead ($0) | copper ($1) | silver ($2) - Cost: $5 | Payback: $3 | Current Balance: $11'
                                 'gold ($5) | silver ($2) | lead ($0) - Cost: $5 | Payback: $7 | Current Balance: $22',
                                 'lead ($0) | silver ($2) | copper ($1) - Cost: $5 | Payback: $3 | Current Balance: $20',
                                 'copper ($1) | copper ($1) | copper ($1) - Cost: $5 | Payback: $3 | Current Balance: $18',
                                 'lead ($0) | copper ($1) | copper ($1) - Cost: $5 | Payback: $2 | Current Balance: $15',
                                 'copper ($1) | lead ($0) | silver ($2) - Cost: $5 | Payback: $3 | Current Balance: $13',
                                 'lead ($0) | copper ($1) | silver ($2) - Cost: $5 | Payback: $3 | Current Balance: $11',
                                 'copper ($1) | copper ($1) | copper ($1) - Cost: $5 | Payback: $3 | Current Balance: $9'
                                 'gold ($5) | silver ($2) | lead ($0) - Cost: $5 | Payback: $7 | Current Balance: $22',
                                 'lead ($0) | silver ($2) | copper ($1) - Cost: $5 | Payback: $3 | Current Balance: $20',
                                 'copper ($1) | copper ($1) | copper ($1) - Cost: $5 | Payback: $3 | Current Balance: $18',
                                 'lead ($0) | copper ($1) | copper ($1) - Cost: $5 | Payback: $2 | Current Balance: $15',
                                 'copper ($1) | lead ($0) | silver ($2) - Cost: $5 | Payback: $3 | Current Balance: $13',
                                 'lead ($0) | copper ($1) | silver ($2) - Cost: $5 | Payback: $3 | Current Balance: $11',
                                 'copper ($1) | copper ($1) | copper ($1) - Cost: $5 | Payback: $3 | Current Balance: $9',
                                 'lead ($0) | copper ($1) | copper ($1) - Cost: $5 | Payback: $2 | Current Balance: $6'
                                 'gold ($5) | silver ($2) | lead ($0) - Cost: $5 | Payback: $7 | Current Balance: $22',
                                 'lead ($0) | silver ($2) | copper ($1) - Cost: $5 | Payback: $3 | Current Balance: $20',
                                 'copper ($1) | copper ($1) | copper ($1) - Cost: $5 | Payback: $3 | Current Balance: $18',
                                 'lead ($0) | copper ($1) | copper ($1) - Cost: $5 | Payback: $2 | Current Balance: $15',
                                 'copper ($1) | lead ($0) | silver ($2) - Cost: $5 | Payback: $3 | Current Balance: $13',
                                 'lead ($0) | copper ($1) | silver ($2) - Cost: $5 | Payback: $3 | Current Balance: $11',
                                 'copper ($1) | copper ($1) | copper ($1) - Cost: $5 | Payback: $3 | Current Balance: $9',
                                 'lead ($0) | copper ($1) | copper ($1) - Cost: $5 | Payback: $2 | Current Balance: $6',
                                 'copper ($1) | copper ($1) | silver ($2) - Cost: $5 | Payback: $4 | Current Balance: $5'
                                 'gold ($5) | silver ($2) | lead ($0) - Cost: $5 | Payback: $7 | Current Balance: $22',
                                 'lead ($0) | silver ($2) | copper ($1) - Cost: $5 | Payback: $3 | Current Balance: $20',
                                 'copper ($1) | copper ($1) | copper ($1) - Cost: $5 | Payback: $3 | Current Balance: $18',
                                 'lead ($0) | copper ($1) | copper ($1) - Cost: $5 | Payback: $2 | Current Balance: $15',
                                 'copper ($1) | lead ($0) | silver ($2) - Cost: $5 | Payback: $3 | Current Balance: $13',
                                 'lead ($0) | copper ($1) | silver ($2) - Cost: $5 | Payback: $3 | Current Balance: $11',
                                 'copper ($1) | copper ($1) | copper ($1) - Cost: $5 | Payback: $3 | Current Balance: $9',
                                 'lead ($0) | copper ($1) | copper ($1) - Cost: $5 | Payback: $2 | Current Balance: $6',
                                 'copper ($1) | copper ($1) | silver ($2) - Cost: $5 | Payback: $4 | Current Balance: $5',
                                 'copper ($1) | lead ($0) | silver ($2) - Cost: $5 | Payback: $3 | Current Balance: $3']

        self.game_frame = Frame()
        self.game_frame.grid()

        # Heading Row
        self.heading_label = Label(self.game_frame, text="Play...",
                                   font="Arial 24 bold", padx=10,
                                   pady=10)
        self.heading_label.grid(row=0)

        # History Button (row 1)
        self.stats_button = Button(self.game_frame,
                                   text="Game Stats",
                                   font="Arial 14", padx=10, pady=10,
                                   command=lambda: self.to_stats(self.round_stats_list))
        self.stats_button.grid(row=1)

    def to_stats(self, game_history, game_stats):
        GameStats(self, game_history, game_stats)


class GameStats:
    def __init__(self, partner, game_history, game_stats):

        print(game_history)

        # disable help button
        partner.stats_button.config(state=DISABLED)

        heading = "Arial 12 bold"
        content = "Arial 12"

        # Sets up child window (ie: help box)
        self.stats_box = Toplevel()

        # If users press cross at top, closes help and 'releases' help button

        self.stats_box.protocol('WM_DELETE_WINDOW', partial(self.close_stats,
                                                            partner))

        # Set up GUI Frame
        self.stats_frame = Frame(self.stats_box)
        self.stats_frame.grid()

        # Set up Help Heading (row 0)
        self.stats_heading_label = Label(self.stats_frame, text="Game Statistics",
                                         font="arial 19 bold")
        self.stats_heading_label.grid(row=0)

        # To Export <instructions> (row 1)
        self.export_instructions = Label(self.stats_frame,
                                         text="Here are your Game Statistics."
                                              "Please use the Export button to "
                                              "access the results of each "
                                              "round that you played", wrap=250,
                                         font="arial 10 italic",
                                         justify=LEFT, fg="green",
                                         padx=10, pady=10)
        self.export_instructions.grid(row=1)

        # Starting Balance (row 2)
        self.details_frame = Frame(self.stats_frame)
        self.details_frame.grid(row=2)

        # Starting balance (row 2.0)

        self.start_balance_label = Label(self.details_frame,
                                         text="Starting Balance:", font=heading,
                                         anchor="e")
        self.start_balance_label.grid(row=0, column=0, padx=0)

        self.start_value_label = Label(self.details_frame, font=content,
                                       text="${}".format(game_stats[0]), anchor="w")
        self.start_value_label.grid(row=0, column=1, padx=0)

        # Current Balance (row 2.2)
        self.current_balance_label = Label(self.details_frame,
                                           text="Current Balance:", font=heading,
                                           anchor="e")
        self.current_balance_label.grid(row=1, column=0, padx=0)

        self.current_balance_value_label = Label(self.details_frame, font=content,
                                                 text="${}".format(game_stats[1]), anchor="e")
        self.current_balance_value_label.grid(row=1, column=1, padx=0)

        if game_stats[1] > game_stats[0]:
            win_loss = "Amount Won:"
            amount = game_stats[1] - game_stats[0]
            win_loss_fg = "green"
        else:
            win_loss = "Amount Lost:"
            amount = game_stats[0] - game_stats[1]
            win_loss_fg = "#660000"

        # Amount won / lost (row 2.3)
        self.wind_loss_label = Label(self.details_frame,
                                     text=win_loss, font=heading,
                                     anchor="e")
        self.wind_loss_label.grid(row=2, column=0, padx=0)

        self.wind_loss_value_label = Label(self.details_frame, font=content, text="${}".format(amount),
                                           fg=win_loss_fg, anchor="w")
        self.wind_loss_value_label.grid(row=2, column=1, padx=0)

        # Rounds Played (row 2.4)
        self.games_played_label = Label(self.details_frame,
                                        text="Rounds Played:", font=heading,
                                        anchor="e")
        self.games_played_label.grid(row=4, column=0, padx=0)

        self.games_played_value_label = Label(self.details_frame, font=content,
                                              text=len(game_history),
                                              anchor="w")
        self.games_played_value_label.grid(row=4, column=1, padx=0)


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Mystery Box Game")
    something = Start(root)
    root.mainloop()
