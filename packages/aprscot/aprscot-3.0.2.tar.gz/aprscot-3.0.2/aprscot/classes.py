#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""APRS Cursor-on-Target Class Definitions."""

import logging
import socket
import threading
import time

import aprscot

__author__ = 'Greg Albrecht W2GMD <oss@undef.net>'
__copyright__ = 'Copyright 2020 Orion Labs, Inc.'
__license__ = 'Apache License, Version 2.0'
__source__ = 'https://github.com/ampledata/aprscot'


class APRSCoT(threading.Thread):

    """APRS Cursor-on-Target Threaded Class."""

    _logger = logging.getLogger(__name__)
    if not _logger.handlers:
        _logger.setLevel(aprscot.LOG_LEVEL)
        _console_handler = logging.StreamHandler()
        _console_handler.setLevel(aprscot.LOG_LEVEL)
        _console_handler.setFormatter(aprscot.LOG_FORMAT)
        _logger.addHandler(_console_handler)
        _logger.propagate = False

    def __init__(self, aprs_interface, cot_host: str) -> None:
        self.aprs_interface = aprs_interface
        self.cot_host: str = cot_host

        # Thread stuff:
        threading.Thread.__init__(self)
        self._stopped = False

    def stop(self):
        """Stops the thread at the next opportunity."""
        self._stopped = True
        return self._stopped

    def send_cot(self, aprs_frame):
        """Sends an APRS Frame to a Cursor-on-Target Host."""
        cot_event = aprscot.aprs_to_cot(aprs_frame)
        if cot_event is None:
            return False

        rendered_event = cot_event.render(encoding='UTF-8', standalone=True)

        self._logger.debug(
            'Sending CoT to %s: "%s"', self.full_addr, rendered_event)

        # is the socket alive?
        assert(self.socket.fileno() != -1)

        self.socket.settimeout(0.5)

        try:
            self.socket.sendall(rendered_event)
            return True
        except Exception as exc:
            self._logger.error(
                'socket.sendall raised an Exception, sleeping: ')
            self._logger.exception(exc)
            # TODO: Make this value configurable, or add ^backoff.
            time.sleep(5)
            self._start_socket()

    def _start_socket(self):
        """Starts the TCP Socket for sending CoT events."""
        self._logger.debug('Setting up socket.')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if ':' in self.cot_host:
            addr, port = self.cot_host.split(':')
        else:
            addr = self.cot_host
            port = aprscot.DEFAULT_COT_PORT

        self.full_addr = (addr, int(port))
        self.socket.connect((addr, int(port)))
        self.socket.setblocking(False)

    def run(self):
        """Runs this Thread, reads APRS & outputs CoT."""
        self._logger.info('Running APRSCoT Thread...')
        self._start_socket()
        self.aprs_interface.consumer(self.send_cot)
