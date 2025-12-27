import csv
import game

def load_match(game_mode, ban_num, max_game_num, match_id, team_blue, team_red):
    """加载比赛数据，不包含历史阵容功能"""
    heroes_all_list = []
    with open('heroes/heroes.csv', 'r') as heroes_all_csv:
        reader = csv.reader(heroes_all_csv)
        for row in reader:
            heroes_all_list.append(row)
            heroes_all_list[-1].extend(['0', '0', '0', '0'])  # 初始化英雄状态
        
        # 简化后的load_game调用，移除了历史阵容相关参数
        game.load_game(
            match_id=match_id,
            game_mode=game_mode,
            ban_num=ban_num,
            team_blue=team_blue,
            team_red=team_red,
            game_num=1,
            heroes_list=heroes_all_list,
            max_game_num=max_game_num
        )