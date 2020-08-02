import shutil
import unittest

from aii.components.design import Designer

cfg = {
    'patch': 'images/distractor/patch/',
    'sign': 'images/distractor/sign/',
    'logo': 'images/distractor/logo/',
    'product': 'images/product',
    'background': 'images/background/',
}


class TestDesigner(unittest.TestCase):

    def test_design(self):
        ds = Designer(cfg)
        ds.generate('_data', 3)
        assert list(ds.dataset.keys()) == [
            'images', 'categories', 'annotations']
        shutil.rmtree('_data/')
