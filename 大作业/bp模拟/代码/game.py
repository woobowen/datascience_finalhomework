import copy
import wx
import csv


def load_regular_game_8ban(match_id, team_blue, team_red, heroes_all_list, team1, team2):
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
            dc.DrawRectangle(-4, -4, width, height)

    class BpFrame(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None, title='WBW的BP模拟器')
            self.SetMinSize((1500, 900))
            display_idx = wx.Display.GetFromPoint(wx.GetMousePosition())
            display_rect = wx.Display(display_idx).GetGeometry()
            win_width, win_height = self.GetSize()
            pos_x = display_rect.x + (display_rect.width - win_width) // 2
            pos_y = display_rect.y + (display_rect.height - win_height) // 2
            self.SetPosition((pos_x, pos_y))
            self.career_list = []
            self.final_hero_pos = 0
            self.Center()
            self.pos = 0
            self.bp_sequence = ['0'] * 18
            self.select_work = 0
            self.Maximize(True)
            self.panel = wx.Panel(self)
            
            # 主布局改为水平排列
            self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
            
            # 左侧面板（BP区域）
            left_panel = wx.Panel(self.panel)
            self.pbox = wx.BoxSizer(wx.VERTICAL)
            select_pos_box = wx.BoxSizer()
            button_box = wx.BoxSizer()
            
            next_game_btn = wx.Button(left_panel, label='结束')
            button_box.Add(next_game_btn, 0, flag=wx.CENTER)
            next_game_btn.Bind(wx.EVT_BUTTON, self.OnClickedNext)
            
            bp_board_box = wx.BoxSizer()
            ban_blue_box = wx.BoxSizer()
            ban_red_box = wx.BoxSizer()
            pick_blue_box = wx.BoxSizer()
            pick_red_box = wx.BoxSizer()
            blue_box = wx.BoxSizer(wx.VERTICAL)
            red_box = wx.BoxSizer(wx.VERTICAL)
            
            self.pbox.Add(select_pos_box, 0, flag=wx.ALIGN_CENTER)
            
            # 英雄选择区域的宽度保持600，高度保持550
            self.hero_grid_panel = wx.ScrolledWindow(left_panel, size=(600, 550))
            self.hero_grid_panel.SetScrollRate(5, 20)
            self.hero_grid = wx.GridSizer(20, 5, 2, 2)
            self.hero_grid_panel.SetSizer(self.hero_grid)

            self.career_text_list = []

            with open('heroes\\hero_settings.csv', 'r', newline='') as setting_csv:
                reader = csv.reader(setting_csv)
                for i in reader:
                    self.career_text_list.append(i)
            self.select_career_btn_list = []
            self.select_all_btn = wx.Button(left_panel, label='全部', size=(80, 40))
            select_pos_box.Add(self.select_all_btn, 1, wx.ALIGN_CENTER)
            self.select_career_btn_list.append(self.select_all_btn)
            self.select_all_btn.Bind(wx.EVT_BUTTON,
                                     lambda event, pram1='全部': self.OnClickedSelectCareer(event, pram1))
            btn_num = 0
            for i in self.career_text_list:
                self.select_career_btn = wx.Button(left_panel, label=i[0], size=(80, 40))
                select_pos_box.Add(self.select_career_btn, 1, wx.ALIGN_CENTER)
                self.select_career_btn_list.append(self.select_career_btn)
                self.select_career_btn.Bind(wx.EVT_BUTTON,
                                            lambda event, pram1=i[0]: self.OnClickedSelectCareer(event, pram1))
                btn_num = btn_num + 1
            self.load_hero_event = wx.CommandEvent(wx.EVT_BUTTON.typeId, self.select_career_btn_list[1].GetId())
            wx.PostEvent(self.select_career_btn_list[0], self.load_hero_event)
            self.pbox.Add(self.hero_grid_panel, 1, flag=wx.EXPAND)
            self.pbox.Add(button_box, 0, flag=wx.ALIGN_CENTER)
            self.pbox.Add(bp_board_box, 0, flag=wx.ALIGN_CENTER)
            
            bmp1 = wx.Image('image\\select_ban.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            select1 = SelectButton(left_panel, -1, bmp1)
            select2 = SelectButton(left_panel, -1, bmp1)
            select3 = SelectButton(left_panel, -1, bmp1)
            select4 = SelectButton(left_panel, -1, bmp1)
            select11 = SelectButton(left_panel, -1, bmp1)
            select12 = SelectButton(left_panel, -1, bmp1)
            select13 = SelectButton(left_panel, -1, bmp1)
            select14 = SelectButton(left_panel, -1, bmp1)
            
            team_blue_text = wx.StaticText(left_panel, -1, label=team_blue)
            team_red_text = wx.StaticText(left_panel, -1, label=team_red)
            team_text_font = wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
            team_blue_text.SetFont(team_text_font)
            team_red_text.SetFont(team_text_font)
            
            ban_blue_box.Add(select1, 0, flag=wx.ALIGN_LEFT)
            ban_blue_box.Add(select3, 0, flag=wx.ALIGN_LEFT)
            ban_blue_box.Add(select12, 0, flag=wx.ALIGN_LEFT)
            ban_blue_box.Add(select14, 0, flag=wx.ALIGN_LEFT)
            ban_blue_box.Add(team_blue_text, 0, flag=wx.CENTRE)
            
            ban_red_box.Add(team_red_text, 0, flag=wx.CENTRE)
            ban_red_box.Add(select13, 0, flag=wx.ALIGN_LEFT)
            ban_red_box.Add(select11, 0, flag=wx.ALIGN_LEFT)
            ban_red_box.Add(select4, 0, flag=wx.ALIGN_LEFT)
            ban_red_box.Add(select2, 0, flag=wx.ALIGN_LEFT)
            
            select_pick_bmp = wx.Image('image\\select_pick.png', wx.BITMAP_TYPE_ANY).Scale(110, 110).ConvertToBitmap()
            select5 = SelectButton(left_panel, -1, select_pick_bmp)
            select8 = SelectButton(left_panel, -1, select_pick_bmp)
            select9 = SelectButton(left_panel, -1, select_pick_bmp)
            select16 = SelectButton(left_panel, -1, select_pick_bmp)
            select17 = SelectButton(left_panel, -1, select_pick_bmp)
            select6 = SelectButton(left_panel, -1, select_pick_bmp)
            select7 = SelectButton(left_panel, -1, select_pick_bmp)
            select10 = SelectButton(left_panel, -1, select_pick_bmp)
            select15 = SelectButton(left_panel, -1, select_pick_bmp)
            select18 = SelectButton(left_panel, -1, select_pick_bmp)
            
            self.select_button = [select1, select2, select3, select4, select5, select6, select7, select8, select9,
                                  select10, select11, select12, select13, select14, select15, select16, select17,
                                  select18]
            
            select1.Bind(wx.EVT_BUTTON, lambda event, pram1=0: self.onChoosePos(event, pram1))
            select2.Bind(wx.EVT_BUTTON, lambda event, pram1=1: self.onChoosePos(event, pram1))
            select3.Bind(wx.EVT_BUTTON, lambda event, pram1=2: self.onChoosePos(event, pram1))
            select4.Bind(wx.EVT_BUTTON, lambda event, pram1=3: self.onChoosePos(event, pram1))
            select5.Bind(wx.EVT_BUTTON, lambda event, pram1=4: self.onChoosePos(event, pram1))
            select6.Bind(wx.EVT_BUTTON, lambda event, pram1=5: self.onChoosePos(event, pram1))
            select7.Bind(wx.EVT_BUTTON, lambda event, pram1=6: self.onChoosePos(event, pram1))
            select8.Bind(wx.EVT_BUTTON, lambda event, pram1=7: self.onChoosePos(event, pram1))
            select9.Bind(wx.EVT_BUTTON, lambda event, pram1=8: self.onChoosePos(event, pram1))
            select10.Bind(wx.EVT_BUTTON, lambda event, pram1=9: self.onChoosePos(event, pram1))
            select11.Bind(wx.EVT_BUTTON, lambda event, pram1=10: self.onChoosePos(event, pram1))
            select12.Bind(wx.EVT_BUTTON, lambda event, pram1=11: self.onChoosePos(event, pram1))
            select13.Bind(wx.EVT_BUTTON, lambda event, pram1=12: self.onChoosePos(event, pram1))
            select14.Bind(wx.EVT_BUTTON, lambda event, pram1=13: self.onChoosePos(event, pram1))
            select15.Bind(wx.EVT_BUTTON, lambda event, pram1=14: self.onChoosePos(event, pram1))
            select16.Bind(wx.EVT_BUTTON, lambda event, pram1=15: self.onChoosePos(event, pram1))
            select17.Bind(wx.EVT_BUTTON, lambda event, pram1=16: self.onChoosePos(event, pram1))
            select18.Bind(wx.EVT_BUTTON, lambda event, pram1=17: self.onChoosePos(event, pram1))
            
            pick_blue_box.Add(select5, 0, flag=wx.ALIGN_LEFT)
            pick_blue_box.Add(select8, 0, flag=wx.ALIGN_LEFT)
            pick_blue_box.Add(select9, 0, flag=wx.ALIGN_LEFT)
            pick_blue_box.Add(select16, 0, flag=wx.ALIGN_LEFT)
            pick_blue_box.Add(select17, 0, flag=wx.ALIGN_LEFT)
            
            pick_red_box.Add(select18, 0, flag=wx.ALIGN_LEFT)
            pick_red_box.Add(select15, 0, flag=wx.ALIGN_LEFT)
            pick_red_box.Add(select10, 0, flag=wx.ALIGN_LEFT)
            pick_red_box.Add(select7, 0, flag=wx.ALIGN_LEFT)
            pick_red_box.Add(select6, 0, flag=wx.ALIGN_LEFT)
            
            blue_box.Add(ban_blue_box, 0, flag=wx.ALIGN_LEFT)
            blue_box.Add(pick_blue_box, 0, flag=wx.ALIGN_LEFT)
            red_box.Add(ban_red_box, 0, flag=wx.ALIGN_RIGHT)
            red_box.Add(pick_red_box, 0, flag=wx.ALIGN_RIGHT)
            
            bp_board_box.Add(blue_box, 0)
            bp_board_box.Add((100, 0), 0, wx.EXPAND)
            bp_board_box.Add(red_box, 0)
            left_panel.SetSizer(self.pbox)
            
            # 右侧面板（AI解说区域）
            # 主要修改点在这里：给 right_panel 设置一个固定的最小高度
            right_panel = wx.Panel(self.panel, size=(420, 600)) # 调整尺寸，特别是高度，留一些余量给标题和边距
            right_sizer = wx.BoxSizer(wx.VERTICAL)

            # AI解说标题
            ai_title = wx.StaticText(right_panel, label="AI解说")
            title_font = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD)
            ai_title.SetFont(title_font)
            right_sizer.Add(ai_title, 0, wx.ALIGN_CENTER | wx.TOP, 10)

            # 解说内容文本框 - 精确设置高度
            # 这里的 size 应该计算为 right_panel 的高度减去标题高度和边距
            # 大致估算: 600 (panel高度) - 10 (top margin) - 20 (title font size approx) - 10 (bottom margin) = ~560
            self.ai_commentary = wx.TextCtrl(right_panel, 
                                            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL,
                                            size=(400, 560)) # 根据 right_panel 的高度调整TextCtrl的高度
            commentary_font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
            self.ai_commentary.SetFont(commentary_font)
            # TextCtrl 使用 proportion=1 和 wx.EXPAND，让它填充 right_panel 剩余的高度
            right_sizer.Add(self.ai_commentary, 1, wx.EXPAND | wx.ALL, 10)

            # 初始解说内容
            self.update_commentary("欢迎使用WBW的BP模拟器！\nAI解说将为您分析双方的BP策略。")

            right_panel.SetSizer(right_sizer) # 移除 SetSizerAndFit，只用 SetSizer

            # 将左右面板添加到主布局
            # right_panel 的 proportion 设为 0，防止 main_sizer 对其进行拉伸
            self.main_sizer.Add(left_panel, 1, wx.EXPAND)
            self.main_sizer.Add(right_panel, 0, wx.EXPAND | wx.TOP | wx.RIGHT | wx.BOTTOM, 10) # 保持右侧面板的宽度固定，高度固定
            self.panel.SetSizer(self.main_sizer)

        def update_commentary(self, text):
            """更新AI解说内容"""
            current_text = self.ai_commentary.GetValue()
            if current_text:
                self.ai_commentary.SetValue(current_text + "\n\n" + text)
            else:
                self.ai_commentary.SetValue(text)
            # 滚动到底部
            self.ai_commentary.ShowPosition(self.ai_commentary.GetLastPosition())

        def OnClickedSelectCareer(self, event, career):
            buttons = []
            blue_select_list = [1, 3, 4, 7, 8, 10, 12, 15, 16]
            red_select_list = [0, 2, 5, 6, 9, 11, 13, 14, 17]
            if team_blue == team1:
                team1_num = 11
                team2_num = 12
            else:
                team1_num = 12
                team2_num = 11
            for item in self.hero_grid.GetChildren():
                item.GetWindow().Destroy()
            self.career_list = []
            select_pick_bmp = wx.Image('image\\select_pick.png', wx.BITMAP_TYPE_ANY).Scale(110, 110).ConvertToBitmap()
            buttons.append(wx.BitmapButton(self.hero_grid_panel, -1, select_pick_bmp))
            self.hero_grid.Add(buttons[0], 1, wx.EXPAND)

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

            for hero_career in self.career_list:
                if hero_career != '':
                    hero = heroes_all_list[int(hero_career)]
                    if hero[0] in self.career_list and hero[0] != '':
                        if hero[team1_num] == '0' and hero[13] == '0' and hero[
                            14] == '0' and self.pos in blue_select_list:
                            select_pick_bmp = wx.Image('heroes\\icon\\' + hero[0] + '.jpg',
                                                       wx.BITMAP_TYPE_ANY).Scale(110, 110).ConvertToBitmap()
                            buttons.append(wx.BitmapButton(self.hero_grid_panel, -1, select_pick_bmp))
                            self.hero_grid.Add(buttons[-1], 1, wx.EXPAND)
                            buttons[-1].Bind(wx.EVT_BUTTON,
                                             lambda event, pram1=hero[0]: self.onClickSelect(event, pram1))
                            buttons[0].Bind(wx.EVT_BUTTON,
                                            lambda event, pram1='0': self.onClickSelect(event, pram1))
                        elif hero[team2_num] == '0' and hero[13] == '0' and hero[
                            14] == '0' and self.pos in red_select_list:
                            select_pick_bmp = wx.Image('heroes\\icon\\' + hero[0] + '.jpg',
                                                       wx.BITMAP_TYPE_ANY).Scale(110, 110).ConvertToBitmap()
                            buttons.append(wx.BitmapButton(self.hero_grid_panel, -1, select_pick_bmp))
                            self.hero_grid.Add(buttons[-1], 1, wx.EXPAND)
                            buttons[-1].Bind(wx.EVT_BUTTON,
                                             lambda event, pram1=hero[0]: self.onClickSelect(event, pram1))
                            buttons[0].Bind(wx.EVT_BUTTON,
                                            lambda event, pram1='0': self.onClickSelect(event, pram1))
                        else:
                            select_pick_bmp = wx.Image('heroes\\icon\\' + hero[0] + '.jpg',
                                                       wx.BITMAP_TYPE_ANY).ConvertToGreyscale().Scale(110,
                                                                                                      110).ConvertToBitmap()
                            buttons.append(wx.BitmapButton(self.hero_grid_panel, -1, select_pick_bmp))
                            self.hero_grid.Add(buttons[-1], 1, wx.EXPAND)
                        if hero[team1_num] == '1' and hero[team2_num] == '0':
                            buttons[-1].SetBackgroundColour(wx.Colour(98, 210, 227))
                        if hero[team2_num] == '1' and hero[team1_num] == '0':
                            buttons[-1].SetBackgroundColour(wx.Colour(232, 172, 172))
                        if hero[12] == '1' and hero[11] == '1':
                            buttons[-1].SetBackgroundColour(wx.Colour(161, 161, 161))
            self.panel.Layout()

        def onChoosePos(self, event, i):
            self.pos = i
            for j in self.select_button:
                if j == self.select_button[i]:
                    j.colour = wx.Colour(255, 0, 0)
                else:
                    j.colour = wx.Colour(255, 255, 255)
            wx.PostEvent(self.select_career_btn_list[self.select_work], self.load_hero_event)
            self.Refresh()
            
            # 更新AI解说
            if i < 4:
                phase = "第一阶段禁用"
            elif i < 8:
                phase = "第一阶段选用"
            elif i < 12:
                phase = "第二阶段禁用"
            elif i < 18:
                phase = "第二阶段选用"
            
            team = "蓝色方" if i in [0, 2, 4, 7, 8, 15, 16] else "红色方"
            self.update_commentary(f"当前BP阶段: {phase}\n当前操作方: {team}\n请选择英雄...")

        def OnClickedNext(self, event):
            if self.final_hero_pos == 1:
                save_list = [[match_id, '1', '1', team_blue, team_red, '8ban']]
                save_list[0].extend(self.bp_sequence)
                with open('save\\save.csv', mode='w', newline='') as file:
                    writer = csv.writer(file)
                    for i in save_list:
                        writer.writerow(i)
                self.Close()
            else:
                mgb = wx.MessageBox('对局尚未结束！', '提示', wx.OK | wx.ICON_INFORMATION)

        def onClickSelect(self, event, id):
            ban_list = [0, 1, 2, 3, 10, 11, 12, 13]
            blue_pick_list = [4, 7, 8, 15, 16]
            red_pick_list = [5, 6, 9, 14, 17]
            
            # 获取英雄名称用于解说
            hero_name = "空Ban" if id == '0' else heroes_all_list[int(id)][1] if id.isdigit() else id
            
            if self.pos == 17:
                self.final_hero_pos = 1
                
            if self.pos in ban_list:
                action = "禁用了"
                # 更新AI解说
                team = "蓝色方" if self.pos in [0, 2, 10, 12] else "红色方"
                self.update_commentary(f"{team} {action} [{hero_name}]")
                
                if id == '0':
                    select_pick_bmp = wx.Image('image\\select_ban.png',
                                               wx.BITMAP_TYPE_ANY).ConvertToGreyscale().Scale(70, 70).ConvertToBitmap()
                else:
                    select_pick_bmp = wx.Image('heroes\\icon\\' + id + '.jpg',
                                               wx.BITMAP_TYPE_ANY).ConvertToGreyscale().Scale(70, 70).ConvertToBitmap()
                ban_hero(self.pos, id, heroes_all_list, int(self.bp_sequence[self.pos]))
                self.select_button[self.pos].SetBitmap(select_pick_bmp)
                self.bp_sequence[self.pos] = id
                self.pos = self.pos + 1

            else:
                action = "选择了"
                # 更新AI解说
                team = "蓝色方" if self.pos in blue_pick_list else "红色方"
                self.update_commentary(f"{team} {action} [{hero_name}]")
                
                select_pick_bmp = wx.Image('heroes\\icon\\' + id + '.jpg',
                                           wx.BITMAP_TYPE_ANY).Scale(110, 110).ConvertToBitmap()

                if team1 == team_blue:
                    if_change = 0
                else:
                    if_change = 1

                if self.pos in blue_pick_list:
                    pick_hero(self.pos, id, heroes_all_list, 'b', if_change, int(self.bp_sequence[self.pos]))
                if self.pos in red_pick_list:
                    pick_hero(self.pos, id, heroes_all_list, 'r', if_change, int(self.bp_sequence[self.pos]))

                self.select_button[self.pos].SetBitmap(select_pick_bmp)
                self.bp_sequence[self.pos] = id
                self.pos = self.pos + 1
                
                # 分析阵容
                if self.pos in [8, 18]: # 第一阶段和第二阶段选完时
                    self.analyze_composition()
            
            if self.pos != 18:
                choose_pos_event = wx.CommandEvent(wx.EVT_BUTTON.typeId, self.select_button[self.pos].GetId())
                wx.PostEvent(self.select_button[self.pos], choose_pos_event)
            else:
                self.select_button[-1].colour = wx.Colour(255, 255, 255)
                self.update_commentary("BP阶段已结束！\n比赛即将开始...")
            wx.PostEvent(self.select_career_btn_list[self.select_work], self.load_hero_event)
        
        def analyze_composition(self):
            """分析当前阵容"""
            blue_picks = [self.bp_sequence[i] for i in [4,7,8,15,16] if self.bp_sequence[i] != '0']
            red_picks = [self.bp_sequence[i] for i in [5,6,9,14,17] if self.bp_sequence[i] != '0']
            
            if len(blue_picks) > 0 or len(red_picks) > 0:
                analysis = "\n阵容分析:\n"
                
                if len(blue_picks) > 0:
                    blue_hero_names = [heroes_all_list[int(id)][1] for id in blue_picks]
                    analysis += f"蓝色方阵容: {', '.join(blue_hero_names)}\n"
                
                if len(red_picks) > 0:
                    red_hero_names = [heroes_all_list[int(id)][1] for id in red_picks]
                    analysis += f"红色方阵容: {', '.join(red_hero_names)}\n"
                
                # 这里可以添加更复杂的阵容分析逻辑
                if len(blue_picks) >= 3:
                    analysis += "蓝色方已选择3个英雄，阵容开始成型。\n"
                if len(red_picks) >= 3:
                    analysis += "红色方已选择3个英雄，阵容开始成型。\n"
                
                self.update_commentary(analysis)

    match_bp_frame = BpFrame()
    match_bp_frame.Show(True)


def pick_hero(bp_pos, hero_id, heroes_all_list, rb, if_change, his_hero_id):
    if id != '0':
        hero_id = int(hero_id)
        if rb == 'b':
            heroes_all_list[his_hero_id][11 + if_change] = '0'
            heroes_all_list[his_hero_id][14] = '0'
            heroes_all_list[hero_id][11 + if_change] = '1'
            heroes_all_list[hero_id][14] = '1'
        else:
            heroes_all_list[his_hero_id][12 + if_change] = '0'
            heroes_all_list[his_hero_id][14] = '0'
            heroes_all_list[hero_id][12 - if_change] = '1'
            heroes_all_list[hero_id][14] = '1'


def ban_hero(bp_pos, hero_id, heroes_all_list, his_hero_id):
    if id != '0':
        hero_id = int(hero_id)
        heroes_all_list[his_hero_id][13] = '0'
        heroes_all_list[hero_id][13] = '1'


bp_pos = 0