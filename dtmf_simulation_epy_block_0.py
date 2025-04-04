"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        self.vectorsize = 16
        gr.sync_block.__init__(
            self,
            name='One Hot to Linear Coordinate Converter',   # will show up in GRC
            in_sig=[(np.uint8, 16)],
            out_sig=[int]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        # self.example_param = example_param

    def work(self, input_items, output_items):
        # convert presence values into one dimensional character coordinate

        input_sum = 0
        coordinate = 0
        for n in range(0,len(input_items[0][0])):
            input_sum += input_items[0][0][n]
            coordinate += n*input_items[0][0][n]

        if input_sum == 0:
            coordinate = 99

        # then, output the coordinate to GNU Radio
        output_items[0][:] = coordinate

        return len(output_items[0])
