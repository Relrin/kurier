import wx.stc


class TextCtrl(wx.TextCtrl):
    DEFAULT_STYLE = wx.TE_MULTILINE | wx.TE_RICH | wx.HSCROLL
    READONLY_FLAGS = wx.TE_READONLY

    def __init__(self, *args, **kwargs):
        is_readonly = kwargs.pop('readonly', False)
        kwargs['style'] = kwargs.get('style', self.DEFAULT_STYLE)

        if is_readonly:
            kwargs['style'] |= self.READONLY_FLAGS

        wx.TextCtrl.__init__(self, *args, **kwargs)
