import copy
import wx
import csv


def load_regular_game_8ban(match_id, team_blue, team_red, game_num, heroes_all_list, max_game_num, team1, team2,
                           history_inf):
    class HistoryInf(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None,
                              title='WBW的BP模拟器【历史阵容】', size=(1500, 900))
            display_idx = wx.Display.GetFromPoint(wx.GetMousePosition())
            # 获取该屏幕的几何信息（x, y, width, height）
            display_rect = wx.Display(display_idx).GetGeometry()
            win_width, win_height = self.GetSize()
            pos_x = display_rect.x + (display_rect.width - win_width) // 2
            pos_y = display_rect.y + (display_rect.height - win_height) // 2
            self.SetPosition((pos_x, pos_y))  # 设置窗口位置
            self.final_hero_pos = 0
            self.Center()
            self.panel = wx.Panel(self)
            self.pbox = wx.BoxSizer(wx.VERTICAL)
            show_heroes_ban_blue_list = [0, 2, 11, 13]
            show_heroes_ban_red_list = [12, 10, 3, 1]
            show_heroes_pick_blue_list = [4, 7, 8, 15, 16]
            show_heroes_pick_red_list = [17, 14, 9, 6, 5]
            for i in range(game_num - 1):
                game_box = wx.BoxSizer(wx.HORIZONTAL)
                self.pbox.Add(game_box, 1, wx.Center)
                blue_box = wx.BoxSizer(wx.VERTICAL)
                red_box = wx.BoxSizer(wx.VERTICAL)
                game_box.Add(blue_box, 0, wx.Center)
                game_box.Add((300, 0), 1, wx.EXPAND, 0)
                game_box.Add(red_box, 0, wx.Center)
                blue_ban_box = wx.BoxSizer(wx.HORIZONTAL)
                blue_pick_box = wx.BoxSizer(wx.HORIZONTAL)
                red_ban_box = wx.BoxSizer(wx.HORIZONTAL)
                red_pick_box = wx.BoxSizer(wx.HORIZONTAL)
                blue_box.Add(blue_ban_box, 0)
                blue_box.Add(blue_pick_box, 0)
                red_box.Add(red_ban_box, 0, flag=wx.ALIGN_RIGHT)
                red_box.Add(red_pick_box, 0, flag=wx.ALIGN_RIGHT)
                team_blue_text = wx.StaticText(self.panel, -1, label=history_inf[i][0])
                team_red_text = wx.StaticText(self.panel, -1, label=history_inf[i][1])
                red_ban_box.Add(team_red_text, 0, flag=wx.CENTRE)
                for j in show_heroes_ban_blue_list:
                    self.bmp = wx.Image('heroes\\icon\\' + history_inf[i][j + 3] + '.jpg',
                                        wx.BITMAP_TYPE_ANY).ConvertToGreyscale().Scale(70, 70).ConvertToBitmap()
                    self.bitmap = wx.StaticBitmap(self.panel, wx.ID_ANY, self.bmp)
                    blue_ban_box.Add(self.bitmap, 1)
                for j in show_heroes_pick_blue_list:
                    self.bmp = wx.Image('heroes\\icon\\' + history_inf[i][j + 3] + '.jpg',
                                        wx.BITMAP_TYPE_ANY).Scale(110, 110).ConvertToBitmap()
                    self.bitmap = wx.StaticBitmap(self.panel, wx.ID_ANY, self.bmp)
                    blue_pick_box.Add(self.bitmap, 1)
                for j in show_heroes_ban_red_list:
                    self.bmp = wx.Image('heroes\\icon\\' + history_inf[i][j + 3] + '.jpg',
                                        wx.BITMAP_TYPE_ANY).ConvertToGreyscale().Scale(70, 70).ConvertToBitmap()
                    self.bitmap = wx.StaticBitmap(self.panel, wx.ID_ANY, self.bmp)
                    red_ban_box.Add(self.bitmap, 1)
                for j in show_heroes_pick_red_list:
                    self.bmp = wx.Image('heroes\\icon\\' + history_inf[i][j + 3] + '.jpg',
                                        wx.BITMAP_TYPE_ANY).Scale(110, 110).ConvertToBitmap()
                    self.bitmap = wx.StaticBitmap(self.panel, wx.ID_ANY, self.bmp)
                    red_pick_box.Add(self.bitmap, 1)
                blue_ban_box.Add(team_blue_text, 0, flag=wx.CENTRE)
                self.panel.SetSizer(self.pbox)

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
            # 设置边框颜色和宽度
            border_color = self.colour  # 边框
            dc.SetPen(wx.Pen(border_color, 1))  # 设置边框颜色和宽度
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            # 绘制一个矩形边框
            width, height = self.GetSize()
            dc.DrawRectangle(-4, -4, width, height)

    class BpFrame(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None,
                              title='WBW的BP模拟器【BO' + str(max_game_num) + '第' + str(game_num) + '局】')
            self.SetMinSize((1500, 900))
            display_idx = wx.Display.GetFromPoint(wx.GetMousePosition())
            # 获取该屏幕的几何信息（x, y, width, height）
            display_rect = wx.Display(display_idx).GetGeometry()
            win_width, win_height = self.GetSize()
            pos_x = display_rect.x + (display_rect.width - win_width) // 2
            pos_y = display_rect.y + (display_rect.height - win_height) // 2
            self.SetPosition((pos_x, pos_y))  # 设置窗口位置
            self.career_list = []
            self.final_hero_pos = 0
            self.Center()
            self.pos = 0
            self.bp_sequence = ['0'] * 18
            self.select_work = 0
            self.Maximize(True)
            self.panel = wx.Panel(self)
            self.pbox = wx.BoxSizer(wx.VERTICAL)
            select_pos_box = wx.BoxSizer()
            button_box = wx.BoxSizer()
            view_history_game_btn = wx.Button(self.panel, label='显示历史阵容')
            view_history_game_btn.Bind(wx.EVT_BUTTON, self.onClickViewHistory)
            # self.resize_panel_btn = wx.Button(self.panel, label='适应面板大小')
            # self.resize_panel_btn.Bind(wx.EVT_BUTTON, self.OnClickedResize)
            if game_num != max_game_num:
                next_game_btn = wx.Button(self.panel, label='下一局')
            else:
                next_game_btn = wx.Button(self.panel, label='结束')
            button_box.Add(next_game_btn, 0, flag=wx.CENTER)
            next_game_btn.Bind(wx.EVT_BUTTON, self.OnClickedNext)
            button_box.Add(view_history_game_btn, 0, flag=wx.CENTER)
            # button_box.Add(self.resize_panel_btn, 0, flag=wx.CENTER)
            bp_board_box = wx.BoxSizer()
            ban_blue_box = wx.BoxSizer()
            ban_red_box = wx.BoxSizer()
            pick_blue_box = wx.BoxSizer()
            pick_red_box = wx.BoxSizer()
            blue_box = wx.BoxSizer(wx.VERTICAL)
            red_box = wx.BoxSizer(wx.VERTICAL)
            self.pbox.Add(select_pos_box, 0, flag=wx.ALIGN_CENTER)
            self.hero_grid_panel = wx.ScrolledWindow(self.panel, size=(900, 550))
            self.hero_grid_panel.SetScrollRate(5, 20)
            self.hero_grid = wx.GridSizer(20, 7, 2, 2)
            self.hero_grid_panel.SetSizer(self.hero_grid)

            self.career_text_list = []

            with open('heroes\\hero_settings.csv', 'r', newline='') as setting_csv:
                reader = csv.reader(setting_csv)
                for i in reader:
                    self.career_text_list.append(i)
            self.select_career_btn_list = []
            self.select_all_btn = wx.Button(self.panel, label='全部', size=(100, 50))
            select_pos_box.Add(self.select_all_btn, 1, wx.ALIGN_CENTER)
            self.select_career_btn_list.append(self.select_all_btn)
            self.select_all_btn.Bind(wx.EVT_BUTTON,
                                     lambda event, pram1='全部': self.OnClickedSelectCareer(event, pram1))
            btn_num = 0
            for i in self.career_text_list:
                self.select_career_btn = wx.Button(self.panel, label=i[0], size=(100, 50))
                select_pos_box.Add(self.select_career_btn, 1, wx.ALIGN_CENTER)
                self.select_career_btn_list.append(self.select_career_btn)
                self.select_career_btn.Bind(wx.EVT_BUTTON,
                                            lambda event, pram1=i[0]: self.OnClickedSelectCareer(event, pram1))
                btn_num = btn_num + 1
            self.load_hero_event = wx.CommandEvent(wx.EVT_BUTTON.typeId, self.select_career_btn_list[1].GetId())
            wx.PostEvent(self.select_career_btn_list[0], self.load_hero_event)
            self.pbox.Add(self.hero_grid_panel, 1, flag=wx.EXPAND)
            # self.pbox.Add((0, 1), 1, wx.EXPAND, 0)
            self.pbox.Add(button_box, 0, flag=wx.ALIGN_CENTER)
            self.pbox.Add(bp_board_box, 0, flag=wx.ALIGN_CENTER)
            bmp1 = wx.Image('image\\select_ban.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            select1 = SelectButton(self.panel, -1, bmp1)
            select2 = SelectButton(self.panel, -1, bmp1)
            select3 = SelectButton(self.panel, -1, bmp1)
            select4 = SelectButton(self.panel, -1, bmp1)
            select11 = SelectButton(self.panel, -1, bmp1)
            select12 = SelectButton(self.panel, -1, bmp1)
            select13 = SelectButton(self.panel, -1, bmp1)
            select14 = SelectButton(self.panel, -1, bmp1)
            team_blue_text = wx.StaticText(self.panel, -1, label=team_blue)
            team_red_text = wx.StaticText(self.panel, -1, label=team_red)
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
            select5 = SelectButton(self.panel, -1, select_pick_bmp)
            select8 = SelectButton(self.panel, -1, select_pick_bmp)
            select9 = SelectButton(self.panel, -1, select_pick_bmp)
            select16 = SelectButton(self.panel, -1, select_pick_bmp)
            select17 = SelectButton(self.panel, -1, select_pick_bmp)
            select6 = SelectButton(self.panel, -1, select_pick_bmp)
            select7 = SelectButton(self.panel, -1, select_pick_bmp)
            select10 = SelectButton(self.panel, -1, select_pick_bmp)
            select15 = SelectButton(self.panel, -1, select_pick_bmp)
            select18 = SelectButton(self.panel, -1, select_pick_bmp)
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
            # self.timeboard=wx.tex
            bp_board_box.Add(blue_box, 0)
            bp_board_box.Add((100, 0), 0, wx.EXPAND)
            bp_board_box.Add(red_box, 0)
            self.panel.SetSizer(self.pbox)

        # def OnClickedResize(self, event):
        #     width, height = self.GetSize()
        #     self.hero_grid_panel.SetSize(width - 25, height - 300)

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
                item.GetWindow().Destroy()  # 删除每个控件
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
            # resize_hero_event = wx.CommandEvent(wx.EVT_BUTTON.typeId, self.resize_panel_btn.GetId())
            # wx.PostEvent(self.resize_panel_btn, resize_hero_event)
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

        def onClickViewHistory(self, event):
            history_inf_frame = HistoryInf()
            history_inf_frame.Show()

        def OnClickedNext(self, event):
            if self.final_hero_pos == 1:
                save_list = [[match_id, str(max_game_num), str(game_num), team_blue, team_red, '8ban']]
                save_list[0].extend(self.bp_sequence)
                with open('save\\save.csv', mode='r') as read_file:
                    reader = csv.reader(read_file)
                    for row in reader:
                        save_list.append(row)
                with open('save\\save.csv', mode='w', newline='') as file:
                    writer = csv.writer(file)
                    for i in save_list:
                        writer.writerow(i)
                new_list = ([team_blue, team_red, '8ban'])
                new_list.extend(self.bp_sequence)
                history_inf.append(new_list)
                next_game = NextGame()
                next_game.Show()
                self.Close()
            else:
                mgb = wx.MessageBox('对局尚未结束！', '提示', wx.OK | wx.ICON_INFORMATION)

        def onClickSelect(self, event, id):
            ban_list = [0, 1, 2, 3, 10, 11, 12, 13]
            blue_pick_list = [4, 7, 8, 15, 16]
            red_pick_list = [5, 6, 9, 14, 17]
            if self.pos == 17:
                self.final_hero_pos = 1
            if self.pos in ban_list:
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
            if self.pos != 18:
                choose_pos_event = wx.CommandEvent(wx.EVT_BUTTON.typeId, self.select_button[self.pos].GetId())
                wx.PostEvent(self.select_button[self.pos], choose_pos_event)
            else:
                self.select_button[-1].colour = wx.Colour(255, 255, 255)
            wx.PostEvent(self.select_career_btn_list[self.select_work], self.load_hero_event)

    class NextGame(wx.Frame):
        def __init__(self):
            if game_num != max_game_num:
                wx.Frame.__init__(self, None, title='下一局', size=(200, 200))
                self.Center()
                self.panel = wx.Panel(self)
                vbox = wx.BoxSizer(wx.VERTICAL)
                choices_list = ['是', '否']
                choices_list2 = ['否', '是']
                self.change_box = wx.RadioBox(self.panel, label='是否换边', choices=choices_list)
                self.normal_box = wx.RadioBox(self.panel, label='巅峰对决', choices=choices_list2)
                ok_button = wx.Button(self.panel, label='确认')
                vbox.Add(self.change_box, 0, wx.ALIGN_CENTER)
                vbox.Add(self.normal_box, 0, wx.ALIGN_CENTER)
                vbox.Add(ok_button, 0, wx.ALIGN_CENTER)
                ok_button.Bind(wx.EVT_BUTTON, self.onNextGame)
            else:
                wx.Frame.__init__(self, None, title='提醒', size=(210, 80))
                self.Center()
                self.panel = wx.Panel(self)
                vbox = wx.BoxSizer(wx.VERTICAL)
                exit_confirm_txt = wx.StaticText(self.panel, label='比赛结束')
                ok_button = wx.Button(self.panel, label='确认')
                vbox.Add(exit_confirm_txt, 0, wx.ALIGN_CENTER)
                vbox.Add(ok_button, 0, wx.ALIGN_CENTER)
                ok_button.Bind(wx.EVT_BUTTON, self.onExit)
            display_idx = wx.Display.GetFromPoint(wx.GetMousePosition())
            # 获取该屏幕的几何信息（x, y, width, height）
            display_rect = wx.Display(display_idx).GetGeometry()
            win_width, win_height = self.GetSize()
            pos_x = display_rect.x + (display_rect.width - win_width) // 2
            pos_y = display_rect.y + (display_rect.height - win_height) // 2
            self.SetPosition((pos_x, pos_y))  # 设置窗口位置
            self.panel.SetSizer(vbox)

        def onExit(self, event):
            self.Close()

        def onNextGame(self, event):
            if self.change_box.GetSelection() == 0:
                team_b = team_red
                team_r = team_blue
            else:
                team_r = team_red
                team_b = team_blue
            for hero in heroes_all_list:
                hero[13] = '0'
                hero[14] = '0'
            if self.normal_box.GetSelection() == 0:
                game_mode_next = 1
            else:
                game_mode_next = 0
            self.Close()
            load_game(match_id, game_mode_next, 8, team_b, team_r, game_num + 1, heroes_all_list,
                      max_game_num, team1, team2, history_inf)

    match_bp_frame = BpFrame()
    match_bp_frame.Show(True)


def load_regular_game_10ban(match_id, team_blue, team_red, game_num, heroes_all_list, max_game_num, team1, team2,
                            history_inf):
    class HistoryInf(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None,
                              title='WBW的BP模拟器【历史阵容】', size=(1500, 900))

            display_idx = wx.Display.GetFromPoint(wx.GetMousePosition())
            # 获取该屏幕的几何信息（x, y, width, height）
            display_rect = wx.Display(display_idx).GetGeometry()
            win_width, win_height = self.GetSize()
            pos_x = display_rect.x + (display_rect.width - win_width) // 2
            pos_y = display_rect.y + (display_rect.height - win_height) // 2
            self.SetPosition((pos_x, pos_y))  # 设置窗口位置
            self.final_hero_pos = 0
            self.Center()
            self.panel = wx.Panel(self)
            self.pbox = wx.BoxSizer(wx.VERTICAL)
            show_heroes_ban_blue_list = [0, 2, 11, 13, 15]
            show_heroes_ban_red_list = [14, 12, 10, 3, 1]
            show_heroes_pick_blue_list = [4, 7, 8, 17, 18]
            show_heroes_pick_red_list = [19, 16, 9, 6, 5]
            for i in range(game_num - 1):
                game_box = wx.BoxSizer(wx.HORIZONTAL)
                self.pbox.Add(game_box, 1, wx.Center)
                blue_box = wx.BoxSizer(wx.VERTICAL)
                red_box = wx.BoxSizer(wx.VERTICAL)
                game_box.Add(blue_box, 0, wx.Center)
                game_box.Add((300, 0), 1, wx.EXPAND, 0)
                game_box.Add(red_box, 0, wx.Center)
                blue_ban_box = wx.BoxSizer(wx.HORIZONTAL)
                blue_pick_box = wx.BoxSizer(wx.HORIZONTAL)
                red_ban_box = wx.BoxSizer(wx.HORIZONTAL)
                red_pick_box = wx.BoxSizer(wx.HORIZONTAL)
                blue_box.Add(blue_ban_box, 0)
                blue_box.Add(blue_pick_box, 0)
                red_box.Add(red_ban_box, 0, flag=wx.ALIGN_RIGHT)
                red_box.Add(red_pick_box, 0, flag=wx.ALIGN_RIGHT)
                team_blue_text = wx.StaticText(self.panel, -1, label=history_inf[i][0])
                team_red_text = wx.StaticText(self.panel, -1, label=history_inf[i][1])
                red_ban_box.Add(team_red_text, 0, flag=wx.CENTRE)
                for j in show_heroes_ban_blue_list:
                    self.bmp = wx.Image('heroes\\icon\\' + history_inf[i][j + 3] + '.jpg',
                                        wx.BITMAP_TYPE_ANY).ConvertToGreyscale().Scale(70, 70).ConvertToBitmap()
                    self.bitmap = wx.StaticBitmap(self.panel, wx.ID_ANY, self.bmp)
                    blue_ban_box.Add(self.bitmap, 1)

                for j in show_heroes_pick_blue_list:
                    self.bmp = wx.Image('heroes\\icon\\' + history_inf[i][j + 3] + '.jpg',
                                        wx.BITMAP_TYPE_ANY).Scale(110, 110).ConvertToBitmap()
                    self.bitmap = wx.StaticBitmap(self.panel, wx.ID_ANY, self.bmp)
                    blue_pick_box.Add(self.bitmap, 1)
                for j in show_heroes_ban_red_list:
                    self.bmp = wx.Image('heroes\\icon\\' + history_inf[i][j + 3] + '.jpg',
                                        wx.BITMAP_TYPE_ANY).ConvertToGreyscale().Scale(70, 70).ConvertToBitmap()
                    self.bitmap = wx.StaticBitmap(self.panel, wx.ID_ANY, self.bmp)
                    red_ban_box.Add(self.bitmap, 1)
                for j in show_heroes_pick_red_list:
                    self.bmp = wx.Image('heroes\\icon\\' + history_inf[i][j + 3] + '.jpg',
                                        wx.BITMAP_TYPE_ANY).Scale(110, 110).ConvertToBitmap()
                    self.bitmap = wx.StaticBitmap(self.panel, wx.ID_ANY, self.bmp)
                    red_pick_box.Add(self.bitmap, 1)
                blue_ban_box.Add(team_blue_text, 0, flag=wx.CENTRE)
                self.panel.SetSizer(self.pbox)

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
            # 设置边框颜色和宽度
            border_color = self.colour  # 边框
            dc.SetPen(wx.Pen(border_color, 1))  # 设置边框颜色和宽度
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            # 绘制一个矩形边框
            width, height = self.GetSize()
            dc.DrawRectangle(-4, -4, width, height)

    class BpFrame(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None,
                              title='WBW的BP模拟器【BO' + str(max_game_num) + '第' + str(game_num) + '局】')

            self.SetMinSize((1500, 900))
            display_idx = wx.Display.GetFromPoint(wx.GetMousePosition())
            # 获取该屏幕的几何信息（x, y, width, height）
            display_rect = wx.Display(display_idx).GetGeometry()
            win_width, win_height = self.GetSize()
            pos_x = display_rect.x + (display_rect.width - win_width) // 2
            pos_y = display_rect.y + (display_rect.height - win_height) // 2
            self.SetPosition((pos_x, pos_y))  # 设置窗口位置
            self.career_list = []
            self.final_hero_pos = 0
            self.Center()
            self.pos = 0
            self.bp_sequence = ['0'] * 20
            self.select_work = 0
            self.Maximize(True)
            self.panel = wx.Panel(self)
            self.pbox = wx.BoxSizer(wx.VERTICAL)
            select_pos_box = wx.BoxSizer()
            button_box = wx.BoxSizer()
            view_history_game_btn = wx.Button(self.panel, label='显示历史阵容')
            view_history_game_btn.Bind(wx.EVT_BUTTON, self.onClickViewHistory)
            # self.resize_panel_btn = wx.Button(self.panel, label='适应面板大小')
            # self.resize_panel_btn.Bind(wx.EVT_BUTTON, self.OnClickedResize)
            if game_num != max_game_num:
                next_game_btn = wx.Button(self.panel, label='下一局')
            else:
                next_game_btn = wx.Button(self.panel, label='结束')
            button_box.Add(next_game_btn, 0, flag=wx.CENTER)
            next_game_btn.Bind(wx.EVT_BUTTON, self.OnClickedNext)
            button_box.Add(view_history_game_btn, 0, flag=wx.CENTER)
            # button_box.Add(self.resize_panel_btn, 0, flag=wx.CENTER)
            bp_board_box = wx.BoxSizer()
            ban_blue_box = wx.BoxSizer()
            ban_red_box = wx.BoxSizer()
            pick_blue_box = wx.BoxSizer()
            pick_red_box = wx.BoxSizer()
            blue_box = wx.BoxSizer(wx.VERTICAL)
            red_box = wx.BoxSizer(wx.VERTICAL)
            self.pbox.Add(select_pos_box, 0, flag=wx.ALIGN_CENTER)
            self.hero_grid_panel = wx.ScrolledWindow(self.panel, size=(900, 550))
            self.hero_grid_panel.SetScrollRate(5, 20)
            self.hero_grid = wx.GridSizer(20, 7, 2, 2)
            self.hero_grid_panel.SetSizer(self.hero_grid)

            self.career_text_list = []

            with open('heroes\\hero_settings.csv', 'r', newline='') as setting_csv:
                reader = csv.reader(setting_csv)
                for i in reader:
                    self.career_text_list.append(i)
            self.select_career_btn_list = []
            self.select_all_btn = wx.Button(self.panel, label='全部', size=(100, 50))
            select_pos_box.Add(self.select_all_btn, 1, wx.ALIGN_CENTER)
            self.select_career_btn_list.append(self.select_all_btn)
            self.select_all_btn.Bind(wx.EVT_BUTTON,
                                     lambda event, pram1='全部': self.OnClickedSelectCareer(event, pram1))
            btn_num = 0
            for i in self.career_text_list:
                self.select_career_btn = wx.Button(self.panel, label=i[0], size=(100, 50))
                select_pos_box.Add(self.select_career_btn, 1, wx.ALIGN_CENTER)
                self.select_career_btn_list.append(self.select_career_btn)
                self.select_career_btn.Bind(wx.EVT_BUTTON,
                                            lambda event, pram1=i[0]: self.OnClickedSelectCareer(event, pram1))
                btn_num = btn_num + 1
            self.load_hero_event = wx.CommandEvent(wx.EVT_BUTTON.typeId, self.select_career_btn_list[1].GetId())
            wx.PostEvent(self.select_career_btn_list[0], self.load_hero_event)
            self.pbox.Add(self.hero_grid_panel, 1, flag=wx.EXPAND)
            # self.pbox.Add((0, 1), 1, wx.EXPAND, 0)
            self.pbox.Add(button_box, 0, flag=wx.ALIGN_CENTER)
            self.pbox.Add(bp_board_box, 0, flag=wx.ALIGN_CENTER)
            bmp1 = wx.Image('image\\select_ban.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            select1 = SelectButton(self.panel, -1, bmp1)
            select2 = SelectButton(self.panel, -1, bmp1)
            select3 = SelectButton(self.panel, -1, bmp1)
            select4 = SelectButton(self.panel, -1, bmp1)
            select11 = SelectButton(self.panel, -1, bmp1)
            select12 = SelectButton(self.panel, -1, bmp1)
            select13 = SelectButton(self.panel, -1, bmp1)
            select14 = SelectButton(self.panel, -1, bmp1)
            select_10ban_ban1 = SelectButton(self.panel, -1, bmp1)
            select_10ban_ban2 = SelectButton(self.panel, -1, bmp1)
            team_blue_text = wx.StaticText(self.panel, -1, label=team_blue)
            team_red_text = wx.StaticText(self.panel, -1, label=team_red)
            team_text_font = wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
            team_blue_text.SetFont(team_text_font)
            team_red_text.SetFont(team_text_font)
            ban_blue_box.Add(select1, 0, flag=wx.ALIGN_LEFT)
            ban_blue_box.Add(select3, 0, flag=wx.ALIGN_LEFT)
            ban_blue_box.Add(select_10ban_ban2, 0, flag=wx.ALIGN_LEFT)
            ban_blue_box.Add(select12, 0, flag=wx.ALIGN_LEFT)
            ban_blue_box.Add(select14, 0, flag=wx.ALIGN_LEFT)
            ban_blue_box.Add(team_blue_text, 0, flag=wx.CENTRE)
            ban_red_box.Add(team_red_text, 0, flag=wx.CENTRE)
            ban_red_box.Add(select13, 0, flag=wx.ALIGN_LEFT)
            ban_red_box.Add(select11, 0, flag=wx.ALIGN_LEFT)
            ban_red_box.Add(select_10ban_ban1, 0, flag=wx.ALIGN_LEFT)
            ban_red_box.Add(select4, 0, flag=wx.ALIGN_LEFT)
            ban_red_box.Add(select2, 0, flag=wx.ALIGN_LEFT)
            select_pick_bmp = wx.Image('image\\select_pick.png', wx.BITMAP_TYPE_ANY).Scale(110, 110).ConvertToBitmap()
            select5 = SelectButton(self.panel, -1, select_pick_bmp)
            select8 = SelectButton(self.panel, -1, select_pick_bmp)
            select9 = SelectButton(self.panel, -1, select_pick_bmp)
            select16 = SelectButton(self.panel, -1, select_pick_bmp)
            select17 = SelectButton(self.panel, -1, select_pick_bmp)
            select6 = SelectButton(self.panel, -1, select_pick_bmp)
            select7 = SelectButton(self.panel, -1, select_pick_bmp)
            select10 = SelectButton(self.panel, -1, select_pick_bmp)
            select15 = SelectButton(self.panel, -1, select_pick_bmp)
            select18 = SelectButton(self.panel, -1, select_pick_bmp)
            self.select_button = [select1, select2, select3, select4, select5, select6, select7, select8, select9,
                                  select10, select_10ban_ban1, select_10ban_ban2, select11, select12, select13,
                                  select14, select15, select16, select17,
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
            select_10ban_ban1.Bind(wx.EVT_BUTTON, lambda event, pram1=10: self.onChoosePos(event, pram1))
            select_10ban_ban2.Bind(wx.EVT_BUTTON, lambda event, pram1=11: self.onChoosePos(event, pram1))
            select11.Bind(wx.EVT_BUTTON, lambda event, pram1=12: self.onChoosePos(event, pram1))
            select12.Bind(wx.EVT_BUTTON, lambda event, pram1=13: self.onChoosePos(event, pram1))
            select13.Bind(wx.EVT_BUTTON, lambda event, pram1=14: self.onChoosePos(event, pram1))
            select14.Bind(wx.EVT_BUTTON, lambda event, pram1=15: self.onChoosePos(event, pram1))
            select15.Bind(wx.EVT_BUTTON, lambda event, pram1=16: self.onChoosePos(event, pram1))
            select16.Bind(wx.EVT_BUTTON, lambda event, pram1=17: self.onChoosePos(event, pram1))
            select17.Bind(wx.EVT_BUTTON, lambda event, pram1=18: self.onChoosePos(event, pram1))
            select18.Bind(wx.EVT_BUTTON, lambda event, pram1=19: self.onChoosePos(event, pram1))
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
            self.panel.SetSizer(self.pbox)

        # def OnClickedResize(self, event):
        #     width, height = self.GetSize()
        #     self.hero_grid_panel.SetSize(width - 25, height - 300)

        def OnClickedSelectCareer(self, event, career):
            buttons = []
            blue_select_list = [1, 3, 4, 7, 8, 10, 12, 14, 17, 18]
            red_select_list = [0, 2, 5, 6, 9, 11, 13, 15, 16, 19]
            if team_blue == team1:
                team1_num = 11
                team2_num = 12
            else:
                team1_num = 12
                team2_num = 11
            for item in self.hero_grid.GetChildren():
                item.GetWindow().Destroy()  # 删除每个控件
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
            # resize_hero_event = wx.CommandEvent(wx.EVT_BUTTON.typeId, self.resize_panel_btn.GetId())
            # wx.PostEvent(self.resize_panel_btn, resize_hero_event)
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

        def onClickViewHistory(self, event):
            history_inf_frame = HistoryInf()
            history_inf_frame.Show()

        def OnClickedNext(self, event):
            if self.final_hero_pos == 1:
                save_list = [[match_id, str(max_game_num), str(game_num), team_blue, team_red, '10ban']]
                save_list[0].extend(self.bp_sequence)
                with open('save\\save.csv', mode='r') as read_file:
                    reader = csv.reader(read_file)
                    for row in reader:
                        save_list.append(row)
                with open('save\\save.csv', mode='w', newline='') as file:
                    writer = csv.writer(file)
                    for i in save_list:
                        writer.writerow(i)
                new_list = ([team_blue, team_red, '10ban'])
                new_list.extend(self.bp_sequence)
                history_inf.append(new_list)

                next_game = NextGame()
                next_game.Show()
                self.Close()
            else:
                mgb = wx.MessageBox('对局尚未结束！', '提示', wx.OK | wx.ICON_INFORMATION)

        def onClickSelect(self, event, id):
            ban_list = [0, 1, 2, 3, 10, 11, 12, 13, 14, 15]
            blue_pick_list = [4, 7, 8, 17, 18]
            red_pick_list = [5, 6, 9, 16, 19]
            if self.pos == 19:
                self.final_hero_pos = 1
            if self.pos in ban_list:
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
            if self.pos != 20:
                choose_pos_event = wx.CommandEvent(wx.EVT_BUTTON.typeId, self.select_button[self.pos].GetId())
                wx.PostEvent(self.select_button[self.pos], choose_pos_event)
            else:
                self.select_button[-1].colour = wx.Colour(255, 255, 255)
            wx.PostEvent(self.select_career_btn_list[self.select_work], self.load_hero_event)

    class NextGame(wx.Frame):
        def __init__(self):
            if game_num != max_game_num:
                wx.Frame.__init__(self, None, title='下一局', size=(200, 200))
    
                self.Center()
                self.panel = wx.Panel(self)
                vbox = wx.BoxSizer(wx.VERTICAL)
                choices_list = ['是', '否']
                choices_list2 = ['否', '是']
                self.change_box = wx.RadioBox(self.panel, label='是否换边', choices=choices_list)
                self.normal_box = wx.RadioBox(self.panel, label='巅峰对决', choices=choices_list2)
                ok_button = wx.Button(self.panel, label='确认')
                vbox.Add(self.change_box, 0, wx.ALIGN_CENTER)
                vbox.Add(self.normal_box, 0, wx.ALIGN_CENTER)
                vbox.Add(ok_button, 0, wx.ALIGN_CENTER)
                ok_button.Bind(wx.EVT_BUTTON, self.onNextGame)
            else:
                wx.Frame.__init__(self, None, title='提醒', size=(210, 80))
    
                self.Center()
                self.panel = wx.Panel(self)
                vbox = wx.BoxSizer(wx.VERTICAL)
                exit_confirm_txt = wx.StaticText(self.panel, label='比赛结束')
                ok_button = wx.Button(self.panel, label='确认')
                vbox.Add(exit_confirm_txt, 0, wx.ALIGN_CENTER)
                vbox.Add(ok_button, 0, wx.ALIGN_CENTER)
                ok_button.Bind(wx.EVT_BUTTON, self.onExit)
            display_idx = wx.Display.GetFromPoint(wx.GetMousePosition())
            # 获取该屏幕的几何信息（x, y, width, height）
            display_rect = wx.Display(display_idx).GetGeometry()
            win_width, win_height = self.GetSize()
            pos_x = display_rect.x + (display_rect.width - win_width) // 2
            pos_y = display_rect.y + (display_rect.height - win_height) // 2
            self.SetPosition((pos_x, pos_y))  # 设置窗口位置
            self.panel.SetSizer(vbox)

        def onExit(self, event):
            self.Close()

        def onNextGame(self, event):
            if self.change_box.GetSelection() == 0:
                team_b = team_red
                team_r = team_blue
            else:
                team_r = team_red
                team_b = team_blue
            for hero in heroes_all_list:
                hero[13] = '0'
                hero[14] = '0'
            if self.normal_box.GetSelection() == 0:
                game_mode_next = 1
            else:
                game_mode_next = 0
            self.Close()
            load_game(match_id, game_mode_next, 10, team_b, team_r, game_num + 1, heroes_all_list,
                      max_game_num, team1, team2, history_inf)

    match_bp_frame = BpFrame()
    match_bp_frame.Show(True)


def load_regular_game_0ban(match_id, team_blue, team_red, game_num, heroes_all_list, max_game_num, team1, team2,
                           history_inf):
    class HistoryInf(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None,
                              title='WBW的BP模拟器【历史阵容】', size=(1500, 900))

            display_idx = wx.Display.GetFromPoint(wx.GetMousePosition())
            # 获取该屏幕的几何信息（x, y, width, height）
            display_rect = wx.Display(display_idx).GetGeometry()
            win_width, win_height = self.GetSize()
            pos_x = display_rect.x + (display_rect.width - win_width) // 2
            pos_y = display_rect.y + (display_rect.height - win_height) // 2
            self.SetPosition((pos_x, pos_y))  # 设置窗口位置
            self.final_hero_pos = 0
            self.Center()
            self.panel = wx.Panel(self)
            self.pbox = wx.BoxSizer(wx.VERTICAL)
            show_heroes_pick_blue_list = [0, 3, 4, 7, 8]
            show_heroes_pick_red_list = [1, 2, 5, 6, 9]
            for i in range(game_num - 1):
                game_box = wx.BoxSizer(wx.HORIZONTAL)
                self.pbox.Add(game_box, 1, wx.Center)
                blue_box = wx.BoxSizer(wx.VERTICAL)
                red_box = wx.BoxSizer(wx.VERTICAL)
                game_box.Add(blue_box, 0, wx.Center)
                game_box.Add((300, 0), 1, wx.EXPAND, 0)
                game_box.Add(red_box, 0, wx.Center)
                blue_ban_box = wx.BoxSizer(wx.HORIZONTAL)
                blue_pick_box = wx.BoxSizer(wx.HORIZONTAL)
                red_ban_box = wx.BoxSizer(wx.HORIZONTAL)
                red_pick_box = wx.BoxSizer(wx.HORIZONTAL)
                blue_box.Add(blue_ban_box, 0)
                blue_box.Add(blue_pick_box, 0)
                red_box.Add(red_ban_box, 0, flag=wx.ALIGN_RIGHT)
                red_box.Add(red_pick_box, 0, flag=wx.ALIGN_RIGHT)
                team_blue_text = wx.StaticText(self.panel, -1, label=history_inf[i][0])
                team_red_text = wx.StaticText(self.panel, -1, label=history_inf[i][1])
                red_ban_box.Add(team_red_text, 0, flag=wx.CENTRE)

                for j in show_heroes_pick_blue_list:
                    self.bmp = wx.Image('heroes\\icon\\' + history_inf[i][j + 3] + '.jpg',
                                        wx.BITMAP_TYPE_ANY).Scale(110, 110).ConvertToBitmap()
                    self.bitmap = wx.StaticBitmap(self.panel, wx.ID_ANY, self.bmp)
                    blue_pick_box.Add(self.bitmap, 1)

                for j in show_heroes_pick_red_list:
                    self.bmp = wx.Image('heroes\\icon\\' + history_inf[i][j + 3] + '.jpg',
                                        wx.BITMAP_TYPE_ANY).Scale(110, 110).ConvertToBitmap()
                    self.bitmap = wx.StaticBitmap(self.panel, wx.ID_ANY, self.bmp)
                    red_pick_box.Add(self.bitmap, 1)
                blue_ban_box.Add(team_blue_text, 0, flag=wx.CENTRE)
                self.panel.SetSizer(self.pbox)

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
            # 设置边框颜色和宽度
            border_color = self.colour  # 边框
            dc.SetPen(wx.Pen(border_color, 1))  # 设置边框颜色和宽度
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            # 绘制一个矩形边框
            width, height = self.GetSize()
            dc.DrawRectangle(-4, -4, width, height)

    class BpFrame(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None,
                              title='WBW的BP模拟器【BO' + str(max_game_num) + '第' + str(game_num) + '局】')

            self.SetMinSize((1500, 900))
            display_idx = wx.Display.GetFromPoint(wx.GetMousePosition())
            # 获取该屏幕的几何信息（x, y, width, height）
            display_rect = wx.Display(display_idx).GetGeometry()
            win_width, win_height = self.GetSize()
            pos_x = display_rect.x + (display_rect.width - win_width) // 2
            pos_y = display_rect.y + (display_rect.height - win_height) // 2
            self.SetPosition((pos_x, pos_y))  # 设置窗口位置
            self.career_list = []
            self.final_hero_pos = 0
            self.Center()
            self.pos = 0
            self.bp_sequence = ['0'] * 10
            self.select_work = 0
            self.Maximize(True)
            self.panel = wx.Panel(self)
            self.pbox = wx.BoxSizer(wx.VERTICAL)
            select_pos_box = wx.BoxSizer()
            button_box = wx.BoxSizer()
            view_history_game_btn = wx.Button(self.panel, label='显示历史阵容')
            view_history_game_btn.Bind(wx.EVT_BUTTON, self.onClickViewHistory)
            # self.resize_panel_btn = wx.Button(self.panel, label='适应面板大小')
            # self.resize_panel_btn.Bind(wx.EVT_BUTTON, self.OnClickedResize)
            if game_num != max_game_num:
                next_game_btn = wx.Button(self.panel, label='下一局')
            else:
                next_game_btn = wx.Button(self.panel, label='结束')
            button_box.Add(next_game_btn, 0, flag=wx.CENTER)
            next_game_btn.Bind(wx.EVT_BUTTON, self.OnClickedNext)
            button_box.Add(view_history_game_btn, 0, flag=wx.CENTER)
            # button_box.Add(self.resize_panel_btn, 0, flag=wx.CENTER)
            bp_board_box = wx.BoxSizer()
            ban_blue_box = wx.BoxSizer()
            ban_red_box = wx.BoxSizer()
            pick_blue_box = wx.BoxSizer()
            pick_red_box = wx.BoxSizer()
            blue_box = wx.BoxSizer(wx.VERTICAL)
            red_box = wx.BoxSizer(wx.VERTICAL)
            self.pbox.Add(select_pos_box, 0, flag=wx.ALIGN_CENTER)
            self.hero_grid_panel = wx.ScrolledWindow(self.panel, size=(900, 550))
            self.hero_grid_panel.SetScrollRate(5, 20)
            self.hero_grid = wx.GridSizer(20, 7, 2, 2)
            self.hero_grid_panel.SetSizer(self.hero_grid)

            self.career_text_list = []

            with open('heroes\\hero_settings.csv', 'r', newline='') as setting_csv:
                reader = csv.reader(setting_csv)
                for i in reader:
                    self.career_text_list.append(i)
            self.select_career_btn_list = []
            self.select_all_btn = wx.Button(self.panel, label='全部', size=(100, 50))
            select_pos_box.Add(self.select_all_btn, 1, wx.ALIGN_CENTER)
            self.select_career_btn_list.append(self.select_all_btn)
            self.select_all_btn.Bind(wx.EVT_BUTTON,
                                     lambda event, pram1='全部': self.OnClickedSelectCareer(event, pram1))
            btn_num = 0
            for i in self.career_text_list:
                self.select_career_btn = wx.Button(self.panel, label=i[0], size=(100, 50))
                select_pos_box.Add(self.select_career_btn, 1, wx.ALIGN_CENTER)
                self.select_career_btn_list.append(self.select_career_btn)
                self.select_career_btn.Bind(wx.EVT_BUTTON,
                                            lambda event, pram1=i[0]: self.OnClickedSelectCareer(event, pram1))
                btn_num = btn_num + 1
            self.load_hero_event = wx.CommandEvent(wx.EVT_BUTTON.typeId, self.select_career_btn_list[1].GetId())
            wx.PostEvent(self.select_career_btn_list[0], self.load_hero_event)
            self.pbox.Add(self.hero_grid_panel, 1, flag=wx.EXPAND)
            # self.pbox.Add((0, 1), 1, wx.EXPAND, 0)
            self.pbox.Add(button_box, 0, flag=wx.ALIGN_CENTER)
            self.pbox.Add(bp_board_box, 0, flag=wx.ALIGN_CENTER)
            team_blue_text = wx.StaticText(self.panel, -1, label=team_blue)
            team_red_text = wx.StaticText(self.panel, -1, label=team_red)
            team_text_font = wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
            team_blue_text.SetFont(team_text_font)
            team_red_text.SetFont(team_text_font)
            ban_blue_box.Add(team_blue_text, 0, flag=wx.CENTRE)
            ban_red_box.Add(team_red_text, 0, flag=wx.CENTRE)
            select_pick_bmp = wx.Image('image\\select_pick.png', wx.BITMAP_TYPE_ANY).Scale(110, 110).ConvertToBitmap()
            select1 = SelectButton(self.panel, -1, select_pick_bmp)
            select2 = SelectButton(self.panel, -1, select_pick_bmp)
            select3 = SelectButton(self.panel, -1, select_pick_bmp)
            select4 = SelectButton(self.panel, -1, select_pick_bmp)
            select5 = SelectButton(self.panel, -1, select_pick_bmp)
            select6 = SelectButton(self.panel, -1, select_pick_bmp)
            select7 = SelectButton(self.panel, -1, select_pick_bmp)
            select8 = SelectButton(self.panel, -1, select_pick_bmp)
            select9 = SelectButton(self.panel, -1, select_pick_bmp)
            select10 = SelectButton(self.panel, -1, select_pick_bmp)
            self.select_button = [select1, select2, select3, select4, select5, select6, select7, select8, select9,
                                  select10]
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

            pick_blue_box.Add(select1, 0, flag=wx.ALIGN_LEFT)
            pick_blue_box.Add(select4, 0, flag=wx.ALIGN_LEFT)
            pick_blue_box.Add(select5, 0, flag=wx.ALIGN_LEFT)
            pick_blue_box.Add(select8, 0, flag=wx.ALIGN_LEFT)
            pick_blue_box.Add(select9, 0, flag=wx.ALIGN_LEFT)
            pick_red_box.Add(select10, 0, flag=wx.ALIGN_LEFT)
            pick_red_box.Add(select7, 0, flag=wx.ALIGN_LEFT)
            pick_red_box.Add(select6, 0, flag=wx.ALIGN_LEFT)
            pick_red_box.Add(select3, 0, flag=wx.ALIGN_LEFT)
            pick_red_box.Add(select2, 0, flag=wx.ALIGN_LEFT)
            blue_box.Add(ban_blue_box, 0, flag=wx.ALIGN_LEFT)
            blue_box.Add(pick_blue_box, 0, flag=wx.ALIGN_LEFT)
            red_box.Add(ban_red_box, 0, flag=wx.ALIGN_RIGHT)
            red_box.Add(pick_red_box, 0, flag=wx.ALIGN_RIGHT)
            bp_board_box.Add(blue_box, 0)
            bp_board_box.Add((100, 0), 0, wx.EXPAND)
            bp_board_box.Add(red_box, 0)
            self.panel.SetSizer(self.pbox)

        # def OnClickedResize(self, event):
        #     width, height = self.GetSize()
        #     self.hero_grid_panel.SetSize(width - 25, height - 300)

        def OnClickedSelectCareer(self, event, career):
            buttons = []
            blue_select_list = [0, 3, 4, 7, 8]
            red_select_list = [1, 2, 5, 6, 9]
            if team_blue == team1:
                team1_num = 11
                team2_num = 12
            else:
                team1_num = 12
                team2_num = 11
            for item in self.hero_grid.GetChildren():
                item.GetWindow().Destroy()  # 删除每个控件
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
            # resize_hero_event = wx.CommandEvent(wx.EVT_BUTTON.typeId, self.resize_panel_btn.GetId())
            # wx.PostEvent(self.resize_panel_btn, resize_hero_event)
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

        def onClickViewHistory(self, event):
            history_inf_frame = HistoryInf()
            history_inf_frame.Show()

        def OnClickedNext(self, event):
            if self.final_hero_pos == 1:
                save_list = [[match_id, str(max_game_num), str(game_num), team_blue, team_red, '0ban']]
                save_list[0].extend(self.bp_sequence)
                with open('save\\save.csv', mode='r') as read_file:
                    reader = csv.reader(read_file)
                    for row in reader:
                        save_list.append(row)
                with open('save\\save.csv', mode='w', newline='') as file:
                    writer = csv.writer(file)
                    for i in save_list:
                        writer.writerow(i)
                new_list = ([team_blue, team_red, '10ban'])
                new_list.extend(self.bp_sequence)
                history_inf.append(new_list)

                next_game = NextGame()
                next_game.Show()
                self.Close()
            else:
                mgb = wx.MessageBox('对局尚未结束！', '提示', wx.OK | wx.ICON_INFORMATION)

        def onClickSelect(self, event, id):
            blue_pick_list = [0, 3, 4, 7, 8]
            red_pick_list = [1, 2, 5, 6, 9]
            if self.pos == 9:
                self.final_hero_pos = 1
            if 1 == 1:
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
            if self.pos != 10:
                choose_pos_event = wx.CommandEvent(wx.EVT_BUTTON.typeId, self.select_button[self.pos].GetId())
                wx.PostEvent(self.select_button[self.pos], choose_pos_event)
            else:
                self.select_button[-1].colour = wx.Colour(255, 255, 255)
            wx.PostEvent(self.select_career_btn_list[self.select_work], self.load_hero_event)

    class NextGame(wx.Frame):
        def __init__(self):
            if game_num != max_game_num:
                wx.Frame.__init__(self, None, title='下一局', size=(200, 200))
    
                self.Center()
                self.panel = wx.Panel(self)
                vbox = wx.BoxSizer(wx.VERTICAL)
                choices_list = ['是', '否']
                choices_list2 = ['否', '是']
                self.change_box = wx.RadioBox(self.panel, label='是否换边', choices=choices_list)
                self.normal_box = wx.RadioBox(self.panel, label='巅峰对决', choices=choices_list2)
                ok_button = wx.Button(self.panel, label='确认')
                vbox.Add(self.change_box, 0, wx.ALIGN_CENTER)
                vbox.Add(self.normal_box, 0, wx.ALIGN_CENTER)
                vbox.Add(ok_button, 0, wx.ALIGN_CENTER)
                ok_button.Bind(wx.EVT_BUTTON, self.onNextGame)
            else:
                wx.Frame.__init__(self, None, title='提醒', size=(210, 80))
    
                self.Center()
                self.panel = wx.Panel(self)
                vbox = wx.BoxSizer(wx.VERTICAL)
                exit_confirm_txt = wx.StaticText(self.panel, label='比赛结束')
                ok_button = wx.Button(self.panel, label='确认')
                vbox.Add(exit_confirm_txt, 0, wx.ALIGN_CENTER)
                vbox.Add(ok_button, 0, wx.ALIGN_CENTER)
                ok_button.Bind(wx.EVT_BUTTON, self.onExit)
            display_idx = wx.Display.GetFromPoint(wx.GetMousePosition())
            # 获取该屏幕的几何信息（x, y, width, height）
            display_rect = wx.Display(display_idx).GetGeometry()
            win_width, win_height = self.GetSize()
            pos_x = display_rect.x + (display_rect.width - win_width) // 2
            pos_y = display_rect.y + (display_rect.height - win_height) // 2
            self.SetPosition((pos_x, pos_y))  # 设置窗口位置
            self.panel.SetSizer(vbox)

        def onExit(self, event):
            self.Close()

        def onNextGame(self, event):
            if self.change_box.GetSelection() == 0:
                team_b = team_red
                team_r = team_blue
            else:
                team_r = team_red
                team_b = team_blue
            for hero in heroes_all_list:
                hero[13] = '0'
                hero[14] = '0'
            if self.normal_box.GetSelection() == 0:
                game_mode_next = 1
            else:
                game_mode_next = 0
            self.Close()
            load_game(match_id, game_mode_next, 0, team_b, team_r, game_num + 1, heroes_all_list,
                      max_game_num, team1, team2, history_inf)

    match_bp_frame = BpFrame()
    match_bp_frame.Show(True)


def load_final_game(match_id, team_blue, team_red, game_num, heroes_all_list, max_game_num, team1, team2,
                    history_inf):
    class HistoryInf(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None,
                              title='WBW的BP模拟器【历史阵容】', size=(1500, 900))

            display_idx = wx.Display.GetFromPoint(wx.GetMousePosition())
            # 获取该屏幕的几何信息（x, y, width, height）
            display_rect = wx.Display(display_idx).GetGeometry()
            win_width, win_height = self.GetSize()
            pos_x = display_rect.x + (display_rect.width - win_width) // 2
            pos_y = display_rect.y + (display_rect.height - win_height) // 2
            self.SetPosition((pos_x, pos_y))  # 设置窗口位置
            self.final_hero_pos = 0
            self.Center()
            self.panel = wx.Panel(self)
            self.pbox = wx.BoxSizer(wx.VERTICAL)
            show_heroes_pick_blue_list = []
            show_heroes_pick_red_list = []
            show_heroes_ban_blue_list = []
            show_heroes_ban_red_list = []
            if history_inf[0][2] == '-1':
                show_heroes_pick_blue_list = [0, 1, 2, 3, 4]
                show_heroes_pick_red_list = [5, 6, 7, 8, 9]
                show_heroes_ban_blue_list = []
                show_heroes_ban_red_list = []
            elif history_inf[0][2] == '8ban':
                show_heroes_ban_blue_list = [0, 2, 11, 13]
                show_heroes_ban_red_list = [12, 10, 3, 1]
                show_heroes_pick_blue_list = [4, 7, 8, 15, 16]
                show_heroes_pick_red_list = [17, 14, 9, 6, 5]
            elif history_inf[0][2] == '10ban':
                show_heroes_ban_blue_list = [0, 2, 11, 13, 15]
                show_heroes_ban_red_list = [14, 12, 10, 3, 1]
                show_heroes_pick_blue_list = [4, 7, 8, 17, 18]
                show_heroes_pick_red_list = [19, 16, 9, 6, 5]
            else:
                show_heroes_pick_blue_list = []
                show_heroes_pick_red_list = []
                show_heroes_ban_blue_list = []
                show_heroes_ban_red_list = []
            for i in range(game_num - 1):
                game_box = wx.BoxSizer(wx.HORIZONTAL)
                self.pbox.Add(game_box, 1, wx.Center)
                blue_box = wx.BoxSizer(wx.VERTICAL)
                red_box = wx.BoxSizer(wx.VERTICAL)
                game_box.Add(blue_box, 0, wx.Center)
                game_box.Add((300, 0), 1, wx.EXPAND, 0)
                game_box.Add(red_box, 0, wx.Center)
                blue_ban_box = wx.BoxSizer(wx.HORIZONTAL)
                blue_pick_box = wx.BoxSizer(wx.HORIZONTAL)
                red_ban_box = wx.BoxSizer(wx.HORIZONTAL)
                red_pick_box = wx.BoxSizer(wx.HORIZONTAL)
                blue_box.Add(blue_ban_box, 0)
                blue_box.Add(blue_pick_box, 0)
                red_box.Add(red_ban_box, 0, flag=wx.ALIGN_RIGHT)
                red_box.Add(red_pick_box, 0, flag=wx.ALIGN_RIGHT)
                team_blue_text = wx.StaticText(self.panel, -1, label=history_inf[i][0])
                team_red_text = wx.StaticText(self.panel, -1, label=history_inf[i][1])
                red_ban_box.Add(team_red_text, 0, flag=wx.CENTRE)
                for j in show_heroes_ban_blue_list:
                    self.bmp = wx.Image('heroes\\icon\\' + history_inf[i][j + 3] + '.jpg',
                                        wx.BITMAP_TYPE_ANY).ConvertToGreyscale().Scale(70, 70).ConvertToBitmap()
                    self.bitmap = wx.StaticBitmap(self.panel, wx.ID_ANY, self.bmp)
                    blue_ban_box.Add(self.bitmap, 1)
                for j in show_heroes_pick_blue_list:
                    self.bmp = wx.Image('heroes\\icon\\' + history_inf[i][j + 3] + '.jpg',
                                        wx.BITMAP_TYPE_ANY).Scale(110, 110).ConvertToBitmap()
                    self.bitmap = wx.StaticBitmap(self.panel, wx.ID_ANY, self.bmp)
                    blue_pick_box.Add(self.bitmap, 1)
                for j in show_heroes_ban_red_list:
                    self.bmp = wx.Image('heroes\\icon\\' + history_inf[i][j + 3] + '.jpg',
                                        wx.BITMAP_TYPE_ANY).ConvertToGreyscale().Scale(70, 70).ConvertToBitmap()
                    self.bitmap = wx.StaticBitmap(self.panel, wx.ID_ANY, self.bmp)
                    red_ban_box.Add(self.bitmap, 1)
                for j in show_heroes_pick_red_list:
                    self.bmp = wx.Image('heroes\\icon\\' + history_inf[i][j + 3] + '.jpg',
                                        wx.BITMAP_TYPE_ANY).Scale(110, 110).ConvertToBitmap()
                    self.bitmap = wx.StaticBitmap(self.panel, wx.ID_ANY, self.bmp)
                    red_pick_box.Add(self.bitmap, 1)
                blue_ban_box.Add(team_blue_text, 0, flag=wx.CENTRE)
                self.panel.SetSizer(self.pbox)

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
            # 设置边框颜色和宽度
            border_color = self.colour  # 边框
            dc.SetPen(wx.Pen(border_color, 1))  # 设置边框颜色和宽度
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            # 绘制一个矩形边框
            width, height = self.GetSize()
            dc.DrawRectangle(-4, -4, width, height)

    class BpFrame(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None,
                              title='WBW的BP模拟器【BO' + str(max_game_num) + '第' + str(game_num) + '局】')

            self.SetMinSize((1500, 900))
            display_idx = wx.Display.GetFromPoint(wx.GetMousePosition())
            # 获取该屏幕的几何信息（x, y, width, height）
            display_rect = wx.Display(display_idx).GetGeometry()
            win_width, win_height = self.GetSize()
            pos_x = display_rect.x + (display_rect.width - win_width) // 2
            pos_y = display_rect.y + (display_rect.height - win_height) // 2
            self.SetPosition((pos_x, pos_y))  # 设置窗口位置
            self.career_list = []
            self.final_hero_pos = 0
            self.Center()
            self.pos = 0
            self.bp_sequence = ['0'] * 10
            self.select_work = 0
            self.Maximize(True)
            self.panel = wx.Panel(self)
            self.pbox = wx.BoxSizer(wx.VERTICAL)
            select_pos_box = wx.BoxSizer()
            button_box = wx.BoxSizer()
            view_history_game_btn = wx.Button(self.panel, label='显示历史阵容')
            view_history_game_btn.Bind(wx.EVT_BUTTON, self.onClickViewHistory)
            # self.resize_panel_btn = wx.Button(self.panel, label='适应面板大小')
            # self.resize_panel_btn.Bind(wx.EVT_BUTTON, self.OnClickedResize)
            if game_num != max_game_num:
                next_game_btn = wx.Button(self.panel, label='下一局')
            else:
                next_game_btn = wx.Button(self.panel, label='结束')
            button_box.Add(next_game_btn, 0, flag=wx.CENTER)
            next_game_btn.Bind(wx.EVT_BUTTON, self.OnClickedNext)
            button_box.Add(view_history_game_btn, 0, flag=wx.CENTER)
            # button_box.Add(self.resize_panel_btn, 0, flag=wx.CENTER)
            bp_board_box = wx.BoxSizer()
            ban_blue_box = wx.BoxSizer()
            ban_red_box = wx.BoxSizer()
            pick_blue_box = wx.BoxSizer()
            pick_red_box = wx.BoxSizer()
            blue_box = wx.BoxSizer(wx.VERTICAL)
            red_box = wx.BoxSizer(wx.VERTICAL)
            self.pbox.Add(select_pos_box, 0, flag=wx.ALIGN_CENTER)
            self.hero_grid_panel = wx.ScrolledWindow(self.panel, size=(900, 550))
            self.hero_grid_panel.SetScrollRate(5, 20)
            self.hero_grid = wx.GridSizer(20, 7, 2, 2)
            self.hero_grid_panel.SetSizer(self.hero_grid)

            self.career_text_list = []

            with open('heroes\\hero_settings.csv', 'r', newline='') as setting_csv:
                reader = csv.reader(setting_csv)
                for i in reader:
                    self.career_text_list.append(i)
            self.select_career_btn_list = []
            self.select_all_btn = wx.Button(self.panel, label='全部', size=(100, 50))
            select_pos_box.Add(self.select_all_btn, 1, wx.ALIGN_CENTER)
            self.select_career_btn_list.append(self.select_all_btn)
            self.select_all_btn.Bind(wx.EVT_BUTTON,
                                     lambda event, pram1='全部': self.OnClickedSelectCareer(event, pram1))
            btn_num = 0
            for i in self.career_text_list:
                self.select_career_btn = wx.Button(self.panel, label=i[0], size=(100, 50))
                select_pos_box.Add(self.select_career_btn, 1, wx.ALIGN_CENTER)
                self.select_career_btn_list.append(self.select_career_btn)
                self.select_career_btn.Bind(wx.EVT_BUTTON,
                                            lambda event, pram1=i[0]: self.OnClickedSelectCareer(event, pram1))
                btn_num = btn_num + 1
            self.load_hero_event = wx.CommandEvent(wx.EVT_BUTTON.typeId, self.select_career_btn_list[1].GetId())
            wx.PostEvent(self.select_career_btn_list[0], self.load_hero_event)
            self.pbox.Add(self.hero_grid_panel, 1, flag=wx.EXPAND)
            # self.pbox.Add((0, 1), 1, wx.EXPAND, 0)
            self.pbox.Add(button_box, 0, flag=wx.ALIGN_CENTER)
            self.pbox.Add(bp_board_box, 0, flag=wx.ALIGN_CENTER)
            team_blue_text = wx.StaticText(self.panel, -1, label=team_blue)
            team_red_text = wx.StaticText(self.panel, -1, label=team_red)
            team_text_font = wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
            team_blue_text.SetFont(team_text_font)
            team_red_text.SetFont(team_text_font)
            ban_blue_box.Add(team_blue_text, 0, flag=wx.CENTRE)
            ban_red_box.Add(team_red_text, 0, flag=wx.CENTRE)
            select_pick_bmp = wx.Image('image\\select_pick.png', wx.BITMAP_TYPE_ANY).Scale(110, 110).ConvertToBitmap()
            select1 = SelectButton(self.panel, -1, select_pick_bmp)
            select2 = SelectButton(self.panel, -1, select_pick_bmp)
            select3 = SelectButton(self.panel, -1, select_pick_bmp)
            select4 = SelectButton(self.panel, -1, select_pick_bmp)
            select5 = SelectButton(self.panel, -1, select_pick_bmp)
            select6 = SelectButton(self.panel, -1, select_pick_bmp)
            select7 = SelectButton(self.panel, -1, select_pick_bmp)
            select8 = SelectButton(self.panel, -1, select_pick_bmp)
            select9 = SelectButton(self.panel, -1, select_pick_bmp)
            select10 = SelectButton(self.panel, -1, select_pick_bmp)
            self.select_button = [select1, select2, select3, select4, select5, select6, select7, select8, select9,
                                  select10]
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

            pick_blue_box.Add(select1, 0, flag=wx.ALIGN_LEFT)
            pick_blue_box.Add(select2, 0, flag=wx.ALIGN_LEFT)
            pick_blue_box.Add(select3, 0, flag=wx.ALIGN_LEFT)
            pick_blue_box.Add(select4, 0, flag=wx.ALIGN_LEFT)
            pick_blue_box.Add(select5, 0, flag=wx.ALIGN_LEFT)
            pick_red_box.Add(select10, 0, flag=wx.ALIGN_LEFT)
            pick_red_box.Add(select9, 0, flag=wx.ALIGN_LEFT)
            pick_red_box.Add(select8, 0, flag=wx.ALIGN_LEFT)
            pick_red_box.Add(select7, 0, flag=wx.ALIGN_LEFT)
            pick_red_box.Add(select6, 0, flag=wx.ALIGN_LEFT)
            blue_box.Add(ban_blue_box, 0, flag=wx.ALIGN_LEFT)
            blue_box.Add(pick_blue_box, 0, flag=wx.ALIGN_LEFT)
            red_box.Add(ban_red_box, 0, flag=wx.ALIGN_RIGHT)
            red_box.Add(pick_red_box, 0, flag=wx.ALIGN_RIGHT)
            bp_board_box.Add(blue_box, 0)
            bp_board_box.Add((100, 0), 0, wx.EXPAND)
            bp_board_box.Add(red_box, 0)
            self.panel.SetSizer(self.pbox)

        # def OnClickedResize(self, event):
        #     width, height = self.GetSize()
        #     self.hero_grid_panel.SetSize(width - 25, height - 300)

        def OnClickedSelectCareer(self, event, career):
            buttons = []
            blue_select_list = [0, 1, 2, 3, 4]
            red_select_list = [5, 6, 7, 8, 9]

            for item in self.hero_grid.GetChildren():
                item.GetWindow().Destroy()  # 删除每个控件
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
                        if self.pos in blue_select_list:
                            select_pick_bmp = wx.Image('heroes\\icon\\' + hero[0] + '.jpg',
                                                       wx.BITMAP_TYPE_ANY).Scale(110, 110).ConvertToBitmap()
                            buttons.append(wx.BitmapButton(self.hero_grid_panel, -1, select_pick_bmp))
                            self.hero_grid.Add(buttons[-1], 1, wx.EXPAND)
                            buttons[-1].Bind(wx.EVT_BUTTON,
                                             lambda event, pram1=hero[0]: self.onClickSelect(event, pram1))
                            buttons[0].Bind(wx.EVT_BUTTON,
                                            lambda event, pram1='0': self.onClickSelect(event, pram1))
                        elif self.pos in red_select_list:
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

            # resize_hero_event = wx.CommandEvent(wx.EVT_BUTTON.typeId, self.resize_panel_btn.GetId())
            # wx.PostEvent(self.resize_panel_btn, resize_hero_event)
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

        def onClickViewHistory(self, event):
            history_inf_frame = HistoryInf()
            history_inf_frame.Show()

        def OnClickedNext(self, event):
            if self.final_hero_pos == 1:
                save_list = [[match_id, str(max_game_num), str(game_num), team_blue, team_red, '-1']]
                save_list[0].extend(self.bp_sequence)
                with open('save\\save.csv', mode='r') as read_file:
                    reader = csv.reader(read_file)
                    for row in reader:
                        save_list.append(row)
                with open('save\\save.csv', mode='w', newline='') as file:
                    writer = csv.writer(file)
                    for i in save_list:
                        writer.writerow(i)
                new_list = ([team_blue, team_red, '-1'])
                new_list.extend(self.bp_sequence)
                history_inf.append(new_list)

                next_game = NextGame()
                next_game.Show()
                self.Close()
            else:
                mgb = wx.MessageBox('对局尚未结束！', '提示', wx.OK | wx.ICON_INFORMATION)

        def onClickSelect(self, event, id):
            blue_pick_list = [0, 3, 4, 7, 8]
            red_pick_list = [1, 2, 5, 6, 9]
            if self.pos == 9:
                self.final_hero_pos = 1
            if 1 == 1:
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
            if self.pos != 10:
                choose_pos_event = wx.CommandEvent(wx.EVT_BUTTON.typeId, self.select_button[self.pos].GetId())
                wx.PostEvent(self.select_button[self.pos], choose_pos_event)
            else:
                self.select_button[-1].colour = wx.Colour(255, 255, 255)
            wx.PostEvent(self.select_career_btn_list[self.select_work], self.load_hero_event)

    class NextGame(wx.Frame):
        def __init__(self):
            if game_num != max_game_num:
                wx.Frame.__init__(self, None, title='下一局', size=(200, 200))
    
                self.Center()
                self.panel = wx.Panel(self)
                vbox = wx.BoxSizer(wx.VERTICAL)
                choices_list = ['是', '否']
                choices_list2 = ['否', '是']
                self.change_box = wx.RadioBox(self.panel, label='是否换边', choices=choices_list)
                self.normal_box = wx.RadioBox(self.panel, label='巅峰对决', choices=choices_list2)
                ok_button = wx.Button(self.panel, label='确认')
                vbox.Add(self.change_box, 0, wx.ALIGN_CENTER)
                vbox.Add(self.normal_box, 0, wx.ALIGN_CENTER)
                vbox.Add(ok_button, 0, wx.ALIGN_CENTER)
                ok_button.Bind(wx.EVT_BUTTON, self.onNextGame)
            else:
                wx.Frame.__init__(self, None, title='提醒', size=(210, 80))
    
                self.Center()
                self.panel = wx.Panel(self)
                vbox = wx.BoxSizer(wx.VERTICAL)
                exit_confirm_txt = wx.StaticText(self.panel, label='比赛结束')
                ok_button = wx.Button(self.panel, label='确认')
                vbox.Add(exit_confirm_txt, 0, wx.ALIGN_CENTER)
                vbox.Add(ok_button, 0, wx.ALIGN_CENTER)
                ok_button.Bind(wx.EVT_BUTTON, self.onExit)
            display_idx = wx.Display.GetFromPoint(wx.GetMousePosition())
            # 获取该屏幕的几何信息（x, y, width, height）
            display_rect = wx.Display(display_idx).GetGeometry()
            win_width, win_height = self.GetSize()
            pos_x = display_rect.x + (display_rect.width - win_width) // 2
            pos_y = display_rect.y + (display_rect.height - win_height) // 2
            self.SetPosition((pos_x, pos_y))  # 设置窗口位置
            self.panel.SetSizer(vbox)

        def onExit(self, event):
            self.Close()

        def onNextGame(self, event):
            if self.change_box.GetSelection() == 0:
                team_b = team_red
                team_r = team_blue
            else:
                team_r = team_red
                team_b = team_blue
            for hero in heroes_all_list:
                hero[13] = '0'
                hero[14] = '0'
            if self.normal_box.GetSelection() == 0:
                game_mode_next = 1
            else:
                game_mode_next = 0
            self.Close()
            load_game(match_id, game_mode_next, -1, team_b, team_r, game_num + 1, heroes_all_list,
                      max_game_num, team1, team2, history_inf)

    match_bp_frame = BpFrame()
    match_bp_frame.Show(True)


def load_regular_game_10ban_3plus2(match_id, team_blue, team_red, game_num, heroes_all_list, max_game_num, team1, team2,
                                   history_inf):
    class HistoryInf(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None,
                              title='WBW的BP模拟器【历史阵容】', size=(1500, 900))
            display_idx = wx.Display.GetFromPoint(wx.GetMousePosition())
            # 获取该屏幕的几何信息（x, y, width, height）
            display_rect = wx.Display(display_idx).GetGeometry()
            win_width, win_height = self.GetSize()
            pos_x = display_rect.x + (display_rect.width - win_width) // 2
            pos_y = display_rect.y + (display_rect.height - win_height) // 2
            self.SetPosition((pos_x, pos_y))  # 设置窗口位置

            self.final_hero_pos = 0
            self.Center()
            self.panel = wx.Panel(self)
            self.pbox = wx.BoxSizer(wx.VERTICAL)
            show_heroes_ban_blue_list = [0, 2, 4, 13, 15]
            show_heroes_ban_red_list = [14, 12, 5, 3, 1]
            show_heroes_pick_blue_list = [6, 9, 10, 17, 18]
            show_heroes_pick_red_list = [19, 16, 11, 8, 7]
            for i in range(game_num - 1):
                game_box = wx.BoxSizer(wx.HORIZONTAL)
                self.pbox.Add(game_box, 1, wx.Center)
                blue_box = wx.BoxSizer(wx.VERTICAL)
                red_box = wx.BoxSizer(wx.VERTICAL)
                game_box.Add(blue_box, 0, wx.Center)
                game_box.Add((300, 0), 1, wx.EXPAND, 0)
                game_box.Add(red_box, 0, wx.Center)
                blue_ban_box = wx.BoxSizer(wx.HORIZONTAL)
                blue_pick_box = wx.BoxSizer(wx.HORIZONTAL)
                red_ban_box = wx.BoxSizer(wx.HORIZONTAL)
                red_pick_box = wx.BoxSizer(wx.HORIZONTAL)
                blue_box.Add(blue_ban_box, 0)
                blue_box.Add(blue_pick_box, 0)
                red_box.Add(red_ban_box, 0, flag=wx.ALIGN_RIGHT)
                red_box.Add(red_pick_box, 0, flag=wx.ALIGN_RIGHT)
                team_blue_text = wx.StaticText(self.panel, -1, label=history_inf[i][0])
                team_red_text = wx.StaticText(self.panel, -1, label=history_inf[i][1])
                red_ban_box.Add(team_red_text, 0, flag=wx.CENTRE)
                for j in show_heroes_ban_blue_list:
                    self.bmp = wx.Image('heroes\\icon\\' + history_inf[i][j + 3] + '.jpg',
                                        wx.BITMAP_TYPE_ANY).ConvertToGreyscale().Scale(70, 70).ConvertToBitmap()
                    self.bitmap = wx.StaticBitmap(self.panel, wx.ID_ANY, self.bmp)
                    blue_ban_box.Add(self.bitmap, 1)

                for j in show_heroes_pick_blue_list:
                    self.bmp = wx.Image('heroes\\icon\\' + history_inf[i][j + 3] + '.jpg',
                                        wx.BITMAP_TYPE_ANY).Scale(110, 110).ConvertToBitmap()
                    self.bitmap = wx.StaticBitmap(self.panel, wx.ID_ANY, self.bmp)
                    blue_pick_box.Add(self.bitmap, 1)
                for j in show_heroes_ban_red_list:
                    self.bmp = wx.Image('heroes\\icon\\' + history_inf[i][j + 3] + '.jpg',
                                        wx.BITMAP_TYPE_ANY).ConvertToGreyscale().Scale(70, 70).ConvertToBitmap()
                    self.bitmap = wx.StaticBitmap(self.panel, wx.ID_ANY, self.bmp)
                    red_ban_box.Add(self.bitmap, 1)
                for j in show_heroes_pick_red_list:
                    self.bmp = wx.Image('heroes\\icon\\' + history_inf[i][j + 3] + '.jpg',
                                        wx.BITMAP_TYPE_ANY).Scale(110, 110).ConvertToBitmap()
                    self.bitmap = wx.StaticBitmap(self.panel, wx.ID_ANY, self.bmp)
                    red_pick_box.Add(self.bitmap, 1)
                blue_ban_box.Add(team_blue_text, 0, flag=wx.CENTRE)
                self.panel.SetSizer(self.pbox)

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
            # 设置边框颜色和宽度
            border_color = self.colour  # 边框
            dc.SetPen(wx.Pen(border_color, 1))  # 设置边框颜色和宽度
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            # 绘制一个矩形边框
            width, height = self.GetSize()
            dc.DrawRectangle(-4, -4, width, height)

    class BpFrame(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None,
                              title='WBW的BP模拟器【BO' + str(max_game_num) + '第' + str(game_num) + '局】')

            self.SetMinSize((1500, 900))
            display_idx = wx.Display.GetFromPoint(wx.GetMousePosition())
            # 获取该屏幕的几何信息（x, y, width, height）
            display_rect = wx.Display(display_idx).GetGeometry()
            win_width, win_height = self.GetSize()
            pos_x = display_rect.x + (display_rect.width - win_width) // 2
            pos_y = display_rect.y + (display_rect.height - win_height) // 2
            self.SetPosition((pos_x, pos_y))  # 设置窗口位置
            self.career_list = []
            self.final_hero_pos = 0
            self.Center()
            self.pos = 0
            self.bp_sequence = ['0'] * 20
            self.select_work = 0
            self.Maximize(True)
            self.panel = wx.Panel(self)
            self.pbox = wx.BoxSizer(wx.VERTICAL)
            select_pos_box = wx.BoxSizer()
            button_box = wx.BoxSizer()
            view_history_game_btn = wx.Button(self.panel, label='显示历史阵容')
            view_history_game_btn.Bind(wx.EVT_BUTTON, self.onClickViewHistory)
            # self.resize_panel_btn = wx.Button(self.panel, label='适应面板大小')
            # self.resize_panel_btn.Bind(wx.EVT_BUTTON, self.OnClickedResize)
            if game_num != max_game_num:
                next_game_btn = wx.Button(self.panel, label='下一局')
            else:
                next_game_btn = wx.Button(self.panel, label='结束')
            button_box.Add(next_game_btn, 0, flag=wx.CENTER)
            next_game_btn.Bind(wx.EVT_BUTTON, self.OnClickedNext)
            button_box.Add(view_history_game_btn, 0, flag=wx.CENTER)
            # button_box.Add(self.resize_panel_btn, 0, flag=wx.CENTER)
            bp_board_box = wx.BoxSizer()
            ban_blue_box = wx.BoxSizer()
            ban_red_box = wx.BoxSizer()
            pick_blue_box = wx.BoxSizer()
            pick_red_box = wx.BoxSizer()
            blue_box = wx.BoxSizer(wx.VERTICAL)
            red_box = wx.BoxSizer(wx.VERTICAL)
            self.pbox.Add(select_pos_box, 0, flag=wx.ALIGN_CENTER)
            self.hero_grid_panel = wx.ScrolledWindow(self.panel, size=(900, 550))
            self.hero_grid_panel.SetScrollRate(5, 20)
            self.hero_grid = wx.GridSizer(20, 7, 2, 2)
            self.hero_grid_panel.SetSizer(self.hero_grid)

            self.career_text_list = []

            with open('heroes\\hero_settings.csv', 'r', newline='') as setting_csv:
                reader = csv.reader(setting_csv)
                for i in reader:
                    self.career_text_list.append(i)
            self.select_career_btn_list = []
            self.select_all_btn = wx.Button(self.panel, label='全部', size=(100, 50))
            select_pos_box.Add(self.select_all_btn, 1, wx.ALIGN_CENTER)
            self.select_career_btn_list.append(self.select_all_btn)
            self.select_all_btn.Bind(wx.EVT_BUTTON,
                                     lambda event, pram1='全部': self.OnClickedSelectCareer(event, pram1))
            btn_num = 0
            for i in self.career_text_list:
                self.select_career_btn = wx.Button(self.panel, label=i[0], size=(100, 50))
                select_pos_box.Add(self.select_career_btn, 1, wx.ALIGN_CENTER)
                self.select_career_btn_list.append(self.select_career_btn)
                self.select_career_btn.Bind(wx.EVT_BUTTON,
                                            lambda event, pram1=i[0]: self.OnClickedSelectCareer(event, pram1))
                btn_num = btn_num + 1
            self.load_hero_event = wx.CommandEvent(wx.EVT_BUTTON.typeId, self.select_career_btn_list[1].GetId())
            wx.PostEvent(self.select_career_btn_list[0], self.load_hero_event)
            self.pbox.Add(self.hero_grid_panel, 1, flag=wx.EXPAND)
            # self.pbox.Add((0, 1), 1, wx.EXPAND, 0)
            self.pbox.Add(button_box, 0, flag=wx.ALIGN_CENTER)
            self.pbox.Add(bp_board_box, 0, flag=wx.ALIGN_CENTER)
            bmp1 = wx.Image('image\\select_ban.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            select1 = SelectButton(self.panel, -1, bmp1)
            select2 = SelectButton(self.panel, -1, bmp1)
            select3 = SelectButton(self.panel, -1, bmp1)
            select4 = SelectButton(self.panel, -1, bmp1)
            select11 = SelectButton(self.panel, -1, bmp1)
            select12 = SelectButton(self.panel, -1, bmp1)
            select13 = SelectButton(self.panel, -1, bmp1)
            select14 = SelectButton(self.panel, -1, bmp1)
            select_10ban_ban1 = SelectButton(self.panel, -1, bmp1)
            select_10ban_ban2 = SelectButton(self.panel, -1, bmp1)
            team_blue_text = wx.StaticText(self.panel, -1, label=team_blue)
            team_red_text = wx.StaticText(self.panel, -1, label=team_red)
            team_text_font = wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
            team_blue_text.SetFont(team_text_font)
            team_red_text.SetFont(team_text_font)
            ban_blue_box.Add(select1, 0, flag=wx.ALIGN_LEFT)
            ban_blue_box.Add(select3, 0, flag=wx.ALIGN_LEFT)
            ban_blue_box.Add(select_10ban_ban1, 0, flag=wx.ALIGN_LEFT)
            ban_blue_box.Add(select12, 0, flag=wx.ALIGN_LEFT)
            ban_blue_box.Add(select14, 0, flag=wx.ALIGN_LEFT)
            ban_blue_box.Add(team_blue_text, 0, flag=wx.CENTRE)
            ban_red_box.Add(team_red_text, 0, flag=wx.CENTRE)
            ban_red_box.Add(select13, 0, flag=wx.ALIGN_LEFT)
            ban_red_box.Add(select11, 0, flag=wx.ALIGN_LEFT)
            ban_red_box.Add(select_10ban_ban2, 0, flag=wx.ALIGN_LEFT)
            ban_red_box.Add(select4, 0, flag=wx.ALIGN_LEFT)
            ban_red_box.Add(select2, 0, flag=wx.ALIGN_LEFT)
            select_pick_bmp = wx.Image('image\\select_pick.png', wx.BITMAP_TYPE_ANY).Scale(110, 110).ConvertToBitmap()
            select5 = SelectButton(self.panel, -1, select_pick_bmp)
            select8 = SelectButton(self.panel, -1, select_pick_bmp)
            select9 = SelectButton(self.panel, -1, select_pick_bmp)
            select16 = SelectButton(self.panel, -1, select_pick_bmp)
            select17 = SelectButton(self.panel, -1, select_pick_bmp)
            select6 = SelectButton(self.panel, -1, select_pick_bmp)
            select7 = SelectButton(self.panel, -1, select_pick_bmp)
            select10 = SelectButton(self.panel, -1, select_pick_bmp)
            select15 = SelectButton(self.panel, -1, select_pick_bmp)
            select18 = SelectButton(self.panel, -1, select_pick_bmp)
            self.select_button = [select1, select2, select3, select4, select_10ban_ban1, select_10ban_ban2, select5,
                                  select6, select7, select8, select9,
                                  select10, select11, select12, select13,
                                  select14, select15, select16, select17,
                                  select18]
            select1.Bind(wx.EVT_BUTTON, lambda event, pram1=0: self.onChoosePos(event, pram1))
            select2.Bind(wx.EVT_BUTTON, lambda event, pram1=1: self.onChoosePos(event, pram1))
            select3.Bind(wx.EVT_BUTTON, lambda event, pram1=2: self.onChoosePos(event, pram1))
            select4.Bind(wx.EVT_BUTTON, lambda event, pram1=3: self.onChoosePos(event, pram1))
            select5.Bind(wx.EVT_BUTTON, lambda event, pram1=6: self.onChoosePos(event, pram1))
            select6.Bind(wx.EVT_BUTTON, lambda event, pram1=7: self.onChoosePos(event, pram1))
            select7.Bind(wx.EVT_BUTTON, lambda event, pram1=8: self.onChoosePos(event, pram1))
            select8.Bind(wx.EVT_BUTTON, lambda event, pram1=9: self.onChoosePos(event, pram1))
            select9.Bind(wx.EVT_BUTTON, lambda event, pram1=10: self.onChoosePos(event, pram1))
            select10.Bind(wx.EVT_BUTTON, lambda event, pram1=11: self.onChoosePos(event, pram1))
            select_10ban_ban1.Bind(wx.EVT_BUTTON, lambda event, pram1=4: self.onChoosePos(event, pram1))
            select_10ban_ban2.Bind(wx.EVT_BUTTON, lambda event, pram1=5: self.onChoosePos(event, pram1))
            select11.Bind(wx.EVT_BUTTON, lambda event, pram1=12: self.onChoosePos(event, pram1))
            select12.Bind(wx.EVT_BUTTON, lambda event, pram1=13: self.onChoosePos(event, pram1))
            select13.Bind(wx.EVT_BUTTON, lambda event, pram1=14: self.onChoosePos(event, pram1))
            select14.Bind(wx.EVT_BUTTON, lambda event, pram1=15: self.onChoosePos(event, pram1))
            select15.Bind(wx.EVT_BUTTON, lambda event, pram1=16: self.onChoosePos(event, pram1))
            select16.Bind(wx.EVT_BUTTON, lambda event, pram1=17: self.onChoosePos(event, pram1))
            select17.Bind(wx.EVT_BUTTON, lambda event, pram1=18: self.onChoosePos(event, pram1))
            select18.Bind(wx.EVT_BUTTON, lambda event, pram1=19: self.onChoosePos(event, pram1))
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
            self.panel.SetSizer(self.pbox)

        # def OnClickedResize(self, event):
        #     width, height = self.GetSize()
        #     self.hero_grid_panel.SetSize(width - 25, height - 300)

        def OnClickedSelectCareer(self, event, career):
            buttons = []
            blue_select_list = [1, 3, 5, 6, 9, 10, 12, 14, 17, 18]
            red_select_list = [0, 2, 4, 7, 8, 11, 13, 15, 16, 19]
            if team_blue == team1:
                team1_num = 11
                team2_num = 12
            else:
                team1_num = 12
                team2_num = 11
            for item in self.hero_grid.GetChildren():
                item.GetWindow().Destroy()  # 删除每个控件
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
            # resize_hero_event = wx.CommandEvent(wx.EVT_BUTTON.typeId, self.resize_panel_btn.GetId())
            # wx.PostEvent(self.resize_panel_btn, resize_hero_event)
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

        def onClickViewHistory(self, event):
            history_inf_frame = HistoryInf()
            history_inf_frame.Show()

        def OnClickedNext(self, event):
            if self.final_hero_pos == 1:
                save_list = [[match_id, str(max_game_num), str(game_num), team_blue, team_red, '3+2']]
                save_list[0].extend(self.bp_sequence)
                with open('save\\save.csv', mode='r') as read_file:
                    reader = csv.reader(read_file)
                    for row in reader:
                        save_list.append(row)
                with open('save\\save.csv', mode='w', newline='') as file:
                    writer = csv.writer(file)
                    for i in save_list:
                        writer.writerow(i)
                new_list = ([team_blue, team_red, '10ban'])
                new_list.extend(self.bp_sequence)
                history_inf.append(new_list)

                next_game = NextGame()
                next_game.Show()
                self.Close()
            else:
                mgb = wx.MessageBox('对局尚未结束！', '提示', wx.OK | wx.ICON_INFORMATION)

        def onClickSelect(self, event, id):
            ban_list = [0, 1, 2, 3, 4, 5, 12, 13, 14, 15]
            blue_pick_list = [6, 9, 10, 17, 18]
            red_pick_list = [7, 8, 11, 16, 19]
            if self.pos == 19:
                self.final_hero_pos = 1
            if self.pos in ban_list:
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
            if self.pos != 20:
                choose_pos_event = wx.CommandEvent(wx.EVT_BUTTON.typeId, self.select_button[self.pos].GetId())
                wx.PostEvent(self.select_button[self.pos], choose_pos_event)
            else:
                self.select_button[-1].colour = wx.Colour(255, 255, 255)
            wx.PostEvent(self.select_career_btn_list[self.select_work], self.load_hero_event)

    class NextGame(wx.Frame):
        def __init__(self):
            if game_num != max_game_num:
                wx.Frame.__init__(self, None, title='下一局', size=(200, 200))
    
                self.Center()
                self.panel = wx.Panel(self)
                vbox = wx.BoxSizer(wx.VERTICAL)
                choices_list = ['是', '否']
                choices_list2 = ['否', '是']
                self.change_box = wx.RadioBox(self.panel, label='是否换边', choices=choices_list)
                self.normal_box = wx.RadioBox(self.panel, label='巅峰对决', choices=choices_list2)
                ok_button = wx.Button(self.panel, label='确认')
                vbox.Add(self.change_box, 0, wx.ALIGN_CENTER)
                vbox.Add(self.normal_box, 0, wx.ALIGN_CENTER)
                vbox.Add(ok_button, 0, wx.ALIGN_CENTER)
                ok_button.Bind(wx.EVT_BUTTON, self.onNextGame)
            else:
                wx.Frame.__init__(self, None, title='提醒', size=(210, 80))
    
                self.Center()
                self.panel = wx.Panel(self)
                vbox = wx.BoxSizer(wx.VERTICAL)
                exit_confirm_txt = wx.StaticText(self.panel, label='比赛结束')
                ok_button = wx.Button(self.panel, label='确认')
                vbox.Add(exit_confirm_txt, 0, wx.ALIGN_CENTER)
                vbox.Add(ok_button, 0, wx.ALIGN_CENTER)
                ok_button.Bind(wx.EVT_BUTTON, self.onExit)
            display_idx = wx.Display.GetFromPoint(wx.GetMousePosition())
            # 获取该屏幕的几何信息（x, y, width, height）
            display_rect = wx.Display(display_idx).GetGeometry()
            win_width, win_height = self.GetSize()
            pos_x = display_rect.x + (display_rect.width - win_width) // 2
            pos_y = display_rect.y + (display_rect.height - win_height) // 2
            self.SetPosition((pos_x, pos_y))  # 设置窗口位置
            self.panel.SetSizer(vbox)

        def onExit(self, event):
            self.Close()

        def onNextGame(self, event):
            if self.change_box.GetSelection() == 0:
                team_b = team_red
                team_r = team_blue
            else:
                team_r = team_red
                team_b = team_blue
            for hero in heroes_all_list:
                hero[13] = '0'
                hero[14] = '0'
            if self.normal_box.GetSelection() == 0:
                game_mode_next = 1
            else:
                game_mode_next = 0
            self.Close()
            load_game(match_id, game_mode_next, 100, team_b, team_r, game_num + 1, heroes_all_list,
                      max_game_num, team1, team2, history_inf)

    match_bp_frame = BpFrame()
    match_bp_frame.Show(True)


def load_game(match_id, game_mode, ban_num, team_blue, team_red, game_num, heroes_all_list, max_game_num, team1, team2,
              history_inf):
    if game_mode == 0:
        load_final_game(match_id, team_blue, team_red, game_num, heroes_all_list, max_game_num, team1,
                        team2,
                        history_inf)
    if game_mode == 1:
        if ban_num == 8:
            load_regular_game_8ban(match_id, team_blue, team_red, game_num, heroes_all_list, max_game_num, team1,
                                   team2,
                                   history_inf)
        if ban_num == 10:
            load_regular_game_10ban(match_id, team_blue, team_red, game_num, heroes_all_list, max_game_num,
                                    team1,
                                    team2, history_inf)
        if ban_num == 0:
            load_regular_game_0ban(match_id, team_blue, team_red, game_num, heroes_all_list, max_game_num, team1,
                                   team2,
                                   history_inf)
        if ban_num == 100:
            load_regular_game_10ban_3plus2(match_id, team_blue, team_red, game_num, heroes_all_list, max_game_num,
                                           team1,
                                           team2,
                                           history_inf)


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
