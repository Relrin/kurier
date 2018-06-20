import wx

from kurier.widgets.text_ctrl import TextCtrl


class RequestDataTab(wx.Panel):

    def __init__(self, *args, **kwargs):
        super(RequestDataTab, self).__init__(*args, **kwargs)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.message_body_ctrl = TextCtrl(self)

        self.InitUI()

    def InitUI(self):
        self.sizer.Add(self.message_body_ctrl, proportion=1, flag=wx.EXPAND)
        self.SetSizer(self.sizer)
