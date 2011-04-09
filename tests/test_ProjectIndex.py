from StringIO import StringIO

from tests import (TEST_PROJECT_INDEX, TEST_INDEX_MARKUP, TEST_INDEX_ATTRS,
                   TEST_PROJECT_TITLE, TEST_PROJECT_COMPANY, TEST_PROJECT_DESC)

from aaarrghh.index import (ProjectIndex, INDEX_ATTRS, TITLE_MARKUP_CHAR,
                            PROJECT_SECTIONS)

def check_attr(p, attr, value):
    p_attr = getattr(p, attr, None)
    assert p_attr == value

def check_values(val1, val2):
    assert val1 == val2


def test_ProjectIndex_init():
    p = ProjectIndex()
    for attr in INDEX_ATTRS.keys():
        yield check_attr, p, attr, INDEX_ATTRS[attr]()


def test_ProjectIndex_load_from_file():
    # Test loading from file
    p = ProjectIndex()
    p.load_index(filename=TEST_PROJECT_INDEX)
    for attr in TEST_INDEX_ATTRS.keys():
        yield check_attr, p, attr, TEST_INDEX_ATTRS[attr]


def test_ProjectIndex_load_from_fp():
    # Test loading from StringIO object
    p = ProjectIndex()
    s = StringIO(open(TEST_PROJECT_INDEX, 'rb').read())
    p.load_index(filename=TEST_PROJECT_INDEX, fp=s)
    s.close()
    for attr in TEST_INDEX_ATTRS.keys():
        yield check_attr, p, attr, TEST_INDEX_ATTRS[attr]


def test_ProjectIndex_dump_to_str():
    p = ProjectIndex(TEST_PROJECT_INDEX)
    assert p.dumps_index() == TEST_INDEX_MARKUP


def test_ProjectIndex_dump_to_file():
    p = ProjectIndex(TEST_PROJECT_INDEX)
    tmpfile = TEST_PROJECT_INDEX + '.tst'
    p.dump_index(filename=tmpfile)
    tmpstr = open(tmpfile, 'rb').read()
    assert tmpstr == TEST_INDEX_MARKUP
    p.dump_index()
    tmpstr = open(TEST_PROJECT_INDEX, 'rb').read()
    assert tmpstr == TEST_INDEX_MARKUP


def test_ProjectIndex_dump_to_fp():
    p = ProjectIndex(TEST_PROJECT_INDEX)
    s = StringIO()
    p.dump_index(fp=s)
    tmpstr = s.getvalue()
    s.close()
    assert tmpstr == TEST_INDEX_MARKUP


def test_ProjectIndex_reset():
    p = ProjectIndex(TEST_PROJECT_INDEX)
    p.reset()
    for attr in INDEX_ATTRS.keys():
        yield check_attr, p, attr, INDEX_ATTRS[attr]()


def test_ProjectIndex_load__get_title():
    p = ProjectIndex()
    lines = open(TEST_PROJECT_INDEX, 'rb').readlines()
    assert TEST_PROJECT_TITLE == p._get_title(lines)


def test_ProjectIndex_load__get_company():
    p = ProjectIndex()
    lines = open(TEST_PROJECT_INDEX, 'rb').readlines()
    assert TEST_PROJECT_COMPANY == p._get_company(lines)


def test_ProjectIndex_load__get_descrition():
    p = ProjectIndex()
    lines = open(TEST_PROJECT_INDEX, 'rb').readlines()
    assert TEST_PROJECT_DESC == p._get_description(lines)


def test_ProjectIndex_load__get_title_boundaries():
    p = ProjectIndex()
    l = TITLE_MARKUP_CHAR * 10
    assert p._get_title_boundaries(l, 5, TITLE_MARKUP_CHAR) == (5, -1)
    assert p._get_title_boundaries(l, 5, TITLE_MARKUP_CHAR, -1) == (5, -1)
    assert p._get_title_boundaries(l, 5, TITLE_MARKUP_CHAR, -1, -1) == (5, -1)
    assert p._get_title_boundaries(l, 5, TITLE_MARKUP_CHAR, -1, 10) == (5, 10)
    assert p._get_title_boundaries(l, 10, TITLE_MARKUP_CHAR, 5) == (5, 10)
    assert p._get_title_boundaries(l, 10, TITLE_MARKUP_CHAR, 5, -1) == (5, 10)


def test_ProjectIndex_load__get_section():
    p = ProjectIndex()
    lines = open(TEST_PROJECT_INDEX, 'rb').readlines()
    for section, data in PROJECT_SECTIONS.items():
        attr = TEST_INDEX_ATTRS[data['attr']]
        yield check_values, attr, p._get_section(section, lines)
