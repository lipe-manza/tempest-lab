#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2022 gr-tempest author.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, gr_unittest
import pmt
# from gnuradio import blocks
from gnuradio.tempest import message_to_var

class qa_message_to_var(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_instance(self):
        # FIXME: Test will fail until you pass sensible arguments to the constructor
        values = []
        instance = message_to_var(values.append)
        instance.msg_handler_function(pmt.cons(pmt.intern("refresh_rate"), pmt.from_double(60.0)))
        instance.msg_handler_function(pmt.cons(pmt.intern("ignored"), pmt.from_double(1.0)))
        self.assertEqual(values, [60.0])

    def test_001_descriptive_test_name(self):
        # set up fg
        self.tb.run()
        # check data


if __name__ == '__main__':
    gr_unittest.run(qa_message_to_var)
