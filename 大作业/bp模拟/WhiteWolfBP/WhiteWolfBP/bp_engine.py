# 文件名: bp_engine.py
import pyodbc
import pandas as pd
import numpy as np

class BPEngine:
    def __init__(self):
        # 数据库连接配置
        self.DB_SERVER = 'LAPTOP-KI0GT6AJ'
        self.DB_NAME = 'king'
        self.CONN_STR = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={self.DB_SERVER};"
            f"DATABASE={self.DB_NAME};"
            f"Trusted_Connection=yes;"
            f"TrustServerCertificate=yes;"
        )
        
        self.all_heroes = set()
        self.synergy_matrix = None
        self.counter_matrix = None
        self.hero_win_rates = {}
        
        print(">>> [系统] 正在初始化大数据引擎，读取历史比赛数据...")
        try:
            self.load_data_and_build_matrices()
            print(">>> [系统] 引擎初始化完成，矩阵构建完毕。")
        except Exception as e:
            print(f">>> [系统警告] 数据库连接或计算失败: {e}")

    def load_data_and_build_matrices(self):
        conn = pyodbc.connect(self.CONN_STR)
        # 读取最近的1000场比赛数据作为样本，保证速度
        sql = "SELECT TOP 1000 WinningTeam, BlueTeamName, RedTeamName, BluePick1, BluePick2, BluePick3, BluePick4, BluePick5, RedPick1, RedPick2, RedPick3, RedPick4, RedPick5 FROM MatchData"
        df = pd.read_sql(sql, conn)
        conn.close()

        records = []
        for idx, row in df.iterrows():
            winner = row['WinningTeam']
            blue_team = row['BlueTeamName']
            red_team = row['RedTeamName']
            
            blue_heroes = [row[f'BluePick{i}'] for i in range(1, 6) if row[f'BluePick{i}']]
            red_heroes = [row[f'RedPick{i}'] for i in range(1, 6) if row[f'RedPick{i}']]
            
            blue_win = 1 if winner == blue_team else 0
            red_win = 1 if winner == red_team else 0

            records.append({'heroes': blue_heroes, 'win': blue_win, 'opponents': red_heroes})
            records.append({'heroes': red_heroes, 'win': red_win, 'opponents': blue_heroes})
            
            self.all_heroes.update(blue_heroes)
            self.all_heroes.update(red_heroes)

        heroes_list = sorted(list(self.all_heroes))
        
        # 初始化矩阵
        self.synergy_matrix = pd.DataFrame(0.0, index=heroes_list, columns=heroes_list)
        self.counter_matrix = pd.DataFrame(0.0, index=heroes_list, columns=heroes_list)
        
        pair_counts = pd.DataFrame(0, index=heroes_list, columns=heroes_list)
        pair_wins = pd.DataFrame(0, index=heroes_list, columns=heroes_list)
        vs_counts = pd.DataFrame(0, index=heroes_list, columns=heroes_list)
        vs_wins = pd.DataFrame(0, index=heroes_list, columns=heroes_list)
        hero_total_games = {h: 0 for h in heroes_list}
        hero_total_wins = {h: 0 for h in heroes_list}

        for rec in records:
            team_heroes = rec['heroes']
            is_win = rec['win']
            enemy_heroes = rec['opponents']

            for h in team_heroes:
                if h in hero_total_games:
                    hero_total_games[h] += 1
                    hero_total_wins[h] += is_win
            
            # 协同统计
            for i in range(len(team_heroes)):
                for j in range(i + 1, len(team_heroes)):
                    h1, h2 = team_heroes[i], team_heroes[j]
                    if h1 in heroes_list and h2 in heroes_list:
                        pair_counts.loc[h1, h2] += 1
                        pair_counts.loc[h2, h1] += 1
                        if is_win:
                            pair_wins.loc[h1, h2] += 1
                            pair_wins.loc[h2, h1] += 1
            
            # 克制统计
            for h1 in team_heroes:
                for h2 in enemy_heroes:
                    if h1 in heroes_list and h2 in heroes_list:
                        vs_counts.loc[h1, h2] += 1
                        if is_win: vs_wins.loc[h1, h2] += 1

        for h in heroes_list:
            self.hero_win_rates[h] = hero_total_wins[h] / hero_total_games[h] if hero_total_games[h] > 0 else 0.5

        min_games = 2
        for h1 in heroes_list:
            for h2 in heroes_list:
                if h1 == h2: continue
                
                # 协同分计算
                games = pair_counts.loc[h1, h2]
                if games >= min_games:
                    rate = pair_wins.loc[h1, h2] / games
                    self.synergy_matrix.loc[h1, h2] = rate - self.hero_win_rates[h1]
                
                # 克制分计算
                v_games = vs_counts.loc[h1, h2]
                if v_games >= min_games:
                    rate = vs_wins.loc[h1, h2] / v_games
                    self.counter_matrix.loc[h1, h2] = rate - 0.5

    def get_analysis_text(self, my_team, enemy_team, top_k=3):
        """
        返回适合在UI文本框显示的分析文本
        """
        if self.synergy_matrix is None:
            return "数据库引擎未就绪。"

        possible_heroes = [h for h in self.all_heroes if h not in my_team and h not in enemy_team]
        scores = []

        for h in possible_heroes:
            total_score = 0
            reasons = []
            
            # 协同加分
            for mate in my_team:
                if mate in self.synergy_matrix.index:
                    val = self.synergy_matrix.loc[h, mate]
                    if val > 0.05:
                        total_score += val * 1.5 # 协同权重
                        reasons.append(f"搭档{mate}胜率↑{val:.0%}")
            
            # 克制加分
            for enemy in enemy_team:
                if enemy in self.counter_matrix.index:
                    val = self.counter_matrix.loc[h, enemy]
                    if val > 0.05:
                        total_score += val * 1.2 # 克制权重
                        reasons.append(f"克制{enemy}胜率{0.5+val:.0%}")
            
            # 基础胜率分
            base_rate = self.hero_win_rates.get(h, 0.5)
            total_score += (base_rate - 0.5) * 0.5
            
            if total_score > 0:
                scores.append((h, total_score, reasons))

        scores.sort(key=lambda x: x[1], reverse=True)
        
        # 格式化输出
        if not scores:
            return "暂无显著数据推荐。"
            
        result_lines = ["【大数据BP建议】:"]
        for i, (hero, score, reasons) in enumerate(scores[:top_k]):
            reason_str = " | ".join(reasons[:2]) # 只取前两个理由
            result_lines.append(f"{i+1}. {hero} (综合分{score:.2f}) -> {reason_str}")
            
        return "\n".join(result_lines)