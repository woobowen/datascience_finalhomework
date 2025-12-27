# 文件名: my_match.py
import csv
import game
import pyodbc

def get_hero_stats_from_db():
    """从SQL Server获取常用/高胜率英雄数据及其具体数值"""
    hero_stats = {}
    try:
        conn_str = (
            r'DRIVER={ODBC Driver 17 for SQL Server};'
            r'SERVER=LAPTOP-KI0GT6AJ;'
            r'DATABASE=king;'
            r'Trusted_Connection=yes;'
        )
        cnxn = pyodbc.connect(conn_str)
        cursor = cnxn.cursor()

        # 【修正】查询高胜率英雄时，同时获取“胜率”这一列的数值
        cursor.execute("SELECT 胜率最高英雄名, 胜率 FROM HighWinRateHeroes")
        for row in cursor.fetchall():
            # 存储一个元组：(类型, 数值)
            hero_stats[row.胜率最高英雄名] = ("高胜率", row.胜率)

        # 【修正】查询最常用英雄时，同时获取“使用局数”这一列的数值
        cursor.execute("SELECT 最常用英雄名, 使用局数 FROM MostUsedHeroes")
        for row in cursor.fetchall():
            if row.最常用英雄名 not in hero_stats:
                # 存储一个元组：(类型, 数值)
                hero_stats[row.最常用英雄名] = ("常选择", row.使用局数)
        
        cnxn.close()
        print("成功从数据库加载英雄数据。")
        return hero_stats
    except Exception as e:
        print(f"连接数据库失败: {e}")
        return {}

def load_match(team_blue, team_red):
    heroes_all_list = []
    with open('heroes/heroes.csv', 'r', encoding='gbk') as heroes_all_csv:
        reader = csv.reader(heroes_all_csv)
        for row in reader:
            heroes_all_list.append(row)
            while len(heroes_all_list[-1]) < 15:
                heroes_all_list[-1].append('0')
        
    hero_stats = get_hero_stats_from_db()

    game.load_regular_game_8ban(
        match_id="1",
        team_blue=team_blue,
        team_red=team_red,
        heroes_all_list=heroes_all_list,
        team1=team_blue,
        team2=team_red,
        hero_stats=hero_stats
    )