#!/usr/bin/env python3
import traceback
import justpy as jp
from starlette.applications import Starlette
import uvicorn
import inspect
import time
import asyncio
from contextlib import contextmanager
from matplotlib import pyplot as plt
from .utils import handle_exceptions, provide_arguments

# start uvicorn with auto-reload; afterwards the auto-reloaded process should not start uvicorn again
if not inspect.stack()[-2].filename.endswith('spawn.py'):
    uvicorn.run('nice_gui:ui', host='0.0.0.0', port=80, lifespan='on', reload=True)

wp = jp.QuasarPage(delete_flag=False, title='Nice GUI', favicon='favicon.png')
wp.head_html = '<script>confirm = () => true;</script>'  # HACK: avoid confirmation dialog for reload

main = jp.Div(a=wp, classes='q-ma-md column items-start', style='row-gap: 1em')
main.add_page(wp)
jp.justpy(lambda: wp, start_server=False)

view_stack = [main]

class Element:

    def __init__(self, view: jp.HTMLBaseComponent):

        view_stack[-1].add(view)
        view.add_page(wp)
        self.view = view

    @property
    def text(self):
        return self.view.text

    @text.setter
    def text(self, text):
        self.view.text = text

    def set_text(self, text):
        self.view.text = text

    def __enter__(self):

        view_stack.append(self.view)

    def __exit__(self, *_):

        view_stack.pop()

class Plot(Element):

    def __init__(self, view, fig):

        super().__init__(view)
        self.fig = fig

    def __enter__(self):

        plt.figure(self.fig)

    def __exit__(self, *_):

        self.view.set_figure(plt.gcf())

class LinePlot(Plot):

    def __init__(self, view, fig, n, limit):

        super().__init__(view, fig)
        self.x = []
        self.Y = [[] for _ in range(n)]
        self.lines = [self.fig.gca().plot([], [])[0] for _ in range(n)]
        self.slice = slice(0 if limit is None else -limit, None)

    def with_legend(self, titles, **kwargs):

        self.fig.gca().legend(titles, **kwargs)
        self.view.set_figure(self.fig)
        return self

    def push(self, x, Y):

        self.x = [*self.x, *x][self.slice]
        for i in range(len(self.lines)):
            self.Y[i] = [*self.Y[i], *Y[i]][self.slice]
            self.lines[i].set_xdata(self.x)
            self.lines[i].set_ydata(self.Y[i])
        flat_y = [y_i for y in self.Y for y_i in y]
        self.fig.gca().set_xlim(min(self.x), max(self.x))
        self.fig.gca().set_ylim(min(flat_y), max(flat_y))
        self.view.set_figure(self.fig)

class Ui(Starlette):

    def __init__(self):
        # NOTE: we enhance our own ui object with all capabilities of jp.app
        self.__dict__.update(jp.app.__dict__)

        self.tasks = []

        @self.on_event('startup')
        def startup():
            [jp.run_task(t) for t in self.tasks]

    def label(self, text='', typography=[]):

        if isinstance(typography, str):
            typography = [typography]
        classes = ' '.join('text-' + t for t in typography)
        view = jp.Div(text=text, classes=classes)
        return Element(view)

    def link(self, text='', href='#', typography=[]):

        if isinstance(typography, str):
            typography = [typography]
        classes = ' '.join('text-' + t for t in typography)
        view = jp.A(text=text, href=href, classes=classes)
        return Element(view)

    def icon(self, name, size='20px', color='dark'):

        view = jp.QIcon(name=name, classes=f'q-pt-xs text-{color}', size=size)
        return Element(view)

    def button(self, text, icon=None, icon_right=None, on_click=None):

        view = jp.QBtn(label=text, color='primary')
        if icon is not None:
            view.icon = icon
        if icon_right is not None:
            view.icon_right = icon_right
        if on_click is not None:
            view.on('click', handle_exceptions(provide_arguments(on_click)))
        return Element(view)

    def checkbox(self, text, on_change=None):

        view = jp.QCheckbox(text=text)
        if on_change is not None:
            view.on('input', handle_exceptions(provide_arguments(on_change, 'value')))
        return Element(view)

    def switch(self, text, on_change=None):

        view = jp.QToggle(text=text)
        if on_change is not None:
            view.on('input', handle_exceptions(provide_arguments(on_change, 'value')))
        return Element(view)

    def radio(self, options, value=None, on_change=None):

        view = jp.QOptionGroup(value=value, options=[{'label': o, 'value': o} for o in options])
        if on_change is not None:
            view.on('input', handle_exceptions(provide_arguments(on_change, 'value')))
        return Element(view)

    def select(self, options, value=None, on_change=None):

        view = jp.QSelect(value=value, options=options)
        if on_change is not None:
            view.on('input', handle_exceptions(provide_arguments(on_change, 'value')))
        return Element(view)

    def slider(self, min, max, on_change=None):

        view = jp.QSlider(min=min, max=max)
        if on_change is not None:
            view.on('input', handle_exceptions(provide_arguments(on_change, 'value')))
        return Element(view)

    def input(self, placeholder=None, value=None, type='text', on_change=None):

        view = jp.QInput(placeholder=placeholder, type=type)
        if value is not None:
            view.value = value
        if on_change is not None:
            view.on('input', handle_exceptions(provide_arguments(on_change, 'value')))
        return Element(view)

    @contextmanager
    def plot(self, close=True):

        fig = plt.figure()
        view = jp.Matplotlib()
        yield Plot(view, fig)
        view.set_figure(fig)
        if close:
            fig.close()

    def line_plot(self, n=1, limit=20):

        fig = plt.figure()
        view = jp.Matplotlib(fig=fig)
        return LinePlot(view, fig, n=n, limit=limit)

    def row(self):

        view = jp.QDiv(classes='row items-start', style='gap: 1em', delete_flag=False)
        return Element(view)

    def column(self):

        view = jp.QDiv(classes='column items-start', style='gap: 1em', delete_flag=False)
        return Element(view)

    def card(self):

        view = jp.QCard(classes='column items-start q-pa-md', style='gap: 1em', delete_flag=False)
        return Element(view)

    def timer(self, interval, callback, *, once=False):

        parent = view_stack[-1]

        async def timeout():

            await asyncio.sleep(interval)
            handle_exceptions(callback)()
            await parent.update()

        async def loop():

            while True:
                try:
                    start = time.time()
                    handle_exceptions(callback)()
                    await parent.update()
                    dt = time.time() - start
                    await asyncio.sleep(interval - dt)
                except:
                    traceback.print_exc()
                    await asyncio.sleep(interval)

        self.tasks.append((timeout() if once else loop()))

ui = Ui()
