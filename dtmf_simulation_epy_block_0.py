"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, example_param=1.0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='One Hot to Linear Coordinate Converter',   # will show up in GRC
            in_sig=[np.uint8, np.uint8, np.uint8, np.uint8],
            out_sig=[int]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.example_param = example_param

    def work(self, input_items, output_items):
        # convert presence values into one dimensional character coordinate

        # first, assign to readable values
        is697present = input_items[0][0]
        is712present = input_items[1][0]

        is1209present = input_items[2][0]
        is1336present = input_items[3][0]

        colCoord = 0*is697present + 1*is712present
        rowCoord = 0*is1209present + 1*is1336present

        if (is697present + is712present + is1209present + is1336present) == 0:
            coordinate = 99
        else:
            coordinate = rowCoord*2+colCoord

        # then, output the coordinate to GNU Radio
        output_items[0][:] = coordinate

        return len(output_items[0])
