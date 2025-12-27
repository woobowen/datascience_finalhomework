import copy
import csv
from datetime import datetime

import wx

import my_match

heroes_all_list = []
hero_settings_list = []
with open('heroes\\hero_settings.csv', 'r') as hero_settings_csv:
    hero_settings_csv_reader = csv.reader(hero_settings_csv)
    for hero_order in hero_settings_csv_reader:
        hero_settings_list.append(hero_order)
with open('heroes\\heroes.csv') as heroes_csv:
    heroes_csv_reader = csv.reader(heroes_csv)
    for row in heroes_csv_reader:
        heroes_all_list.append(row)


class DeleteCareer(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, '提醒', size=(250, 90),
                          style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        display_idx = wx.Display.GetFromPoint(wx.GetMousePosition())
        # 获取该屏幕的几何信息（x, y, width, height）
        display_rect = wx.Display(display_idx).GetGeometry()
        win_width, win_height = self.GetSize()
        pos_x = display_rect.x + (display_rect.width - win_width) // 2
        pos_y = display_rect.y + (display_rect.height - win_height) // 2
        self.SetPosition((pos_x, pos_y))  # 设置窗口位置
        self.SetIcon(wx.Icon("image\\WhiteWolfBP.ico", wx.BITMAP_TYPE_ICO))
        self.Center()
        self.panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(vbox)
        self.confirm_text = wx.StaticText(self.panel, label='是否确认删除？')
        hbox = wx.BoxSizer()
        vbox.Add(self.confirm_text, 0, wx.ALIGN_CENTER)
        vbox.Add(hbox, 0, wx.ALIGN_CENTER)
        ok_btn = wx.Button(self.panel, label='确认')
        cancel_btn = wx.Button(self.panel, label='取消')
        hbox.Add(ok_btn, 0, wx.ALIGN_CENTER)
        hbox.Add(cancel_btn, 0, wx.ALIGN_CENTER)
        self.career_list = []
        ok_btn.Bind(wx.EVT_BUTTON, self.OnClickOk)
        cancel_btn.Bind(wx.EVT_BUTTON, self.OnClickCancel)
        self.Show()

    def OnClickOk(self, event):
        self.Close()
        with open('heroes\\hero_settings.csv', 'r', newline='') as infile:
            reader = csv.reader(infile)
            for line in reader:
                self.career_list.append(line)
        self.career_list.pop()
        with open('heroes\\hero_settings.csv', 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(self.career_list)
            main_frame.main_change.career_list.pop()
            main_frame.main_change.init()

    def OnClickCancel(self, event):
        self.Close()


class AddCareer(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, '设置', size=(250, 120), pos=(400, 400),
                          style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        display_idx = wx.Display.GetFromPoint(wx.GetMousePosition())
        # 获取该屏幕的几何信息（x, y, width, height）
        display_rect = wx.Display(display_idx).GetGeometry()
        win_width, win_height = self.GetSize()
        pos_x = display_rect.x + (display_rect.width - win_width) // 2
        pos_y = display_rect.y + (display_rect.height - win_height) // 2
        self.SetPosition((pos_x, pos_y))  # 设置窗口位置
        self.SetIcon(wx.Icon("image\\WhiteWolfBP.ico", wx.BITMAP_TYPE_ICO))
        self.Center()
        self.career_list = []
        self.panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(hbox)
        self.career_sb = wx.StaticBox(self.panel, label='请输入分组名：')
        self.career_sb_sizer = wx.StaticBoxSizer(self.career_sb, wx.VERTICAL)
        self.career_name_text = wx.TextCtrl(self.panel)
        self.career_sb_sizer.Add(self.career_name_text, 0, wx.ALIGN_CENTER)
        hbox.Add(self.career_sb_sizer, 0, wx.ALIGN_CENTER)
        self.ok_btn = wx.Button(self.panel, label='确定')
        hbox.Add(self.ok_btn, 0, wx.ALIGN_CENTER)
        self.ok_btn.Bind(wx.EVT_BUTTON, self.OnClickConfirm)
        self.Show()

    def OnClickConfirm(self, event):
        self.Close()
        with open('heroes\\hero_settings.csv', 'r', newline='') as infile:
            reader = csv.reader(infile)
            for line in reader:
                self.career_list.append(line)
        self.career_list.append([self.career_name_text.GetValue()])
        with open('heroes\\hero_settings.csv', 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(self.career_list)
        main_frame.main_change.career_list.append([self.career_name_text.GetValue()])
        main_frame.main_change.init()


class MainChange(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, '英雄偏好设置', size=(400, 400),
                          style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        display_idx = wx.Display.GetFromPoint(wx.GetMousePosition())
        # 获取该屏幕的几何信息（x, y, width, height）
        display_rect = wx.Display(display_idx).GetGeometry()
        win_width, win_height = self.GetSize()
        pos_x = display_rect.x + (display_rect.width - win_width) // 2
        pos_y = display_rect.y + (display_rect.height - win_height) // 2
        self.SetPosition((pos_x, pos_y))  # 设置窗口位置
        self.SetIcon(wx.Icon("image\\WhiteWolfBP.ico", wx.BITMAP_TYPE_ICO))
        self.edit_order = ''
        self.Center()
        self.hero_list_frame = None
        self.panel = wx.Panel(self)
        hbox = wx.BoxSizer()
        self.panel.SetSizer(hbox)
        self.select_career = wx.ScrolledWindow(self.panel, size=(300, 400))
        self.select_career.SetScrollRate(0, 5)
        self.select_career_vbox = wx.BoxSizer(wx.VERTICAL)
        self.select_career.SetSizer(self.select_career_vbox)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox.Add(self.select_career, 3)
        hbox.Add(vbox, 1)
        edit_btn = wx.Button(self.panel, label='编辑')
        add_btn = wx.Button(self.panel, label='添加')
        delete_btn = wx.Button(self.panel, label='删除')
        vbox.Add(edit_btn, 0)
        vbox.Add(add_btn, 0)
        vbox.Add(delete_btn, 0)
        self.career_list = []
        edit_btn.Bind(wx.EVT_BUTTON, self.edit_career)
        add_btn.Bind(wx.EVT_BUTTON, self.add_career)
        delete_btn.Bind(wx.EVT_BUTTON, self.delete_career)
        with open('heroes\\hero_settings.csv', 'r', newline='') as infile:
            reader = csv.reader(infile)
            for line in reader:
                self.career_list.append(line)
        self.choices_list = []
        self.choices_list = []
        for i in self.career_list:
            self.choices_list.append(i[0])
        self.choice_career_radio_box = wx.RadioBox(self.select_career, label='设置英雄分组',
                                                   choices=self.choices_list,
                                                   style=wx.RA_VERTICAL, majorDimension=len(self.choices_list),
                                                   size=(300, 400))
        self.init()
        self.Show()

    def init(self):
        self.choices_list = []
        for i in self.career_list:
            self.choices_list.append(i[0])
        self.select_career_vbox.Clear()
        self.choice_career_radio_box.Destroy()
        self.choice_career_radio_box = wx.RadioBox(self.select_career, label='设置英雄分组',
                                                   choices=self.choices_list,
                                                   style=wx.RA_VERTICAL, majorDimension=len(self.choices_list),
                                                   size=(300, 400))
        self.select_career_vbox.Add(self.choice_career_radio_box, 0)
        self.edit_order = ''
        self.choice_career_radio_box.Layout()
        self.panel.Layout()
        self.select_career_vbox.Layout()

    def edit_career(self, event):
        self.edit_order = self.career_list[self.choice_career_radio_box.GetSelection()][0]
        self.hero_list_frame = HeroListSetting()
        print(self.hero_list_frame)

    def add_career(self, event):
        self.add_career_frame = AddCareer()

    def delete_career(self, event):
        self.delete_career_frame = DeleteCareer()


class Confirm(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, '提醒', size=(250, 90),
                          style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        display_idx = wx.Display.GetFromPoint(wx.GetMousePosition())
        # 获取该屏幕的几何信息（x, y, width, height）
        display_rect = wx.Display(display_idx).GetGeometry()
        win_width, win_height = self.GetSize()
        pos_x = display_rect.x + (display_rect.width - win_width) // 2
        pos_y = display_rect.y + (display_rect.height - win_height) // 2
        self.SetPosition((pos_x, pos_y))  # 设置窗口位置
        self.SetIcon(wx.Icon("image\\WhiteWolfBP.ico", wx.BITMAP_TYPE_ICO))
        self.panel = wx.Panel(self)
        self.Center()
        vbox = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(self.panel, label='是否确认保存')
        hbox = wx.BoxSizer()
        self.panel.SetSizer(vbox)
        vbox.Add(text, 1, wx.ALIGN_CENTER)
        vbox.Add(hbox, 1, wx.ALIGN_CENTER)
        ok_button = wx.Button(self.panel, label='确认')
        cancel_button = wx.Button(self.panel, label='取消')
        hbox.Add(ok_button, 0)
        hbox.Add(cancel_button, 0)
        ok_button.Bind(wx.EVT_BUTTON, self.confirm_frame)
        cancel_button.Bind(wx.EVT_BUTTON, self.close_frame)
        self.Show()

    def close_frame(self, event):
        self.Close()

    def confirm_frame(self, event):
        self.Close()
        main_frame.main_change.hero_list_frame.Close()
        heroes = []
        main_frame.main_change.hero_list_frame.new_hero_panels_list[
            0] = main_frame.main_change.hero_list_frame.edit_order
        with open('heroes\\hero_settings.csv', 'r', newline='') as infile:
            reader = csv.reader(infile)
            for line in reader:
                heroes.append(line)
            for i, v in enumerate(heroes):
                if v[0] == main_frame.main_change.edit_order:
                    heroes[i] = main_frame.main_change.hero_list_frame.new_hero_panels_list
        with open('heroes\\hero_settings.csv', 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(heroes)


class AddHeroFrame(wx.Frame):
    def __init__(self, tmp_new_hero_list):
        wx.Frame.__init__(self, None, wx.ID_ANY, "新增英雄【" + main_frame.main_change.hero_list_frame.edit_order + '】',
                          size=(1000, 415),
                          style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        display_idx = wx.Display.GetFromPoint(wx.GetMousePosition())
        # 获取该屏幕的几何信息（x, y, width, height）
        display_rect = wx.Display(display_idx).GetGeometry()
        win_width, win_height = self.GetSize()
        pos_x = display_rect.x + (display_rect.width - win_width) // 2
        pos_y = display_rect.y + (display_rect.height - win_height) // 2
        self.SetPosition((pos_x, pos_y))  # 设置窗口位置
        self.SetIcon(wx.Icon("image\\WhiteWolfBP.ico", wx.BITMAP_TYPE_ICO))
        self.panel = wx.Panel(self)
        self.Center()
        vbox = wx.BoxSizer(wx.VERTICAL)
        hero_grid = wx.GridSizer(19, 8, 1, 1)
        ok_btn = wx.Button(self.panel, label='确定')
        self.hero_cbs = []
        print(tmp_new_hero_list)
        for hero in heroes_all_list:
            if hero[0] not in tmp_new_hero_list and hero[1] != '' and hero[1] != '英雄':
                self.hero_cb = wx.CheckBox(self.panel, label=hero[1])
                self.hero_cbs.append(self.hero_cb)
                hero_grid.Add(self.hero_cb, 0)
        vbox.Add(hero_grid, 0, wx.ALIGN_CENTER)
        vbox.Add(ok_btn, 0, wx.ALIGN_CENTER)
        ok_btn.Bind(wx.EVT_BUTTON, self.OnClickOk)
        self.panel.SetSizer(vbox)
        self.Show()

    def OnClickOk(self, event):
        add_list = []
        for i in self.hero_cbs:
            if i.GetValue():
                for j in heroes_all_list:
                    if j[1] == i.GetLabel():
                        add_list.append(j[0])
        self.Close()
        main_frame.main_change.hero_list_frame.new_hero_panels_list.extend(add_list)
        main_frame.main_change.hero_list_frame.old_hero_panels_list.extend(add_list)
        main_frame.main_change.hero_list_frame.num = len(main_frame.main_change.hero_list_frame.hero_panels)
        for i in add_list:
            main_frame.main_change.hero_list_frame.hero_penal = wx.Panel(
                main_frame.main_change.hero_list_frame.order_panel)
            main_frame.main_change.hero_list_frame.hero_penal_box = wx.BoxSizer(wx.VERTICAL)
            main_frame.main_change.hero_list_frame.hero_box = wx.BoxSizer()
            main_frame.main_change.hero_list_frame.hero_penal.SetSizer(
                main_frame.main_change.hero_list_frame.hero_penal_box)
            main_frame.main_change.hero_list_frame.delete_button = wx.Button(
                main_frame.main_change.hero_list_frame.hero_penal, size=(20, 20),
                label='×')
            hero_name_list = wx.StaticText(main_frame.main_change.hero_list_frame.hero_penal,
                                           label=heroes_all_list[int(i)][1])
            main_frame.main_change.hero_list_frame.move_top = wx.Button(
                main_frame.main_change.hero_list_frame.hero_penal, label='↑')
            main_frame.main_change.hero_list_frame.move_top1 = wx.Button(
                main_frame.main_change.hero_list_frame.hero_penal, label='↑↑')
            main_frame.main_change.hero_list_frame.move_bot1 = wx.Button(
                main_frame.main_change.hero_list_frame.hero_penal, label='↓↓')
            main_frame.main_change.hero_list_frame.delete_button.Bind(wx.EVT_BUTTON,
                                                                      lambda event,
                                                                             pram=main_frame.main_change.hero_list_frame.num: main_frame.main_change.hero_list_frame.onClickDelete(
                                                                          event, pram))
            main_frame.main_change.hero_list_frame.move_top.Bind(wx.EVT_BUTTON,
                                                                 lambda event,
                                                                        pram=main_frame.main_change.hero_list_frame.num: main_frame.main_change.hero_list_frame.onClickMoveTop(
                                                                     event, pram))
            main_frame.main_change.hero_list_frame.move_top1.Bind(wx.EVT_BUTTON,
                                                                  lambda event,
                                                                         pram=main_frame.main_change.hero_list_frame.num: main_frame.main_change.hero_list_frame.onClickMoveTop1(
                                                                      event, pram))
            main_frame.main_change.hero_list_frame.move_bot1.Bind(wx.EVT_BUTTON,
                                                                  lambda event,
                                                                         pram=main_frame.main_change.hero_list_frame.num: main_frame.main_change.hero_list_frame.onClickMoveBot1(
                                                                      event, pram))
            main_frame.main_change.hero_list_frame.hero_box.Add(main_frame.main_change.hero_list_frame.delete_button, 0,
                                                                wx.ALIGN_CENTER)
            main_frame.main_change.hero_list_frame.hero_box.Add(hero_name_list, 3, wx.ALIGN_CENTER)
            main_frame.main_change.hero_list_frame.hero_box.Add(main_frame.main_change.hero_list_frame.move_top1, 1,
                                                                wx.ALIGN_CENTER)
            main_frame.main_change.hero_list_frame.hero_box.Add(main_frame.main_change.hero_list_frame.move_bot1, 1,
                                                                wx.ALIGN_CENTER)
            main_frame.main_change.hero_list_frame.delete_buttons.append(
                main_frame.main_change.hero_list_frame.delete_button)
            main_frame.main_change.hero_list_frame.move_top_buttons.append(
                main_frame.main_change.hero_list_frame.move_top)
            main_frame.main_change.hero_list_frame.move_top1_buttons.append(
                main_frame.main_change.hero_list_frame.move_top1)
            main_frame.main_change.hero_list_frame.move_bot1_buttons.append(
                main_frame.main_change.hero_list_frame.move_bot1)
            main_frame.main_change.hero_list_frame.hero_panels.append(main_frame.main_change.hero_list_frame.hero_penal)
            main_frame.main_change.hero_list_frame.order_box.Add(main_frame.main_change.hero_list_frame.hero_penal, 0,
                                                                 wx.ALIGN_LEFT)
            main_frame.main_change.hero_list_frame.hero_penal_box.Add(main_frame.main_change.hero_list_frame.hero_box,
                                                                      0)
            main_frame.main_change.hero_list_frame.inner_panel = wx.Panel(
                main_frame.main_change.hero_list_frame.hero_penal, size=(400, 1))
            main_frame.main_change.hero_list_frame.inner_panel.SetBackgroundColour(wx.Colour(20, 0, 0))
            main_frame.main_change.hero_list_frame.hero_penal_box.Add(
                main_frame.main_change.hero_list_frame.inner_panel, 0)
            main_frame.main_change.hero_list_frame.num = main_frame.main_change.hero_list_frame.num + 1
        main_frame.main_change.hero_list_frame.order_panel.Layout()
        main_frame.main_change.hero_list_frame.order_box.Layout()
        main_frame.main_change.hero_list_frame.panel.Layout()


class ChangeNameFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "更改名称", size=(240, 90),
                          style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        display_idx = wx.Display.GetFromPoint(wx.GetMousePosition())
        # 获取该屏幕的几何信息（x, y, width, height）
        display_rect = wx.Display(display_idx).GetGeometry()
        win_width, win_height = self.GetSize()
        pos_x = display_rect.x + (display_rect.width - win_width) // 2
        pos_y = display_rect.y + (display_rect.height - win_height) // 2
        self.SetPosition((pos_x, pos_y))  # 设置窗口位置
        self.SetIcon(wx.Icon("image\\WhiteWolfBP.ico", wx.BITMAP_TYPE_ICO))
        self.panel = wx.Panel(self)
        self.Center()
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.name_text = wx.TextCtrl(self.panel, value=main_frame.main_change.hero_list_frame.edit_order)
        ok_btn = wx.Button(self.panel, label='确认')
        ok_btn.Bind(wx.EVT_BUTTON, self.ConfirmName)
        vbox.Add(self.name_text, 0, wx.ALIGN_CENTRE, )
        vbox.Add(ok_btn, 0, wx.ALIGN_CENTRE)
        self.panel.SetSizer(vbox)
        self.Show()

    def ConfirmName(self, event):
        self.Close()
        main_frame.main_change.hero_list_frame.edit_order = self.name_text.GetValue()
        main_frame.main_change.hero_list_frame.Title = "英雄顺序设置【" + main_frame.main_change.hero_list_frame.edit_order + '】'
        main_frame.main_change.hero_list_frame.Layout()


class HeroListSetting(wx.Frame):
    def __init__(self):
        self.edit_order = main_frame.main_change.edit_order
        wx.Frame.__init__(self, None, wx.ID_ANY, "英雄顺序设置【" + self.edit_order + '】', size=(440, 900),
                          style=wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX)
        self.SetIcon(wx.Icon("image\\WhiteWolfBP.ico", wx.BITMAP_TYPE_ICO))
        self.SetMinSize((440, 800))  # 最小尺寸
        self.SetMaxSize((440, 1000))  # 最大尺寸
        display_idx = wx.Display.GetFromPoint(wx.GetMousePosition())
        # 获取该屏幕的几何信息（x, y, width, height）
        display_rect = wx.Display(display_idx).GetGeometry()
        win_width, win_height = self.GetSize()
        pos_x = display_rect.x + (display_rect.width - win_width) // 2
        pos_y = display_rect.y + (display_rect.height - win_height) // 2
        self.SetPosition((pos_x, pos_y))  # 设置窗口位置
        self.panel = wx.Panel(self)
        self.Center()
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.order_panel = wx.ScrolledWindow(self.panel)
        self.order_panel.SetScrollRate(5, 10)
        vbox.Add(self.order_panel, 1, wx.EXPAND)
        vbox.Add((10, 10), 0)
        hbox = wx.BoxSizer()
        vbox.Add(hbox, 0, wx.CENTRE)
        change_name_btn = wx.Button(self.panel, label='更改分类名称')
        add_hero_btn = wx.Button(self.panel, label='添加新英雄')
        confirm_btn = wx.Button(self.panel, label='保存改动')
        change_name_btn.Bind(wx.EVT_BUTTON, self.ChangeName)
        add_hero_btn.Bind(wx.EVT_BUTTON, self.AddHero)
        confirm_btn.Bind(wx.EVT_BUTTON, self.Confirm)
        hbox.Add(change_name_btn, 0)
        hbox.Add(add_hero_btn, 0)
        hbox.Add(confirm_btn, 0)
        self.panel.SetSizer(vbox)
        self.order_box = wx.BoxSizer(wx.VERTICAL)
        self.delete_buttons = []
        self.move_top_buttons = []
        self.move_top1_buttons = []
        self.move_bot1_buttons = []
        self.hero_panels = []
        self.new_hero_panels_list = []
        self.old_hero_panels_list = []
        self.hero_settings_list = []
        with open('heroes\\hero_settings.csv', 'r') as self.hero_settings_csv:
            csv_reader = csv.reader(self.hero_settings_csv)
            for i in csv_reader:
                self.hero_settings_list.append(i)
        for hero_settings in self.hero_settings_list:
            if hero_settings[0] == self.edit_order:
                self.num = 0
                hero_settings_ini = [x for x in hero_settings if x != '']
                self.old_hero_panels_list = copy.copy(hero_settings_ini)
                self.new_hero_panels_list = copy.copy(hero_settings_ini)
                for hero_id in hero_settings:
                    if hero_id != hero_settings[0] and hero_id != '':
                        self.hero_penal = wx.Panel(self.order_panel)
                        self.hero_penal_box = wx.BoxSizer(wx.VERTICAL)
                        self.hero_box = wx.BoxSizer()
                        self.hero_penal.SetSizer(self.hero_penal_box)
                        self.delete_button = wx.Button(self.hero_penal, size=(20, 20), label='×')
                        hero_name_list = wx.StaticText(self.hero_penal, label=heroes_all_list[int(hero_id)][1])
                        self.move_top = wx.Button(self.hero_penal, label='↑')
                        self.move_top1 = wx.Button(self.hero_penal, label='↑↑')
                        self.move_bot1 = wx.Button(self.hero_penal, label='↓↓')
                        self.delete_button.Bind(wx.EVT_BUTTON,
                                                lambda event, pram=self.num: self.onClickDelete(event, pram))
                        self.move_top.Bind(wx.EVT_BUTTON,
                                           lambda event, pram=self.num: self.onClickMoveTop(event, pram))
                        self.move_top1.Bind(wx.EVT_BUTTON,
                                            lambda event, pram=self.num: self.onClickMoveTop1(event, pram))
                        self.move_bot1.Bind(wx.EVT_BUTTON,
                                            lambda event, pram=self.num: self.onClickMoveBot1(event, pram))
                        self.hero_box.Add(self.delete_button, 0, wx.ALIGN_CENTER)
                        self.hero_box.Add(hero_name_list, 3, wx.ALIGN_CENTER)
                        self.hero_box.Add(self.move_top1, 1, wx.ALIGN_CENTER)
                        self.hero_box.Add(self.move_bot1, 1, wx.ALIGN_CENTER)
                        self.delete_buttons.append(self.delete_button)
                        self.move_top_buttons.append(self.move_top)
                        self.move_top1_buttons.append(self.move_top1)
                        self.move_bot1_buttons.append(self.move_bot1)
                        self.hero_panels.append(self.hero_penal)
                        self.order_box.Add(self.hero_penal, 0, wx.ALIGN_LEFT)
                        self.hero_penal_box.Add(self.hero_box, 0)
                        self.inner_panel = wx.Panel(self.hero_penal, size=(400, 1))
                        self.inner_panel.SetBackgroundColour(wx.Colour(20, 0, 0))
                        self.hero_penal_box.Add(self.inner_panel, 0)
                        self.num = self.num + 1
        self.order_panel.SetSizer(self.order_box)
        self.Show()

    def Confirm(self, event):
        confirm_frame = Confirm()

    def ChangeName(self, event):
        change_name_frame = ChangeNameFrame()

    def AddHero(self, event):
        add_hero_frame = AddHeroFrame(self.new_hero_panels_list)

    def onClickDelete(self, event, num):
        self.new_hero_panels_list.remove(self.old_hero_panels_list[num + 1])
        print(self.new_hero_panels_list)
        self.order_box.Detach(self.hero_panels[num])
        self.hero_panels[num].Destroy()
        self.order_box.Layout()
        self.order_panel.Layout()
        self.Layout()
        self.panel.Layout()

    def onClickMoveTop(self, event, num):
        true_index = 0
        for index, value in enumerate(self.old_hero_panels_list):
            if self.old_hero_panels_list[num + 1] == value:
                true_index = index
        if self.old_hero_panels_list[true_index] != self.new_hero_panels_list[1]:
            for index, value in enumerate(self.new_hero_panels_list):
                if value == self.old_hero_panels_list[num + 1]:
                    tmp = self.new_hero_panels_list[index - 1]
                    self.new_hero_panels_list[index - 1] = self.new_hero_panels_list[index]
                    self.new_hero_panels_list[index] = tmp
                    print(self.new_hero_panels_list)
                    self.order_box.Detach(self.hero_panels[num])
                    for i, v in enumerate(self.new_hero_panels_list):
                        if v == self.new_hero_panels_list[index - 1]:
                            self.order_box.Insert(i - 1, self.hero_panels[num], 0)
                            break
                    break
            self.order_box.Layout()
        self.new_hero_panels_list = [x for x in self.new_hero_panels_list if x != '']

    def onClickMoveTop1(self, event, num):
        print(self.old_hero_panels_list[num + 1])
        self.new_hero_panels_list.remove(self.old_hero_panels_list[num + 1])
        self.new_hero_panels_list.insert(1, self.old_hero_panels_list[num + 1])
        print(self.new_hero_panels_list)
        self.order_box.Detach(self.hero_panels[num])
        self.order_box.Insert(0, self.hero_panels[num], 0)
        self.order_box.Layout()
        self.order_panel.Layout()
        self.Layout()
        self.panel.Layout()
        self.new_hero_panels_list = [x for x in self.new_hero_panels_list if x != '']

    def onClickMoveBot1(self, event, num):
        print(self.old_hero_panels_list[num + 1])
        self.new_hero_panels_list.remove(self.old_hero_panels_list[num + 1])
        self.new_hero_panels_list.append(self.old_hero_panels_list[num + 1])
        self.order_box.Detach(self.hero_panels[num])
        self.order_box.Add(self.hero_panels[num], 0)
        self.order_box.Layout()
        self.order_panel.Layout()
        self.Layout()
        self.panel.Layout()
        self.new_hero_panels_list = [x for x in self.new_hero_panels_list if x != '']


class ViewHistoryRecord(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None,
                          title='历史记录',
                          style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX), size=(900, 550))

        display_idx = wx.Display.GetFromPoint(wx.GetMousePosition())
        # 获取该屏幕的几何信息（x, y, width, height）
        display_rect = wx.Display(display_idx).GetGeometry()
        win_width, win_height = self.GetSize()
        pos_x = display_rect.x + (display_rect.width - win_width) // 2
        pos_y = display_rect.y + (display_rect.height - win_height) // 2
        self.SetPosition((pos_x, pos_y))  # 设置窗口位置

        self.SetIcon(wx.Icon("image\\WhiteWolfBP.ico", wx.BITMAP_TYPE_ICO))
        self.main_change = None
        self.panel = wx.Panel(self)
        self.Center()
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.history_record_window = wx.ScrolledWindow(self.panel, size=(900, 550))
        self.history_record_window.SetScrollRate(0, 20)
        vbox.Add(self.history_record_window, 0, wx.ALIGN_CENTER)
        self.vbox2 = wx.BoxSizer(wx.VERTICAL)
        self.save_list = []
        with open('save\\save.csv', 'r', newline='') as infile:
            reader = csv.reader(infile)
            for r in reader:
                self.save_list.append(r)
        match_id = 0
        self.save_list[0].insert(0, '0')
        for i, v in enumerate(self.save_list):
            try:
                if v[6] == '-1':
                    v[6] = '无BP'
                if v[3] == '1':
                    try:
                        match_id += 1
                        self.save_list[i + 1].insert(0, str(match_id))
                    except IndexError:
                        break
                else:
                    self.save_list[i + 1].insert(0, str(match_id))
            except IndexError:
                break
        view_history_num = 0
        line = wx.StaticLine(self.history_record_window, style=wx.LI_HORIZONTAL, size=(300, 2))
        line.SetBackgroundColour(wx.BLACK)  # 设置线颜色
        line.SetForegroundColour(wx.BLACK)  # 设置线颜色
        self.vbox2.Add(line, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)  # 添加线并设置间距
        for i, v in enumerate(self.save_list):
            if len(v) < 4:
                self.save_list.remove(v)
                continue
            if v[0] == str(view_history_num):

                self.view_game_info_sizer = wx.BoxSizer(wx.HORIZONTAL)

                self.game_mode_txt = wx.StaticText(self.history_record_window,
                                                   style=wx.TE_MULTILINE | wx.TE_RICH2 | wx.ALIGN_CENTER
                                                   , label=v[6] + '  BO' + v[2], size=(120, 23))

                font1 = wx.Font(
                    12,  # 字号
                    wx.FONTFAMILY_DEFAULT,  # 字体系列
                    wx.FONTSTYLE_NORMAL,  # 字体样式
                    wx.FONTWEIGHT_BOLD,  # 字体粗细(加粗)
                    False,  # 下划线
                    "微软雅黑")  # 字体名称
                font2 = wx.Font(
                    22,  # 字号
                    wx.FONTFAMILY_DEFAULT,  # 字体系列
                    wx.FONTSTYLE_NORMAL,  # 字体样式
                    wx.FONTWEIGHT_NORMAL,  # 字体粗细(加粗)
                    False,  # 下划线
                    "微软雅黑")  # 字体名称
                vs_font = wx.Font(
                    22,  # 字号
                    wx.FONTFAMILY_DEFAULT,  # 字体系列
                    wx.FONTSTYLE_NORMAL,  # 字体样式
                    wx.FONTWEIGHT_BOLD,  # 字体粗细(加粗)
                    False,  # 下划线
                    "Times New Roman")  # 字体名称
                font3 = wx.Font(
                    10,  # 字号
                    wx.FONTFAMILY_DEFAULT,  # 字体系列
                    wx.FONTSTYLE_NORMAL,  # 字体样式
                    wx.FONTWEIGHT_NORMAL,  # 字体粗细(加粗)
                    True,  # 下划线
                    "微软雅黑")  # 字体名称
                self.game_mode_txt.SetFont(font1)
                self.game_mode_txt.SetForegroundColour(wx.WHITE)
                if v[6] == '无BP':
                    self.game_mode_txt.SetBackgroundColour(wx.BLACK)
                if v[6] == '0ban':
                    self.game_mode_txt.SetBackgroundColour(wx.Colour('#737373'))
                if v[6] == '8ban':
                    self.game_mode_txt.SetBackgroundColour(wx.BLUE)
                if v[6] == '10ban':
                    self.game_mode_txt.SetBackgroundColour(wx.Colour('#A52A2A'))
                if v[6] == '3+2':
                    self.game_mode_txt.SetBackgroundColour(wx.GREEN)
                self.view_game_info_sizer.Add(self.game_mode_txt, 1, wx.ALIGN_CENTER)
                self.vbox2.Add(self.view_game_info_sizer, 1, wx.ALIGN_CENTER)
                self.game_team_sizer = wx.BoxSizer(wx.VERTICAL)
                self.game_team1_sizer = wx.BoxSizer(wx.HORIZONTAL)
                self.game_team_sizer.Add(self.game_team1_sizer, 3, wx.ALIGN_CENTER)
                team1_txt = wx.StaticText(self.history_record_window,
                                          style=wx.TE_MULTILINE | wx.TE_RICH2 | wx.ALIGN_RIGHT
                                          , label=v[4] + '    ')
                vs_txt = wx.StaticText(self.history_record_window, style=wx.TE_MULTILINE | wx.TE_RICH2
                                       , label=' VS ')
                team2_txt = wx.StaticText(self.history_record_window,
                                          style=wx.TE_MULTILINE | wx.TE_RICH2 | wx.ALIGN_LEFT
                                          , label='    ' + v[5])
                team1_txt.SetFont(font2)
                team2_txt.SetFont(font2)
                vs_txt.SetFont(vs_font)
                vs_txt.SetBackgroundColour(wx.BLACK)
                vs_txt.SetForegroundColour(wx.WHITE)
                self.game_team1_sizer.Add(team1_txt, 1, wx.ALIGN_CENTER)
                self.game_team1_sizer.Add(vs_txt, 0, wx.ALIGN_CENTER)
                self.game_team1_sizer.Add(team2_txt, 1, wx.ALIGN_CENTER)
                self.view_game_info_sizer.Add(self.game_team_sizer, 5, wx.ALIGN_CENTER)
                time_txt = wx.StaticText(self.history_record_window,
                                         style=wx.TE_MULTILINE | wx.TE_RICH2 | wx.ALIGN_CENTER
                                         , label=v[1] + ':00:00 【场数:' + v[3] + '】')
                time_txt.SetFont(font3)
                self.select_match_btn = wx.Button(self.history_record_window, label='查看BP')
                self.select_match_btn.Bind(wx.EVT_BUTTON,
                                           lambda event, pram1=int(v[0]): self.OnClickedViewBP(event, pram1))
                self.view_game_info_sizer.Add(self.select_match_btn, 1, wx.ALIGN_CENTER)
                self.game_team_sizer.Add(time_txt, 1, wx.ALIGN_CENTER)
                line = wx.StaticLine(self.history_record_window, style=wx.LI_HORIZONTAL, size=(300, 2))
                line.SetBackgroundColour(wx.BLACK)  # 设置线颜色
                line.SetForegroundColour(wx.BLACK)  # 设置线颜色
                self.vbox2.Add(line, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)  # 添加线并设置间距
                view_history_num += 1

        self.history_record_window.SetSizer(self.vbox2)
        self.panel.SetSizer(vbox)
        self.Show()

    def OnClickedViewBP(self, event, m_id):
        print(m_id)
        history_inf = HistoryInf(m_id, self.save_list)


class HistoryInf(wx.Frame):
    def __init__(self, m_id, save_list):
        style = wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX
        wx.Frame.__init__(self, None,
                          title='白狼王的BP模拟器【历史阵容】', size=(1100, 900), style=style)
        self.save_list = save_list
        self.SetIcon(wx.Icon("image\\WhiteWolfBP.ico", wx.BITMAP_TYPE_ICO))
        self.SetMaxSize((1100, -1))
        self.SetMinSize((1100, -1))
        display_idx = wx.Display.GetFromPoint(wx.GetMousePosition())
        # 获取该屏幕的几何信息（x, y, width, height）
        display_rect = wx.Display(display_idx).GetGeometry()
        win_width, win_height = self.GetSize()
        pos_x = display_rect.x + (display_rect.width - win_width) // 2
        pos_y = display_rect.y + (display_rect.height - win_height) // 2
        self.SetPosition((pos_x, pos_y))  # 设置窗口位置
        self.Center()
        self.panel = wx.ScrolledWindow(self)
        self.panel.SetScrollRate(0, 20)
        self.pbox = wx.BoxSizer(wx.VERTICAL)
        show_heroes_pick_blue_list = []
        show_heroes_pick_red_list = []
        show_heroes_ban_blue_list = []
        show_heroes_ban_red_list = []
        for m in range(len(self.save_list)):
            if self.save_list[-m - 1][0] == str(m_id):
                if self.save_list[-m - 1][6] == '无BP':
                    show_heroes_pick_blue_list = [0, 1, 2, 3, 4]
                    show_heroes_pick_red_list = [5, 6, 7, 8, 9]
                    show_heroes_ban_blue_list = []
                    show_heroes_ban_red_list = []
                if self.save_list[-m - 1][6] == '8ban':
                    show_heroes_ban_blue_list = [0, 2, 11, 13]
                    show_heroes_ban_red_list = [12, 10, 3, 1]
                    show_heroes_pick_blue_list = [4, 7, 8, 15, 16]
                    show_heroes_pick_red_list = [17, 14, 9, 6, 5]
                if self.save_list[-m - 1][6] == '10ban':
                    show_heroes_ban_blue_list = [0, 2, 11, 13, 15]
                    show_heroes_ban_red_list = [14, 12, 10, 3, 1]
                    show_heroes_pick_blue_list = [4, 7, 8, 17, 18]
                    show_heroes_pick_red_list = [19, 16, 9, 6, 5]
                if self.save_list[-m - 1][6] == '0ban':
                    show_heroes_pick_blue_list = [0, 3, 4, 7, 8]
                    show_heroes_pick_red_list = [1, 2, 5, 6, 9]
                if self.save_list[-m - 1][6] == '3+2':
                    show_heroes_ban_blue_list = [0, 2, 4, 13, 15]
                    show_heroes_ban_red_list = [14, 12, 5, 3, 1]
                    show_heroes_pick_blue_list = [6, 9, 10, 17, 18]
                    show_heroes_pick_red_list = [19, 16, 11, 8, 7]
                game_box = wx.BoxSizer(wx.HORIZONTAL)
                self.pbox.Add(game_box, 1, wx.Center)
                line = wx.StaticLine(self.panel, style=wx.LI_HORIZONTAL, size=(300, 6))
                line.SetBackgroundColour(wx.BLACK)  # 设置线颜色
                line.SetForegroundColour(wx.BLACK)  # 设置线颜色
                self.pbox.Add(line, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)  # 添加线并设置间距
                blue_box = wx.BoxSizer(wx.VERTICAL)
                red_box = wx.BoxSizer(wx.VERTICAL)
                game_box.Add(blue_box, 0, wx.Center)
                game_box.Add((60, 0), 0, wx.EXPAND, 0)
                game_box.Add(red_box, 0, wx.Center)
                blue_ban_box = wx.BoxSizer(wx.HORIZONTAL)
                blue_pick_box = wx.BoxSizer(wx.HORIZONTAL)
                red_ban_box = wx.BoxSizer(wx.HORIZONTAL)
                red_pick_box = wx.BoxSizer(wx.HORIZONTAL)
                blue_box.Add(blue_ban_box, 0)
                blue_box.Add(blue_pick_box, 0)
                red_box.Add(red_ban_box, 0, flag=wx.ALIGN_RIGHT)
                red_box.Add(red_pick_box, 0, flag=wx.ALIGN_RIGHT)
                team_blue_text = wx.StaticText(self.panel, -1, label=self.save_list[-m - 1][4])
                team_red_text = wx.StaticText(self.panel, -1, label=self.save_list[-m - 1][5])
                font = wx.Font(
                    15,  # 字号
                    wx.FONTFAMILY_DEFAULT,  # 字体系列
                    wx.FONTSTYLE_NORMAL,  # 字体样式
                    wx.FONTWEIGHT_BOLD,  # 字体粗细(加粗)
                    False,  # 下划线
                    "微软雅黑")  # 字体名称
                team_blue_text.SetFont(font)
                team_red_text.SetFont(font)
                red_ban_box.Add(team_red_text, 0, flag=wx.CENTRE)
                for j in show_heroes_ban_blue_list:
                    self.bmp = wx.Image('heroes\\icon\\' + self.save_list[-m - 1][j + 7] + '.jpg',
                                        wx.BITMAP_TYPE_ANY).ConvertToGreyscale().Scale(70, 70).ConvertToBitmap()
                    self.bitmap = wx.StaticBitmap(self.panel, wx.ID_ANY, self.bmp)
                    blue_ban_box.Add(self.bitmap, 1)
                for j in show_heroes_pick_blue_list:
                    self.bmp = wx.Image('heroes\\icon\\' + self.save_list[-m - 1][j + 7] + '.jpg',
                                        wx.BITMAP_TYPE_ANY).Scale(100, 100).ConvertToBitmap()
                    self.bitmap = wx.StaticBitmap(self.panel, wx.ID_ANY, self.bmp)
                    blue_pick_box.Add(self.bitmap, 1)
                for j in show_heroes_ban_red_list:
                    self.bmp = wx.Image('heroes\\icon\\' + self.save_list[-m - 1][j + 7] + '.jpg',
                                        wx.BITMAP_TYPE_ANY).ConvertToGreyscale().Scale(70, 70).ConvertToBitmap()
                    self.bitmap = wx.StaticBitmap(self.panel, wx.ID_ANY, self.bmp)
                    red_ban_box.Add(self.bitmap, 1)
                for j in show_heroes_pick_red_list:
                    self.bmp = wx.Image('heroes\\icon\\' + self.save_list[-m - 1][j + 7] + '.jpg',
                                        wx.BITMAP_TYPE_ANY).Scale(100, 100).ConvertToBitmap()
                    self.bitmap = wx.StaticBitmap(self.panel, wx.ID_ANY, self.bmp)
                    red_pick_box.Add(self.bitmap, 1)
                blue_ban_box.Add(team_blue_text, 0, flag=wx.CENTRE)
                self.panel.SetSizer(self.pbox)
        self.Show()


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None,
                          title='白狼王的BP模拟器', size=(600, 220),
                          style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.SetIcon(wx.Icon("image\\WhiteWolfBP.ico", wx.BITMAP_TYPE_ICO))
        display_idx = wx.Display.GetFromPoint(wx.GetMousePosition())
        # 获取该屏幕的几何信息（x, y, width, height）
        display_rect = wx.Display(display_idx).GetGeometry()
        win_width, win_height = self.GetSize()
        pos_x = display_rect.x + (display_rect.width - win_width) // 2
        pos_y = display_rect.y + (display_rect.height - win_height) // 2
        self.SetPosition((pos_x, pos_y))  # 设置窗口位置
        self.main_change = None
        self.panel = wx.Panel(self)
        self.Center()
        vbox = wx.BoxSizer(wx.VERTICAL)
        title_text = wx.StaticText(self.panel, wx.ALIGN_CENTER, label='白狼王的BP模拟器')
        title2_text = wx.StaticText(self.panel, wx.ALIGN_CENTER, label='微信：WhiteWolfHD')
        title_text.SetFont(wx.Font(40, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        title2_text.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        title_text.SetForegroundColour(wx.WHITE)
        title_text.SetBackgroundColour(wx.BLACK)
        self.start_bp_btn = wx.Button(self.panel, label='开始BP')
        self.show_bp_btn = wx.Button(self.panel, label='查看记录')
        self.setting_btn = wx.Button(self.panel, label='设置')
        self.preference_btn = wx.Button(self.panel, label='对局偏好')
        self.show_bp_btn.Bind(wx.EVT_BUTTON, self.onClickShowBpHistory)
        self.start_bp_btn.Bind(wx.EVT_BUTTON, self.onClickStart)
        self.setting_btn.Bind(wx.EVT_BUTTON, self.onClickSetting)
        self.preference_btn.Bind(wx.EVT_BUTTON, self.onClickPreference)
        vbox.Add(title_text, 1, wx.ALIGN_CENTER)
        vbox.Add(title2_text, 1, wx.ALIGN_CENTER)
        vbox.Add(self.start_bp_btn, 1, wx.ALIGN_CENTER)
        vbox.Add(self.show_bp_btn, 1, wx.ALIGN_CENTER)
        vbox.Add(self.setting_btn, 1, wx.ALIGN_CENTER)
        vbox.Add(self.preference_btn, 1, wx.ALIGN_CENTER)
        self.panel.SetSizer(vbox)
        self.Show()

    def onClickShowBpHistory(self, event):
        view_history_record_frame = ViewHistoryRecord()

    def onClickStart(self, event):
        start_settings_frame = StartSettingsFrame()

    def onClickSetting(self, event):
        self.main_change = MainChange()

    def onClickPreference(self, event):
        ChangePreferenceFrame()


class ChangePreferenceFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None,
                          title='开始游戏', size=(400, 280),
                          style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.SetIcon(wx.Icon("image\\WhiteWolfBP.ico", wx.BITMAP_TYPE_ICO))
        display_idx = wx.Display.GetFromPoint(wx.GetMousePosition())
        # 获取该屏幕的几何信息（x, y, width, height）
        display_rect = wx.Display(display_idx).GetGeometry()
        win_width, win_height = self.GetSize()
        pos_x = display_rect.x + (display_rect.width - win_width) // 2
        pos_y = display_rect.y + (display_rect.height - win_height) // 2
        self.SetPosition((pos_x, pos_y))  # 设置窗口位置
        self.panel = wx.Panel(self)
        self.Center()
        max_game_num_list = ['BO1', 'BO3', 'BO5', 'BO7', 'BO9']
        ban_num_list = ['0', '8', '2+3', '无BP', '3+2']
        self.max_game_num_box = wx.RadioBox(self.panel, label='赛制', choices=max_game_num_list)
        self.ban_num_box = wx.RadioBox(self.panel, label='ban位数量', choices=ban_num_list)
        self.team1_box = wx.StaticBox(self.panel, label='蓝色方')
        self.team2_box = wx.StaticBox(self.panel, label='红色方')
        team1_box_sizer = wx.StaticBoxSizer(self.team1_box, wx.VERTICAL)
        team2_box_sizer = wx.StaticBoxSizer(self.team2_box, wx.VERTICAL)
        try:
            with open('save\\preference.csv', 'r', newline='') as preference_csv:
                reader = csv.reader(preference_csv)
                for row1 in reader:
                    preference_list = row1
            print(preference_list)
            self.max_game_num_box.SetSelection(int(preference_list[1]))
            self.ban_num_box.SetSelection(int(preference_list[0]))
            self.team1_text = wx.TextCtrl(self.panel, size=(250, 15), value=preference_list[2])
            self.team2_text = wx.TextCtrl(self.panel, size=(250, 15), value=preference_list[3])
        except FileNotFoundError:
            self.max_game_num_box.SetSelection(1)
            self.ban_num_box.SetSelection(1)
            self.team1_text = wx.TextCtrl(self.panel, size=(250, 15), value='Team1')
            self.team2_text = wx.TextCtrl(self.panel, size=(250, 15), value='Team2')
        team1_box_sizer.Add(self.team1_text, 1, wx.ALIGN_CENTRE)
        team2_box_sizer.Add(self.team2_text, 1, wx.ALIGN_CENTRE)
        self.start_btn = wx.Button(self.panel, label='确定')
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.max_game_num_box, 1, wx.ALIGN_CENTRE)
        vbox.Add(self.ban_num_box, 1, wx.ALIGN_CENTRE)
        vbox.Add(team1_box_sizer, 1, wx.ALIGN_CENTRE)
        vbox.Add(team2_box_sizer, 1, wx.ALIGN_CENTRE)
        vbox.Add(self.start_btn, 1, wx.ALIGN_CENTRE)
        self.start_btn.Bind(wx.EVT_BUTTON, self.OnClickConfirm)
        self.panel.SetSizer(vbox)
        self.Show()

    def OnClickConfirm(self, event):
        preference_list = [self.ban_num_box.GetSelection(), self.max_game_num_box.GetSelection(),
                           self.team1_text.GetValue(), self.team2_text.GetValue()]
        with open('save\\preference.csv', 'w', newline='') as preference_csv:
            writer = csv.writer(preference_csv)
            writer.writerow(preference_list)
        self.Close()


class StartSettingsFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None,
                          title='开始游戏', size=(400, 280),
                          style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.SetIcon(wx.Icon("image\\WhiteWolfBP.ico", wx.BITMAP_TYPE_ICO))
        self.Center()
        display_idx = wx.Display.GetFromPoint(wx.GetMousePosition())
        # 获取该屏幕的几何信息（x, y, width, height）
        display_rect = wx.Display(display_idx).GetGeometry()
        win_width, win_height = self.GetSize()
        pos_x = display_rect.x + (display_rect.width - win_width) // 2
        pos_y = display_rect.y + (display_rect.height - win_height) // 2
        self.SetPosition((pos_x, pos_y))  # 设置窗口位置
        self.panel = wx.Panel(self)
        max_game_num_list = ['BO1', 'BO3', 'BO5', 'BO7', 'BO9']
        ban_num_list = ['0', '8', '2+3', '无BP', '3+2']
        self.max_game_num_box = wx.RadioBox(self.panel, label='赛制', choices=max_game_num_list)
        self.ban_num_box = wx.RadioBox(self.panel, label='ban位数量', choices=ban_num_list)
        self.team1_box = wx.StaticBox(self.panel, label='蓝色方')
        self.team2_box = wx.StaticBox(self.panel, label='红色方')
        team1_box_sizer = wx.StaticBoxSizer(self.team1_box, wx.VERTICAL)
        team2_box_sizer = wx.StaticBoxSizer(self.team2_box, wx.VERTICAL)
        try:
            with open('save\\preference.csv', 'r', newline='') as preference_csv:
                reader = csv.reader(preference_csv)
                for row1 in reader:
                    preference_list = row1
            print(preference_list)
            self.max_game_num_box.SetSelection(int(preference_list[1]))
            self.ban_num_box.SetSelection(int(preference_list[0]))
            self.team1_text = wx.TextCtrl(self.panel, size=(250, 15), value=preference_list[2])
            self.team2_text = wx.TextCtrl(self.panel, size=(250, 15), value=preference_list[3])
        except FileNotFoundError:
            self.max_game_num_box.SetSelection(1)
            self.ban_num_box.SetSelection(1)
            self.team1_text = wx.TextCtrl(self.panel, size=(250, 15), value='Team1')
            self.team2_text = wx.TextCtrl(self.panel, size=(250, 15), value='Team2')
        team1_box_sizer.Add(self.team1_text, 1, wx.ALIGN_CENTRE)
        team2_box_sizer.Add(self.team2_text, 1, wx.ALIGN_CENTRE)
        self.start_btn = wx.Button(self.panel, label='开始')
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.max_game_num_box, 1, wx.ALIGN_CENTRE)
        vbox.Add(self.ban_num_box, 1, wx.ALIGN_CENTRE)
        vbox.Add(team1_box_sizer, 1, wx.ALIGN_CENTRE)
        vbox.Add(team2_box_sizer, 1, wx.ALIGN_CENTRE)
        vbox.Add(self.start_btn, 1, wx.ALIGN_CENTRE)
        self.start_btn.Bind(wx.EVT_BUTTON, self.OnClickStart)
        self.panel.SetSizer(vbox)
        self.Show()

    def OnClickStart(self, event):
        num_list = [1, 3, 5, 7, 9]
        ban_num_list = [0, 8, 10, 0, 100]
        if self.ban_num_box.GetSelection() == 3:
            game_mode = 0
            my_match.load_match(game_mode, -1,
                                num_list[self.max_game_num_box.GetSelection()], datetime.now().strftime('%Y-%m-%d %H'),
                                self.team1_text.GetValue(), self.team2_text.GetValue())
        else:
            game_mode = 1
            my_match.load_match(game_mode, ban_num_list[self.ban_num_box.GetSelection()],
                                num_list[self.max_game_num_box.GetSelection()], datetime.now().strftime('%Y-%m-%d %H'),
                                self.team1_text.GetValue(), self.team2_text.GetValue())
        self.Close()


if __name__ == '__main__':
    white_wolf_bp_simulator_app = wx.App(False)
    main_frame = MainFrame()
    white_wolf_bp_simulator_app.MainLoop()
