"""Pannable, zoomable graph area with axes and gridlines."""

from functools import partial
import imgui
import numpy as np

from concur.extra_widgets.pan_zoom import PanZoom, pan_zoom
import concur.draw as draw
from concur.core import lift, orr, optional, map


margins = [50, 10, -10, -20]


class Frame(PanZoom):
    def __init__(self, top_left, bottom_right, keep_aspect=True, fix_axis=None):
        """
        Simple PanZoom re-export with specified margins.

        Args:
            top_left:     Coordinates of the top left corner of the displayed content area.
            bottom_right: Coordinates of the bottom right corner of the displayed content area.
            keep_aspect:  Keep aspect ratio (x/y) equal to a given constant and zoom proportionally.
                          if keep_aspect==True, it is equivalent to keep_aspect==1.
            fix_axis:     Do not zoom in a given axis (`'x'`, `'y'`, or `None`).
        """
        super().__init__(top_left, bottom_right, keep_aspect=keep_aspect, fix_axis=fix_axis, margins=margins)


def _frame(content_gen, show_grid, tf, event_gen):

    min_tick_spacing = 50
    viewport_s = [r + o for r, o in zip(tf.view_s, margins)]
    viewport_c = np.concatenate([np.matmul(tf.s2c, [*viewport_s[:2], 1])[:2], np.matmul(tf.s2c, [*viewport_s[2:], 1])[:2]])
    bg = draw.rect_filled(*tf.view_s, (1, 1, 1, 1))
    if viewport_s[2] <= viewport_s[0] or viewport_s[3] <= viewport_s[1]:
        return bg

    def ticks(a, b, max_n_ticks):
        a, b = min(a, b), max(a, b)
        w = b - a
        min_sep = w / max_n_ticks
        candidates = np.array([10 ** np.floor(np.log10(min_sep)) * f for f in [1, 2, 5, 10]])
        sep = candidates[candidates > min_sep]
        if len(sep) == 0:
            return []
        else:
            sep = sep[0]
            return np.arange(np.ceil(a / sep) * sep, b + 1e-10, sep)

    hticks_c = ticks(viewport_c[3], viewport_c[1], (viewport_s[3] - viewport_s[1]) / min_tick_spacing)
    vticks_c = ticks(viewport_c[2], viewport_c[0], (viewport_s[2] - viewport_s[0]) / min_tick_spacing)
    hticks_s = np.matmul(tf.c2s, np.stack([np.zeros_like(hticks_c), hticks_c, np.ones_like(hticks_c)]))[1]
    vticks_s = np.matmul(tf.c2s, np.stack([vticks_c, np.zeros_like(vticks_c), np.ones_like(vticks_c)]))[0]

    def tick_labels():
        def tick_format(ticks_c, align):
            mag = max(1, abs(ticks_c[0]), abs(ticks_c[-1]))
            stride = abs(ticks_c[1] - ticks_c[0]) if len(ticks_c) > 1 else 1
            some_negative = ticks_c[0] < 0 or ticks_c[-1] < 0
            msd = int(np.floor(np.log10(mag)))
            lsd = int(np.minimum(0, np.floor(np.log10(stride))))
            if 1 + msd - lsd + (lsd < 0) + some_negative > 6:
                format = f"{{:{align}6.1g}}"
            else:
                format = f"{{:{align}6.{-lsd}f}}"
            return format
            print(f"msd: {msd}, stride: {lsd}, n_chars: {1 + msd - lsd + (lsd < 0) + some_negative}")
            format_x = f"{{:<6.{-lsd}f}}"
            format_y = f"{{:>6.{-lsd}f}}"
        xtick_labels = [
            draw.text(tick_format(vticks_c, "<").format(tc), ts, viewport_s[3], (0, 0, 0, 1))
            for ts, tc in zip(vticks_s, vticks_c)]
        ytick_labels = [
            draw.text(tick_format(hticks_c, ">").format(tc), viewport_s[0] - 45, ts - 7, (0, 0, 0, 1))
            for ts, tc in zip(hticks_s, hticks_c)]
        return orr(xtick_labels + ytick_labels)

    def grid():
        hlines = [draw.line(tf.view_s[0], tick, tf.view_s[2], tick, (0, 0, 0, 0.3)) for tick in hticks_s]
        vlines = [draw.line(tick, tf.view_s[1], tick, tf.view_s[3], (0, 0, 0, 0.3)) for tick in vticks_s]
        return orr(hlines + vlines)

    return orr([
        bg,
        lift(imgui.push_clip_rect, *viewport_s, True),
        optional(content_gen is not None, content_gen, tf, event_gen),
        optional(show_grid, grid),
        lift(imgui.pop_clip_rect),
        draw.rect(*viewport_s, (0, 0, 0, 1)),
        tick_labels(),
    ])


def frame(name, state, width=None, height=None, content_gen=None, drag_tag=None, down_tag=None, hover_tag=None, show_grid=True):
    """The frame widget.

    `state` is an instance of `Frame`. See the
    [plot example](https://github.com/potocpav/python-concur/blob/master/examples/plot.py)
    for an usage example.

    Content is specified using `content_gen`, analogously to how it's done in `concur.extra_widgets.image.image`.
    """
    def content_gen_with_opt_events(tf, event_gen):
        if drag_tag or down_tag or hover_tag:
            kwargs = dict(tf=tf, event_gen=event_gen)
        else:
            kwargs = dict(tf=tf)
        return optional(content_gen is not None, content_gen, **kwargs)

    return map(
        lambda v: ((v[0], v[1][0]) if v[1][0] is not None else v[1][1]),
        pan_zoom(
            name, state, width, height,
            content_gen=partial(_frame, content_gen_with_opt_events, show_grid),
            drag_tag=drag_tag, down_tag=down_tag, hover_tag=hover_tag
        )
    )
