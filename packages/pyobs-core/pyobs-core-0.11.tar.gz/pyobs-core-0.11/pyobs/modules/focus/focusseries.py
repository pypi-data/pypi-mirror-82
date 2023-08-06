import logging
from typing import Union
import threading
import numpy as np

from pyobs.comm import RemoteException
from pyobs.interfaces import IFocuser, ICamera, IAutoFocus, IFilters
from pyobs.events import FocusFoundEvent
from pyobs import PyObsModule, get_object
from pyobs.mixins import CameraSettingsMixin
from pyobs.modules import timeout
from pyobs.utils.focusseries import FocusSeries

log = logging.getLogger(__name__)


class AutoFocusSeries(PyObsModule, CameraSettingsMixin, IAutoFocus):
    """Module for auto-focusing a telescope."""

    def __init__(self, focuser: Union[str, IFocuser], camera: Union[str, ICamera], filters: Union[str, IFilters],
                 series: FocusSeries, offset: bool = False, *args, **kwargs):
        """Initialize a new auto focus system.

        Args:
            focuser: Name of IFocuser.
            camera: Name of ICamera.
            filters: Name of IFilters, if any.
            offset: If True, offsets are used instead of absolute focus values.
        """
        PyObsModule.__init__(self, *args, **kwargs)

        # store focuser and camera
        self._focuser = focuser
        self._camera = camera
        self._filters = filters
        self._offset = offset
        self._abort = threading.Event()

        # create focus series
        self._series: FocusSeries = get_object(series, FocusSeries)

        # storage for data
        self._data_lock = threading.RLock()
        self._data = []

        # init camera settings mixin
        CameraSettingsMixin.__init__(self, *args, filters=filters, **kwargs)

    def open(self):
        """Open module"""
        PyObsModule.open(self)

        # register event
        self.comm.register_event(FocusFoundEvent)

        # check focuser and camera
        try:
            self.proxy(self._focuser, IFocuser)
            self.proxy(self._camera, ICamera)
        except ValueError:
            log.warning('Either camera or focuser do not exist or are not of correct type at the moment.')

    def close(self):
        """Close module."""

    @timeout(600000)
    def auto_focus(self, count: int, step: float, exposure_time: int, *args, **kwargs) -> (float, float):
        """Perform an auto-focus series.

        This method performs an auto-focus series with "count" images on each side of the initial guess and the given
        step size. With count=3, step=1 and guess=10, this takes images at the following focus values:
            7, 8, 9, 10, 11, 12, 13

        Args:
            count: Number of images to take on each side of the initial guess. Should be an odd number.
            step: Step size.
            exposure_time: Exposure time for images.

        Returns:
            Tuple of obtained best focus value and its uncertainty.

        Raises:
            ValueError: If focus could not be obtained.
            FileNotFoundException: If image could not be downloaded.
        """
        log.info('Performing auto-focus...')

        # get focuser
        log.info('Getting proxy for focuser...')
        focuser: IFocuser = self.proxy(self._focuser, IFocuser)

        # get camera
        log.info('Getting proxy for camera...')
        camera: ICamera = self.proxy(self._camera, ICamera)

        # do camera settings
        self._do_camera_settings(camera)

        # get filter wheel and current filter
        filter_name = 'unknown'
        try:
            filter_wheel: IFilters = self.proxy(self._filters, IFilters)
            filter_name = filter_wheel.get_filter().wait()
        except ValueError:
            log.warning('Either camera or focuser do not exist or are not of correct type at the moment.')

        # get focus as first guess
        try:
            if self._offset:
                guess = 0
                log.info('Using focus offset of 0mm as initial guess.')
            else:
                guess = focuser.get_focus().wait()
                log.info('Using current focus of %.2fmm as initial guess.', guess)
        except RemoteException:
            raise ValueError('Could not fetch current focus value.')

        # define array of focus values to iterate
        focus_values = np.linspace(guess - count * step, guess + count * step, 2 * count + 1)

        # define set_focus method
        set_focus = focuser.set_focus_offset if self._offset else focuser.set_focus

        # reset
        self._series.reset()
        self._abort = threading.Event()

        # loop focus values
        log.info('Starting focus series...')
        for foc in focus_values:
            # set focus
            log.info('Changing focus to %.2fmm...', foc)
            if self._abort.is_set():
                raise InterruptedError()
            try:
                set_focus(float(foc)).wait()
            except RemoteException:
                raise ValueError('Could not set new focus value.')

            # do exposure
            log.info('Taking picture...')
            if self._abort.is_set():
                raise InterruptedError()
            try:
                filename = camera.expose(exposure_time=exposure_time, image_type=ICamera.ImageType.FOCUS,
                                         count=1).wait()[0]
            except RemoteException:
                log.error('Could not take image.')
                continue

            # download image
            log.info('Downloading image...')
            image = self.vfs.download_image(filename)

            # analyse
            log.info('Analysing picture...')
            try:
                self._series.analyse_image(image)
            except:
                # do nothing..
                log.error('Could not analyse image.')
                continue

        # fit focus
        if self._abort.is_set():
            raise InterruptedError()
        focus = self._series.fit_focus()

        # check
        if focus is None or focus[0] is None or np.isnan(focus[0]):
            raise ValueError('Could not fit focus.')

        # "absolute" will be the absolute focus value, i.e. focus+offset
        absolute = None

        # log and set focus
        if self._offset:
            log.info('Setting new focus offset of (%.3f+-%.3f) mm.', focus[0], focus[1])
            absolute = focus[0] + focuser.get_focus().wait()
            focuser.set_focus_offset(focus[0]).wait()
        else:
            log.info('Setting new focus value of (%.3f+-%.3f) mm.', focus[0], focus[1])
            absolute = focus[0] + focuser.get_focus_offset().wait()
            focuser.set_focus(focus[0]).wait()

        # send event
        self.comm.send_event(FocusFoundEvent(absolute, focus[1], filter_name))

        # return result
        return focus[0], focus[1]

    def auto_focus_status(self, *args, **kwargs) -> dict:
        """Returns current status of auto focus.

        Returned dictionary contains a list of focus/fwhm pairs in X and Y direction.

        Returns:
            Dictionary with current status.
        """
        return {}

    @timeout(20000)
    def abort(self, *args, **kwargs):
        """Abort current actions."""
        self._abort.set()


__all__ = ['AutoFocusSeries']
