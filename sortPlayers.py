import json


class PlayerSorter:
    def __init__(self, players_per_role, roles_per_player):
        self.players_per_role = players_per_role
        self.roles_per_player = roles_per_player
        self.players_per_role = {
            "Top": [],
            "Jungle": [],
            "Mid": [],
            "Bot": [],
            "Support": []
        }

        with open("players.json") as f:
            self.player_info = json.load(f)

    def sort_players(self):
        pass
