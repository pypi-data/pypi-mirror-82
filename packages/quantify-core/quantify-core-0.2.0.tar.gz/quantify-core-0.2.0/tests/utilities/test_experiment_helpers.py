import numpy as np
from quantify.utilities.experiment_helpers import create_plotmon_from_historical
from quantify.data.handling import set_datadir
from tests.helpers import get_test_data_dir


test_datadir = get_test_data_dir()


def test_create_plotmon_from_historical():
    set_datadir(test_datadir)
    plotmon = create_plotmon_from_historical('20200504-191556-002-4209ee')

    x = plotmon.curves[0]['config']['x']
    y = plotmon.curves[0]['config']['y']

    x_exp = np.linspace(0, 5, 50)
    y_exp = np.cos(np.pi * x_exp) * -1
    np.testing.assert_allclose(x[:50], x_exp)
    np.testing.assert_allclose(y[:50], y_exp)

    cfg = plotmon.secondary_QtPlot.traces[0]['config']
    assert np.shape(cfg['z']) == (11, 50)
    assert cfg['xlabel'] == 'Time'
    assert cfg['xunit'] == 's'
    assert cfg['ylabel'] == 'Amplitude'
    assert cfg['yunit'] == 'V'
    assert cfg['zlabel'] == 'Signal level'
    assert cfg['zunit'] == 'V'

    plotmon.close()
    set_datadir(None)
