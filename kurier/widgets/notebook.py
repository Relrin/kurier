import wx

from wx.lib.agw.aui import AuiNotebook
from wx.lib.agw.aui import AUI_NB_CLOSE_ON_ACTIVE_TAB, AUI_NB_MIDDLE_CLICK_CLOSE, \
    AUI_NB_TAB_MOVE, EVT_AUINOTEBOOK_PAGE_CLOSED, AUI_NB_TAB_EXTERNAL_MOVE, \
    AUI_NB_TAB_SPLIT

from kurier.amqp.events import EVT_UPDATE_AMQP_TAB_NAME
from kurier.widgets.amqp_tab import AmqpTab


class CustomAuiNotebook(AuiNotebook):
    MAX_TAB_LABEL_LENGTH = 25

    def __init__(self, parent, *args, **kwargs):
        super(CustomAuiNotebook, self).__init__(parent, *args, **kwargs)
        self.SetAGWWindowStyleFlag(
            self.GetAGWWindowStyleFlag()
            & ~AUI_NB_CLOSE_ON_ACTIVE_TAB
            & ~AUI_NB_MIDDLE_CLICK_CLOSE
            & ~AUI_NB_TAB_MOVE
            & ~AUI_NB_TAB_EXTERNAL_MOVE
            & ~AUI_NB_TAB_SPLIT
        )

        self.InitUI()
        self.BindEvents()

    def InitUI(self):
        self.AddNewTabAsButton()
        self.AddNewTab()

    def BindEvents(self):
        self.Bind(EVT_AUINOTEBOOK_PAGE_CLOSED, self.OnTabClose)
        self.Bind(EVT_UPDATE_AMQP_TAB_NAME, self.OnUpdateAmqpTabName)

    def AddNewTab(self, tab_name="New tab"):
        new_tab = AmqpTab(self)
        self.InsertPage(self.GetPageCount(), new_tab, tab_name, select=True)

    def AddNewTabAsButton(self):
        new_tab_button = wx.Control(self)
        new_tab_button.isNewTabButton = True
        self.InsertPage(0, new_tab_button, "+", select=False)

    def InsertPage(self, page_index, page, *args, **kwargs):
        super(CustomAuiNotebook, self).InsertPage(page_index, page, *args, **kwargs)
        if self.GetPageCount() > 1:
            self.SetAGWWindowStyleFlag(self.GetAGWWindowStyleFlag() | AUI_NB_CLOSE_ON_ACTIVE_TAB)

    def OnTabClose(self, event):
        event.Skip()
        if self.GetPageCount() <= 2:
            self.AddNewTab()

    def OnTabClicked(self, event):
        super(CustomAuiNotebook, self).OnTabClicked(event)

        event.Skip()
        page = self.GetCurrentPage()
        if getattr(page, 'isNewTabButton', False):
            self.AddNewTab()

            control = event.GetEventObject()
            window = control.GetWindowFromIdx(self.GetPageCount() - 1)
            self.SetSelectionToWindow(window)

    def OnUpdateAmqpTabName(self, event):
        index = self.GetSelection()
        new_page_label = "exchange:{}; routing key:{}".format(
            event.GetExchangeName(),
            event.GetRoutingKey()
        )[:self.MAX_TAB_LABEL_LENGTH]
        self.SetPageText(index, new_page_label)
