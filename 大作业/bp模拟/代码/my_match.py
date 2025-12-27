import csv
import game


def load_match(game_mode, ban_num, max_game_num, match_id, team_blue, team_red):
    heroes_all_list = []
    with open('heroes/heroes.csv', 'r') as heroes_all_csv:
        reader = csv.reader(heroes_all_csv)
        for row in reader:
            heroes_all_list.append(row)
            heroes_all_list[-1].extend(['0', '0', '0', '0'])
        game.load_game(match_id, game_mode, ban_num, team_blue, team_red, 1, heroes_all_list, max_game_num,
                       team_blue,
                       team_red, [])
