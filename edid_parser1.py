#!/usr/bin/env python
"""Wrapper for EDID data parsing and loading.
  See for more info:
  http://en.wikipedia.org/wiki/Extended_display_identification_data
"""


# Constants lifted from EDID documentation.
# a. Constants needed for verification
MINIMAL_SIZE = 128  # EDID record must be not less than 128 Bytes
VERSION = 1
MAGIC = bytearray([0, 255, 255, 255, 255, 255, 255, 0])  # for Py 3
MAGIC_OFFSET = 0
VERSION_OFFSET = 18  # 12h
# REVISION_OFFSET = 19  # 13h
CHECKSUM_OFFSET = 127  # 7Fh
PIXEL_CLOCK_OFFSET = 54  # 36h
# b. Constants for monitor info
MANUFACTURER_ID_OFFSET = 8
MANUFACTURER_ID_BITS = 5
PRODUCT_ID_OFFSET = 10
PRODUCT_SERIAL_OFFSET = 12  # 0Ch
WEEK_OFFSET = 16
YEAR_OFFSET = 17
WIDTH_CM_OFFSET = 21
HEIGHT_CM_OFFSET = 22  # often bullshit. will calculate based on aspect ratio
FEATURES24_OFFSET = 24
FORMER_PIXDIM_OFFSET = 35  # 23h
TIMING_BLOCK_OFFSET = 38  # 26h
DESCR_1_OFFSET = 54

HORIZONTAL_OFFSET = 56
HORIZONTAL_HIGH_OFFSET = 58
VERTICAL_OFFSET = 59
VERTICAL_HIGH_OFFSET = 61


def parse(blob):
    """EDID Parser"""

    def read_short(offset):
        return (blob[offset] << 8) | blob[offset + 1]

     # a. VERIFICATION BLOCK
    # Check size, magic, and version
    if len(blob) < MINIMAL_SIZE:
        logging.warning("EDID parsing error: length too small.")
        return None
    if (blob[MAGIC_OFFSET:(MAGIC_OFFSET + len(MAGIC))] !=
            MAGIC):
        logging.warning("EDID parse error: incorrect header.")
        return None
    if blob[VERSION_OFFSET] != VERSION:
        logging.warning("EDID parse error: unsupported EDID version.")
        return None
    # Verify checksum
    if sum([i for i in blob[:CHECKSUM_OFFSET + 1]]) % 0x100 != 0:
        logging.warning("EDID parse error: checksum error.")
        return None
    # Currently we don't support EDID not using pixel clock
    pixel_clock = read_short(PIXEL_CLOCK_OFFSET)
    if not pixel_clock:
        logging.warning("EDID parse error: "
                        "non-pixel clock format is not supported yet.")
        return None

    widthmm = (blob[66] | ((blob[68] & 0xF0) << 4))
    heightmm = (blob[67] | ((blob[68] & 0x0F) << 8))

    width = (blob[HORIZONTAL_OFFSET] |
             ((blob[HORIZONTAL_HIGH_OFFSET] >> 4) << 8))
    height = (blob[VERTICAL_OFFSET] |
              ((blob[VERTICAL_HIGH_OFFSET] >> 4) << 8))

    return widthmm, heightmm, width, height
