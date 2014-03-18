using System;
using System.IO;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Management;
using System.Text;
using System.Windows.Forms;
using System.Threading;
using System.Runtime.InteropServices;

namespace MAD_POS {
  public partial class MainF : Form {

    private ShellNotifications Notifications = new ShellNotifications();

    public MainF() {
      InitializeComponent();
    }

    //#region USB

    ////Data structure that stores the connection management
    //[StructLayout(LayoutKind.Sequential)]
    //public struct DEV_BROADCAST_VOLUME {
    //  public int dbcv_size;
    //  public int dbcv_devicetype;
    //  public int dbcv_reserved;
    //  public int dbcv_unitmask;
    //}

    ////Method to overwrite that manages the arrival of new storage units
    //protected override void WndProc(ref Message m) {
    //  //This definitions are stored in “dbt.h” and “winuser.h”
    //  // There has been a change in the devices
    //  const int WM_DEVICECHANGE = 0x0219;
    //  // System detects a new device
    //  const int DBT_DEVICEARRIVAL = 0x8000;
    //  // Device removal request
    //  const int DBT_DEVICEQUERYREMOVE = 0x8001;
    //  // Device removal failed
    //  const int DBT_DEVICEQUERYREMOVEFAILED = 0x8002;
    //  // Device removal is pending
    //  const int DBT_DEVICEREMOVEPENDING = 0x8003;
    //  // The device has been succesfully removed from the system
    //  const int DBT_DEVICEREMOVECOMPLETE = 0x8004;
    //  // Logical Volume (A disk has been inserted, such a usb key or external HDD)
    //  const int DBT_DEVTYP_VOLUME = 0x00000002;

    //  switch (m.Msg) {
    //    //If system devices change…
    //    case WM_DEVICECHANGE:
    //      switch (m.WParam.ToInt32()) {
    //        //If there is a new device…
    //        case DBT_DEVICEARRIVAL: {
    //          int devType = Marshal.ReadInt32(m.LParam, 4);
    //          //…and is a Logical Volume (A storage device)
    //          if (devType == DBT_DEVTYP_VOLUME) {
    //            DEV_BROADCAST_VOLUME vol;
    //            vol = (DEV_BROADCAST_VOLUME)Marshal.PtrToStructure(m.LParam, typeof(DEV_BROADCAST_VOLUME));
    //            MessageBox.Show("A storage device has been inserted, unit: " + UnitName(vol.dbcv_unitmask));
    //          }
    //        }
    //        break;
    //        case DBT_DEVICEREMOVECOMPLETE:
    //          MessageBox.Show("Device removed from system.");
    //        break;
    //        case SHCNE_MEDIAINSERTED: {
    //          int devType = Marshal.ReadInt32(m.LParam, 4);
    //          //…and is a Logical Volume (A storage device)
    //          if (devType == DBT_DEVTYP_VOLUME) {
    //            DEV_BROADCAST_VOLUME vol;
    //            vol = (DEV_BROADCAST_VOLUME)Marshal.PtrToStructure(m.LParam, typeof(DEV_BROADCAST_VOLUME));
    //            MessageBox.Show("A storage device has been inserted, unit: " + UnitName(vol.dbcv_unitmask));
    //          }
    //        }
    //        break;
    //        case SHCNE_MEDIAREMOVED: {
    //          int devType = Marshal.ReadInt32(m.LParam, 4);
    //          //…and is a Logical Volume (A storage device)
    //          if (devType == DBT_DEVTYP_VOLUME) {
    //            DEV_BROADCAST_VOLUME vol;
    //            vol = (DEV_BROADCAST_VOLUME)Marshal.PtrToStructure(m.LParam, typeof(DEV_BROADCAST_VOLUME));
    //            MessageBox.Show("A storage device has been inserted, unit: " + UnitName(vol.dbcv_unitmask));
    //          }
    //        }
    //        break;
    //      }
    //    break;
    //  }

    //  //After the custom manager, we want to use the default system’s manager
    //  base.WndProc(ref m);
    //}
 
    ////Method to detect the unit name (”D:”, “F:”, etc)
    //char UnitName(int unitmask) {
    //  char[] units ={'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'};
    //  int i = 0;

    //  //Convert the mask in an array, and search
    //  //the index for the first occurrenc (the unit’s name)
    //  System.Collections.BitArray ba = new System.Collections.BitArray(System.BitConverter.GetBytes(unitmask));

    //  foreach (bool var in ba) {
    //    if (var == true) break;
    //    i++;
    //  }

    //  return units[i];
    //}

    //#endregion USB

    private void startupMain() {
      tsCalendar.Text = DateTime.Now.ToString("dd MMMM yyyy, hh:mm:ss tt");
      tCalendar.Interval = 1000;
      tCalendar.Enabled = true;
      tcMenu.SelectedIndex = 0;
      rtbLogMessage.Clear();
      pbCopyFiles.Value = 0;
      rtbLogMessage.AppendText("Please insert Storage Devices to Download MAD data.\n");
    }

    private void tCalendar_Tick(object sender, EventArgs e) {
      tsCalendar.Text = DateTime.Now.ToString("dd MMMM yyyy, hh:mm:ss tt");
    }

    protected override void WndProc(ref Message m) {
      switch (m.Msg) {
        case (int)ShellNotifications.WM_SHNOTIFY:
          if (Notifications.NotificationReceipt(m.WParam, m.LParam)) {
            NotifyInfos infos = (NotifyInfos)Notifications.NotificationsReceived[Notifications.NotificationsReceived.Count - 1];
            NewOperation(infos);
          }
          break;
      }
      base.WndProc(ref m);
    }

    private void NewOperation(NotifyInfos infos) {
      switch (infos.Notification.ToString()) {
        case "SHCNE_MEDIAINSERTED": {
            rtbLogMessage.AppendText(String.Format("A storage device has been inserted, unit: {0}\n", infos.Item1));
            rtbLogMessage.AppendText("Copying MAD Data...\n");
            copyMADData(infos);
            rtbLogMessage.AppendText("Copying MAD Data Completed.\n");
          }
          break;
        case "SHCNE_MEDIAREMOVED": {
            rtbLogMessage.AppendText("Device removed from system.\n");
            Notifications.NotificationsReceived.Clear();
          }
          break;
        case "SHCNE_DRIVEADD": {
            rtbLogMessage.AppendText(String.Format("A storage device has been inserted, unit: {0}\n", infos.Item1));
            rtbLogMessage.AppendText("Copying MAD Data...\n");
            copyMADData(infos);
            rtbLogMessage.AppendText("Copying MAD Data Completed.\n");
          }
          break;
        case "SHCNE_DRIVEREMOVED": {
            rtbLogMessage.AppendText("Device removed from system.\n");
            Notifications.NotificationsReceived.Clear();
          }
          break;
      }
    }

    private static void DirectoryCopy(string sourceDirName, string destDirName, bool copySubDirs) {
      // Get the subdirectories for the specified directory.
      DirectoryInfo dir = new DirectoryInfo(sourceDirName);
      DirectoryInfo[] dirs = dir.GetDirectories();

      if (!dir.Exists) {
        throw new DirectoryNotFoundException("Source directory does not exist or could not be found: " + sourceDirName);
      }

      // If the destination directory doesn't exist, create it. 
      if (!Directory.Exists(destDirName)) {
        Directory.CreateDirectory(destDirName);
      }

      // Get the files in the directory and copy them to the new location.
      FileInfo[] files = dir.GetFiles();
      foreach (FileInfo file in files) {
        string temppath = Path.Combine(destDirName, file.Name);
        file.CopyTo(temppath, false);
      }

      // If copying subdirectories, copy them and their contents to new location. 
      if (copySubDirs) {
        foreach (DirectoryInfo subdir in dirs) {
          string temppath = Path.Combine(destDirName, subdir.Name);
          DirectoryCopy(subdir.FullName, temppath, copySubDirs);
        }
      }
    }

    private void copyMADData(NotifyInfos infos) {
      string sourceDirectory = AppDomain.CurrentDomain.BaseDirectory + "/data";
      string destinationDirectory = infos.Item1 + DateTime.Now.ToString("yyyyMMddhhmmss") + "-data";
      DirectoryCopy(sourceDirectory, @destinationDirectory, true);
    }

    private void MainF_Load(object sender, EventArgs e) {
      if (Notifications.RegisterChangeNotify(this.Handle, ShellNotifications.CSIDL.CSIDL_DESKTOP, true) > 0) {
        startupMain();
      } else {
        MessageBox.Show("Something problem with the computer");
        System.Windows.Forms.Application.Exit();
      }
    }

    private void MainF_Resize(object sender, EventArgs e) {
      this.Refresh();
    }

    private void MainF_FormClosing(object sender, FormClosingEventArgs e) {
      Notifications.UnregisterChangeNotify();
      System.Windows.Forms.Application.Exit();
    }
  }
}
