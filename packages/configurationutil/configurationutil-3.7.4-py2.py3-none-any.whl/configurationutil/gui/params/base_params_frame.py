# encoding: utf-8

from abc import ABCMeta, abstractmethod
from future.utils import with_metaclass
from collections import OrderedDict
from uiutil import (BaseScrollFrame,
                    BaseFrame,
                    Position,
                    Separator,
                    Label,
                    Button,
                    TextEntry,
                    RadioButton,
                    Combobox)
from uiutil.tk_names import (askquestion,
                             E,
                             W,
                             S,
                             NSEW,
                             EW)


class HeadingsFrame(BaseFrame):

    def __init__(self,
                 headings,
                 *args,
                 **kwargs):
        super(HeadingsFrame, self).__init__(*args,
                                            **kwargs)

        for heading in headings:
            Label(text=heading,
                  column=Position.START if heading == headings[0] else Position.NEXT,
                  sticky=W)

        Separator()

        self.nice_grid_columns()


class ParamsBaseConfigFrame(with_metaclass(ABCMeta, BaseFrame, object)):

    BUTTON_WIDTH = 2
    KEY_ENTRY_WIDTH = 15
    VALUE_ENTRY_WIDTH = 30
    HEADINGS = [
        u'Key',
        u'Value'
    ]

    def __init__(self,
                 sort_params=False,
                 canvas_height=120,
                 canvas_width=460,
                 *args,
                 **kwargs):

        super(ParamsBaseConfigFrame, self).__init__(*args,
                                                    **kwargs)

        self._sort_params = sort_params
        self._canvas_height = canvas_height
        self._canvas_width = canvas_width

        self._radio_list = OrderedDict()
        self._param_elements = OrderedDict()

        self._draw()

    def _draw(self):

        self._build_headings_frame()

        Separator()

        self._build_records_frame()

        Separator()

        self._build_button_frame()

        self.nice_grid()

    def _build_headings_frame(self):

        self.headings_frame = HeadingsFrame(headings=self.HEADINGS,
                                            sticky=NSEW)

    def _build_records_frame(self):

        self._scroll_frame = BaseScrollFrame(parent=self,
                                             canvas_height=self._canvas_height,
                                             canvas_width=self._canvas_width)
        self._scroll_frame.grid(row=1,
                                column=0,
                                sticky=NSEW)

        self.draw_records()

        self._scroll_frame.nice_grid_columns()

    def draw_records(self):

        select_next_row = True

        params = sorted(self._params) if self._sort_params else self._params

        for param in params:
            self._draw_param(param)

            if select_next_row:
                self._radio_list[param].value = param
                select_next_row = False

        self._draw_param(u'')

    def _draw_param(self,
                    key):

        self._radio_list[key] = RadioButton(frame=self._scroll_frame,
                                            value=key,
                                            row=Position.NEXT,
                                            column=Position.START,
                                            sticky=W)

        # Get the key values
        key_values = self.key_field_values(key=key)

        if isinstance(key_values, list):
            key_field = Combobox(frame=self._scroll_frame,
                                 postcommand=lambda k=key: self.populate_key_field(k),
                                 width=self.KEY_ENTRY_WIDTH,
                                 column=Position.NEXT,
                                 sticky=EW,
                                 sort=True)

            key_field.value = key

        else:
            key_field = TextEntry(frame=self._scroll_frame,
                                  value=key_values,
                                  width=self.KEY_ENTRY_WIDTH,
                                  column=Position.NEXT,
                                  sticky=EW)

        self._param_elements[key] = key_field

    def _build_button_frame(self):

        self.button_frame = BaseFrame(#row=Position.NEXT,
                                      sticky=(E, S))

        self.delete_record_button = Button(frame=self.button_frame,
                                           text=u'-',
                                           width=self.BUTTON_WIDTH,
                                           command=self._delete,
                                           column=Position.START
                                           )

        self.add_record_button = Button(frame=self.button_frame,
                                        text=u'+',
                                        width=self.BUTTON_WIDTH,
                                        command=self._add,
                                        column=Position.NEXT
                                        )

        self.button_frame.nice_grid()

    def _add(self):
        self.update_params()
        self._refresh_scroll_frame()

    def _delete(self):
        selected = self.selected
        # TODO: Selected could be '', for a new unsaved value.
        #       it will not be clear to a user why it can't be removed.
        if selected:
            result = askquestion(u"Delete Record",
                                 u"Are you sure you want to delete {r}?".format(r=selected),
                                 icon=u'warning',
                                 parent=self)

            if result == u'yes':
                self._perform_delete(selected=selected)

                self.update_params()
                self._refresh_scroll_frame()

    def _refresh_scroll_frame(self):

        self._radio_list = OrderedDict()
        self._param_elements = OrderedDict()

        self._scroll_frame.destroy()
        self._build_records_frame()
        self.nice_grid()

        self.update_geometry()

    @abstractmethod
    def _perform_delete(self,
                        selected):
        pass

    @abstractmethod
    def update_params(self):
        pass

    @property
    def params(self):
        return self._params

    @property
    def selected(self):
        any_key = self._radio_list.keys()[0]
        return self._radio_list[any_key].value

    def key_field_values(self,
                         key):
        return key

    def populate_key_field(self,
                           key):
        pass
