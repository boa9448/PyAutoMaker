import unittest

import env
import PyAutoMaker as pam

class TestClassDDModule(unittest.TestCase):
    def setUp(self) -> None:
        self.dd = pam.DDUtil()
        return super().setUp()

    def test_key(self) -> None:
        self.dd.key(ord("A"), pam.KEY_STATUS_PRESS)
        self.dd.key(ord("A"), pam.KEY_STATUS_RELEASE)

    def test_move(self) -> None:
        self.dd.move(0, 0, False)

if __name__ == "__main__":
    unittest.main()