import pytest


@pytest.mark.ci
def test_gw(asr_tmpdir_w_params, test_material, mockgpaw, mocker, get_webcontent):
    import numpy as np
    import gpaw
    from gpaw.response.g0w0 import G0W0
    mocker.patch.object(gpaw.GPAW, "_get_band_gap")
    gpaw.GPAW._get_band_gap.return_value = 1
    mocker.patch.object(gpaw.GPAW, "_get_fermi_level")
    gpaw.GPAW._get_fermi_level.return_value = 0.5

    from asr.gw import main
    test_material.write("structure.json")
    ndim = sum(test_material.pbc)

    def calculate(self):
        eps = self.calc.get_all_eigenvalues()[np.newaxis, :, 0:6]

        return {"qp": eps,
                "Z": np.zeros_like(eps) + 1,
                "eps": eps}

    mocker.patch.object(G0W0, "calculate", calculate)
    if ndim > 1:
        results = main()
        assert results['gap_gw'] == pytest.approx(1)
        get_webcontent()
    else:
        with pytest.raises(NotImplementedError):
            main()
