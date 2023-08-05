# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""
This module tests some of the methods related to the ``ECSV``
reader/writer.

Requires `pyyaml <https://pyyaml.org/>`_ to be installed.
"""
import os
import copy
import sys
from io import StringIO

import pytest
import numpy as np

from astropy.table import Table, Column, QTable, NdarrayMixin
from astropy.table.table_helpers import simple_table
from astropy.coordinates import SkyCoord, Latitude, Longitude, Angle, EarthLocation
from astropy.time import Time, TimeDelta
from astropy.units import allclose as quantity_allclose
from astropy.units import QuantityInfo
from astropy.tests.helper import catch_warnings

from astropy.io.ascii.ecsv import DELIMITERS
from astropy.io import ascii
from astropy import units as u

try:
    import yaml  # noqa
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

DTYPES = ['bool', 'int8', 'int16', 'int32', 'int64', 'uint8', 'uint16', 'uint32',
          'uint64', 'float16', 'float32', 'float64', 'float128',
          'str']
if os.name == 'nt' or sys.maxsize <= 2**32:
    DTYPES.remove('float128')

T_DTYPES = Table()

for dtype in DTYPES:
    if dtype == 'bool':
        data = np.array([False, True, False])
    elif dtype == 'str':
        data = np.array(['ab 0', 'ab, 1', 'ab2'])
    else:
        data = np.arange(3, dtype=dtype)
    c = Column(data, unit='m / s', description='descr_' + dtype,
               meta={'meta ' + dtype: 1})
    T_DTYPES[dtype] = c

T_DTYPES.meta['comments'] = ['comment1', 'comment2']

# Corresponds to simple_table()
SIMPLE_LINES = ['# %ECSV 0.9',
                '# ---',
                '# datatype:',
                '# - {name: a, datatype: int64}',
                '# - {name: b, datatype: float64}',
                '# - {name: c, datatype: string}',
                '# schema: astropy-2.0',
                'a b c',
                '1 1.0 c',
                '2 2.0 d',
                '3 3.0 e']


@pytest.mark.skipif('not HAS_YAML')
def test_write_simple():
    """
    Write a simple table with common types.  This shows the compact version
    of serialization with one line per column.
    """
    t = simple_table()

    out = StringIO()
    t.write(out, format='ascii.ecsv')
    assert out.getvalue().splitlines() == SIMPLE_LINES


@pytest.mark.skipif('not HAS_YAML')
def test_write_full():
    """
    Write a full-featured table with common types and explicitly checkout output
    """
    t = T_DTYPES['bool', 'int64', 'float64', 'str']
    lines = ['# %ECSV 0.9',
             '# ---',
             '# datatype:',
             '# - name: bool',
             '#   unit: m / s',
             '#   datatype: bool',
             '#   description: descr_bool',
             '#   meta: {meta bool: 1}',
             '# - name: int64',
             '#   unit: m / s',
             '#   datatype: int64',
             '#   description: descr_int64',
             '#   meta: {meta int64: 1}',
             '# - name: float64',
             '#   unit: m / s',
             '#   datatype: float64',
             '#   description: descr_float64',
             '#   meta: {meta float64: 1}',
             '# - name: str',
             '#   unit: m / s',
             '#   datatype: string',
             '#   description: descr_str',
             '#   meta: {meta str: 1}',
             '# meta: !!omap',
             '# - comments: [comment1, comment2]',
             '# schema: astropy-2.0',
             'bool int64 float64 str',
             'False 0 0.0 "ab 0"',
             'True 1 1.0 "ab, 1"',
             'False 2 2.0 ab2']

    out = StringIO()
    t.write(out, format='ascii.ecsv')
    assert out.getvalue().splitlines() == lines


@pytest.mark.skipif('not HAS_YAML')
def test_write_read_roundtrip():
    """
    Write a full-featured table with all types and see that it round-trips on
    readback.  Use both space and comma delimiters.
    """
    t = T_DTYPES
    for delimiter in DELIMITERS:
        out = StringIO()
        t.write(out, format='ascii.ecsv', delimiter=delimiter)

        t2s = [Table.read(out.getvalue(), format='ascii.ecsv'),
               Table.read(out.getvalue(), format='ascii'),
               ascii.read(out.getvalue()),
               ascii.read(out.getvalue(), format='ecsv', guess=False),
               ascii.read(out.getvalue(), format='ecsv')]
        for t2 in t2s:
            assert t.meta == t2.meta
            for name in t.colnames:
                assert t[name].attrs_equal(t2[name])
                assert np.all(t[name] == t2[name])


@pytest.mark.skipif('not HAS_YAML')
def test_bad_delimiter():
    """
    Passing a delimiter other than space or comma gives an exception
    """
    out = StringIO()
    with pytest.raises(ValueError) as err:
        T_DTYPES.write(out, format='ascii.ecsv', delimiter='|')
    assert 'only space and comma are allowed' in str(err.value)


@pytest.mark.skipif('not HAS_YAML')
def test_bad_header_start():
    """
    Bad header without initial # %ECSV x.x
    """
    lines = copy.copy(SIMPLE_LINES)
    lines[0] = '# %ECV 0.9'
    with pytest.raises(ascii.InconsistentTableError):
        Table.read('\n'.join(lines), format='ascii.ecsv', guess=False)


@pytest.mark.skipif('not HAS_YAML')
def test_bad_delimiter_input():
    """
    Illegal delimiter in input
    """
    lines = copy.copy(SIMPLE_LINES)
    lines.insert(2, '# delimiter: |')
    with pytest.raises(ValueError) as err:
        Table.read('\n'.join(lines), format='ascii.ecsv', guess=False)
    assert 'only space and comma are allowed' in str(err.value)


@pytest.mark.skipif('not HAS_YAML')
def test_multidim_input():
    """
    Multi-dimensional column in input
    """
    t = Table([np.arange(4).reshape(2, 2), [1, 2]], names=['a', 'b'])
    out = StringIO()
    with pytest.raises(ValueError,
                       match="ECSV format does not support multidimensional column 'a'"):
        t.write(out, format='ascii.ecsv')

    # Now check that the hint works
    names = [name for name in t.colnames if len(t[name].shape) <= 1]
    assert names == ['b']
    ascii.write(t[names], out, format='ecsv')


@pytest.mark.skipif('not HAS_YAML')
def test_round_trip_empty_table():
    """Test fix in #5010 for issue #5009 (ECSV fails for empty type with bool type)"""
    t = Table(dtype=[bool, 'i', 'f'], names=['a', 'b', 'c'])
    out = StringIO()
    t.write(out, format='ascii.ecsv')
    t2 = Table.read(out.getvalue(), format='ascii.ecsv')
    assert t.dtype == t2.dtype
    assert len(t2) == 0


@pytest.mark.skipif('not HAS_YAML')
def test_csv_ecsv_colnames_mismatch():
    """
    Test that mismatch in column names from normal CSV header vs.
    ECSV YAML header raises the expected exception.
    """
    lines = copy.copy(SIMPLE_LINES)
    header_index = lines.index('a b c')
    lines[header_index] = 'a b d'
    with pytest.raises(ValueError) as err:
        ascii.read(lines, format='ecsv')
    assert "column names from ECSV header ['a', 'b', 'c']" in str(err.value)


@pytest.mark.skipif('not HAS_YAML')
def test_regression_5604():
    """
    See https://github.com/astropy/astropy/issues/5604 for more.
    """
    t = Table()
    t.meta = {"foo": 5 * u.km, "foo2": u.s}
    t["bar"] = [7] * u.km

    out = StringIO()
    t.write(out, format="ascii.ecsv")

    assert '!astropy.units.Unit' in out.getvalue()
    assert '!astropy.units.Quantity' in out.getvalue()


def assert_objects_equal(obj1, obj2, attrs, compare_class=True):
    if compare_class:
        assert obj1.__class__ is obj2.__class__

    info_attrs = ['info.name', 'info.format', 'info.unit', 'info.description']
    for attr in attrs + info_attrs:
        a1 = obj1
        a2 = obj2
        for subattr in attr.split('.'):
            try:
                a1 = getattr(a1, subattr)
                a2 = getattr(a2, subattr)
            except AttributeError:
                a1 = a1[subattr]
                a2 = a2[subattr]

        if isinstance(a1, np.ndarray) and a1.dtype.kind == 'f':
            assert quantity_allclose(a1, a2, rtol=1e-10)
        else:
            assert np.all(a1 == a2)


el = EarthLocation(x=[1, 2] * u.km, y=[3, 4] * u.km, z=[5, 6] * u.km)
sc = SkyCoord([1, 2], [3, 4], unit='deg,deg', frame='fk4',
              obstime='J1990.5')
scc = sc.copy()
scc.representation_type = 'cartesian'
tm = Time([51000.5, 51001.5], format='mjd', scale='tai', precision=5, location=el[0])
tm2 = Time(tm, format='iso')
tm3 = Time(tm, location=el)
tm3.info.serialize_method['ecsv'] = 'jd1_jd2'

# NOTE: in the test below the name of the column "x" for the Quantity is
# important since it tests the fix for #10215 (namespace clash, where "x"
# clashes with "el.x").
mixin_cols = {
    'tm': tm,
    'tm2': tm2,
    'tm3': tm3,
    'dt': TimeDelta([1, 2] * u.day),
    'sc': sc,
    'scc': scc,
    'scd': SkyCoord([1, 2], [3, 4], [5, 6], unit='deg,deg,m', frame='fk4',
                    obstime=['J1990.5'] * 2),
    'x': [1, 2] * u.m,
    'qdb': [10, 20] * u.dB(u.mW),
    'qdex': [4.5, 5.5] * u.dex(u.cm/u.s**2),
    'qmag': [21, 22] * u.ABmag,
    'lat': Latitude([1, 2] * u.deg),
    'lon': Longitude([1, 2] * u.deg, wrap_angle=180. * u.deg),
    'ang': Angle([1, 2] * u.deg),
    'el': el,
    # 'nd': NdarrayMixin(el)  # not supported yet
}

time_attrs = ['value', 'shape', 'format', 'scale', 'precision',
              'in_subfmt', 'out_subfmt', 'location']
compare_attrs = {
    'c1': ['data'],
    'c2': ['data'],
    'tm': time_attrs,
    'tm2': time_attrs,
    'tm3': time_attrs,
    'dt': ['shape', 'value', 'format', 'scale'],
    'sc': ['ra', 'dec', 'representation_type', 'frame.name'],
    'scc': ['x', 'y', 'z', 'representation_type', 'frame.name'],
    'scd': ['ra', 'dec', 'distance', 'representation_type', 'frame.name'],
    'x': ['value', 'unit'],
    'qdb': ['value', 'unit'],
    'qdex': ['value', 'unit'],
    'qmag': ['value', 'unit'],
    'lon': ['value', 'unit', 'wrap_angle'],
    'lat': ['value', 'unit'],
    'ang': ['value', 'unit'],
    'el': ['x', 'y', 'z', 'ellipsoid'],
    'nd': ['x', 'y', 'z'],
}


@pytest.mark.skipif('not HAS_YAML')
def test_ecsv_mixins_ascii_read_class():
    """Ensure that ascii.read(ecsv_file) returns the correct class
    (QTable if any Quantity subclasses, Table otherwise).
    """
    # Make a table with every mixin type except Quantities
    t = QTable({name: col for name, col in mixin_cols.items()
                if not isinstance(col.info, QuantityInfo)})
    out = StringIO()
    t.write(out, format="ascii.ecsv")
    t2 = ascii.read(out.getvalue(), format='ecsv')
    assert type(t2) is Table

    # Add a single quantity column
    t['lon'] = mixin_cols['lon']

    out = StringIO()
    t.write(out, format="ascii.ecsv")
    t2 = ascii.read(out.getvalue(), format='ecsv')
    assert type(t2) is QTable


@pytest.mark.skipif('not HAS_YAML')
def test_ecsv_mixins_qtable_to_table():
    """Test writing as QTable and reading as Table.  Ensure correct classes
    come out.
    """
    names = sorted(mixin_cols)

    t = QTable([mixin_cols[name] for name in names], names=names)
    out = StringIO()
    t.write(out, format="ascii.ecsv")
    t2 = Table.read(out.getvalue(), format='ascii.ecsv')

    assert t.colnames == t2.colnames

    for name, col in t.columns.items():
        col2 = t2[name]
        attrs = compare_attrs[name]
        compare_class = True

        if isinstance(col.info, QuantityInfo):
            # Downgrade Quantity to Column + unit
            assert type(col2) is Column
            # Class-specific attributes like `value` or `wrap_angle` are lost.
            attrs = ['unit']
            compare_class = False
            # Compare data values here (assert_objects_equal doesn't know how in this case)
            assert np.allclose(col.value, col2, rtol=1e-10)

        assert_objects_equal(col, col2, attrs, compare_class)


@pytest.mark.skipif('not HAS_YAML')
@pytest.mark.parametrize('table_cls', (Table, QTable))
def test_ecsv_mixins_as_one(table_cls):
    """Test write/read all cols at once and validate intermediate column names"""
    names = sorted(mixin_cols)

    serialized_names = ['ang',
                        'dt',
                        'el.x', 'el.y', 'el.z',
                        'lat',
                        'lon',
                        'qdb',
                        'qdex',
                        'qmag',
                        'sc.ra', 'sc.dec',
                        'scc.x', 'scc.y', 'scc.z',
                        'scd.ra', 'scd.dec', 'scd.distance',
                        'scd.obstime',
                        'tm',  # serialize_method is formatted_value
                        'tm2',  # serialize_method is formatted_value
                        'tm3.jd1', 'tm3.jd2',    # serialize is jd1_jd2
                        'tm3.location.x', 'tm3.location.y', 'tm3.location.z',
                        'x']

    t = table_cls([mixin_cols[name] for name in names], names=names)

    out = StringIO()
    t.write(out, format="ascii.ecsv")
    t2 = table_cls.read(out.getvalue(), format='ascii.ecsv')

    assert t.colnames == t2.colnames

    # Read as a ascii.basic table (skip all the ECSV junk)
    t3 = table_cls.read(out.getvalue(), format='ascii.basic')
    assert t3.colnames == serialized_names


@pytest.mark.skipif('not HAS_YAML')
@pytest.mark.parametrize('name_col', list(mixin_cols.items()))
@pytest.mark.parametrize('table_cls', (Table, QTable))
def test_ecsv_mixins_per_column(table_cls, name_col):
    """Test write/read one col at a time and do detailed validation"""
    name, col = name_col

    c = [1.0, 2.0]
    t = table_cls([c, col, c], names=['c1', name, 'c2'])
    t[name].info.description = 'description'

    if not t.has_mixin_columns:
        pytest.skip('column is not a mixin (e.g. Quantity subclass in Table)')

    if isinstance(t[name], NdarrayMixin):
        pytest.xfail('NdarrayMixin not supported')

    out = StringIO()
    t.write(out, format="ascii.ecsv")
    t2 = table_cls.read(out.getvalue(), format='ascii.ecsv')

    assert t.colnames == t2.colnames

    for colname in t.colnames:
        assert_objects_equal(t[colname], t2[colname], compare_attrs[colname])

    # Special case to make sure Column type doesn't leak into Time class data
    if name.startswith('tm'):
        assert t2[name]._time.jd1.__class__ is np.ndarray
        assert t2[name]._time.jd2.__class__ is np.ndarray


@pytest.mark.skipif('HAS_YAML')
def test_ecsv_but_no_yaml_warning():
    """
    Test that trying to read an ECSV without PyYAML installed when guessing
    emits a warning, but reading with guess=False gives an exception.
    """
    with catch_warnings() as w:
        ascii.read(SIMPLE_LINES)
    assert len(w) == 1
    assert "file looks like ECSV format but PyYAML is not installed" in str(w[0].message)

    with pytest.raises(ascii.InconsistentTableError) as exc:
        ascii.read(SIMPLE_LINES, format='ecsv')
    assert "PyYAML package is required" in str(exc.value)


@pytest.mark.skipif('not HAS_YAML')
def test_round_trip_masked_table_default(tmpdir):
    """Test (mostly) round-trip of MaskedColumn through ECSV using default serialization
    that uses an empty string "" to mark NULL values.  Note:

    >>> simple_table(masked=True)
    <Table masked=True length=3>
      a      b     c
    int64 float64 str1
    ----- ------- ----
       --     1.0    c
        2     2.0   --
        3      --    e
    """
    filename = str(tmpdir.join('test.ecsv'))

    t = simple_table(masked=True)  # int, float, and str cols with one masked element
    t.write(filename)

    t2 = Table.read(filename)
    assert t2.masked is False
    assert t2.colnames == t.colnames
    for name in t2.colnames:
        # From formal perspective the round-trip columns are the "same"
        assert np.all(t2[name].mask == t[name].mask)
        assert np.all(t2[name] == t[name])

        # But peeking under the mask shows that the underlying data are changed
        # because by default ECSV uses "" to represent masked elements.
        t[name].mask = False
        t2[name].mask = False
        assert not np.all(t2[name] == t[name])  # Expected diff


@pytest.mark.skipif('not HAS_YAML')
def test_round_trip_masked_table_serialize_mask(tmpdir):
    """Same as prev but set the serialize_method to 'data_mask' so mask is written out"""
    filename = str(tmpdir.join('test.ecsv'))

    t = simple_table(masked=True)  # int, float, and str cols with one masked element
    t['c'][0] = ''  # This would come back as masked for default "" NULL marker

    # MaskedColumn with no masked elements. See table the MaskedColumnInfo class
    # _represent_as_dict() method for info about we test a column with no masked elements.
    t['d'] = [1, 2, 3]

    t.write(filename, serialize_method='data_mask')

    t2 = Table.read(filename)
    assert t2.masked is False
    assert t2.colnames == t.colnames
    for name in t2.colnames:
        assert np.all(t2[name].mask == t[name].mask)
        assert np.all(t2[name] == t[name])

        # Data under the mask round-trips also (unmask data to show this).
        t[name].mask = False
        t2[name].mask = False
        assert np.all(t2[name] == t[name])


@pytest.mark.skipif('not HAS_YAML')
@pytest.mark.parametrize('table_cls', (Table, QTable))
def test_round_trip_user_defined_unit(table_cls, tmpdir):
    """Ensure that we can read-back enabled user-defined units."""
    # Test adapted from #8897, where it was noted that this works
    # but was not tested.
    filename = str(tmpdir.join('test.ecsv'))
    unit = u.def_unit('bandpass_sol_lum')
    t = table_cls()
    t['l'] = np.arange(5) * unit
    t.write(filename)
    # without the unit enabled, get UnrecognizedUnit
    with catch_warnings(u.UnitsWarning) as w:
        t2 = table_cls.read(filename)
    assert isinstance(t2['l'].unit, u.UnrecognizedUnit)
    assert str(t2['l'].unit) == 'bandpass_sol_lum'
    if table_cls is QTable:
        assert len(w) == 1
        assert f"'{unit!s}' did not parse" in str(w[0].message)
        assert np.all(t2['l'].value == t['l'].value)
    else:
        assert len(w) == 0
        assert np.all(t2['l'] == t['l'])

    # But with it enabled, it works.
    with u.add_enabled_units(unit):
        with catch_warnings(u.UnitsWarning) as w:
            t3 = table_cls.read(filename)
        assert len(w) == 0
        assert t3['l'].unit is unit
        assert np.all(t3['l'] == t['l'])

        # Just to be sure, aloso try writing with unit enabled.
        filename2 = str(tmpdir.join('test2.ecsv'))
        t3.write(filename2)
        with catch_warnings(u.UnitsWarning) as w:
            t4 = table_cls.read(filename)
        assert len(w) == 0
        assert t4['l'].unit is unit
        assert np.all(t4['l'] == t['l'])
