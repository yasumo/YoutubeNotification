import wx
import wx.adv
import discordbot

TRAY_TOOLTIP = 'test app'
TRAY_ICON = 'icon/icon.ico'


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)

    return item


def post_discord(str):
    print(str)
    pass


# def open_site():
#     print("open site.")
#     pass
    # import webbrowser
    # webbrowser.open_new(r"https://www.google.com/")


class TaskBarIcon(wx.adv.TaskBarIcon):

    def __init__(self, frame):
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, self.on_test_discord)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Test Discord', self.on_test_discord)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)

        return menu

    def set_icon(self, path):
        icon = wx.Icon(wx.Bitmap(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

#    def on_open_site(self, event):
#        open_site()

    def on_test_discord(self, event):
        post_discord("test")

    def on_exit(self, event):
        print('exit')
        wx.CallAfter(self.Destroy)
        self.frame.Close()


class App(wx.App):

    def OnInit(self):
        frame=wx.Frame(None)
        self.SetTopWindow(frame)
        TaskBarIcon(frame)

        print('launch App')
        return True
