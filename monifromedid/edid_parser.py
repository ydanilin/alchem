#!/usr/bin/env python
# coding=utf-8

import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

"""Wrapper for EDID data parsing and loading.
  See for more info:
  http://en.wikipedia.org/wiki/Extended_display_identification_data
"""


class EdidParser:
    def __init__(self):
        # Constants lifted from EDID documentation.
        # a. Constants needed for verification
        self.MINIMAL_SIZE = 128  # EDID record must be not less than 128 Bytes
        self.VERSION = 1
        self.MAGIC = bytearray([0, 255, 255, 255, 255, 255, 255, 0])  # for Py 3
        self.MAGIC_OFFSET = 0
        self.VERSION_OFFSET = 18  # 12h
        self.CHECKSUM_OFFSET = 127  # 7Fh
        self.PIXEL_CLOCK_OFFSET = 54  # 36h
        self.DETTIMING_DESCRIPTOR_OFFSET = 54  # 36h
        # b. Constants for monitor info (figures for offsets as per wiki doc)
        self.HORIZONTAL_OFFSET = self.DETTIMING_DESCRIPTOR_OFFSET + 2
        self.HORIZONTAL_HIGH_OFFSET = self.DETTIMING_DESCRIPTOR_OFFSET + 4
        self.VERTICAL_OFFSET = self.DETTIMING_DESCRIPTOR_OFFSET + 5
        self.VERTICAL_HIGH_OFFSET = self.DETTIMING_DESCRIPTOR_OFFSET + 7
        self.HORIZONTAL_MM_OFFSET = self.DETTIMING_DESCRIPTOR_OFFSET + 12
        self.VERTICAL_MM_OFFSET = self.DETTIMING_DESCRIPTOR_OFFSET + 13
        self.HORVER_MM_HIGH_OFFSET = self.DETTIMING_DESCRIPTOR_OFFSET + 14

    def read_short(self, blob, offset):
        return (blob[offset] << 8) | blob[offset + 1]

    def parse(self, blob):
        """EDID Parser"""
        # a. VERIFICATION BLOCK
        # Check size, magic, and version
        if len(blob) < self.MINIMAL_SIZE:
            log.warning("EDID parsing error: length too small.")
            return None
        if (blob[self.MAGIC_OFFSET:(self.MAGIC_OFFSET + len(self.MAGIC))] !=
                self.MAGIC):
            log.warning("EDID parse error: incorrect header.")
            return None
        if blob[self.VERSION_OFFSET] != self.VERSION:
            log.warning("EDID parse error: unsupported EDID version.")
            return None
        # Verify checksum
        if sum([i for i in blob[:self.CHECKSUM_OFFSET + 1]]) % 0x100 != 0:
            log.warning("EDID parse error: checksum error.")
            return None
        # Currently we don't support EDID not using pixel clock
        pixel_clock = self.read_short(blob, self.PIXEL_CLOCK_OFFSET)
        if not pixel_clock:
            log.warning("EDID parse error: "
                            "non-pixel clock format is not supported yet.")
            return None
        # Millimeters
        widthMm = (blob[self.HORIZONTAL_MM_OFFSET] | (
                                (blob[self.HORVER_MM_HIGH_OFFSET] & 0xF0) << 4
                                                      )
                   )
        heightMm = (blob[self.VERTICAL_MM_OFFSET] | (
                                (blob[self.HORVER_MM_HIGH_OFFSET] & 0x0F) << 8
                                                     )
                    )
        # Pixels
        width = (blob[self.HORIZONTAL_OFFSET] |
                 ((blob[self.HORIZONTAL_HIGH_OFFSET] >> 4) << 8))
        height = (blob[self.VERTICAL_OFFSET] |
                  ((blob[self.VERTICAL_HIGH_OFFSET] >> 4) << 8))

        return widthMm, heightMm, width, height
