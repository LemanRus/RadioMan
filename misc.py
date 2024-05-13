from kivy.properties import NumericProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivymd.uix.behaviors import CircularRippleBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField
from kivymd.uix.appbar import MDTopAppBar, MDTopAppBarTitle


class ImageButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        self.ripple_scale = 0.85
        super().__init__(**kwargs)


class MaxLengthInput(TextInput):
    max_length = NumericProperty(0)

    def insert_text(self, substring, from_undo=False):
        if len(self.text) < self.max_length:
            return super().insert_text(substring, from_undo=from_undo)


class MDGridScreen(GridLayout):
    pass


class MDIconCard(MDCard):
    pass


class MDShortenLabel(MDLabel):
    pass


class MDPaddedList(MDList):
    pass


class MDBackTopBar(MDTopAppBar):
    pass


class MDNoBackTopBar(MDTopAppBar):
    pass


class MD50spIconButton(MDIconButton):
    pass


class MDDumbLabel(MDLabel):
    pass


class MDTextLabel(MDLabel):
    pass


class MDPaddedCard(MDCard):
    pass


class MDCentered06TextField(MDTextField):
    pass


class MDVerticalCard(MDCard):
    pass


class MDAdaptiveBoxLayout(MDBoxLayout):
    pass


class MDRaisedCenteredButton(MDButton):
    pass


class MDCenteredTopAppBarTitle(MDTopAppBarTitle):
    pass
