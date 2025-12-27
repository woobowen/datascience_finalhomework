using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media.Imaging;

namespace KPLAssistant
{
    public partial class TeamAnalysisWindow : Window
    {
        private string imageRootPath = @"C:\Users\lenovo\Desktop\暑期课\大作业\";
        // Python解释器路径 (与你之前的代码保持一致)
        private string pythonPath = @"C:\Users\lenovo\AppData\Local\Programs\Python\Python312\python.exe";
        // Python脚本路径 (请确保将下文的python代码保存为这个文件)
        private string scriptPath = @"C:\Users\lenovo\Desktop\暑期课\大作业\team_analysis.py";

        public TeamAnalysisWindow()
        {
            InitializeComponent();
            PopulateTeamComboBox();
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

        private async void BtnGenerateReport_Click(object sender, RoutedEventArgs e)
        {
            if (TeamComboBox.SelectedItem == null)
            {
                MessageBox.Show("请先选择一支战队。", "提示");
                return;
            }

            string selectedTeam = TeamComboBox.SelectedItem.ToString().Replace(" ", ""); // 去除空格传递给Python

            LoadingOverlay.Visibility = Visibility.Visible;
            ReportTextBox.Text = "正在连接Python引擎进行分析...";

            try
            {
                string result = await Task.Run(() => RunPythonAnalysis(selectedTeam));
                ReportTextBox.Text = result;
            }
            catch (Exception ex)
            {
                ReportTextBox.Text = $"分析失败：\n{ex.Message}";
            }
            finally
            {
                LoadingOverlay.Visibility = Visibility.Collapsed;
            }
        }

        private string RunPythonAnalysis(string teamName)
        {
            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = pythonPath;
            // 传递参数：脚本路径 + 战队名
            start.Arguments = $"\"{scriptPath}\" \"{teamName}\"";
            start.UseShellExecute = false;
            start.RedirectStandardOutput = true;
            start.RedirectStandardError = true; // 获取错误信息
            start.CreateNoWindow = true;
            start.StandardOutputEncoding = Encoding.UTF8; // 确保中文不乱码
            start.StandardErrorEncoding = Encoding.UTF8;

            using (Process process = Process.Start(start))
            {
                using (StreamReader reader = process.StandardOutput)
                {
                    string result = reader.ReadToEnd();
                    string error = process.StandardError.ReadToEnd();

                    process.WaitForExit();

                    if (!string.IsNullOrEmpty(error))
                    {
                        // 如果有错误输出，返回错误信息（方便调试）
                        return $"Python 脚本错误:\n{error}\n\n部分输出:\n{result}";
                    }
                    return result;
                }
            }
        }
    }
}