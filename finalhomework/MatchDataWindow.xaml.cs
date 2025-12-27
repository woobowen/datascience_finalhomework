using Microsoft.Data.SqlClient;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media.Imaging;

namespace KPLAssistant
{
    public partial class MatchDataWindow : Window
    {
        // ====================== 【请确认以下两行配置】 ======================
        private string connectionString = @"Server=LAPTOP-KI0GT6AJ;Database=king;Integrated Security=True;TrustServerCertificate=True;";
        private string imageRootPath = @"C:\Users\lenovo\Desktop\暑期课\大作业\";
        // =====================================================================

        public MatchDataWindow()
        {
            InitializeComponent();
            this.Loaded += (s, e) => {
                PopulateTeamComboBox();
                PopulateMatchCountComboBox();
            };
        }

        private void PopulateTeamComboBox()
        {
            var teams = new List<string>
            {
                "成都 AG 超玩会", "重庆狼队", "北京 WB", "苏州 KSG", "广州 TTG",
                "武汉 eStarPro", "济南 RW 侠", "佛山 DRG", "深圳 DYG", "杭州 LGD.NBW",
                "BOA", "西安 WE", "北京 JDG", "长沙 TES.A", "上海 EDG.M",
                "上海 RNG.M", "南通 Hero 久竞", "XYG"
            };
            TeamComboBox.ItemsSource = teams;
        }

        private void PopulateMatchCountComboBox()
        {
            for (int i = 1; i <= 20; i++)
            {
                MatchCountComboBox.Items.Add(i);
            }
            MatchCountComboBox.SelectedIndex = 9; // 默认选择10场
        }

        private void TeamComboBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (TeamComboBox.SelectedItem == null) return;
            string selectedTeam = TeamComboBox.SelectedItem.ToString();
            string logoPath = $"{imageRootPath}kpl战队队徽\\{selectedTeam.Replace(" ", "")}.jpg";
            try
            {
                LogoImage.Source = new BitmapImage(new Uri(logoPath, UriKind.Absolute));
            }
            catch { LogoImage.Source = null; }
        }

        // 在 MatchDataWindow.xaml.cs 中
        // 在 MatchDataWindow.xaml.cs 中
        private async void QueryButton_Click(object sender, RoutedEventArgs e)
        {
            if (TeamComboBox.SelectedItem == null)
            {
                MessageBox.Show("请先选择一个战队！", "提示");
                return;
            }
            if (!int.TryParse(MatchCountComboBox.Text, out int matchCount) || matchCount < 1 || matchCount > 20)
            {
                MessageBox.Show("请输入或选择1到20之间的有效场数！", "提示");
                return;
            }

            string selectedTeam = TeamComboBox.SelectedItem.ToString();
            var matches = new System.Collections.ObjectModel.ObservableCollection<MatchInfo>();

            try
            {
                using (var connection = new SqlConnection(connectionString))
                {
                    await connection.OpenAsync();

                    // 【关键修正1】在C#中，先将我们选择的队名中的空格去掉
                    string teamNameForQuery = selectedTeam.Replace(" ", "");

                    // 【关键修正2】在SQL中，使用REPLACE函数同样去掉数据库字段里的空格，再进行模糊匹配
                    string query = @"SELECT TOP (@MatchCount) * FROM MatchData 
                             WHERE REPLACE(BlueTeamName, ' ', '') LIKE @TeamName OR REPLACE(RedTeamName, ' ', '') LIKE @TeamName";

                    using (var command = new SqlCommand(query, connection))
                    {
                        // 参数绑定时，使用我们处理过的不带空格的队名
                        command.Parameters.AddWithValue("@TeamName", $"%{teamNameForQuery}%");
                        command.Parameters.AddWithValue("@MatchCount", matchCount);

                        using (var reader = await command.ExecuteReaderAsync())
                        {
                            while (await reader.ReadAsync())
                            {
                                // 这部分代码保持不变
                                matches.Add(new MatchInfo
                                {
                                    BlueTeamName = reader["BlueTeamName"]?.ToString(),
                                    RedTeamName = reader["RedTeamName"]?.ToString(),
                                    WinningTeam = reader["WinningTeam"]?.ToString(),
                                    BlueBan1 = reader["BlueBan1"]?.ToString(),
                                    BlueBan2 = reader["BlueBan2"]?.ToString(),
                                    BlueBan3 = reader["BlueBan3"]?.ToString(),
                                    BlueBan4 = reader["BlueBan4"]?.ToString(),
                                    RedBan1 = reader["RedBan1"]?.ToString(),
                                    RedBan2 = reader["RedBan2"]?.ToString(),
                                    RedBan3 = reader["RedBan3"]?.ToString(),
                                    RedBan4 = reader["RedBan4"]?.ToString(),
                                    BluePick1 = reader["BluePick1"]?.ToString(),
                                    BluePick2 = reader["BluePick2"]?.ToString(),
                                    BluePick3 = reader["BluePick3"]?.ToString(),
                                    BluePick4 = reader["BluePick4"]?.ToString(),
                                    BluePick5 = reader["BluePick5"]?.ToString(),
                                    RedPick1 = reader["RedPick1"]?.ToString(),
                                    RedPick2 = reader["RedPick2"]?.ToString(),
                                    RedPick3 = reader["RedPick3"]?.ToString(),
                                    RedPick4 = reader["RedPick4"]?.ToString(),
                                    RedPick5 = reader["RedPick5"]?.ToString()
                                });
                            }
                        }
                    }
                }

                MatchDataGrid.ItemsSource = matches;

                if (!matches.Any())
                {
                    MessageBox.Show("未找到该战队的比赛数据。", "查询结果");
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"数据库查询时发生错误: {ex.Message}", "严重错误");
            }
        }
    }
}