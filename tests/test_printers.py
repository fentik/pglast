# -*- coding: utf-8 -*-
# :Project:   pglast -- Tests on the printers registry
# :Created:   sab 05 ago 2017 10:31:23 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2017, 2018, 2019, 2021 Lele Gaifax
#

import pytest

from pglast.printers import NODE_PRINTERS, PrinterAlreadyPresentError
from pglast.printers import get_printer_for_node_tag, node_printer


def test_registry():
    with pytest.raises(NotImplementedError):
        get_printer_for_node_tag(None, 'non_existing')

    with pytest.raises(ValueError):
        @node_printer()
        def tag(node, output):
            pass

    with pytest.raises(ValueError):
        @node_printer('one', 'two', 'three')
        def tag2(node, output):
            pass

    try:
        @node_printer('test_tag1')
        def tag1(node, output):
            pass

        assert get_printer_for_node_tag(None, 'test_tag1') is tag1

        with pytest.raises(PrinterAlreadyPresentError):
            @node_printer('test_tag1')
            def tag3(node, output):
                pass

        @node_printer('test_tag1', override=True)
        def tag1_bis(node, output):
            pass

        assert get_printer_for_node_tag(None, 'test_tag1') is tag1_bis

        @node_printer('test_tag_3')
        def generic_tag3(node, output):
            pass

        @node_printer('test_tag_1', 'test_tag_3')
        def specific_tag3(node, output):
            pass

        @node_printer(('test_tag_a', 'test_tag_b'), 'test_tag_3')
        def specific_tag4(node, output):
            pass

        assert get_printer_for_node_tag(None, 'test_tag_3') is generic_tag3
        assert get_printer_for_node_tag('Foo', 'test_tag_3') is generic_tag3
        assert get_printer_for_node_tag('test_tag_1', 'test_tag_3') is specific_tag3
        assert get_printer_for_node_tag('test_tag_a', 'test_tag_3') is specific_tag4
        assert get_printer_for_node_tag('test_tag_b', 'test_tag_3') is specific_tag4
    finally:
        NODE_PRINTERS.pop('test_tag1', None)