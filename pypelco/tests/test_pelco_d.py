
from __future__ import print_function

from unittest import TestCase
from pelco_d import PelcoD


class TestPelcoD(TestCase):

    def test_01_set_word(self):
        pelco = PelcoD(1)
        print(pelco.hex(' 0x'))

    def test_04_checksum(self):
        """Insure the check sum is calculated corectly."""

        # This data is from the pelco-D Protocol Manual Pg 6
        test_data_set = [[0x01, 0x88, 0x00, 0x00, 0x00, 0x89],
                         [0x01, 0x08, 0x00, 0x00, 0x00, 0x09],
                         [0x02, 0x00, 0x04, 0x00, 0x20, 0x26],
                         [0x02, 0x00, 0x00, 0x00, 0x00, 0x02],
                         [0x0A, 0x88, 0x90, 0x00, 0x40, 0x62]]
        for test_data in test_data_set:
            pelco = PelcoD(test_data[0])
            pelco.set_words(*test_data[1:5])
            assert pelco.check_sum() == test_data[5]
