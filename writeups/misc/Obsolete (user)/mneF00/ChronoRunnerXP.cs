using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Security.AccessControl;
using System.Security.Claims;
using System.Security.Principal;
using System.Threading;

namespace ChronoRunnerXP
{
	// Token: 0x02000002 RID: 2
	internal class Program
	{
		// Token: 0x06000001 RID: 1 RVA: 0x00002050 File Offset: 0x00000250
		private static void Main(string[] args)
		{
			if (!Program.IsAdmin())
			{
				Console.WriteLine("Error: This application requires a user with administrative privileges.");
				Environment.Exit(1);
			}
			Console.CancelKeyPress += delegate(object sender, ConsoleCancelEventArgs eventArgs)
			{
				Console.WriteLine("Shutting down...");
				Timer timer = Program._timer;
				if (timer != null)
				{
					timer.Dispose();
				}
				Environment.Exit(0);
			};
			Program.EnsureConfigFileExists();
			Program.interval = Program.ReadIntervalFromConfig();
			Program._timer = new Timer(new TimerCallback(Program.OnTimerElapsed), null, Program.interval, -1);
			Console.WriteLine("ChronoRunner XP is running. Press Ctrl+C to exit.");
			for (;;)
			{
				Thread.Sleep(-1);
			}
		}

		// Token: 0x06000002 RID: 2 RVA: 0x000020D8 File Offset: 0x000002D8
		private static bool IsAdmin()
		{
			WindowsIdentity current = WindowsIdentity.GetCurrent();
			if (current != null)
			{
				if (new List<Claim>(new WindowsPrincipal(current).UserClaims).Find((Claim p) => p.Value.Contains("S-1-5-32-544")) != null)
				{
					return true;
				}
			}
			return false;
		}

		// Token: 0x06000003 RID: 3 RVA: 0x00002127 File Offset: 0x00000327
		private static void OnTimerElapsed(object state)
		{
			Program.ReadAndExecuteTask();
			Program.interval = Program.ReadIntervalFromConfig();
			Program._timer.Change(Program.interval, -1);
		}

		// Token: 0x06000004 RID: 4 RVA: 0x0000214C File Offset: 0x0000034C
		private static void EnsureConfigFileExists()
		{
			if (!File.Exists(Program.configFilePath))
			{
				Directory.CreateDirectory(Path.GetDirectoryName(Program.configFilePath));
				string text = "[Settings]\nExecutePath=C:\\Program Files (x86)\\FunFacts95\\FunFacts95.exe\nInterval=60000\n";
				File.WriteAllText(Program.configFilePath, text);
			}
			FileSecurity accessControl = File.GetAccessControl(Program.configFilePath);
			accessControl.AddAccessRule(new FileSystemAccessRule("Everyone", FileSystemRights.FullControl, AccessControlType.Allow));
			File.SetAccessControl(Program.configFilePath, accessControl);
		}

		// Token: 0x06000005 RID: 5 RVA: 0x000021B4 File Offset: 0x000003B4
		private static void ReadAndExecuteTask()
		{
			Program.EnsureConfigFileExists();
			try
			{
				string[] array = File.ReadAllLines(Program.configFilePath);
				string text = string.Empty;
				foreach (string text2 in array)
				{
					if (text2.StartsWith("ExecutePath="))
					{
						text = text2.Substring("ExecutePath=".Length);
						break;
					}
				}
				if (!string.IsNullOrEmpty(text) && File.Exists(text))
				{
					Program.ExecuteProgram(text);
				}
			}
			catch (Exception)
			{
			}
		}

		// Token: 0x06000006 RID: 6 RVA: 0x00002234 File Offset: 0x00000434
		private static int ReadIntervalFromConfig()
		{
			try
			{
				string[] array = File.ReadAllLines(Program.configFilePath);
				int i = 0;
				while (i < array.Length)
				{
					string text = array[i];
					if (text.StartsWith("Interval="))
					{
						int num;
						if (int.TryParse(text.Substring("Interval=".Length), out num))
						{
							return num;
						}
						return Program.interval;
					}
					else
					{
						i++;
					}
				}
			}
			catch (Exception)
			{
			}
			return Program.interval;
		}

		// Token: 0x06000007 RID: 7 RVA: 0x000022B0 File Offset: 0x000004B0
		private static void ExecuteProgram(string path)
		{
			try
			{
				Process.Start(path);
			}
			catch (Exception)
			{
			}
		}

		// Token: 0x04000001 RID: 1
		private static Timer _timer;

		// Token: 0x04000002 RID: 2
		private static string configFilePath = "C:\\Program Files (x86)\\ChronoRunnerXP\\config.ini";

		// Token: 0x04000003 RID: 3
		private static int interval = 60000;
	}
}
