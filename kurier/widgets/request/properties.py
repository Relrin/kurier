import wx

from kurier.interfaces import IStateRestorable
from kurier.utils.converters import StringConverter, IntegerConverter
from kurier.widgets.list_ctrl import EditableListCtrl


class RequestPropertiesTab(IStateRestorable, wx.Panel):
    USED_COLUMNS = ["Property name", "Value"]
    UTILITY_ROW_TEXT = "Click here for adding a new property..."

    CUSTOM_CONVERTERS = {
        "delivery_mode": (IntegerConverter, {"default": 2})
    }

    def __init__(self, *args, **kwargs):
        super(RequestPropertiesTab, self).__init__(*args, **kwargs)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.properties_ctrl = EditableListCtrl(
            self,
            columns=self.USED_COLUMNS,
            utility_row_text=self.UTILITY_ROW_TEXT
        )

        self.InitUI()

    def InitUI(self):
        self.AddUtilityRow()

        self.sizer.Add(self.properties_ctrl, proportion=1, flag=wx.EXPAND)
        self.SetSizer(self.sizer)

    def InitFromState(self, **state):
        self.ClearPropertiesTab()

        properties = state.get("properties", {})
        for key, value in properties.items():
            self.AddNewProperty(key, value)

    def GetHeaderConverter(self, header):
        cls, options = self.CUSTOM_CONVERTERS.get(header, (StringConverter, {}))
        return cls(**options)

    def ClearPropertiesTab(self):
        self.DeleteUtilityRow()
        self.properties_ctrl.DeleteAllItems()
        self.AddUtilityRow()

    def AddUtilityRow(self):
        self.properties_ctrl.AddUtilityRow()
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelected)

    def DeleteUtilityRow(self):
        self.properties_ctrl.DeleteUtilityRow()
        self.Unbind(wx.EVT_LIST_ITEM_SELECTED, handler=self.OnListItemSelected)

    def AddNewProperty(self, header_name, value=wx.EmptyString):
        insert_index = self.properties_ctrl.GetItemCount() - 1
        self.properties_ctrl.AddNewRow(header_name, value, insert_index)

        # TODO: Add auto-completion for the property names so that they will be unique
        # if self.properties_ctrl.GetItemCount() > len(self.AVAILABLE_PROPERTIES):
        #     self.DeleteUtilityRow()

    def OnListItemSelected(self, event):
        event.Skip()
        row_info = event.GetItem()

        # TODO: Add new row and focus on selection a property from ComboBox (dynamic)
        if row_info.GetId() == self.properties_ctrl.GetItemCount() - 1:
            self.AddNewProperty('Key')

    def GetProperties(self):
        properties = {}

        rows = self.properties_ctrl.GetItemCount() - 1
        for row in range(rows):
            key = self.properties_ctrl.GetItem(itemIdx=row, col=0).GetText().strip()
            value = self.properties_ctrl.GetItem(itemIdx=row, col=1).GetText()
            converter = self.GetHeaderConverter(key)
            properties[key] = converter.to_internal_value(value)

        return properties
