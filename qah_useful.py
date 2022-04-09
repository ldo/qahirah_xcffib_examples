"""Useful common definitions for qahirah_xcffib_examples programs.
"""
#+
# Copyright 2022 by Lawrence D'Oliveiro <ldo@geek-central.gen.nz>. This
# code is licensed CC0
# <https://creativecommons.org/publicdomain/zero/1.0/>; do with it
# what you will.
#-

from qahirah import \
    CAIRO, \
    Context, \
    Colour, \
    Pattern, \
    Vector, \
    Rect

def flat_bevel \
  (
    gx : Context,
    *,
    bounds : Rect, # bounds of widget
    base_colour : Colour, # colour to use for main part of widget
    border : float, # width of bevel
    invert : bool, # True for inverted button state, False for normal
    colour_adjust_factor : float = 0.5,
      # factor for lightening/darkening base_colour to simulate highlight/shadow
      # 0 to use base_colour unchanged, 1 for maximum bright/dark
  ) :
    "draws a filled rectangle with a faceted bevelled frame, simulating a light" \
    " coming from the upper left."
    (gx
        .set_source_colour(base_colour)
        .rectangle(bounds)
        .fill()
    )
    inner_frame = bounds.inset(border * Vector(1, 1))
    points = list \
      (
        zip
          (
            list(p.pt for p in bounds.to_path().segments[0].points),
            list(p.pt for p in inner_frame.to_path().segments[0].points),
          )
      )
    colours = \
        [
            base_colour.replace_hsva
              (
                v = lambda v : 1 - ((1 - colour_adjust_factor) * (1 - v)),
                  # lighten
              ),
            base_colour.replace_hsva
              (
                v = lambda v : (1 - colour_adjust_factor) * v
                  # darken
              ),
        ]
    for i in range(4) :
        prev = points[i - 1]
        cur = points[i]
        (gx
            .move_to(prev[1])
            .line_to(prev[0])
            .line_to(cur[0])
            .line_to(cur[1])
            .close_path()
            .set_source_colour(colours[int(invert) ^ (i // 2)])
            .fill()
        )
    #end for
#end flat_bevel

def round_bevel \
  (
    gx : Context,
    *,
    bounds : Rect, # bounds of widget
    base_colour : Colour, # colour to use for main part of widget
    border : float, # width of bevel
    invert : bool, # True for inverted button state, False for normal
    colour_adjust_factor : float = 0.5,
      # factor for lightening/darkening base_colour to simulate highlight/shadow
      # 0 to use base_colour unchanged, 1 for maximum bright/dark
  ) :
    (gx
        .set_source_colour(base_colour)
        .rectangle(bounds)
        .fill()
    )
    inner_frame = bounds.inset(border * Vector(1, 1))
    points = list \
      (
        zip
          (
            list(p.pt for p in bounds.to_path().segments[0].points),
            list(p.pt for p in inner_frame.to_path().segments[0].points),
          )
      )
    colours = \
        [
            base_colour.replace_hsva
              (
                v = lambda v : 1 - ((1 - colour_adjust_factor) * (1 - v))
                  # lighten
              ),
            base_colour.replace_hsva
              (
                v = lambda v : (1 - colour_adjust_factor) * v
                  # darken
              ),
        ]
    gradients = \
        [
            Pattern.create_linear # left edge
              (
                p0 = (0, 0),
                p1 = (border, 0),
                colour_stops =
                    (
                        (0, colours[int(invert)]),
                        (1, base_colour),
                    )
              ),
            Pattern.create_linear # top edge
              (
                p0 = (0, 0),
                p1 = (0, border),
                colour_stops =
                    (
                        (0, colours[int(invert)]),
                        (1, base_colour),
                    )
              ),
            Pattern.create_linear # right edge
              (
                p0 = (bounds.right - border, 0),
                p1 = (bounds.right, 0),
                colour_stops =
                    (
                        (0, base_colour),
                        (1, colours[int(not invert)]),
                    )
              ),
            Pattern.create_linear # bottom edge
              (
                p0 = (0, bounds.bottom - border),
                p1 = (0, bounds.bottom),
                colour_stops =
                    (
                        (0, base_colour),
                        (1, colours[int(not invert)]),
                    )
              ),
        ]
    for i in range(4) :
        prev = points[i - 1]
        cur = points[i]
        (gx
            .move_to(prev[1])
            .line_to(prev[0])
            .line_to(cur[0])
            .line_to(cur[1])
            .close_path()
            .set_source(gradients[i])
            .fill()
        )
    #end for
#end round_bevel
