import pytest
import numpy as np
from astropy.io import fits
from astropy.table import Table
from astropy import units as u
from synphot import SourceSpectrum

from pyckles import SpectralLibrary


class TestInit:
    def test_initialised_with_nothing(self):
        assert isinstance(SpectralLibrary(), SpectralLibrary)

    def test_initialises_with_correct_name(self):
        pickles = SpectralLibrary("Pickles")
        assert isinstance(pickles, SpectralLibrary)
        assert isinstance(pickles.table, Table)

    def test_nothing_loaded_for_wrong_name(self):
        pickles = SpectralLibrary("Bogus")
        assert isinstance(pickles, SpectralLibrary)
        assert pickles.table is None


class TestGetAttr:
    def test_returns_bintablehdu_for_correct_name_attribute_call(self):
        pickles = SpectralLibrary("Pickles")
        spec = pickles.A0V
        assert isinstance(spec, fits.BinTableHDU)

    def test_returns_attribute_error_if_spec_name_not_in_catalogue(self):
        pickles = SpectralLibrary("Pickles")
        with pytest.raises(AttributeError):
            pickles.ATV

    def test_returns_arrays_with_return_style_set_to_array(self):
        pickles = SpectralLibrary("Pickles")
        pickles.meta["return_style"] = "array"
        spec = pickles.A0V
        assert isinstance(spec[0], np.ndarray)
        assert isinstance(spec[1], np.ndarray)

    def test_returns_quantity_with_return_style_set_to_quantity(self):
        pickles = SpectralLibrary("Pickles")
        pickles.meta["return_style"] = "quantity"
        spec = pickles.A0V
        assert isinstance(spec[1], u.Quantity)
        assert spec[1].unit == u.Unit("erg s-1 angstrom-1 cm-2")

    def test_returns_sourcespectrum_with_return_style_set_to_synphot(self):
        pickles = SpectralLibrary("Pickles")
        pickles.meta["return_style"] = "synphot"
        spec = pickles.A0V
        assert isinstance(spec, SourceSpectrum)

