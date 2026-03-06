# SQL Drills Reference

## Sub-Skills Taxonomy

### Filtering (Beginner)
- WHERE clauses
- IN/NOT IN
- BETWEEN
- LIKE patterns
- NULL handling

### Joins (Intermediate)
- INNER JOIN
- LEFT/RIGHT JOIN
- Self-joins
- Multiple table joins
- JOIN vs subquery choice

### Aggregation (Intermediate)
- GROUP BY basics
- HAVING vs WHERE
- Multiple aggregates
- Conditional aggregation (CASE in aggregate)

### Window Functions (Advanced)
- ROW_NUMBER/RANK/DENSE_RANK
- LAG/LEAD
- Running totals (SUM OVER)
- Moving averages
- PARTITION BY + ORDER BY

### Subqueries (Intermediate-Advanced)
- Scalar subqueries
- Correlated subqueries
- EXISTS/NOT EXISTS
- Subquery in FROM (derived tables)

### CTEs (Advanced)
- Basic CTE structure
- Multiple CTEs
- Recursive CTEs

## Exercise Templates

### Window Function Drill
```sql
-- Given: sales(id, product, amount, sale_date)
-- Return each sale with:
-- - running total per product
-- - rank within product by amount
-- - difference from previous sale
```

### Self-Join Drill
```sql
-- Given: employees(id, name, manager_id)
-- Return employee name with their manager's name
-- Include employees without managers
```

### Correlated Subquery Drill
```sql
-- Given: orders(id, customer_id, amount, order_date)
-- Return orders where amount > customer's average
```

## Test Data Pattern

Always provide minimal test data for verification:
```sql
CREATE TEMP TABLE test_data AS
SELECT * FROM (VALUES
    (1, 'A', 100),
    (2, 'B', 200)
) AS t(id, category, value);
```

## Difficulty Calibration

| Level | Characteristics |
|-------|----------------|
| 1 | Single table, basic clause |
| 2 | Single join or simple aggregation |
| 3 | Multiple joins or window function |
| 4 | Correlated subquery or complex window |
| 5 | Recursive CTE or query optimization |
