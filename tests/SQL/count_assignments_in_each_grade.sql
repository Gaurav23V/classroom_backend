-- Write query to get count of assignments in each grade
SELECT grade, COUNT(*) as count
FROM assignments
WHERE state = 'GRADED'
GROUP BY grade
ORDER BY grade;