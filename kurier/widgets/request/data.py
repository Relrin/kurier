import wx

from kurier.widgets.text_ctrl import TextCtrl


class RequestDataTab(wx.Panel):
    TAB_SIZE = 4

    def __init__(self, *args, **kwargs):
        super(RequestDataTab, self).__init__(*args, **kwargs)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.message_body_ctrl = TextCtrl(self)

        self.InitUI()

    def InitUI(self):
        self.sizer.Add(self.message_body_ctrl, proportion=1, flag=wx.EXPAND)
        self.SetSizer(self.sizer)

    def GetData(self):
        text = self.message_body_ctrl.GetValue()
        text = text.replace("\t", " " * self.TAB_SIZE)
        text = text.replace("\n", "")

        # Prevent replacing " and ' symbols onto duck-foot alternative on Mac OS X
        text = text.replace("’", "\'")
        text = text.replace("”", "\"")
        return text
