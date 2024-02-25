from enum import Enum as enum


class JERSEYNUM(enum):
    Empty = 9999


class Game:
    """Setup the game"""
    def __init__(self):
        self.home_teamname = "Home Team"
        self.visiting_teamname = "Visiting Team"
        self.game_time = "Jan 1, 1970"
        self.location = "Zimbabwe"
        self.current_teamname = self.home_teamname

    def set_home_team(self, team):
        self.home_team = team

    def set_visiting_team(self, team):
        self.visiting_team = team

    def set_game_time(self, gtime):
        self.game_time = gtime

    def set_location(self, location):
        self.location = location

    def set_current_team(self):
        for team in enumerate([self.visiting_team, self.home_team], 1):
            print(team)
        selection = input("\n Select a team --> ")
        if selection == 1:
            self.current_team = self.visiting_team
            self.current_team = self.visiting_teamname
        else:
            self.current_team = self.home_team
            self.current_teamname = self.home_teamname


class BaseballTeam:
    """Setup the baseball team object"""

    def __init__(self, team_name):
        self.roster = []
        self.lineup = []
        self.running_lineup = []
        self.teamname = team_name
        self.numplayers = 9
        self.home_or_visitor = None

    def __repr__(self):
        return str(self.roster)

    def __str__(self):
        retstr = ""
        for count, item in enumerate(self.roster, 1):
            retstr = retstr + str(count) + ". " + str(item) + "\n"
        return retstr

    def add_player_to_roster(self, first_name='Empty', last_name='Empty', number=JERSEYNUM.Empty.value):
        """Add a player to the roster"""

        if type(number) != 'int':
            number = int(number)

        if len(self.roster) == 0:
            self.roster.append(first_name, last_name, number)
            print(self)
        else:
            for player in self.roster:
                if player[2] != number:
                    self.roster.append((first_name, last_name, number))
                    print(self)
                    return
                else:
                    print(f"Sorry.  Uniform number {number} already exists.  Player not added.")

    def del_player_from_roster(self, number):
        """Delete a player from the roster by uniform number"""

        for player in self.roster:
            if player[2] == number:
                if player in self.lineup:
                    ans = input(f"WARNING!  {player} is in the lineup.  This player will be deleted from the lineup.  Continue? [y, n] --> ")
                    if ans == 'y' or ans == 'yes' or ans == 'Yes':
                        self.roster.remove(player)
                        self.lineup.remove(player)
                        print(self)
                else:
                    self.roster.remove(player)
                    print(self)
                return
        print(f"Sorry, uniform number {number} does not exist on the roster.")

    def del_player_from_lineup(self, number):
        """Delete a player from the lineup by uniform number"""

        for player in self.lineup:
            if player[2] == number:
                self.lineup.remove(player)
                return
        print(f"Sorry, uniform number {number} does not exist in the lineup.")

    def save_roster(self, team_name):
        """Save the current roster"""

        try:
            with open(team_name+".txt", 'w') as fn:
                fn.write(str(self.roster))
            print("Roster successfully saved.\n")

        except IOError:
            print("Failed to save roster.\n")

    def read_roster(self, team_name):
        """Read the roster from a file"""

        with open(team_name+".txt") as fn:
            line = fn.readline()
            self.roster = eval(str(line))

            print(self)

    def set_initial_lineup(self):
        """Set the initial lineup"""

        if len(renegades.roster) == 0:
            print("The roster has not been set.  There must be a roster to create a lineup.\n")
            return

        self.lineup = []
        not_added_str = "***** NOT ADDED! ******\nPlease enter an existing integer of somebody on the roster."
        print(self.__str__())
        i = 1
        while i < self.numplayers + 1:
            print(f"\nPlease select a player from the roster for batting position {i}")
            selection = input()
            if not selection.isdigit():
                print(not_added_str)
                continue
            if int(selection) > len(self.roster) or int(selection) < 1:
                print(not_added_str)
                continue

            player = self.roster[int(selection)-1]
            if player not in self.lineup:
                self.lineup.append(player)
                i += 1
            else:
                print(f"Sorry.  Player {player} is already in the lineup.")
                continue

            self.print_lineup()

    @staticmethod
    def find_player_by_jersey(player_list, jersey_num):
        """Find a player by jersey number and return the tuple"""
        for p in player_list:
            if p[2] == jersey_num:
                return p
        return None

    def substitute_player(self, jersey_number_going_out, jersey_number_coming_in):
        """Substitute a player in the lineup.  If jersey_number_going_out is None then add the player to the end."""

        ADDPLAYERTOEND = False
        if jersey_number_going_out is None:
            ADDPLAYERTOEND = True
            player_going_out = None
        else:
            player_going_out = self.find_player_by_jersey(self.lineup, jersey_number_going_out)
            if player_going_out is None:
                print(f"Error.  Player with Jersey number {jersey_number_going_out} is not in the lineup.")
                return False

        player_coming_in = self.find_player_by_jersey(self.roster, jersey_number_coming_in)
        if player_coming_in is None:
            print(f"Error.  Player with Jersey number {jersey_number_going_out} is not on the roster.")
            return False

        if ADDPLAYERTOEND:
            self.lineup.append(player_coming_in)
        else:
            if player_coming_in in self.lineup:
                print(f"Player {player_coming_in} is already in the lineup.")
                retstr = input("Would you still like to move this player to the new spot in the lineup?--> ")
                if retstr.lower == 'yes' or retstr.lower() == 'y':
                    self.lineup[self.lineup.index(player_coming_in)] = ('Empty', 'Empty', JERSEYNUM.Empty.value)
                    self.lineup[self.lineup.index(player_going_out)] = player_coming_in

            else:
                self.lineup[self.lineup.index(player_going_out)] = player_coming_in

        print("")
        self.print_lineup()

    def print_lineup(self):
        """Print the lineup to the console"""

        if len(self.lineup) == 0:
            print("The lineup has not been set.\n")

        else:

            prstr = ""
            for count, item in enumerate(self.lineup, 1):
                prstr = prstr + str(count) + ". " + str(item) + "\n"
            print(f"**** Current lineup for {self.teamname} ****")
            print(prstr)

    def set_home_visitor(self, hv):
        """Set home or visitor for this team"""

        if hv.lower() == "home" or hv.lower() == "visitors":
            self.home_or_visitor = hv
        else:
            "Error.  Home or Visitors are the only options."

    def update_numplayers(self, np):
        """Update the number of players allowed in the lineup"""

        self.numplayers = int(np)

    def shift_lineup(self):
        """Shift the lineup to the left."""
        player1 = self.lineup[0]
        self.lineup = self.lineup[1:]
        self.lineup.append(player1)


def quit_fn():
    """Menu: quit"""
    raise SystemExit


def auto_input_roster():
    """Menu: Input roster automatically using read"""

    current_team.read_roster(current_team.teamname)


def delete_player():
    """Menu: Delete a player from the roster."""

    player_to_delete = input("What is the jersey number of the player to be deleted? --> ")
    current_team.del_player_from_roster(int(player_to_delete))


def add_player():
    """Menu: Add a player to the roster"""

    first_name = input("Player's First Name --> ")
    last_name = input("Player's Last Name --> ")
    number = input("Player's jersey number --> ")
    current_team.add_player_to_roster(first_name=first_name, last_name=last_name, number=int(number))


def save_roster():
    """Menu: Save the roster to a file"""
    current_team.save_roster(current_team.teamname)


def input_lineup():
    """Menu: Set the initial lineup"""
    current_team.set_initial_lineup()


def print_players_not_in_lineup():
    print("Current roster players not in the lineup:")
    for player in current_team.roster:
        if player not in current_team.lineup:
            print(player)


def substitute():
    """Menu: Substitution"""
    print_players_not_in_lineup()
    player_going_out = input("What is the jersey number of the player going out? --> ")
    player_coming_in = input("What is the jersey number of the player coming in? --> ")
    current_team.substitute_player(int(player_going_out), int(player_coming_in))


def show_lineup():
    """Menu: Show the current lineup"""
    current_team.print_lineup()


def show_roster():
    """Menu: Show the current roster"""
    print(current_team)


def settings_menu_func():

    print("")
    settings_menu = {
        1: ("Number of players in lineup", set_lineup_num),
        2: ("Set current team", game.set_current_team),
        3: ("Back to Main Menu", settings_quit)
        }

    for settings_key in sorted(settings_menu.keys()):
        print(str(settings_key) + ":" + settings_menu[settings_key][0])

    settings_ans = input("Settings Menu --> ")
    settings_menu.get(int(settings_ans), [None, invalid])[1]()


def set_lineup_num():
    nump = input("How many players should be in the lineup? --> ")
    current_team.update_numplayers(nump)
    if len(current_team.lineup) == 0 or len(current_team.lineup) == nump:
        return

    if int(nump) > len(current_team.lineup):
        print(f"\nPlease add {int(nump) - len(current_team.lineup)} more players to the lineup.\n")
    else:
        print(f"\nPlease remove {len(current_team.lineup - int(nump))} players from the lineup.\n")


def add_player_to_lu():
    print_players_not_in_lineup()
    p_to_add = input("Enter the jersey number of the player to add to the lineup --> ")
    current_team.substitute_player(None, int(p_to_add))
    current_team.update_numplayers(len(current_team.lineup))
    current_team.print_lineup()


def delete_player_from_lu():
    current_team.print_lineup()
    p_to_del = input("Enter the jersey number of the player to delete from the lineup --> ")
    current_team.del_player_from_lineup(int(p_to_del))
    current_team.update_numplayers(len(current_team.lineup))
    current_team.print_lineup()


def settings_quit():
    return


def invalid():
    """Menu: Invalid menu choice"""
    print("INVALID CHOICE!")


game = Game()
game.set_home_team("Renegades")
game.set_visiting_team("ProSwing")
team_h = BaseballTeam(game.home_team)
team_v = BaseballTeam(game.visiting_team)
game.current_team = team_h

while True:

    print(f"****** {game.current_teamname} Main Menu ******")
    menu = {
            1: ("Auto input roster", auto_input_roster),
            2: ("Add player to roster", add_player),
            3: ("Delete player from roster", delete_player),
            4: ("Show roster", show_roster),
            5: ("Save roster", save_roster),
            6: ("Input initial lineup", input_lineup),
            7: ("Add player to lineup", add_player_to_lu),
            8: ("Delete player from lineup", delete_player_from_lu),
            9: ("Substitution", substitute),
            10: ("Show current lineup", show_lineup),
            11: ("Settings", settings_menu_func),
            12: ("Quit", quit_fn)
           }

    for key in sorted(menu.keys()):
        print(str(key)+":" + menu[key][0])

    ans = input("Main Menu --> ")
    menu.get(int(ans), [None, invalid])[1]()
