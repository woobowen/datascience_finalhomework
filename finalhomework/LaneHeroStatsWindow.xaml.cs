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
    public partial class LaneHeroStatsWindow : Window
    {
        private string connectionString = @"Server=LAPTOP-KI0GT6AJ;Database=king;Integrated Security=True;TrustServerCertificate=True;";
        private string imageRootPath = @"C:\Users\lenovo\Desktop\暑期课\大作业\";

        // 【关键修正1】创建一个字典来存储中文名和数据库英文名的映射关系
        private Dictionary<string, string> laneMapping;

        public LaneHeroStatsWindow()
        {
            InitializeComponent();

            // 初始化这个字典
            laneMapping = new Dictionary<string, string>
            {
                { "对抗路", "TOP" },
                { "打野", "JUN" },
                { "中路", "MID" },
                { "发育路", "BOT" },
                { "游走", "SUP" } // 注意：这里用“游走”代替了“辅助”，与游戏内说法统一
            };

            this.Loaded += (s, e) => {
                PopulateLaneComboBox();
                PopulateDataTypeComboBox();
            };
        }

        private void PopulateLaneComboBox()
        {
            // 下拉列表的数据源现在是字典的键（即所有中文名）
            LaneComboBox.ItemsSource = laneMapping.Keys;
            LaneComboBox.SelectedIndex = 0;
        }

        private void PopulateDataTypeComboBox()
        {
            DataTypeComboBox.ItemsSource = new List<string> { "高胜率英雄", "常选择英雄" };
            DataTypeComboBox.SelectedIndex = 0;
        }

        private void LaneComboBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (LaneComboBox.SelectedItem == null) return;
            string selectedLane = LaneComboBox.SelectedItem.ToString();
            // 请确保你的分路图标文件名是中文，例如："对抗路.png", "打野.png" 等
            string iconPath = $"{imageRootPath}分路图标\\{selectedLane}.png";
            try
            {
                LaneIconImage.Source = new BitmapImage(new Uri(iconPath));
            }
            catch { LaneIconImage.Source = null; }
        }

        private async void QueryButton_Click(object sender, RoutedEventArgs e)
        {
            if (LaneComboBox.SelectedItem == null || DataTypeComboBox.SelectedItem == null)
            {
                MessageBox.Show("请先选择分路和查询类型！", "提示");
                return;
            }

            string selectedLaneChinese = LaneComboBox.SelectedItem.ToString();
            string selectedType = DataTypeComboBox.SelectedItem.ToString();

            // 【关键修正2】通过字典，将用户选择的中文分路“翻译”成数据库需要的英文缩写
            string laneForQuery = laneMapping[selectedLaneChinese];

            string tableName, heroColumn, statColumn, statLabel;

            if (selectedType == "高胜率英雄")
            {
                tableName = "HighWinRateHeroes";
                heroColumn = "胜率最高英雄名";
                statColumn = "胜率";
                statLabel = "胜率: ";
            }
            else
            {
                tableName = "MostUsedHeroes";
                heroColumn = "最常用英雄名";
                statColumn = "使用局数";
                statLabel = "使用局数: ";
            }

            string query = $"SELECT TOP 6 {heroColumn}, {statColumn} FROM {tableName} WHERE 位置 = @Lane ORDER BY {statColumn} DESC";

            var heroList = new ObservableCollection<LaneHeroData>();

            try
            {
                using (var connection = new SqlConnection(connectionString))
                {
                    await connection.OpenAsync();
                    using (var command = new SqlCommand(query, connection))
                    {
                        // 【关键修正3】将翻译后的英文缩写作为参数传入SQL查询
                        command.Parameters.AddWithValue("@Lane", laneForQuery);

                        using (var reader = await command.ExecuteReaderAsync())
                        {
                            while (await reader.ReadAsync())
                            {
                                string heroName = reader[heroColumn]?.ToString();
                                string statDisplayValue;

                                if (selectedType == "高胜率英雄")
                                {
                                    double winRate = Convert.ToDouble(reader[statColumn]);
                                    statDisplayValue = statLabel + winRate.ToString("P2");
                                }
                                else
                                {
                                    statDisplayValue = statLabel + reader[statColumn]?.ToString() + " 局";
                                }

                                heroList.Add(new LaneHeroData
                                {
                                    HeroName = heroName,
                                    StatDisplay = statDisplayValue,
                                    HeroImagePath = $"{imageRootPath}英雄\\{heroName}.jpg"
                                });
                            }
                        }
                    }
                }
                HeroResultListView.ItemsSource = heroList;
                if (!heroList.Any())
                {
                    MessageBox.Show("未找到该分路的相关英雄数据。", "查询结果");
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"数据库查询时发生错误: {ex.Message}", "严重错误");
            }
        }
    }
}