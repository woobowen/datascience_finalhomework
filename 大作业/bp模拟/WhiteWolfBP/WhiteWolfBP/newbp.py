# 文件名: newbp.py
import csv
import wx
import my_match

class StartBPFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None,
                          title='WBW的BP模拟器',
                          size=(600, 400),
                          style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        
        self.panel = wx.Panel(self)
        
        # 定义颜色
        bgColor = wx.Colour(28, 33, 43)      # 深蓝灰背景
        textColor = wx.Colour(224, 224, 224)  # 亮灰色文字
        accentColor = wx.Colour(65, 105, 225)   # 青色高亮

        self.panel.SetBackgroundColour(bgColor)

        # 添加标题
        title = wx.StaticText(self.panel, label="WBW的BP模拟器")
        title_font = wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title.SetFont(title_font)
        title.SetForegroundColour(wx.WHITE)

        # 赛制说明
        mode_info = wx.StaticText(self.panel, label="8个Ban位单场比赛模式")
        mode_font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        mode_info.SetFont(mode_font)
        mode_info.SetForegroundColour(textColor)

        # 队伍名称输入框
        team1_label = wx.StaticText(self.panel, label="蓝色方队伍名称:")
        team1_label.SetForegroundColour(textColor)
        self.team1_text = wx.TextCtrl(self.panel, size=(300, -1), value="蓝色方")
        
        team2_label = wx.StaticText(self.panel, label="红色方队伍名称:")
        team2_label.SetForegroundColour(textColor)
        self.team2_text = wx.TextCtrl(self.panel, size=(300, -1), value="红色方")
        
        try:
            with open('save\\preference.csv', 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                prefs = next(reader)
                self.team1_text.SetValue(prefs[0])
                self.team2_text.SetValue(prefs[1])
        except:
            pass
        
        # 开始按钮
        start_btn = wx.Button(self.panel, label='开始BP', size=(200, 50))
        start_btn.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        # 【颜色修改】将按钮文字颜色设置为主题高亮色（青蓝色）
        start_btn.SetForegroundColour(accentColor)
        
        start_btn.Bind(wx.EVT_BUTTON, self.on_start)
        
        # 布局
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(title, flag=wx.ALIGN_CENTER|wx.TOP, border=20)
        vbox.AddSpacer(15)
        vbox.Add(mode_info, flag=wx.ALIGN_CENTER)
        vbox.AddSpacer(30)
        
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(team1_label, flag=wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, border=10)
        hbox1.Add(self.team1_text, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=50)
        
        vbox.AddSpacer(20)
        
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(team2_label, flag=wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, border=10)
        hbox2.Add(self.team2_text, proportion=1)
        vbox.Add(hbox2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=50)
        
        vbox.AddSpacer(40)
        vbox.Add(start_btn, flag=wx.ALIGN_CENTER)
        vbox.AddSpacer(20)
        
        self.panel.SetSizer(vbox)
        self.Center()
        self.Show()

    def on_start(self, event):
        with open('save\\preference.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                self.team1_text.GetValue(),
                self.team2_text.GetValue()
            ])
        
        my_match.load_match(
            team_blue=self.team1_text.GetValue(),
            team_red=self.team2_text.GetValue()
        )
        self.Close()

if __name__ == '__main__':
    app = wx.App()
    frame = StartBPFrame()
    app.MainLoop()