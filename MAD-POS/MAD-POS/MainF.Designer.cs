namespace MAD_POS {
  partial class MainF {
    /// <summary>
    /// Required designer variable.
    /// </summary>
    private System.ComponentModel.IContainer components = null;

    /// <summary>
    /// Clean up any resources being used.
    /// </summary>
    /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
    protected override void Dispose(bool disposing) {
      if (disposing && (components != null)) {
        components.Dispose();
      }
      base.Dispose(disposing);
    }

    #region Windows Form Designer generated code

    /// <summary>
    /// Required method for Designer support - do not modify
    /// the contents of this method with the code editor.
    /// </summary>
    private void InitializeComponent() {
      this.components = new System.ComponentModel.Container();
      this.ssMain = new System.Windows.Forms.StatusStrip();
      this.tsCalendar = new System.Windows.Forms.ToolStripStatusLabel();
      this.tCalendar = new System.Windows.Forms.Timer(this.components);
      this.tcMenu = new System.Windows.Forms.TabControl();
      this.tpStorage = new System.Windows.Forms.TabPage();
      this.tpBluetooth = new System.Windows.Forms.TabPage();
      this.lStorage = new System.Windows.Forms.Label();
      this.rtbLogMessage = new System.Windows.Forms.RichTextBox();
      this.pbCopyFiles = new System.Windows.Forms.ProgressBar();
      this.ssMain.SuspendLayout();
      this.tcMenu.SuspendLayout();
      this.tpStorage.SuspendLayout();
      this.SuspendLayout();
      // 
      // ssMain
      // 
      this.ssMain.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.tsCalendar});
      this.ssMain.Location = new System.Drawing.Point(0, 705);
      this.ssMain.Name = "ssMain";
      this.ssMain.Size = new System.Drawing.Size(1008, 24);
      this.ssMain.TabIndex = 0;
      // 
      // tsCalendar
      // 
      this.tsCalendar.BorderSides = System.Windows.Forms.ToolStripStatusLabelBorderSides.Right;
      this.tsCalendar.Name = "tsCalendar";
      this.tsCalendar.Size = new System.Drawing.Size(58, 19);
      this.tsCalendar.Text = "Calendar";
      // 
      // tCalendar
      // 
      this.tCalendar.Interval = 1000;
      this.tCalendar.Tick += new System.EventHandler(this.tCalendar_Tick);
      // 
      // tcMenu
      // 
      this.tcMenu.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
      this.tcMenu.Appearance = System.Windows.Forms.TabAppearance.Buttons;
      this.tcMenu.Controls.Add(this.tpStorage);
      this.tcMenu.Controls.Add(this.tpBluetooth);
      this.tcMenu.Location = new System.Drawing.Point(12, 12);
      this.tcMenu.Multiline = true;
      this.tcMenu.Name = "tcMenu";
      this.tcMenu.SelectedIndex = 0;
      this.tcMenu.Size = new System.Drawing.Size(984, 690);
      this.tcMenu.TabIndex = 1;
      // 
      // tpStorage
      // 
      this.tpStorage.Controls.Add(this.pbCopyFiles);
      this.tpStorage.Controls.Add(this.rtbLogMessage);
      this.tpStorage.Controls.Add(this.lStorage);
      this.tpStorage.Location = new System.Drawing.Point(4, 33);
      this.tpStorage.Name = "tpStorage";
      this.tpStorage.Padding = new System.Windows.Forms.Padding(3);
      this.tpStorage.Size = new System.Drawing.Size(976, 653);
      this.tpStorage.TabIndex = 0;
      this.tpStorage.Text = "Storage Devices";
      this.tpStorage.UseVisualStyleBackColor = true;
      // 
      // tpBluetooth
      // 
      this.tpBluetooth.Location = new System.Drawing.Point(4, 33);
      this.tpBluetooth.Name = "tpBluetooth";
      this.tpBluetooth.Padding = new System.Windows.Forms.Padding(3);
      this.tpBluetooth.Size = new System.Drawing.Size(976, 653);
      this.tpBluetooth.TabIndex = 1;
      this.tpBluetooth.Text = "Bluetooth";
      this.tpBluetooth.UseVisualStyleBackColor = true;
      // 
      // lStorage
      // 
      this.lStorage.Anchor = System.Windows.Forms.AnchorStyles.Top;
      this.lStorage.AutoSize = true;
      this.lStorage.Font = new System.Drawing.Font("Segoe UI", 21.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
      this.lStorage.Location = new System.Drawing.Point(128, 10);
      this.lStorage.Name = "lStorage";
      this.lStorage.Size = new System.Drawing.Size(748, 40);
      this.lStorage.TabIndex = 0;
      this.lStorage.Text = "Please insert Storage Devices to Download MAD data";
      this.lStorage.Visible = false;
      // 
      // rtbLogMessage
      // 
      this.rtbLogMessage.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
      this.rtbLogMessage.BackColor = System.Drawing.SystemColors.Window;
      this.rtbLogMessage.Location = new System.Drawing.Point(7, 6);
      this.rtbLogMessage.Name = "rtbLogMessage";
      this.rtbLogMessage.ReadOnly = true;
      this.rtbLogMessage.Size = new System.Drawing.Size(963, 615);
      this.rtbLogMessage.TabIndex = 1;
      this.rtbLogMessage.Text = "";
      // 
      // pbCopyFiles
      // 
      this.pbCopyFiles.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
      this.pbCopyFiles.Location = new System.Drawing.Point(7, 627);
      this.pbCopyFiles.Name = "pbCopyFiles";
      this.pbCopyFiles.Size = new System.Drawing.Size(963, 23);
      this.pbCopyFiles.Style = System.Windows.Forms.ProgressBarStyle.Continuous;
      this.pbCopyFiles.TabIndex = 2;
      // 
      // MainF
      // 
      this.AutoScaleDimensions = new System.Drawing.SizeF(9F, 21F);
      this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
      this.ClientSize = new System.Drawing.Size(1008, 729);
      this.Controls.Add(this.tcMenu);
      this.Controls.Add(this.ssMain);
      this.Font = new System.Drawing.Font("Segoe UI", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
      this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
      this.KeyPreview = true;
      this.Margin = new System.Windows.Forms.Padding(4, 5, 4, 5);
      this.MinimizeBox = false;
      this.Name = "MainF";
      this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
      this.Text = "MAD-POS";
      this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.MainF_FormClosing);
      this.Load += new System.EventHandler(this.MainF_Load);
      this.Resize += new System.EventHandler(this.MainF_Resize);
      this.ssMain.ResumeLayout(false);
      this.ssMain.PerformLayout();
      this.tcMenu.ResumeLayout(false);
      this.tpStorage.ResumeLayout(false);
      this.tpStorage.PerformLayout();
      this.ResumeLayout(false);
      this.PerformLayout();

    }

    #endregion

    private System.Windows.Forms.StatusStrip ssMain;
    private System.Windows.Forms.ToolStripStatusLabel tsCalendar;
    private System.Windows.Forms.Timer tCalendar;
    private System.Windows.Forms.TabControl tcMenu;
    private System.Windows.Forms.TabPage tpStorage;
    private System.Windows.Forms.TabPage tpBluetooth;
    private System.Windows.Forms.Label lStorage;
    private System.Windows.Forms.RichTextBox rtbLogMessage;
    private System.Windows.Forms.ProgressBar pbCopyFiles;

  }
}

