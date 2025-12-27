using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;
using System.Windows;
using HtmlAgilityPack;

namespace KPLAssistant
{
    public partial class MainWindow : Window
    {
        private string imageRootPath = @"C:\Users\lenovo\Desktop\暑期课\大作业\";

        public MainWindow()
        {
            InitializeComponent();
            this.Loaded += MainWindow_Loaded;
            // 注册编码提供程序，以支持GBK等编码
            System.Text.Encoding.RegisterProvider(System.Text.CodePagesEncodingProvider.Instance);
        }

        // 修改：不再需要async，因为加载赛果的方法不再是异步的
        private async void MainWindow_Loaded(object sender, RoutedEventArgs e)
        {
            await LoadHupuPostsAsync();
            LoadTeamRankings();
            LoadRecentMatches(); // 修改：调用新的同步方法
        }

        // (这部分代码保持不变)
        private void LoadTeamRankings()
        {
            var teamData = new[]
            {
                new { Rank = 1, Name = "成都 AG 超玩会", Wins = 52 },
                new { Rank = 2, Name = "重庆狼队", Wins = 50 },
                new { Rank = 3, Name = "北京 WB", Wins = 35 }
            };
            var allRankings = teamData.Select(t => new TeamRanking
            {
                Rank = t.Rank,
                TeamName = t.Name,
                Wins = t.Wins,
                LogoPath = $"{imageRootPath}kpl战队队徽\\{t.Name.Replace(" ", "")}.jpg"
            }).ToList();
            var displayList = new List<object>();
            var podiumViewModel = new PodiumViewModel
            {
                TopThree = new List<TeamRanking>
                {
                    allRankings.First(r => r.Rank == 2),
                    allRankings.First(r => r.Rank == 1),
                    allRankings.First(r => r.Rank == 3)
                }
            };
            displayList.Add(podiumViewModel);
            ListViewTeamRankings.ItemsSource = displayList;
        }

        // (这部分代码保持不变)
        private async Task LoadHupuPostsAsync()
        {
            string url = "https://bbs.hupu.com/kog-hot";
            var postTitles = new List<string>();
            try
            {
                using (var httpClient = new HttpClient())
                {
                    httpClient.DefaultRequestHeaders.Add("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36");
                    string html = await httpClient.GetStringAsync(url);
                    var htmlDocument = new HtmlDocument();
                    htmlDocument.LoadHtml(html);
                    var titleNodes = htmlDocument.DocumentNode.SelectNodes("//a[contains(@class, 'p-title')]");
                    if (titleNodes != null)
                    {
                        postTitles = titleNodes.Take(5).Select(node => node.InnerText.Trim()).ToList();
                    }
                }
                if (postTitles.Any()) { ListViewHupuPosts.ItemsSource = postTitles; }
                else { ListViewHupuPosts.ItemsSource = new List<string> { "加载虎扑帖子失败。" }; }
            }
            catch (Exception ex) { ListViewHupuPosts.ItemsSource = new List<string> { $"错误: {ex.Message}" }; }
        }

        // 【关键修改】重写整个方法，不再进行网络爬取，而是使用静态数据
        private void LoadRecentMatches()
        {
            var recentMatches = new ObservableCollection<RecentMatchInfo>();

            // 定义比赛中的队伍名
            string team1 = "上海EDG.M";
            string team2 = "桐乡情久";
            string team3 = "南京Hero久竞";
            string team4 = "济南RW侠";

            // 创建比赛数据列表
            recentMatches.Add(new RecentMatchInfo
            {
                MatchDate = "2025-11-07",
                MatchTime = "17:00",
                MatchState = "已结束",
                TeamAName = team1,
                TeamBName = team2,
                TeamAScore = "2",
                TeamBScore = "3",
                // 【关键修正】根据本地路径规则生成Logo路径
                TeamALogo = $"{imageRootPath}kpl战队队徽\\{team1.Replace(" ", "")}.jpg",
                TeamBLogo = $"{imageRootPath}kpl战队队徽\\{team2.Replace(" ", "")}.jpg"
            });

            recentMatches.Add(new RecentMatchInfo
            {
                MatchDate = "2025-11-16",
                MatchTime = "20:00",
                MatchState = "已结束",
                TeamAName = team3,
                TeamBName = team4,
                TeamAScore = "2",
                TeamBScore = "3",
                // 【关键修正】根据本地路径规则生成Logo路径
                TeamALogo = $"{imageRootPath}kpl战队队徽\\{team3.Replace(" ", "")}.jpg",
                TeamBLogo = $"{imageRootPath}kpl战队队徽\\{team4.Replace(" ", "")}.jpg"
            });

            // 将创建好的静态数据列表绑定到界面
            ListViewRecentMatches.ItemsSource = recentMatches;
        }

        // ... (三个按钮的Click事件处理方法保持不变) ...
        private void BtnTeamInfo_Click(object sender, RoutedEventArgs e)
        {
            TeamInfoWindow infoWindow = new TeamInfoWindow();
            infoWindow.Show();
        }

        private void BtnTeamStats_Click(object sender, RoutedEventArgs e)
        {
            MatchDataWindow matchDataWindow = new MatchDataWindow();
            matchDataWindow.Show();
        }

        private void BtnHeroData_Click(object sender, RoutedEventArgs e)
        {
            HeroDataWindow heroDataWindow = new HeroDataWindow();
            heroDataWindow.Show();
        }

        private void BtnLaneHeroStats_Click(object sender, RoutedEventArgs e)
        {
            LaneHeroStatsWindow laneHeroStatsWindow = new LaneHeroStatsWindow();
            laneHeroStatsWindow.Show();
        }
        private void BtnTeamAnalysis_Click(object sender, RoutedEventArgs e)
        {
            // 创建并显示分析窗口（我们马上会创建这个类）
            TeamAnalysisWindow analysisWindow = new TeamAnalysisWindow();
            analysisWindow.Show();
        }
        // 在 MainWindow.xaml.cs 文件中
        private void BtnLineupSimulator_Click(object sender, RoutedEventArgs e)
        {
            // 【已更新】使用你提供的第一个Python解释器路径
            string pythonPath = @"C:\Users\lenovo\AppData\Local\Programs\Python\Python312\python.exe";

            // 【请确认】这是你 newbp.py 文件的完整路径，如果不同请修改
            string scriptPath = @"C:\Users\lenovo\Desktop\暑期课\大作业\bp模拟\WhiteWolfBP\WhiteWolfBP\newbp.py";

            try
            {
                System.Diagnostics.ProcessStartInfo startInfo = new System.Diagnostics.ProcessStartInfo();
                startInfo.FileName = pythonPath;
                startInfo.Arguments = scriptPath;
                startInfo.UseShellExecute = false;
                startInfo.CreateNoWindow = true; // 不显示黑色的命令行窗口
                startInfo.WorkingDirectory = System.IO.Path.GetDirectoryName(scriptPath); // 设置工作目录，确保Python脚本能找到csv等文件

                System.Diagnostics.Process.Start(startInfo);
            }
            catch (Exception ex)
            {
                MessageBox.Show($"无法启动BP模拟器，请检查Python和脚本路径是否正确。\n错误: {ex.Message}", "启动失败");
            }
        }
    }
}