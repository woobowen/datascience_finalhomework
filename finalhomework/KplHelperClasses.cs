// 文件名: KplHelperClasses.cs

// 确保这些using语句都在文件的最上方
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Media;

// 确保命名空间正确
namespace KPLAssistant
{
    // =======================================================
    // ==           排行榜功能需要用到的3个类             ==
    // =======================================================

    // 1. 排名数据模型
    public class TeamRanking
    {
        public int Rank { get; set; }
        public string TeamName { get; set; }
        public int Wins { get; set; }
        public string LogoPath { get; set; }
    }

    // 2. 领奖台数据模型 (用于打包前三名)
    public class PodiumViewModel
    {
        public List<TeamRanking> TopThree { get; set; }
    }

    // 3. 排行榜模板选择器
    public class LeaderboardTemplateSelector : DataTemplateSelector
    {
        public DataTemplate PodiumTemplate { get; set; }
        public DataTemplate RegularRowTemplate { get; set; }

        public override DataTemplate SelectTemplate(object item, DependencyObject container)
        {
            if (item is PodiumViewModel)
            {
                return PodiumTemplate;
            }
            if (item is TeamRanking)
            {
                return RegularRowTemplate;
            }
            return base.SelectTemplate(item, container);
        }
    }

    // =======================================================
    // ==           比赛数据功能需要用到的2个类           ==
    // =======================================================

    // 4. 单场比赛数据模型
    public class MatchInfo
    {
        public string BlueTeamName { get; set; }
        public string RedTeamName { get; set; }
        public string WinningTeam { get; set; }
        public string BlueBan1 { get; set; }
        public string BlueBan2 { get; set; }
        public string BlueBan3 { get; set; }
        public string BlueBan4 { get; set; }
        public string RedBan1 { get; set; }
        public string RedBan2 { get; set; }
        public string RedBan3 { get; set; }
        public string RedBan4 { get; set; }
        public string BluePick1 { get; set; }
        public string BluePick2 { get; set; }
        public string BluePick3 { get; set; }
        public string BluePick4 { get; set; }
        public string BluePick5 { get; set; }
        public string RedPick1 { get; set; }
        public string RedPick2 { get; set; }
        public string RedPick3 { get; set; }
        public string RedPick4 { get; set; }
        public string RedPick5 { get; set; }
    }

    // 5. 比赛数据高亮颜色转换器
    // 在 KplHelperClasses.cs 文件中找到并替换
    public class TeamMatchToBrushConverter : IMultiValueConverter
    {
        public object Convert(object[] values, Type targetType, object parameter, CultureInfo culture)
        {
            if (values.Length < 2 || !(values[0] is string cellTeam) || !(values[1] is string selectedTeam))
            {
                return Brushes.Transparent;
            }

            if (!string.IsNullOrEmpty(cellTeam) && !string.IsNullOrEmpty(selectedTeam) &&
                cellTeam.Replace(" ", "") == selectedTeam.Replace(" ", ""))
            {
                // 【颜色修改】从之前的黄色改为半透明的青蓝色，更具科技感
                return new SolidColorBrush(Color.FromArgb(64, 0, 255, 255)); // #4000FFFF
            }

            return Brushes.Transparent;
        }

        public object[] ConvertBack(object value, Type[] targetTypes, object parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }
    public class HeroStats
    {
        public string HeroName { get; set; }
        public int Count { get; set; }
        public string CountLabel { get; set; } // 用于显示 "禁用次数:" 或 "选择次数:"
        public string HeroImagePath { get; set; }
    }

    // 在 KplHelperClasses.cs 文件中找到并替换
    public class RecentMatchInfo
    {
        public string TeamAName { get; set; }
        public string TeamBName { get; set; }
        public string TeamALogo { get; set; }
        public string TeamBLogo { get; set; }
        public string TeamAScore { get; set; }
        public string TeamBScore { get; set; }
        public string MatchState { get; set; }
        public string MatchDate { get; set; } // 新增：比赛日期
        public string MatchTime { get; set; } // 新增：比赛时间
    }

    public class LaneHeroData
    {
        public string HeroName { get; set; }
        public string StatDisplay { get; set; } // 用于统一显示 "胜率: 55.23%" 或 "使用: 123局"
        public string HeroImagePath { get; set; }
    }
}
