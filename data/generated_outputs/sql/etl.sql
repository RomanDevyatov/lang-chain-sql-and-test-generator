```sql
CREATE OR REPLACE VIEW user_metrics_view__staging AS
SELECT
    user_id,
    -- Sum of revenue for purchase events only
    SUM(CASE WHEN event_type = 'purchase' THEN revenue ELSE 0 END) AS total_revenue,
    -- Count of all events
    COUNT(*) AS total_events,
    -- Average revenue per event, handle division by zero
    CASE
        WHEN COUNT(*) = 0 THEN 0
        ELSE SUM(CASE WHEN event_type = 'purchase' THEN revenue ELSE 0 END) * 1.0 / COUNT(*)
    END AS avg_revenue_per_event
FROM raw_events
GROUP BY user_id;
```