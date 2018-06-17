from wx.lib.agw.aui import AuiNotebook
from wx.lib.agw.aui import AUI_NB_CLOSE_ON_ACTIVE_TAB, AUI_NB_MIDDLE_CLICK_CLOSE, \
    AUI_NB_TAB_MOVE, AUI_NB_TAB_EXTERNAL_MOVE, AUI_NB_TAB_SPLIT, AUI_NB_CLOSE_BUTTON

from kurier.widgets.response.headers import ResponseHeadersTab
from kurier.widgets.response.properties import ResponsePropertiesTab
from kurier.widgets.response.data import ResponseDataTab


class ResponseNotebook(AuiNotebook):

    def __init__(self, *args, **kwargs):
        super(ResponseNotebook, self).__init__(*args, **kwargs)
        self.SetAGWWindowStyleFlag(
            self.GetAGWWindowStyleFlag()
            & ~AUI_NB_CLOSE_ON_ACTIVE_TAB
            & ~AUI_NB_MIDDLE_CLICK_CLOSE
            & ~AUI_NB_TAB_MOVE
            & ~AUI_NB_TAB_EXTERNAL_MOVE
            & ~AUI_NB_TAB_SPLIT
            & ~AUI_NB_CLOSE_BUTTON
        )
        self.properties_tab = None
        self.headers_tab = None
        self.data_tab = None

        self.InitUI()

    def InitUI(self):
        self.properties_tab = ResponsePropertiesTab(self)
        self.AddPage(self.properties_tab, "Properties", select=True)

        self.headers_tab = ResponseHeadersTab(self)
        self.AddPage(self.headers_tab, "Headers", select=False)

        self.data_tab = ResponseDataTab(self)
        self.AddPage(self.data_tab, "Message body", select=False)
