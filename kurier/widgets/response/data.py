import wx

from kurier.utils.data_renderer import DataRenderer
from kurier.widgets.text_ctrl import TextCtrl


class ResponseDataTab(wx.Panel):

    def __init__(self, *args, **kwargs):
        super(ResponseDataTab, self).__init__(*args, **kwargs)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.message_body_ctrl = TextCtrl(self, readonly=True)

        self.InitUI()

    def InitUI(self):
        self.sizer.Add(self.message_body_ctrl, proportion=1, flag=wx.EXPAND)
        self.SetSizer(self.sizer)

    def SetText(self, response_data, mimetype):
        text = DataRenderer().Render(response_data, mimetype)
        self.message_body_ctrl.SetValue(text)

    def Clean(self):
        self.message_body_ctrl.Clear()

    def RenderBody(self, body, mimetype):
        self.Clean()
        self.SetText(body, mimetype)
