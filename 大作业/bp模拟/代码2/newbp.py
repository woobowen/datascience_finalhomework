import csv
from datetime import datetime
import wx
import my_match

# 读取英雄数据
heroes_all_list = []
with open('heroes\\heroes.csv') as heroes_csv:
    heroes_csv_reader = csv.reader(heroes_csv)
    heroes_all_list = list(heroes_csv_reader)

class StartBPFrame(wx.Frame):
    def __init__(self):
        # 增大窗口尺寸为600x400
        wx.Frame.__init__(self, None,
                          title='WBW的BP模拟器', 
                          size=(600, 400),
                          style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        
        
        
        # 创建主面板
        self.panel = wx.Panel(self)
        
        # 添加标题（使用更大的字体）
        title = wx.StaticText(self.panel, label="WBW的BP模拟器")
        title_font = wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title.SetFont(title_font)
        
        # 赛制说明（使用稍大的字体）
        mode_info = wx.StaticText(self.panel, label="当前模式：BO1赛制 | 8个Ban位")
        mode_font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        mode_info.SetFont(mode_font)
        
        # 队伍名称输入框（增大尺寸）
        team1_label = wx.StaticText(self.panel, label="蓝色方队伍名称:")
        self.team1_text = wx.TextCtrl(self.panel, size=(300, -1), value="蓝色方")
        
        team2_label = wx.StaticText(self.panel, label="红色方队伍名称:")
        self.team2_text = wx.TextCtrl(self.panel, size=(300, -1), value="红色方")
        
        # 尝试读取偏好设置
        try:
            with open('save\\preference.csv', 'r', newline='') as f:
                reader = csv.reader(f)
                prefs = next(reader)
                self.team1_text.SetValue(prefs[2])
                self.team2_text.SetValue(prefs[3])
        except:
            pass
        
        # 开始按钮（增大尺寸）
        start_btn = wx.Button(self.panel, label='开始BP', size=(200, 50))
        start_btn.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        start_btn.Bind(wx.EVT_BUTTON, self.on_start)
        
        # 布局（使用更合理的间距）
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
        self.Show()

    def on_start(self, event):
        """开始BP比赛"""
        # 保存偏好设置
        with open('save\\preference.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([1, 0,  # 8ban, BO1
                           self.team1_text.GetValue(),
                           self.team2_text.GetValue()])
        
        # 启动比赛 - 修正后的调用方式
        my_match.load_match(
            game_mode=1,                     # 有BP模式
            ban_num=8,                      # 8个ban位
            max_game_num=1,                 # BO1
            match_id=datetime.now().strftime('%Y-%m-%d %H'),
            team_blue=self.team1_text.GetValue(),
            team_red=self.team2_text.GetValue()
        )
        self.Close()

if __name__ == '__main__':
    app = wx.App()
    frame = StartBPFrame()
    app.MainLoop()