import numpy
import pytest
from matchms import Spectrum
from matchms.filtering import derive_inchi_from_smiles


def test_derive_inchi_from_smiles():
    """Test if conversion to inchi works when only smiles is given.
    """
    pytest.importorskip("rdkit")
    spectrum_in = Spectrum(mz=numpy.array([], dtype='float'),
                           intensities=numpy.array([], dtype='float'),
                           metadata={"smiles": "C1CCCCC1"})

    spectrum = derive_inchi_from_smiles(spectrum_in)
    inchi = spectrum.get("inchi").replace('"', '')
    assert inchi == 'InChI=1S/C6H12/c1-2-4-6-5-3-1/h1-6H2', "Expected different InChI"
