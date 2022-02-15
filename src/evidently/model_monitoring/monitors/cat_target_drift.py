from typing import Generator

from evidently.analyzers import cat_target_drift_analyzer
from evidently.model_monitoring import monitoring


class CatTargetDriftMonitorMetrics:
    """Class for category target grift metrics.

    Metrics list:
        - count: quantity of rows in `reference` and `current` datasets
        - drift: p_value for the data drift
    """
    _tag = 'cat_target_drift'
    count = monitoring.ModelMonitoringMetric(f'{_tag}:count', ['dataset'])
    drift = monitoring.ModelMonitoringMetric(f'{_tag}:drift', ['kind'])


class CatTargetDriftMonitor(monitoring.ModelMonitor):
    def monitor_id(self) -> str:
        return 'cat_target_drift'

    def analyzers(self):
        return [cat_target_drift_analyzer.CatTargetDriftAnalyzer]

    def metrics(self, analyzer_results) -> Generator[monitoring.MetricsType, None, None]:
        results = cat_target_drift_analyzer.CatTargetDriftAnalyzer.get_results(analyzer_results)

        # quantity of rows in income data
        yield CatTargetDriftMonitorMetrics.count.create(results.reference_data_count, dict(dataset='prediction'))
        yield CatTargetDriftMonitorMetrics.count.create(results.current_data_count, dict(dataset='current'))

        if results.prediction_metrics:
            yield CatTargetDriftMonitorMetrics.drift.create(results.prediction_metrics.drift, dict(kind='prediction'))

        if results.target_metrics:
            yield CatTargetDriftMonitorMetrics.drift.create(results.target_metrics.drift, dict(kind='target'))
