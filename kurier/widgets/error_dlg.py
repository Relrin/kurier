import wx


class ErrorDialog(wx.MessageDialog):
    DEFAULT_STYLE = wx.OK | wx.CENTRE | wx.ICON_ERROR

    def __init__(self, parent, exception, title="Error"):
        super(ErrorDialog, self).__init__(
            parent,
            message=self.ExceptionToString(exception),
            caption=title,
            style=self.DEFAULT_STYLE
        )

    def ExceptionToString(self, exception):
        return str(exception)

    def ShowDialog(self):
        self.ShowModal()
        self.Destroy()
