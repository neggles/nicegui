from nicegui.deprecation import deprecated
from os import getenv

from .aggrid import AgGrid
from .audio import Audio
from .avatar import Avatar
from .badge import Badge
from .button import Button
from .card import Card
from .card import CardActions
from .card import CardSection
from .chart import Chart
from .chat_message import ChatMessage
from .checkbox import Checkbox
from .color_input import ColorInput
from .color_picker import ColorPicker
from .colors import Colors
from .column import Column
from .dark_mode import DarkMode
from .date import Date
from .dialog import Dialog
from .expansion import Expansion
from .grid import Grid
from .html import Html
from .icon import Icon
from .image import Image
from .input import Input
from .interactive_image import InteractiveImage
from .joystick import Joystick
from .keyboard import Keyboard
from .knob import Knob
from .label import Label
from .link import Link
from .link import LinkTarget
from .log import Log
from .markdown import Markdown
from .menu import Menu
from .menu import MenuItem
from .mermaid import Mermaid
from .number import Number
from .plotly import Plotly
from .progress import CircularProgress
from .progress import LinearProgress
from .query import query
from .radio import Radio
from .row import Row
from .scene import Scene
from .select import Select
from .separator import Separator
from .slider import Slider
from .spinner import Spinner
from .splitter import Splitter
from .stepper import Step
from .stepper import Stepper
from .stepper import StepperNavigation
from .switch import Switch
from .table import Table
from .tabs import Tab
from .tabs import TabPanel
from .tabs import TabPanels
from .tabs import Tabs
from .textarea import Textarea
from .time import Time
from .toggle import Toggle
from .tooltip import Tooltip
from .tree import Tree
from .upload import Upload
from .video import Video

__all__ = [
    "AgGrid",
    "Audio",
    "Avatar",
    "Badge",
    "Button",
    "Card",
    "CardActions",
    "CardSection",
    "Chart",
    "ChatMessage",
    "Checkbox",
    "ColorInput",
    "ColorPicker",
    "Colors",
    "Column",
    "DarkMode",
    "Date",
    "Dialog",
    "Expansion",
    "Grid",
    "Html",
    "Icon",
    "Image",
    "Input",
    "InteractiveImage",
    "Joystick",
    "Keyboard",
    "Knob",
    "Label",
    "Link",
    "LinkTarget",
    "Log",
    "Markdown",
    "Menu",
    "MenuItem",
    "Mermaid",
    "Number",
    "Plotly",
    "CircularProgress",
    "LinearProgress",
    "query",
    "Radio",
    "Row",
    "Scene",
    "Select",
    "Separator",
    "Slider",
    "Spinner",
    "Splitter",
    "Step",
    "Stepper",
    "StepperNavigation",
    "Switch",
    "Table",
    "Tab",
    "TabPanel",
    "TabPanels",
    "Tabs",
    "Textarea",
    "Time",
    "Toggle",
    "Tooltip",
    "Tree",
    "Upload",
    "Video",
]


if getenv("MATPLOTLIB", "true").lower() == "true":
    from .line_plot import LinePlot
    from .pyplot import Pyplot

    plot = deprecated(Pyplot, "ui.plot", "ui.pyplot", 317)
    __all__.extend(["line_plot", "pyplot", "plot"])
