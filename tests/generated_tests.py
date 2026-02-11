```python
def test_total_revenue_not_null_and_non_negative(user_metrics_df):
    assert user_metrics_df['total_revenue'].notnull().all()
    assert (user_metrics_df['total_revenue'] >= 0).all()

def test_total_events_greater_than_zero(user_metrics_df):
    assert (user_metrics_df['total_events'] > 0).all()

def test_avg_revenue_per_event_non_negative(user_metrics_df):
    assert (user_metrics_df['avg_revenue_per_event'] >= 0).all()

def test_no_duplicate_user_ids(user_metrics_df):
    assert user_metrics_df['user_id'].is_unique
```