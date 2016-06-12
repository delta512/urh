import unittest

from urh.signalprocessing.LabelSet import LabelSet
from urh.signalprocessing.Participant import Participant
from urh.signalprocessing.ProtocolAnalyzer import ProtocolAnalyzer
from urh.signalprocessing.ProtocolBlock import ProtocolBlock
from urh.signalprocessing.Ruleset import Rule, Ruleset, Mode


class TestAutoAssignments(unittest.TestCase):
    def setUp(self):
        self.protocol = ProtocolAnalyzer(None)
        with open("./data/rwe_decoded_bits.txt") as f:
            for line in f:
                self.protocol.blocks.append(ProtocolBlock.from_plain_bits_str(line.replace("\n", ""), {}))
                self.protocol.blocks[-1].labelset = self.protocol.default_labelset

        self.assertEqual(self.protocol.num_blocks, 42)
        self.assertEqual(self.protocol.plain_hex_str[0][16:18], "2d")

    def test_labelset_assign_by_value(self):
        start = 8
        end = 15
        hex_value = "9a7d9a7d"

        lblset = LabelSet("autotest")
        lblset.ruleset = Ruleset(Mode.all_apply, [Rule(start, end, "=", hex_value, 1)])
        lblset.assigned_automatically = True

        self.protocol.labelsets.append(lblset)
        self.protocol.update_auto_labelsets()
        matching_indices = [0, 2, 3, 21, 23, 24]
        for i, block in enumerate(self.protocol.blocks):
            if i in matching_indices:
                self.assertEqual(block.labelset, lblset, msg=str(i))
            else:
                self.assertEqual(block.labelset, self.protocol.default_labelset, msg=str(i))

    def test_two_assign_participants_by_rssi(self):
        rssis = [[0.65389872, 0.13733707, 0.1226876, 0.73320961, 0.64940965, 0.12463234, 0.12296994,
                 0.68053716, 0.66020358, 0.12428901, 0.12312815, 0.69160986, 0.65582329, 0.12536003,
                 0.12587067, 0.66315573, 0.66313261, 0.12816505, 0.13491708, 0.66950738, 0.14047238],
                 [0.26651502, 0.2073856, 0.13547869, 0.25948182, 0.28204739, 0.13716124, 0.13526952,
                 0.24828221, 0.25431305, 0.13681877, 0.13650328, 0.28083691, 0.25550124, 0.13498682,
                 0.13611424, 0.2629154, 0.26388499, 0.13780586, 0.13561584, 0.27228078, 0.1356563]]
        alice = Participant(name="Alice", shortname="A")
        bob = Participant(name="Bob", shortname="B")
        excpected_partis = [[alice, bob, bob, alice, alice, bob, bob,
                  alice, alice, bob, bob, alice, alice, bob,
                  bob, alice, alice, bob, bob, alice, bob],
                  [alice, bob, bob, alice, alice, bob, bob,
                   alice, alice, bob, bob, alice, alice, bob,
                   bob, alice, alice, bob, bob, alice, bob]]