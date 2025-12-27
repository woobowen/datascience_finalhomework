import sys
import pyodbc
from openai import OpenAI

# ================= 1. 基础配置 =================
# 强制设置输出编码为 UTF-8，防止中文乱码
sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "50fcde62-d03f-4bdb-9d02-91481829504c"
MODEL_ID = "doubao-seed-1-6-flash-250828"
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"

# 数据库连接字符串
DB_SERVER = 'LAPTOP-KI0GT6AJ'
DB_NAME = 'king'

CONN_STR = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={DB_SERVER};"
    f"DATABASE={DB_NAME};"
    f"Trusted_Connection=yes;"
    f"TrustServerCertificate=yes;"
)

# ================= 2. 核心功能函数 =================

def get_detailed_team_data(team_name):
    """
    连接数据库，查询：基础数据 + 常禁用英雄 + 常使用英雄
    """
    conn = None
    try:
        conn = pyodbc.connect(CONN_STR)
        cursor = conn.cursor()
        
        # 处理战队名（去除空格，用于模糊匹配）
        clean_name = team_name.replace(' ', '')
        search_param = f"%{clean_name}%"

        # --- 第一步：查询基础数据 (team_info) ---
        cursor.execute("SELECT * FROM team_info WHERE REPLACE(team, ' ', '') LIKE ?", (search_param,))
        base_row = cursor.fetchone()
        
        if not base_row:
            return None

        columns = [column[0] for column in cursor.description]
        base_data = dict(zip(columns, base_row))
        
        # 处理胜率字符串
        win_rate_raw = base_data.get('win_rate', '未知')

        # --- 第二步：查询该战队常禁用英雄 (TeamHeroBan) ---
        # 对应 C# 中的逻辑：按 BanCount 降序取前 6 名
        sql_ban = "SELECT TOP 6 HeroName FROM TeamHeroBan WHERE REPLACE(TeamName, ' ', '') LIKE ? ORDER BY BanCount DESC"
        cursor.execute(sql_ban, (search_param,))
        ban_list = [row[0] for row in cursor.fetchall()]
        ban_str = "、".join(ban_list) if ban_list else "暂无数据"

        # --- 第三步：查询该战队常选择英雄 (TeamHeroChoose) ---
        # 对应 C# 中的逻辑：按 ChooseCount 降序取前 6 名
        sql_pick = "SELECT TOP 6 HeroName FROM TeamHeroChoose WHERE REPLACE(TeamName, ' ', '') LIKE ? ORDER BY ChooseCount DESC"
        cursor.execute(sql_pick, (search_param,))
        pick_list = [row[0] for row in cursor.fetchall()]
        pick_str = "、".join(pick_list) if pick_list else "暂无数据"

        # --- 第四步：组装所有数据 ---
        full_report_data = (
            f"【基础面板数据】\n"
            f"- 战队排名: {base_data.get('ranking', '未知')}\n"
            f"- 胜率: {win_rate_raw}\n"
            f"- 场均击杀: {base_data.get('avg_kills', 0)} (衡量进攻性)\n"
            f"- 场均死亡: {base_data.get('avg_deaths', 0)} (衡量容错率)\n"
            f"- 分均经济: {base_data.get('avg_economy', 0)} (衡量运营能力)\n\n"
            f"【关键英雄池数据】\n"
            f"- 战队最常使用的英雄(代表体系): {pick_str}\n"
            f"- 战队最常禁用的英雄(代表惧怕点): {ban_str}\n"
        )
        return full_report_data

    except pyodbc.Error as e:
        return f"数据库查询出错: {e}"
    finally:
        if conn:
            conn.close()

def get_ai_analysis(team_name, data_context):
    """
    调用豆包 AI 生成深度战略报告
    """
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    # --- 关键修改：升级 Prompt，要求输出战术建议和克制方法 ---
    system_prompt = """
    你是一名KPL王者荣耀职业联赛的顶级战术分析师。
    你需要根据用户提供的“基础数据”和“BP（禁用/选择）数据”写一份深度战队分析报告。

    请严格按照以下格式分四个章节输出（不要使用Markdown的#号，直接用【】作为标题）：

    【战队风格与体系】
    结合场均击杀（高则为打架队，低则运营队）和常用英雄，分析他们的核心打法。
    例如：如果常用英雄里有大乔/老夫子，说明擅长带线运营；如果有鲁班大师/张飞，说明擅长团战。

    【优势与短板】
    基于胜率和死亡数分析。
    
    【针对性提升建议】
    针对该战队目前的常用阵容，提出1-2条改进方向（如：扩充英雄池、加强前期节奏等）。

    【如何克制这支战队】
    这是最重要的部分。
    1. BP建议：针对他们“最常使用”的英雄，对手应该禁用谁？
    2. 战术针对：针对他们“最常禁用”的英雄（通常是他们害怕的），对手应该选什么类型的英雄来压制？
    
    要求：语言犀利专业，字数在300字左右，干货满满。
    """

    user_message = f"分析目标：{team_name}\n数据详情：\n{data_context}"

    try:
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=0.7, # 稍微增加创造性
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"AI 分析生成失败: {e}"

# ================= 3. 程序入口 =================

if __name__ == "__main__":
    # 接收命令行参数（战队名）
    if len(sys.argv) > 1:
        target_team = sys.argv[1]
    else:
        target_team = "成都AG超玩会" # 默认测试
    
    # 1. 获取完整数据
    team_data = get_detailed_team_data(target_team)
    
    if team_data and "基础面板数据" in team_data:
        # 2. 只要获取到了数据，就发送给AI
        report = get_ai_analysis(target_team, team_data)
        print(report)
    else:
        # 如果没找到数据，或者数据库报错
        print(f"无法生成报告：{team_data if team_data else '未找到该战队数据'}")