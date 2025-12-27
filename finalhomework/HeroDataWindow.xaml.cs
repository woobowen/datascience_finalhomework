using Microsoft.Data.SqlClient;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media.Imaging;

namespace KPLAssistant
{
    public partial class HeroDataWindow : Window
    {
        // ====================== 【请确认以下两行配置】 ======================
        private string connectionString = @"Server=LAPTOP-KI0GT6AJ;Database=king;Integrated Security=True;TrustServerCertificate=True;";
        private string imageRootPath = @"C:\Users\lenovo\Desktop\暑期课\大作业\";
        // =====================================================================

        public HeroDataWindow()
        {
            InitializeComponent();
            this.Loaded += (s, e) => {
                PopulateTeamComboBox();
                PopulateDataTypeComboBox();
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

        private void PopulateDataTypeComboBox()
        {
            DataTypeComboBox.ItemsSource = new List<string> { "常禁用英雄", "常选择英雄" };
            DataTypeComboBox.SelectedIndex = 0; // 默认选中第一个
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

        private async void QueryButton_Click(object sender, RoutedEventArgs e)
        {
            if (TeamComboBox.SelectedItem == null || DataTypeComboBox.SelectedItem == null)
            {
                MessageBox.Show("请先选择一个战队和查询类型！", "提示");
                return;
            }

            string selectedTeam = TeamComboBox.SelectedItem.ToString();
            string selectedType = DataTypeComboBox.SelectedItem.ToString();

            // --- 动态构建查询 ---
            string tableName;
            string countColumnName;
            string countLabel;

            if (selectedType == "常禁用英雄")
            {
                tableName = "TeamHeroBan";
                countColumnName = "BanCount";
                countLabel = "禁用次数:";
            }
            else // 常选择英雄
            {
                tableName = "TeamHeroChoose";
                countColumnName = "ChooseCount";
                countLabel = "选择次数:";
            }

            string teamNameForQuery = selectedTeam.Replace(" ", "");
            string query = $"SELECT HeroName, {countColumnName} FROM {tableName} WHERE REPLACE(TeamName, ' ', '') LIKE @TeamName ORDER BY {countColumnName} DESC";

            var heroStatsList = new ObservableCollection<HeroStats>();

            try
            {
                using (var connection = new SqlConnection(connectionString))
                {
                    await connection.OpenAsync();
                    using (var command = new SqlCommand(query, connection))
                    {
                        command.Parameters.AddWithValue("@TeamName", $"%{teamNameForQuery}%");
                        using (var reader = await command.ExecuteReaderAsync())
                        {
                            while (await reader.ReadAsync())
                            {
                                string heroName = reader["HeroName"]?.ToString();
                                heroStatsList.Add(new HeroStats
                                {
                                    HeroName = heroName,
                                    Count = Convert.ToInt32(reader[countColumnName]),
                                    CountLabel = countLabel,
                                    // 构建英雄图片的完整路径
                                    HeroImagePath = $"{imageRootPath}英雄\\{heroName}.jpg"
                                });
                            }
                        }
                    }
                }

                HeroListView.ItemsSource = heroStatsList;
                if (!heroStatsList.Any())
                {
                    MessageBox.Show("未找到该战队的相关英雄数据。", "查询结果");
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"数据库查询时发生错误: {ex.Message}", "严重错误");
            }
        }
    }
}