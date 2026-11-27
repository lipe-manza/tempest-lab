#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2022 gr-tempest author.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, gr_unittest
import tempfile
from pathlib import Path
from PIL import Image
import numpy
# from gnuradio import blocks
from gnuradio.tempest import image_source

class qa_image_source(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_instance(self):
        # FIXME: Test will fail until you pass sensible arguments to the constructor
        with tempfile.TemporaryDirectory() as directory:
            image = Path(directory) / "reference.png"
            Image.new("L", (2, 2), 37).save(image)
            instance = image_source(str(image), 2, 2, 4, 4, 1)
            output = numpy.empty(4, dtype=numpy.float32)
            rows = []
            for _ in range(4):
                self.assertEqual(instance.work([], [output]), 4)
                rows.append(output.copy())
            self.assertEqual(numpy.array(rows).tolist(), [[0, 0, 0, 0], [0, 37, 37, 0], [0, 37, 37, 0], [0, 0, 0, 0]])

    def test_001_descriptive_test_name(self):
        # set up fg
        self.tb.run()
        # check data


if __name__ == '__main__':
    gr_unittest.run(qa_image_source)
