"""
This is a test of using the pytmx library with Tiled.
"""
import pygame as pg

import pytmx

from pytmx.util_pygame import load_pygame


class Renderer(object):
    """
    This object renders tile maps from Tiled
    """
    def __init__(self, filename):
        tm = load_pygame(filename, pixelalpha=True)
        self.size = tm.width * tm.tilewidth, tm.height * tm.tileheight
        self.tmx_data = tm

    def render(self, surface):

        tw = self.tmx_data.tilewidth
        th = self.tmx_data.tileheight
        gt = self.tmx_data.get_tile_image_by_gid

        if self.tmx_data.background_color:
            surface.fill(self.HTMLColorToRGB(self.tmx_data.background_color))

        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = gt(gid)
                    if tile:
                        surface.blit(tile, (x * tw, y * th))

            elif isinstance(layer, pytmx.TiledObjectGroup):
                pass

            elif isinstance(layer, pytmx.TiledImageLayer):
                image = gt(layer.gid)
                if image:
                    surface.blit(image, (0, 0))

    def make_map(self):
        temp_surface = pg.Surface(self.size)
        self.render(temp_surface)
        return temp_surface

    def HTMLColorToRGB(self, colorstring):
        """
        convert #RRGGBB to an (R, G, B) tuple

        Source: http://code.activestate.com/recipes/266466/
        """
        colorstring = colorstring.strip()
        if colorstring[0] == '#': colorstring = colorstring[1:]
        if len(colorstring) != 6:
            raise ValueError, "input #%s is not in #RRGGBB format" % colorstring
        r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
        r, g, b = [int(n, 16) for n in (r, g, b)]

        return (r, g, b)
