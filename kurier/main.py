import wx
from async_gui.toolkits.wx import WxEngine


engine = WxEngine()


class Application(wx.Frame):
    WINDOW_TITLE = "Kurier"
    DEFAULT_SIZE = (800, 600)

    def __init__(self):
        super(Application, self).__init__(None, title=self.WINDOW_TITLE, size=self.DEFAULT_SIZE)
        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        pass


if __name__ == '__main__':
    app = wx.App(redirect=False)
    engine.main_app = app
    Application()
    app.MainLoop()
