import unittest

from Orange.data import Table
from Orange.widgets.tests.base import WidgetTest

from orangecontrib.timeseries import Timeseries
from orangecontrib.timeseries.widgets.owseasonaladjustment import OWSeasonalAdjustment


class TestOWSeasonalAdjustment(WidgetTest):
    def setUp(self):
        self.widget = self.create_widget(OWSeasonalAdjustment)  # type: OWSeasonalAdjustment

    def test_negative_values(self):
        """
        Multiplicative seasonality does not work if there are negative
        values.
        GH-35
        """
        w = self.widget
        table = Table("iris")
        table.X[1, 0] = -1
        time_series = Timeseries(table)
        w.decomposition = 1
        w.autocommit = True
        self.assertFalse(w.Error.seasonal_decompose_fail.is_shown())
        self.send_signal(w.Inputs.time_series, time_series)
        self.widget.view.selectAll()
        self.assertTrue(w.Error.seasonal_decompose_fail.is_shown())
        self.send_signal(w.Inputs.time_series, None)
        self.assertFalse(w.Error.seasonal_decompose_fail.is_shown())

    def test_too_many_periods(self):
        """
        Do not crash when there are too many season periods.
        GH-38
        """
        w = self.widget
        time_series = Timeseries(Table("iris")[::30])
        self.assertEqual(w.n_periods, 12)
        self.send_signal(w.Inputs.time_series, time_series)
        self.assertEqual(w.n_periods, 4)

    def test_not_enough_instances(self):
        """
        At least three instances are needed.
        GH-38
        """
        w = self.widget
        time_series = Timeseries(Table("iris")[:2])
        self.assertFalse(w.Error.not_enough_instances.is_shown())
        self.send_signal(w.Inputs.time_series, time_series)
        self.assertTrue(w.Error.not_enough_instances.is_shown())
        self.send_signal(w.Inputs.time_series, None)
        self.assertFalse(w.Error.not_enough_instances.is_shown())


if __name__ == "__main__":
    unittest.main()