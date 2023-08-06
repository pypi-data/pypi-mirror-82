# Created: 16.03.2011, 2018 rewritten for pytest
# Copyright (C) 2011-2019, Manfred Moitzi
# License: MIT License
import pytest

from ezdxf.entities.ltype import Linetype


@pytest.fixture
def linetype():
    return Linetype.new('FFFF', dxfattribs={
        'name': 'TEST',
        'description': 'TESTDESC',
        'pattern': [0.2, 0.1, -0.1]
    })


def test_name(linetype):
    assert linetype.dxf.name == 'TEST'


def test_description(linetype):
    assert linetype.dxf.description == 'TESTDESC'


def test_pattern_items_count(linetype):
    assert isinstance(linetype, Linetype)
    assert len(linetype.pattern_tags) == 7
    assert linetype.pattern_tags.is_complex_type() is False


def test_pattern_tags_details(linetype):
    # pattern tags are accessible but these are implementation details !!!
    assert linetype.pattern_tags.tags[0] == (72, 65)
    assert linetype.pattern_tags.tags[2].value == .2


def test_complex_linetype_name():
    complex_ltype = Linetype.new('FFFF', dxfattribs={
        'name': 'GASLEITUNG',
        'description': 'Gasleitung ----GAS----GAS----GAS----GAS----GAS----GAS--',
        'length': 3.0,  # length is required for complex line types
        'pattern': 'A,.5,-.2,["GAS",STANDARD,S=.1,U=0.0,X=-0.1,Y=-.05],-.25',
    })

    assert complex_ltype.dxf.name == 'GASLEITUNG'
    assert complex_ltype.dxf.description == 'Gasleitung ----GAS----GAS----GAS----GAS----GAS----GAS--'
    assert len(complex_ltype.pattern_tags) == 16

