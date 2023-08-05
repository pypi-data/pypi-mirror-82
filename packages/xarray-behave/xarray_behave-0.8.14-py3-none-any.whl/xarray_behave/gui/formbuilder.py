"""
Module for creating a form from a yaml file.

Example:

>>> widget = YamlFormWidget(yaml_file="example.yaml")
>>> widget.mainAction.connect(my_function)

my_function will get called with form data when user clicks the main button
(main button has type "button" and default "main action")

"""
# modified from https://sleap.ai/_modules/sleap/gui/formbuilder.html
import yaml
from typing import Any, Dict, List, Optional
try:
    import PySide2  # this will force pyqtgraph to use PySide instead of PyQt4/5
except ImportError:
    pass
from pyqtgraph.Qt import QtWidgets, QtCore, QtGui



class YamlDialog(QtGui.QDialog):
    def __init__(self, yaml_file, parent=None, title=None,
                 main_callback=None, callbacks={}):
        super().__init__(parent=parent)
        self.setWindowTitle(title)
        self.form = YamlFormWidget(yaml_file)
        if main_callback is None:
            def main_callback():
                """Accepts and closes dialog."""
                self.accept()
                self.close()
        self.form.mainAction.connect(main_callback)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.form)
        for button, callback in callbacks.items():
            self.form.buttons[button].clicked.connect(callback)
        self.setLayout(layout)


class YamlFormWidget(QtWidgets.QGroupBox):
    """
    Custom QWidget which creates form based on yaml file.

    Args:
        yaml_file: filename
        which_form (optional): key to form in yaml file, default "main"
    """

    mainAction = QtCore.Signal(dict)
    valueChanged = QtCore.Signal()

    def __init__(
        self,
        yaml_file,
        which_form: str = "main",
        field_options_lists: Optional[Dict[str, list]] = None,
        *args,
        **kwargs,
    ):
        super(YamlFormWidget, self).__init__(*args, **kwargs)

        with open(yaml_file, "r") as form_yaml:
            items_to_create = yaml.load(form_yaml, Loader=yaml.SafeLoader)

        self.which_form = which_form
        self.form_layout = FormBuilderLayout(
            items_to_create[self.which_form], field_options_lists=field_options_lists
        )
        self.setLayout(self.form_layout)

        if items_to_create[self.which_form]:
            for item in items_to_create[self.which_form]:
                if (
                    item["type"] == "button"
                    and item.get("default", "") == "main action"
                ):
                    self.buttons[item["name"]].clicked.connect(self.trigger_main_action)

        self.form_layout.valueChanged.connect(self.valueChanged)

    def __getitem__(self, key):
        """Return value for specified form field."""
        return FormBuilderLayout.get_widget_value(self.fields[key])

    def __setitem__(self, key, val):
        """Set value for specified form field."""
        FormBuilderLayout.set_widget_value(self.fields[key], val)

    @property
    def buttons(self):
        """Returns a list of buttons in form (so we can connect to handlers)."""
        return self.form_layout.buttons

    @property
    def fields(self):
        """Return a dict of {name: widget} fields in form."""
        return self.form_layout.fields

    def set_form_data(self, data):
        """Set data for form from dict."""
        self.form_layout.set_form_data(data)

    def get_form_data(self):
        """Returns dict of form data."""
        return self.form_layout.get_form_data()

    def trigger_main_action(self):
        """Emit mainAction signal with form data."""
        self.mainAction.emit(self.get_form_data())


class FormBuilderLayout(QtWidgets.QFormLayout):
    """
    Custom QFormLayout which populates itself from list of form fields.

    Args:
        items_to_create: list which gets passed to :meth:`get_form_data`
                         (see there for details about format)
    """

    valueChanged = QtCore.Signal()

    def __init__(self, items_to_create, field_options_lists=None, *args, **kwargs):
        super(FormBuilderLayout, self).__init__(*args, **kwargs)

        self.buttons = dict()
        self.fields = dict()
        self.field_options_lists = field_options_lists or dict()
        self.build_form(items_to_create)

    def get_form_data(self) -> dict:
        """Gets all user-editable data from the widgets in the form layout.

        Returns:
            Dict with key:value for each user-editable widget in layout
        """
        widgets = self.fields.values()
        data = {
            w.objectName(): self.get_widget_value(w)
            for w in widgets
            if len(w.objectName())
            and type(w) not in (QtWidgets.QLabel, QtWidgets.QPushButton)
        }
        stacked_data = [w.get_data() for w in widgets if type(w) == StackBuilderWidget]
        for stack in stacked_data:
            data.update(stack)
        return data

    def set_form_data(self, data: dict):
        """Set specified user-editable data.

        Args:
            data: dictionary of datay, key should match field name
        """
        widgets = self.fields
        for name, val in data.items():
            if name in widgets:
                self.set_widget_value(widgets[name], val)
            else:
                pass

    @staticmethod
    def set_widget_value(widget: QtWidgets.QWidget, val):
        """Set value for specific widget."""
        if hasattr(widget, "isChecked"):
            widget.setChecked(val)
        elif hasattr(widget, "value"):
            widget.setValue(val)
        elif hasattr(widget, "currentText"):
            widget.setCurrentText(str(val))
        elif hasattr(widget, "text"):
            widget.setText(str(val))
        else:
            print(f"don't know how to set value for {widget}")
        # for macOS we need to call repaint (bug in Qt?)
        widget.repaint()

    @staticmethod
    def get_widget_value(widget: QtWidgets.QWidget) -> Any:
        """Returns value of form field.

        This determines the method appropriate for the type of widget.

        Args:
            widget: The widget for which to return value.
        Returns:
            value (can be bool, numeric, string, or None)
        """
        if hasattr(widget, "isChecked"):
            val = widget.isChecked()
        elif hasattr(widget, "value"):
            val = widget.value()
        elif hasattr(widget, "currentText"):
            val = widget.currentText()
        elif hasattr(widget, "text"):
            val = widget.text()
        elif hasattr(widget, "currentIndex"):
            val = widget.currentIndex()
        else:
            print(widget)
            val = None
        if widget.property("field_data_type") == "sci":
            val = float(val)
        elif widget.property("field_data_type") == "int":
            val = int(val)
        elif widget.property("field_data_type").startswith("file_"):
            val = None if val == "None" else val
        return val

    def build_form(self, items_to_create: List[Dict[str, Any]]):
        """Adds widgets to form layout for each item in items_to_create.

        Args:
            items_to_create: list of dictionaries with keys

              * name: used as key when we return form data as dict
              * label: string to show in form
              * type: supports double, int, bool, list, button, stack,
                      file_dir, file_open
              * default: default value for form field
              * [options]: comma separated list of options,
                used for list or stack field-types
              * for stack, array of dicts w/ form data for each stack page

        A "stack" has a dropdown menu that determines which stack page to show.

        Returns:
            None.
        """
        if not items_to_create:
            return
        for item in items_to_create:
            # double: show spinbox (number w/ up/down controls)
            if item["type"] == "double":
                field = QtWidgets.QDoubleSpinBox()
                field.setValue(item["default"])
                field.valueChanged.connect(lambda: self.valueChanged.emit())

            # int: show spinbox (number w/ up/down controls)
            elif item["type"] == "int":
                field = QtWidgets.QSpinBox()
                if "range" in item.keys():
                    min, max = list(map(int, item["range"].split(",")))
                    field.setRange(min, max)
                elif item["default"] > 100:
                    min, max = 0, item["default"] * 10
                    field.setRange(min, max)
                field.setValue(item["default"])
                field.valueChanged.connect(lambda: self.valueChanged.emit())

            # bool: show checkbox
            elif item["type"] == "bool":
                field = QtWidgets.QCheckBox()
                field.setChecked(item["default"])
                field.stateChanged.connect(lambda: self.valueChanged.emit())

            # list: show drop-down menu
            elif item["type"] == "list":
                field = FieldComboWidget()

                if item["name"] in self.field_options_lists:
                    field.set_options(self.field_options_lists[item["name"]])
                elif "options" in item:
                    field.set_options(
                        item["options"].split(","), select_item=item.get("default", "")
                    )

                field.currentIndexChanged.connect(lambda: self.valueChanged.emit())

            # button
            elif item["type"] == "button":
                field = QtWidgets.QPushButton(item["label"])
                self.buttons[item["name"]] = field

            # string
            elif item["type"] == "string":
                field = QtWidgets.QLineEdit()
                val = item.get("default", "")
                val = "" if val is None else val
                field.setText(str(val))

            # stacked: show menu and form panel corresponding to menu selection
            elif item["type"] == "stacked":
                field = StackBuilderWidget(
                    item, field_options_lists=self.field_options_lists
                )

            # If we don't recognize the type, just show a text box
            else:
                field = QtWidgets.QLineEdit()
                field.setText(str(item.get("default", "")))
                if item["type"].split("_")[0] == "file":
                    field.setDisabled(True)

            # Store name and type on widget
            field.setObjectName(item["name"])
            field.setProperty("field_data_type", item.get("dtype", item["type"]))
            # Store widget by name
            self.fields[item["name"]] = field
            # Add field (and label if appropriate) to form layout
            if item["type"] in ("stacked"):
                self.addRow(field)
            elif item["type"] in ("button"):
                self.addRow("", field)
            else:
                self.addRow(item["label"] + ":", field)

            # file_[open|dir]: show button to select file/directory
            if item["type"].split("_")[0] == "file":
                self.addRow("", self._make_file_button(item, field))

    def _make_file_button(
        self, item: Dict, field: QtWidgets.QWidget
    ) -> QtWidgets.QPushButton:
        """Creates the button for a file_* field-type."""
        file_button = QtWidgets.QPushButton("Select " + item["label"])

        if item["type"].split("_")[-1] == "open":
            # Define function for button to trigger
            def select_file(*args, x=field):
                filter = item.get("filter", "Any File (*.*)")
                filename, _ = QtWidgets.QFileDialog.getOpenFileName(
                    None, directory=None, caption="Open File", filter=filter
                )
                if len(filename):
                    x.setText(filename)
                self.valueChanged.emit()

        elif item["type"].split("_")[-1] == "dir":
            # Define function for button to trigger
            def select_file(*args, x=field):
                filename = QtWidgets.QFileDialog.getExistingDirectory(None, directory=None, caption="Open File")
                if len(filename):
                    x.setText(filename)
                self.valueChanged.emit()

        else:
            select_file = lambda: print(f"no action set for type {item['type']}")

        file_button.clicked.connect(select_file)
        return file_button


class StackBuilderWidget(QtWidgets.QWidget):
    """
    A custom widget that shows different subforms depending on menu selection.

    Args:
        stack_data: Dictionary for field from `items_to_create`.
            The "options" key will give the list of options to show in
            menu. Each of the "options" will also be the key of a dictionary
            within stack_data that has the same structure as the dictionary
            passed to :meth:`FormBuilderLayout.build_form()`.
    """

    def __init__(self, stack_data, field_options_lists=None, *args, **kwargs):
        super(StackBuilderWidget, self).__init__(*args, **kwargs)

        self.option_list = stack_data["options"].split(",")

        self.field_options_lists = field_options_lists or None

        multi_layout = QtWidgets.QFormLayout()
        multi_layout.setFormAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.combo_box = QtWidgets.QComboBox()
        self.stacked_widget = ResizingStackedWidget()

        self.combo_box.activated.connect(self.switch_to_idx)

        self.page_layouts = dict()

        for page in self.option_list:

            # add page
            self.page_layouts[page] = FormBuilderLayout(
                stack_data[page], field_options_lists=self.field_options_lists
            )

            page_widget = QtWidgets.QGroupBox()
            page_widget.setLayout(self.page_layouts[page])

            self.stacked_widget.addWidget(page_widget)

            # add option to menu
            self.combo_box.addItem(page)

        if len(stack_data.get("label", "")):
            combo_label = f"{stack_data['label']}:"
        else:
            combo_label = ""

        multi_layout.addRow(combo_label, self.combo_box)
        multi_layout.addRow(self.stacked_widget)

        self.setValue(stack_data["default"])

        self.setLayout(multi_layout)

    def switch_to_idx(self, idx):
        """Switch currently shown widget from stack."""
        self.stacked_widget.setCurrentIndex(idx)
        # Only show if the widget contains more than an empty layout
        if len(self.stacked_widget.currentWidget().children()) > 1:
            self.stacked_widget.show()
        else:
            self.stacked_widget.hide()

    def value(self):
        """Returns value of menu."""
        return self.combo_box.currentText()

    def setValue(self, value):
        """Sets value of menu."""
        if value not in self.option_list:
            return
        idx = self.option_list.index(value)
        self.combo_box.setCurrentIndex(idx)
        self.switch_to_idx(idx)

    def get_data(self):
        """Returns value from currently shown subform."""
        return self.page_layouts[self.value()].get_form_data()


class FieldComboWidget(QtWidgets.QComboBox):
    """
    A custom ComboBox widget with method to easily add set of options.
    """

    def __init__(self, *args, **kwargs):
        super(FieldComboWidget, self).__init__(*args, **kwargs)
        self.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.setMinimumContentsLength(3)

    def set_options(self, options_list: List[str], select_item: Optional[str] = None):
        """
        Sets list of menu options.

        Args:
            options_list: List of items (strings) to show in menu.
            select_item: Item to select initially.

        Returns:
            None.
        """
        self.clear()
        for item in options_list:
            if item == "---":
                self.insertSeparator(self.count())
            else:
                self.addItem(item)
        if select_item is not None and select_item in options_list:
            idx = options_list.index(select_item)
            self.setCurrentIndex(idx)


class ResizingStackedWidget(QtWidgets.QStackedWidget):
    """
    QStackedWidget that updates its sizeHint and minimumSizeHint as needed.
    """

    def __init__(self, *args, **kwargs):
        super(ResizingStackedWidget, self).__init__(*args, **kwargs)

    def sizeHint(self):
        """Qt method."""
        return self.currentWidget().sizeHint()

    def minimumSizeHint(self):
        """Qt method."""
        return self.currentWidget().minimumSizeHint()
