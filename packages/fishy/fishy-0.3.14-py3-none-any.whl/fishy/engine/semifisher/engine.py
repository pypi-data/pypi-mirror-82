import time
import typing
from collections import Callable
from threading import Thread

import cv2
import logging

import pywintypes

from fishy.engine.IEngine import IEngine
from fishy.engine.semifisher import fishing_event
from .fishing_event import HookEvent, StickEvent, LookEvent, IdleEvent
from .fishing_mode import FishingMode
from .pixel_loc import PixelLoc
from fishy.engine.window import Window

if typing.TYPE_CHECKING:
    from fishy.gui import GUI


class SemiFisherEngine(IEngine):
    def __init__(self, config, gui_ref: 'Callable[[], GUI]'):
        super().__init__(config, gui_ref)
        self.fishPixWindow = None

    def run(self):
        """
        Starts the fishing
        code explained in comments in detail
        """

        action_key = self.config.get("action_key", "e")
        borderless = self.config.get("borderless", False)

        # initialize widow
        # noinspection PyUnresolvedReferences
        try:
            Window.init(borderless)
        except pywintypes.error:
            logging.info("Game window not found")
            self.start = False
            return

        # initializes fishing modes and their callbacks
        FishingMode("hook", 0, HookEvent(action_key, False))
        FishingMode("stick", 1, StickEvent())
        FishingMode("look", 2, LookEvent(action_key))
        FishingMode("idle", 3, IdleEvent(self.config.get("uid"), self.config.get("sound_notification")))

        self.fishPixWindow = Window(color=cv2.COLOR_RGB2HSV)

        # check for game window and stuff
        self.gui.bot_started(True)
        logging.info("Starting the bot engine, look at the fishing hole to start fishing")
        Thread(target=self._wait_and_check).start()
        while self.start:
            # Services to be ran in the start of the main loop
            success = Window.loop()

            if not success:
                self.gui.bot_started(False)
                self.toggle_start()
                continue

            # get the PixelLoc and find the color values, to give it to `FishingMode.Loop`
            self.fishPixWindow.crop = PixelLoc.val
            hue_value = self.fishPixWindow.get_capture()[0][0][0]
            FishingMode.loop(hue_value)
            # Services to be ran in the end of the main loop
            Window.loop_end()
        logging.info("Fishing engine stopped")
        self.gui.bot_started(False)

    def _wait_and_check(self):
        time.sleep(10)
        if not fishing_event._FishingStarted and self.start:
            self.gui.show_error("Doesn't look like fishing has started\n\n"
                                "Check out #read-me-first on our discord channel to troubleshoot the issue")

    def show_pixel_vals(self):
        def show():
            freq = 0.5
            t = 0
            while t < 10.0:
                t += freq
                logging.debug(str(FishingMode.CurrentMode.label) + ":" + str(self.fishPixWindow.get_capture()[0][0]))
                time.sleep(freq)

        logging.debug("Will display pixel values for 10 seconds")
        time.sleep(5)
        Thread(target=show, args=()).start()



