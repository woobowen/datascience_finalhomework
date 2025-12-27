# 文件名: game.py
import copy
import wx
import csv
import doubao_ai
import threading
import bp_engine

def load_regular_game_8ban(match_id, team_blue, team_red, heroes_all_list, team1, team2, hero_stats):
    class SelectButton(wx.BitmapButton):
        def __init__(self, parent, id, bitmap):
            super().__init__(parent, id, bitmap)
            self.Bind(wx.EVT_PAINT, self.on_paint)
            self.colour = wx.Colour(255, 255, 255)

        def on_paint(self, event):
            dc = wx.PaintDC(self)
            self.draw_border(dc)
            bitmap = self.GetBitmap()
            dc.DrawBitmap(bitmap, 0, 0, True)

        def draw_border(self, dc):
            border_color = self.colour
            dc.SetPen(wx.Pen(border_color, 1))
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            width, height = self.GetSize()
            dc.DrawRectangle(0, 0, width, height)

    class BpFrame(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None, title='WBW的BP模拟器')
            self.SetSize((1500, 900))
            self.Maximize(True)
            self.Center()

            # 【样式修改】定义颜色
            self.bgColor = wx.Colour(28, 33, 43)      # 深蓝灰背景 #1C212B
            self.panelColor = wx.Colour(40, 48, 64)    # 面板背景色 #283040
            self.textColor = wx.Colour(224, 224, 224)  # 亮灰色文字 #E0E0E0
            self.accentColor = wx.Colour(0, 255, 255)   # 青色高亮 #00FFFF
            
            self.hero_stats = hero_stats
            self.career_list = []
            self.final_hero_pos = 0
            self.pos = 0
            self.bp_sequence = ['0'] * 18
            self.select_work = 0
            self.bp_engine = bp_engine.BPEngine()

            self.panel = wx.Panel(self)
            self.panel.SetBackgroundColour(self.bgColor) # 【样式修改】设置主面板背景色

            root_sizer = wx.BoxSizer(wx.VERTICAL)
            top_sizer = wx.BoxSizer(wx.HORIZONTAL)
            
            hero_panel = wx.Panel(self.panel, size=(900, -1))
            hero_panel.SetBackgroundColour(self.panelColor)
            hero_selection_sizer = wx.BoxSizer(wx.VERTICAL)
            
            select_pos_box = wx.BoxSizer(wx.HORIZONTAL)
            self.hero_grid_panel = wx.ScrolledWindow(hero_panel)
            self.hero_grid_panel.SetBackgroundColour(self.panelColor)
            self.hero_grid_panel.SetScrollRate(10, 10)
            self.hero_grid = wx.GridSizer(rows=0, cols=8, vgap=5, hgap=5)
            self.hero_grid_panel.SetSizer(self.hero_grid)
            
            hero_selection_sizer.Add(select_pos_box, 0, wx.EXPAND | wx.ALL, 5)
            hero_selection_sizer.Add(self.hero_grid_panel, 1, wx.EXPAND)
            hero_panel.SetSizer(hero_selection_sizer)

            self.career_text_list = []
            with open('heroes\\hero_settings.csv', 'r', newline='', encoding='gbk') as setting_csv:
                reader = csv.reader(setting_csv)
                for i in reader:
                    self.career_text_list.append(i)

            self.select_career_btn_list = []
            self.select_all_btn = wx.Button(hero_panel, label='全部', size=(-1, 40))
            select_pos_box.Add(self.select_all_btn, 1, wx.EXPAND | wx.ALL, 2)
            self.select_career_btn_list.append(self.select_all_btn)
            self.select_all_btn.Bind(wx.EVT_BUTTON, lambda event, pram1='全部': self.OnClickedSelectCareer(event, pram1))

            for i in self.career_text_list:
                self.select_career_btn = wx.Button(hero_panel, label=i[0], size=(-1, 40))
                select_pos_box.Add(self.select_career_btn, 1, wx.EXPAND | wx.ALL, 2)
                self.select_career_btn_list.append(self.select_career_btn)
                self.select_career_btn.Bind(wx.EVT_BUTTON, lambda event, pram1=i[0]: self.OnClickedSelectCareer(event, pram1))

            ai_panel = wx.Panel(self.panel, size=(600, -1))
            ai_panel.SetBackgroundColour(self.panelColor)
            ai_sizer = wx.BoxSizer(wx.VERTICAL)
            ai_title = wx.StaticText(ai_panel, label="AI解说")
            title_font = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD)
            ai_title.SetFont(title_font)
            ai_title.SetForegroundColour(self.accentColor)
            
            self.ai_commentary = wx.TextCtrl(ai_panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
            commentary_font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
            self.ai_commentary.SetFont(commentary_font)
            self.ai_commentary.SetBackgroundColour(self.bgColor)
            self.ai_commentary.SetForegroundColour(self.textColor)
            
            ai_sizer.Add(ai_title, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)
            ai_sizer.Add(self.ai_commentary, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
            ai_panel.SetSizer(ai_sizer)
            
            top_sizer.Add(hero_panel, 0, wx.EXPAND | wx.ALL, 5)
            top_sizer.Add(ai_panel, 0, wx.EXPAND | wx.ALL, 5)
            
            button_box = wx.BoxSizer(wx.HORIZONTAL)
            self.analyze_btn = wx.Button(self.panel, label='分析阵容')
            self.analyze_btn.Disable()
            self.analyze_btn.Bind(wx.EVT_BUTTON, self.OnAnalyzeClicked)
            
            next_game_btn = wx.Button(self.panel, label='结束')
            next_game_btn.Bind(wx.EVT_BUTTON, self.OnClickedNext)
            
            button_box.Add(self.analyze_btn, 0, wx.CENTER | wx.RIGHT, 10)
            button_box.Add(next_game_btn, 0, wx.CENTER)
            
            bp_board_box = wx.BoxSizer(wx.HORIZONTAL)
            ban_blue_box = wx.BoxSizer(wx.HORIZONTAL)
            ban_red_box = wx.BoxSizer(wx.HORIZONTAL)
            pick_blue_box = wx.BoxSizer(wx.HORIZONTAL)
            pick_red_box = wx.BoxSizer(wx.HORIZONTAL)
            blue_box = wx.BoxSizer(wx.VERTICAL)
            red_box = wx.BoxSizer(wx.VERTICAL)
            
            bmp1 = wx.Image('image\\select_ban.png', wx.BITMAP_TYPE_ANY).Scale(70,70).ConvertToBitmap()
            select1, select2, select3, select4 = SelectButton(self.panel, -1, bmp1), SelectButton(self.panel, -1, bmp1), SelectButton(self.panel, -1, bmp1), SelectButton(self.panel, -1, bmp1)
            select11, select12, select13, select14 = SelectButton(self.panel, -1, bmp1), SelectButton(self.panel, -1, bmp1), SelectButton(self.panel, -1, bmp1), SelectButton(self.panel, -1, bmp1)

            team_blue_text = wx.StaticText(self.panel, -1, label=f"蓝色方：{team_blue}")
            team_red_text = wx.StaticText(self.panel, -1, label=f"红色方：{team_red}")
            team_text_font = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD)
            team_blue_text.SetFont(team_text_font)
            team_red_text.SetFont(team_text_font)
            team_blue_text.SetForegroundColour(wx.Colour(135, 206, 250)) # 天蓝色
            team_red_text.SetForegroundColour(wx.Colour(255, 69, 0))    # 红色

            ban_blue_box.Add(select1, 0, wx.ALL, 2)
            ban_blue_box.Add(select3, 0, wx.ALL, 2)
            ban_blue_box.Add(select12, 0, wx.ALL, 2)
            ban_blue_box.Add(select14, 0, wx.ALL, 2)
            ban_blue_box.AddStretchSpacer(1)
            ban_blue_box.Add(team_blue_text, 0, wx.ALIGN_CENTER_VERTICAL)

            ban_red_box.Add(team_red_text, 0, wx.ALIGN_CENTER_VERTICAL)
            ban_red_box.AddStretchSpacer(1)
            ban_red_box.Add(select13, 0, wx.ALL, 2)
            ban_red_box.Add(select11, 0, wx.ALL, 2)
            ban_red_box.Add(select4, 0, wx.ALL, 2)
            ban_red_box.Add(select2, 0, wx.ALL, 2)
            
            select_pick_bmp = wx.Image('image\\select_pick.png', wx.BITMAP_TYPE_ANY).Scale(110, 110).ConvertToBitmap()
            select5, select8, select9, select16, select17 = SelectButton(self.panel, -1, select_pick_bmp), SelectButton(self.panel, -1, select_pick_bmp), SelectButton(self.panel, -1, select_pick_bmp), SelectButton(self.panel, -1, select_pick_bmp), SelectButton(self.panel, -1, select_pick_bmp)
            select6, select7, select10, select15, select18 = SelectButton(self.panel, -1, select_pick_bmp), SelectButton(self.panel, -1, select_pick_bmp), SelectButton(self.panel, -1, select_pick_bmp), SelectButton(self.panel, -1, select_pick_bmp), SelectButton(self.panel, -1, select_pick_bmp)
            
            self.select_button = [select1, select2, select3, select4, select5, select6, select7, select8, select9, select10, select11, select12, select13, select14, select15, select16, select17, select18]
            
            bindings = [(btn, i) for i, btn in enumerate(self.select_button)]
            for btn, index in bindings:
                btn.Bind(wx.EVT_BUTTON, lambda event, i=index: self.onChoosePos(event, i))

            pick_blue_box.Add(select5, 0, wx.ALL, 2)
            pick_blue_box.Add(select8, 0, wx.ALL, 2)
            pick_blue_box.Add(select9, 0, wx.ALL, 2)
            pick_blue_box.Add(select16, 0, wx.ALL, 2)
            pick_blue_box.Add(select17, 0, wx.ALL, 2)
            
            pick_red_box.Add(select18, 0, wx.ALL, 2)
            pick_red_box.Add(select15, 0, wx.ALL, 2)
            pick_red_box.Add(select10, 0, wx.ALL, 2)
            pick_red_box.Add(select7, 0, wx.ALL, 2)
            pick_red_box.Add(select6, 0, wx.ALL, 2)
            
            blue_box.Add(ban_blue_box, 0, wx.EXPAND)
            blue_box.Add(pick_blue_box, 1, wx.ALIGN_CENTER_HORIZONTAL)
            red_box.Add(ban_red_box, 0, wx.EXPAND)
            red_box.Add(pick_red_box, 1, wx.ALIGN_CENTER_HORIZONTAL)
            
            bp_board_box.Add(blue_box, 1, wx.EXPAND | wx.ALL, 5)
            bp_board_box.Add(red_box, 1, wx.EXPAND | wx.ALL, 5)
            
            root_sizer.Add(top_sizer, 1, wx.EXPAND)
            root_sizer.Add(button_box, 0, wx.ALIGN_CENTER | wx.ALL, 5)
            root_sizer.Add(bp_board_box, 0, wx.EXPAND | wx.ALL, 5)
            
            self.panel.SetSizer(root_sizer)
            
            self.load_hero_event = wx.CommandEvent(wx.EVT_BUTTON.typeId, self.select_career_btn_list[0].GetId())
            wx.PostEvent(self.select_career_btn_list[0], self.load_hero_event)
            self.onChoosePos(None, 0)
        
        def update_commentary(self, text):
            if self.ai_commentary.GetValue():
                self.ai_commentary.AppendText(f"\n\n{text}")
            else:
                self.ai_commentary.SetValue(text)
            self.ai_commentary.ShowPosition(self.ai_commentary.GetLastPosition())

        def OnClickedSelectCareer(self, event, career):
            for item in self.hero_grid.GetChildren():
                item.GetWindow().Destroy()
            self.career_list = []
            
            select_pick_bmp = wx.Image('image\\select_pick.png', wx.BITMAP_TYPE_ANY).Scale(90, 90).ConvertToBitmap()
            empty_btn = wx.BitmapButton(self.hero_grid_panel, -1, select_pick_bmp)
            empty_btn.Bind(wx.EVT_BUTTON, lambda event, pram1='0': self.onClickSelect(event, pram1))
            self.hero_grid.Add(empty_btn, 1, wx.EXPAND)

            for i, v in enumerate(self.career_text_list):
                if v[0] == career:
                    self.select_work = i + 1
                    self.career_list = copy.copy(v)
                    self.career_list.pop(0)
            if career == '全部':
                self.select_work = 0
                for i in heroes_all_list:
                    if i[0] != 'ID':
                        self.career_list.append(i[0])

            for hero_id_str in self.career_list:
                if hero_id_str != '':
                    hero = heroes_all_list[int(hero_id_str)]
                    is_banned_or_picked = hero[13] == '1' or hero[14] == '1'
                    
                    bmp = wx.Image('heroes\\icon\\' + hero[0] + '.jpg', wx.BITMAP_TYPE_ANY)
                    if is_banned_or_picked:
                        bmp = bmp.ConvertToGreyscale()
                    
                    bmp = bmp.Scale(90, 90).ConvertToBitmap()
                    btn = wx.BitmapButton(self.hero_grid_panel, -1, bmp)
                    
                    if not is_banned_or_picked:
                        btn.Bind(wx.EVT_BUTTON, lambda event, pram1=hero[0]: self.onClickSelect(event, pram1))
                    
                    self.hero_grid.Add(btn, 1, wx.EXPAND)

            self.hero_grid_panel.Layout()
            self.panel.Layout()
            
        def onChoosePos(self, event, i):
            self.pos = i
            for idx, btn in enumerate(self.select_button):
                btn.colour = wx.Colour(255, 0, 0) if idx == i else wx.Colour(255, 255, 255)
                btn.Refresh()
            
            if i < 4: phase = "第一轮禁用"
            elif i < 10: phase = "第一轮选用"
            elif i < 14: phase = "第二轮禁用"
            else: phase = "第二轮选用"
            
            blue_team_turns = [0, 2, 4, 7, 8, 11, 13, 15, 16]
            team = "蓝色方" if i in blue_team_turns else "红色方"
            self.update_commentary(f"当前BP阶段: {phase}\n当前操作方: {team}\n请选择英雄...")
            
            wx.PostEvent(self.select_career_btn_list[self.select_work], self.load_hero_event)

        def OnClickedNext(self, event):
            if self.final_hero_pos == 1:
                save_list = [[match_id, '1', '1', team_blue, team_red, '8ban']]
                save_list[0].extend(self.bp_sequence)
                with open('save\\save.csv', mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    for row in save_list:
                        writer.writerow(row)
                self.Close()
            else:
                wx.MessageBox('对局尚未结束！', '提示', wx.OK | wx.ICON_INFORMATION)

        def onClickSelect(self, event, id):
            ban_list = [0, 1, 2, 3, 10, 11, 12, 13]
            blue_pick_list = [4, 7, 8, 15, 16]
            red_pick_list = [5, 6, 9, 14, 17]
            blue_team_turns = [0, 2, 4, 7, 8, 11, 13, 15, 16]

            if self.pos >= 18: return

            hero_name = heroes_all_list[int(id)][1] if id != '0' and id.isdigit() else "空Ban"
            team = "蓝色方" if self.pos in blue_team_turns else "红色方"
            
            if self.pos in ban_list:
                comment = f"{team} 禁用了 [{hero_name}]"
                self.update_commentary(comment)
                if id == '0':
                    bmp = wx.Image('image\\select_ban.png', wx.BITMAP_TYPE_ANY).ConvertToGreyscale().Scale(70, 70).ConvertToBitmap()
                else:
                    bmp = wx.Image('heroes\\icon\\' + id + '.jpg', wx.BITMAP_TYPE_ANY).ConvertToGreyscale().Scale(70, 70).ConvertToBitmap()
                self.select_button[self.pos].SetBitmap(bmp)
                ban_hero(self.pos, id, heroes_all_list, int(self.bp_sequence[self.pos]))
            else:
                comment = f"{team} 选择了 [{hero_name}]"
                
                if hero_name in self.hero_stats:
                    stat_type, stat_value = self.hero_stats[hero_name]
                    formatted_stat = ""
                    if stat_type == "高胜率":
                        formatted_stat = f"高胜率英雄 (胜率: {stat_value:.2%})"
                    elif stat_type == "常选择":
                        formatted_stat = f"常选择英雄 (使用: {stat_value} 局)"
                    
                    if formatted_stat:
                        comment += f" (值得注意！数据库记录 -> {formatted_stat})"

                self.update_commentary(comment)
                
                bmp = wx.Image('heroes\\icon\\' + id + '.jpg', wx.BITMAP_TYPE_ANY).Scale(110, 110).ConvertToBitmap()
                self.select_button[self.pos].SetBitmap(bmp)
                
                if_change = 0 if team1 == team_blue else 1
                if self.pos in blue_pick_list:
                    pick_hero(self.pos, id, heroes_all_list, 'b', if_change, int(self.bp_sequence[self.pos]))
                if self.pos in red_pick_list:
                    pick_hero(self.pos, id, heroes_all_list, 'r', if_change, int(self.bp_sequence[self.pos]))
                
                blue_picks_ids_current = [self.bp_sequence[i] for i in blue_pick_list if self.bp_sequence[i] != '0']
                red_picks_ids_current = [self.bp_sequence[i] for i in red_pick_list if self.bp_sequence[i] != '0']
                if self.pos in blue_pick_list: blue_picks_ids_current.append(id)
                else: red_picks_ids_current.append(id)
                blue_picks_names = [heroes_all_list[int(h_id)][1] for h_id in blue_picks_ids_current]
                red_picks_names = [heroes_all_list[int(h_id)][1] for h_id in red_picks_ids_current]

                prompt = (f"当前是BP阶段，{team}刚刚选择了[{hero_name}]。"
                          f"目前蓝色方已选：[{'、'.join(blue_picks_names)}]，"
                          f"红色方已选：[{'、'.join(red_picks_names)}]。"
                          f"请对{team}的这一手选择进行一句话的简短专业评述。")
                
                threading.Thread(target=self.call_ai_and_update, args=(prompt,)).start()

            self.bp_sequence[self.pos] = id
            self.pos += 1
            self.show_data_recommendation()
            
            if self.pos < 18:
                self.onChoosePos(None, self.pos)
            else:
                self.final_hero_pos = 1
                self.analyze_btn.Enable()
                self.select_button[-1].colour = wx.Colour(255, 255, 255)
                self.select_button[-1].Refresh()
                self.update_commentary("BP阶段已结束！请点击“分析阵容”获取最终解读。")

            wx.PostEvent(self.select_career_btn_list[self.select_work], self.load_hero_event)
            
        def call_ai_and_update(self, prompt):
            ai_response = doubao_ai.get_ai_commentary(prompt)
            wx.CallAfter(self.update_commentary, f"【AI解说】: {ai_response}")

        def OnAnalyzeClicked(self, event):
            self.update_commentary("\n正在生成最终阵容分析...")
            blue_picks_ids = [self.bp_sequence[i] for i in [4, 7, 8, 15, 16] if self.bp_sequence[i] != '0']
            red_picks_ids = [self.bp_sequence[i] for i in [5, 6, 9, 14, 17] if self.bp_sequence[i] != '0']
            
            blue_hero_names = [heroes_all_list[int(id)][1] for id in blue_picks_ids]
            red_hero_names = [heroes_all_list[int(id)][1] for id in red_picks_ids]

            prompt = (f"请以职业选手的视角，为以下KPL阵容进行50-100字的最终解读和分析。"
                      f"蓝色方阵容: [{', '.join(blue_hero_names)}]。"
                      f"红色方阵容: [{', '.join(red_hero_names)}]。")
            
            threading.Thread(target=self.call_ai_and_update_final, args=(prompt,)).start()
            self.analyze_btn.Disable()

        def show_data_recommendation(self):
            # 1. 解析当前阵容
            blue_pick_idx = [4, 7, 8, 15, 16]
            red_pick_idx = [5, 6, 9, 14, 17]
            
            blue_heroes = [heroes_all_list[int(self.bp_sequence[i])][1] for i in blue_pick_idx if self.bp_sequence[i] != '0']
            red_heroes = [heroes_all_list[int(self.bp_sequence[i])][1] for i in red_pick_idx if self.bp_sequence[i] != '0']
            
            # 2. 判断当前是谁选人
            blue_turns = [4, 7, 8, 15, 16]
            red_turns = [5, 6, 9, 14, 17]
            
            current_idx = self.pos
            if current_idx in blue_turns:
                my_team, enemy_team = blue_heroes, red_heroes
            elif current_idx in red_turns:
                my_team, enemy_team = red_heroes, blue_heroes
            else:
                return # Ban人阶段暂不推荐

            # 3. 获取文本
            analysis_text = self.bp_engine.get_analysis_text(my_team, enemy_team)
            
            # 4. 显示在AI解说框 (使用 AppendText)
            # 加几个换行符让它和上一条消息分开，并且用分隔符醒目显示
            self.ai_commentary.AppendText(f"\n\n------------------------------\n{analysis_text}\n------------------------------")
            self.ai_commentary.ShowPosition(self.ai_commentary.GetLastPosition())

        def call_ai_and_update_final(self, prompt):
            final_comment = doubao_ai.get_ai_commentary(prompt)
            wx.CallAfter(self.update_commentary, f"\n--- 最终阵容分析 ---\n【AI解说】: {final_comment}")

    match_bp_frame = BpFrame()
    match_bp_frame.Show(True)


def pick_hero(bp_pos, hero_id, heroes_all_list, rb, if_change, his_hero_id):
    if his_hero_id != 0:
        if rb == 'b':
            heroes_all_list[his_hero_id][11 + if_change] = '0'
            heroes_all_list[his_hero_id][14] = '0'
        else:
            heroes_all_list[his_hero_id][12 - if_change] = '0'
            heroes_all_list[his_hero_id][14] = '0'
    
    if hero_id != '0':
        hero_id = int(hero_id)
        if rb == 'b':
            heroes_all_list[hero_id][11 + if_change] = '1'
            heroes_all_list[hero_id][14] = '1'
        else:
            heroes_all_list[hero_id][12 - if_change] = '1'
            heroes_all_list[hero_id][14] = '1'


def ban_hero(bp_pos, hero_id, heroes_all_list, his_hero_id):
    if his_hero_id != 0:
        heroes_all_list[his_hero_id][13] = '0'

    if hero_id != '0':
        hero_id = int(hero_id)
        heroes_all_list[hero_id][13] = '1'

bp_pos = 0