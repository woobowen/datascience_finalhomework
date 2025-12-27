using Microsoft.Data.SqlClient;
using System;
using System.Collections.Generic;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media.Imaging;

namespace KPLAssistant
{
    public partial class TeamInfoWindow : Window
    {
        // 数据库连接字符串，使用Windows身份验证
        private string connectionString = @"Server=LAPTOP-KI0GT6AJ;Database=king;Integrated Security=True;TrustServerCertificate=True;";

        // 图片文件夹的根路径，请确保结尾有"\"
        private string imageRootPath = @"C:\Users\lenovo\Desktop\暑期课\大作业\";

        public TeamInfoWindow()
        {
            InitializeComponent();

            // 窗口加载时，初始化下拉列表
            this.Loaded += (s, e) => {
                PopulateTeamComboBox();
            };
        }

        // 填充战队选择列表
        private void PopulateTeamComboBox()
        {
            // 根据你提供的图片，创建战队列表
            var teams = new List<string>
            {
                "成都AG超玩会", "重庆狼队", "北京WB", "苏州KSG", "广州TTG",
                "武汉eStarPro", "济南RW侠", "佛山DRG", "深圳DYG", "杭州LGD.NBW",
                "BOA", "西安WE", "北京JDG", "长沙TES.A", "上海EDG.M",
                "上海RNG.M", "南通Hero久竞", "XYG"
            };
            TeamComboBox.ItemsSource = teams;
        }

        

        // 当用户选择一个新战队时，自动更新Logo
        private void TeamComboBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (TeamComboBox.SelectedItem == null) return;

            string selectedTeam = TeamComboBox.SelectedItem.ToString();
            // Logo路径: ...\kpl战队队徽\战队名称.jpg
            string logoPath = $"{imageRootPath}kpl战队队徽\\{selectedTeam}.jpg";

            try
            {
                LogoImage.Source = new BitmapImage(new Uri(logoPath, UriKind.Absolute));
            }
            catch (Exception ex)
            {
                // 如果图片加载失败，清空图片框并提示
                LogoImage.Source = null;
                MessageBox.Show($"无法加载Logo图片: {logoPath}\n错误: {ex.Message}", "图片错误", MessageBoxButton.OK, MessageBoxImage.Warning);
            }
        }

        // “点击查询”按钮的逻辑
        // 【替换为这个新版本】
        private async void QueryButton_Click(object sender, RoutedEventArgs e)
        {
            // 1. 输入验证（只验证是否选择了战队）
            if (TeamComboBox.SelectedItem == null)
            {
                MessageBox.Show("请先选择一个战队！", "提示", MessageBoxButton.OK, MessageBoxImage.Information);
                return;
            }

            // (局数相关的验证已删除)

            string selectedTeam = TeamComboBox.SelectedItem.ToString();

            try
            {
                using (SqlConnection connection = new SqlConnection(connectionString))
                {
                    await connection.OpenAsync();
                    string query = "SELECT * FROM team_info WHERE REPLACE(team, ' ', '') LIKE @teamName";
                    using (SqlCommand command = new SqlCommand(query, connection))
                    {
                        string teamNameForQuery = selectedTeam.Replace(" ", "");
                        command.Parameters.AddWithValue("@teamName", $"%{teamNameForQuery}%");

                        using (SqlDataReader reader = await command.ExecuteReaderAsync())
                        {
                            if (await reader.ReadAsync())
                            {
                                // 3. 更新UI界面 (不再处理局数)
                                RankingText.Text = reader["ranking"].ToString();
                                MatchesText.Text = reader["matches"].ToString(); // 直接使用数据库中的总场次
                                WinsText.Text = reader["wins"].ToString();
                                WinRateText.Text = string.Format("{0:P2}", reader["win_rate"]);
                                KdaText.Text = reader["avg_kda"].ToString();
                                KillsText.Text = reader["avg_kills"].ToString();
                                DeathsText.Text = reader["avg_deaths"].ToString();
                                AssistsText.Text = reader["avg_assists"].ToString();
                                EconomyText.Text = reader["avg_economy"].ToString();
                            }
                            else
                            {
                                MessageBox.Show("在数据库中未找到该战队的数据。", "查询失败", MessageBoxButton.OK, MessageBoxImage.Error);
                            }
                        }
                    }
                }

                string infoImagePath = $"{imageRootPath}kpl战队信息\\{selectedTeam.Replace(" ", "")}.png";
                InfoImage.Source = new BitmapImage(new Uri(infoImagePath, UriKind.Absolute));
            }
            catch (Exception ex)
            {
                MessageBox.Show($"数据库查询或图片加载时发生错误: {ex.Message}", "严重错误", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }
    }
}