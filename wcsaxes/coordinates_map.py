from .coordinate_helpers import CoordinateHelper
from .transforms import WCSWorld2PixelTransform
from .utils import coord_type_from_ctype

from . import six


class CoordinatesMap(object):

    def __init__(self, axes, wcs):

        # Keep track of parent axes and WCS
        self._axes = axes
        self._wcs = wcs

        # Set up transform
        self._transform = WCSWorld2PixelTransform(self._wcs)

        # Set up coordinates
        self._coords = {}
        for coord_index in [0, 1]:
            coord_type = coord_type_from_ctype(wcs.wcs.ctype[coord_index])
            self._coords[coord_index] = CoordinateHelper(parent_axes=axes,
                                                         transform=self._transform,
                                                         coord_index=coord_index,
                                                         coord_type=coord_type)


        # Set up aliases for coordinates
        name_1 = self._wcs.wcs.ctype[0][:4].replace('-', '')
        self._coords[name_1.lower()] = self._coords[0]
        name_2 = self._wcs.wcs.ctype[1][:4].replace('-', '')
        self._coords[name_2.lower()] = self._coords[1]

        # Common default settings
        self._coords[0].set_axislabels_position('b')
        self._coords[1].set_axislabels_position('l')
        self._coords[0].set_ticklabels_position('b')
        self._coords[1].set_ticklabels_position('l')

    def __getitem__(self, item):
        if isinstance(item, six.string_types):
            return self._coords[item.lower()]
        else:
            return self._coords[item]

    def set_visible(self, visibility):
        raise NotImplementedError()

    def enable_offset_mode(self, reference_coordinates):
        raise NotImplementedError()

    def disable_offset_mode(self):
        raise NotImplementedError()

    def grid(self, draw_grid=True, **kwargs):
        """
        Plot gridlines for both coordinates.

        Standard matplotlib appearance options (color, alpha, etc.) can be
        passed as keyword arguments.

        Parameters
        ----------
        draw_grid : bool
            Whether to show the gridlines
        """
        self[0].grid(draw_grid=draw_grid, **kwargs)
        self[1].grid(draw_grid=draw_grid, **kwargs)