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

        with open("players.json") as f:
            self.player_info = json.load(f)

        self.construct_roles_per_player()
        self.main_sort()

    def construct_roles_per_player(self):
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
        del self.players_per_role[role]
        self.construct_roles_per_player()

    def remove_player(self, player):
        for k, v in self.players_per_role.items():
            if player in v:
                v.remove(player)
        self.construct_roles_per_player()

    def main_sort(self):
        for i in range(5):
            lowest_role_player = self.find_min_player()
            lowest_player_role = self.find_min_role()
            # TODO ERRORS RETURN THE CURRENT SORTED ROLES WITH THE OUTSTANDING ROLES TO BE SORTED
            if self.player_role_count[lowest_role_player] == 0:
                print(f"(Player {lowest_role_player} needs to select more roles)")
                # TODO RETURN ERROR HERE (Player X needs to select more roles)
            elif self.role_player_count[lowest_player_role] <= 1:
                print(f"(Role {lowest_player_role} needs more players)")
                # TODO RETURN ERROR HERE (Role X needs more players)
            elif self.player_role_count[lowest_role_player] == 1:
                self.single_role_sort(lowest_role_player, self.roles_per_player[lowest_role_player][0])
            elif self.role_player_count[lowest_player_role] == 2:
                self.instant_sort(lowest_role_player)
            elif self.role_player_count[lowest_player_role] > 2:
                self.player_value_sort(lowest_role_player)

    def find_min_role(self):
        return min(self.role_player_count, key=self.role_player_count.get)

    def find_min_player(self):
        return min(self.player_role_count, key=self.player_role_count.get)

    def instant_sort(self, role):
        self.resultant_roles[role] = self.players_per_role[role]
        self.remove_player(self.players_per_role[role][0])
        self.remove_player(self.players_per_role[role][1])
        self.remove_role(role)

    def single_role_sort(self, player, role):
        opponents = self.players_per_role[role].copy()
        opponents.remove(player)
        self.resultant_roles[role] = self.find_best_opponent(player, opponents, role)
        self.remove_player(player)
        self.remove_player(self.resultant_roles[role][1])
        self.remove_role(role)

    def player_value_sort(self, role):
        pair_list = []
        pair_list_mmr = []
        opponents = self.players_per_role[role].copy()
        for i, player in enumerate(self.players_per_role[role][:-1], 1):
            pair_list.append(self.find_best_opponent(player, opponents[:i], role))
            pair_list_mmr.append(abs(pair_list[i - 1][0] - pair_list[i - 1][1]))
        self.resultant_roles[role] = pair_list[pair_list_mmr.index(min(pair_list_mmr))]
        self.remove_player(self.resultant_roles[role][0])
        self.remove_player(self.resultant_roles[role][1])
        self.remove_role(role)

    def find_best_opponent(self, player, opponents, role):
        opponent_list = []
        player_mmr = self.player_info[player][role]
        for opponent in opponents:
            opponent_list.append(abs(player_mmr - self.player_info[opponent][role]))

        return [player, opponents[opponent_list.index(min(opponent_list))]]
