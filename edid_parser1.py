#!/usr/bin/env python
"""Wrapper for EDID data parsing and loading.
  See for more info:
  http://en.wikipedia.org/wiki/Extended_display_identification_data
"""
import itertools

try:
    zip_longest = itertools.zip_longest
except AttributeError:
    zip_longest = itertools.izip_longest


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    # Taken from itertools recipe.
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


# Constants lifted from EDID documentation.
# a. Constants needed for verification
MINIMAL_SIZE = 128  # EDID record must be not less than 128 Bytes
VERSION = 1
# MAGIC = '\x00\xff\xff\xff\xff\xff\xff\x00' # was for Py 2
MAGIC = bytearray([0, 255, 255, 255, 255, 255, 255, 0])  # for Py 3
MAGIC_OFFSET = 0
VERSION_OFFSET = 18  # 12h
REVISION_OFFSET = 19  # 13h
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

    def read_litendian16(offset):
        return (blob[offset + 1] << 8) | blob[offset]

    def read_litendian32(offset):
        return ((blob[offset + 3] << 24) |
                (blob[offset + 2] << 16) |
                (blob[offset + 1] << 8) |
                blob[offset]
                )

    def read_bigendian24(offset):
        return ((blob[offset] << 16) |
                (blob[offset + 1] << 8) |
                (blob[offset + 2])
                )

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

    # b. INFO RETRIEVAL BLOCK
    # Extract manufactuer
    vendor_name = ''
    vendor_code = read_short(MANUFACTURER_ID_OFFSET)
    # vendor_code: [0 | char1 | char2 | char3]
    for i in range(2, -1, -1):
        vendor_char = (vendor_code >> (i * MANUFACTURER_ID_BITS)) & 0x1F
        vendor_char = chr(vendor_char + ord('@'))
        vendor_name += vendor_char
    product_id = read_litendian16(PRODUCT_ID_OFFSET)
    print(vendor_name)
    print(hex(product_id).split('x')[1].upper())

    serial = read_litendian32(PRODUCT_SERIAL_OFFSET)
    if serial == 16843009:  # if only 01 01 01 01h
        serial = 0  # means no serial
    print(serial)

    week = blob[WEEK_OFFSET]
    year = blob[YEAR_OFFSET] + 1990
    print((week, year))

    widthcm = blob[WIDTH_CM_OFFSET]
    heightcm = blob[HEIGHT_CM_OFFSET]

    prefferedResIndex = (blob[FEATURES24_OFFSET] & 0x2) >> 1

    oldPixDims = read_bigendian24(FORMER_PIXDIM_OFFSET)
    oldRes = {0: (720, 400),
              1: (720, 400),
              2: (640, 480),
              3: (640, 480),
              4: (640, 480),
              5: (640, 480),
              6: (800, 600),
              7: (800, 600),
              8: (800, 600),
              9: (800, 600),
              10: (832, 624),
              11: (1024, 768),
              12: (1024, 768),
              13: (1024, 768),
              14: (1024, 768),
              15: (1280, 1024),
              16: (1152, 870)}
    legacyRes = set()
    print(bin(oldPixDims))
    for i in range(17):
        if (oldPixDims & (0x800000 >> i)) >> (23 - i):
            legacyRes.add(oldRes[i])

    print(list(legacyRes))

    widthmm = (blob[66] |
               ((blob[68] & 0xF0) << 4))
    heightmm = (blob[67] |
                ((blob[68] & 0x0F) << 8))

    timingBlock = blob[TIMING_BLOCK_OFFSET:DESCR_1_OFFSET]
    ratios = {0: (16, 10),
              1: (4, 3),
              2: (5, 4),
              3: (16, 9)}
    for word in grouper(timingBlock, 2):
        if (word[0], word[0]) != (1, 1):
            Xresolution = (word[0] + 31) * 8
            ind = (word[1] & 0xC0) >> 6
            ratio = ratios[ind]
            Yresolution = Xresolution / ratio[0] * ratio[1]
            print('puk', Xresolution, Yresolution, ratio)

    width = (blob[HORIZONTAL_OFFSET] |
             ((blob[HORIZONTAL_HIGH_OFFSET] >> 4) << 8))
    height = (blob[VERTICAL_OFFSET] |
              ((blob[VERTICAL_HIGH_OFFSET] >> 4) << 8))

    border = blob[69]
    print('Border: ', border)

    textDescType = blob[93]
    if textDescType in [255, 254, 252]:
        stri = str(blob[95:108])
        i = stri.find('\n')
        print(stri[:i])

    print(widthcm, heightcm)
    print(widthcm, widthcm * 9 / 16)

    return widthmm, heightmm, width, height
