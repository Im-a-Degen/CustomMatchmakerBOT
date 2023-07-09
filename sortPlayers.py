import json


# ---------------------------------------------------------
# SORTING PRIORITY:
# PLAYERS WITH SINGLE ROLES SELECTED
# ROLES WITH ONLY 2 PLAYERS IN IT
# LOWEST PLAYER COUNT ROLE WITH MORE THAN 2 PLAYER IN IT
# IF ROLES ARE TIED, PRIORITY BECOMES:
# JUNGLE -> MID -> SUPPORT -> BOT -> TOP
#
# ---------------------------------------------------------


class PlayerSorter:
    """Class to sort players into roles based on specified rules.

    Args:
        players_per_role (dict): A dictionary mapping roles to a list of players assigned to that role.

    Attributes:
        players_per_role (dict): A dictionary mapping roles to a list of players assigned to that role.
        roles_per_player (dict): A dictionary mapping players to the roles they are assigned to.
        role_player_count (dict): A dictionary mapping roles to the number of players assigned to that role.
        player_role_count (dict): A dictionary mapping players to the number of roles they are assigned to.
        resultant_roles (dict): A dictionary mapping roles to a list of sorted players for each role.
        player_info (dict): A dictionary containing player information loaded from a JSON file.
        error_message (list): A list to store any error messages encountered during sorting.
        error_detected (bool): A flag indicating if any errors were detected during sorting.
    """
    def __init__(self, players_per_role):
        self.players_per_role = players_per_role
        self.roles_per_player = {}
        self.role_player_count = {}
        self.player_role_count = {}
        self.resultant_roles = {
            "Top": [],
            "Jungle": [],
            "Mid": [],
            "Bot": [],
            "Support": []
        }
        self.player_info = {}
        self.error_message = []
        self.error_detected = False

        with open("players.json") as f:
            self.player_info = json.load(f)

        self.construct_roles_per_player()
        self.main_sort()

    def construct_roles_per_player(self):
        """Constructs the roles_per_player, player_role_count, and role_player_count
        dictionaries based on the current players_per_role dictionary.
        """
        self.roles_per_player.clear()
        self.player_role_count.clear()
        self.role_player_count.clear()
        for k, v in self.players_per_role.items():
            for player in v:
                if player in self.roles_per_player:
                    self.roles_per_player[player].append(k)
                    self.player_role_count[player] += 1
                else:
                    self.roles_per_player[player] = [k]
                    self.player_role_count[player] = 1
            self.role_player_count[k] = len(v)

    def remove_role(self, role):
        """Removes a role from the players_per_role dictionary and updates the relevant dictionaries accordingly.

        Args:
            role (str): The role to be removed.
        """
        del self.players_per_role[role]
        self.construct_roles_per_player()

    def remove_player(self, player):
        """Removes a player from the players_per_role dictionary and updates the relevant dictionaries accordingly.

        Args:
            player (str): The player to be removed.
        """
        for k, v in self.players_per_role.items():
            if player in v:
                v.remove(player)
        self.construct_roles_per_player()

    def main_sort(self):
        """Performs the main sorting algorithm to assign players to roles and populate the resultant_roles dictionary.

        """
        while sum((len(v) for v in self.resultant_roles.values())) < 10:
            lowest_role_player = self.find_min_player()
            lowest_player_role = self.find_min_role()
            if self.player_role_count[lowest_role_player] == 0:
                self.error_detected = True
                self.error_message.append(f"(Player {lowest_role_player} needs to select more roles)")
                self.remove_player(lowest_role_player)
            elif self.player_role_count[lowest_role_player] == 1:
                role = self.roles_per_player[lowest_role_player][0]
                self.resultant_roles[role].append(lowest_role_player)
                self.remove_player(lowest_role_player)

            elif len(self.resultant_roles[lowest_player_role]) == 1:
                if self.role_player_count[lowest_player_role] == 0:
                    self.error_detected = True
                    self.error_message.append(f"(Role {lowest_player_role} needs more players)")
                    self.remove_role(lowest_player_role)
                elif self.role_player_count[lowest_player_role] <= 1:
                    self.resultant_roles[lowest_player_role].append(self.players_per_role[0])
                    self.remove_player(self.players_per_role[0])
                    self.remove_role(lowest_player_role)
                elif self.role_player_count[lowest_player_role] > 1:
                    self.single_role_sort(self.resultant_roles[lowest_player_role][0], lowest_player_role)
            else:
                if self.role_player_count[lowest_player_role] <= 1:
                    self.error_detected = True
                    self.error_message.append(f"(Role {lowest_player_role} needs more players)")
                    self.remove_role(lowest_player_role)
                elif self.role_player_count[lowest_player_role] == 2:
                    self.instant_sort(lowest_player_role)
                elif self.role_player_count[lowest_player_role] > 2:
                    self.player_value_sort(lowest_player_role)
        if self.error_detected:
            self.error_output()

    def error_output(self):
        """Handles error cases during sorting by populating
        the resultant_roles dictionary with "No Player" placeholders.
        """
        for k, v in self.resultant_roles.items():
            while len(v) < 2:
                self.resultant_roles[k].append("No Player")

    def find_min_role(self):
        """Finds the role with the fewest assigned players.

        Returns:
            str: The role with the fewest assigned players.
        """
        return min(self.role_player_count, key=self.role_player_count.get)

    def find_min_player(self):
        """Finds the player assigned to the fewest roles.

        Returns:
            str: The player assigned to the fewest roles.
        """
        return min(self.player_role_count, key=self.player_role_count.get)

    def instant_sort(self, role):
        """Sorts a role instantly when it has exactly two players assigned to it.

        Args:
            role (str): The role to be sorted.
        """
        self.resultant_roles[role] = self.players_per_role[role].copy()
        self.remove_player(self.resultant_roles[role][0])
        self.remove_player(self.resultant_roles[role][1])
        self.remove_role(role)

    def single_role_sort(self, player, role):
        """Sorts a player who has only one role selected, matching them with the best opponent for that role.

        Args:
            player (str): The player to be sorted.
            role (str): The role for which the player needs an opponent.

        """
        opponents = self.players_per_role[role].copy()
        self.resultant_roles[role] = self.find_best_opponent(player, opponents, role)
        self.remove_player(self.resultant_roles[role][1])
        self.remove_role(role)

    def player_value_sort(self, role):
        """Sorts a role by comparing player MMR values and selecting the best player-opponent pair based on MMR difference.

        Args:
            role (str): The role to be sorted.
        """
        pair_list = []
        pair_list_mmr = []
        opponents = self.players_per_role[role].copy()
        for i, player in enumerate(self.players_per_role[role][:-1], 1):
            opponents.remove(player)
            player_mmr = self.player_info[player][role]
            pair_list.append(self.find_best_opponent(player, opponents, role))
            pair_list_mmr.append(abs(player_mmr - self.player_info[pair_list[i-1][1]][role]))
        self.resultant_roles[role] = pair_list[pair_list_mmr.index(min(pair_list_mmr))]
        self.remove_player(self.resultant_roles[role][0])
        self.remove_player(self.resultant_roles[role][1])
        self.remove_role(role)

    def find_best_opponent(self, player, opponents, role):
        """Finds the best opponent for a player based on MMR difference in a specific role.

        Args:
            player (str): The player for whom an opponent needs to be found.
            opponents (list): A list of potential opponents for the player.
            role (str): The role for which the opponents are being considered.

        Returns:
            list: A list containing the player and their best opponent for the role.
        """
        opponent_list = []
        player_mmr = self.player_info[player][role]
        for opponent in opponents:
            opponent_list.append(abs(player_mmr - self.player_info[opponent][role]))

        return [player, opponents[opponent_list.index(min(opponent_list))]]
