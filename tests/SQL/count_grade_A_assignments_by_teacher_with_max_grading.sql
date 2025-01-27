-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH teacher_grading_counts AS (
    SELECT teacher_id, COUNT(*) as grading_count
    FROM assignments
    WHERE state = 'GRADED'
    GROUP BY teacher_id
    ORDER BY grading_count DESC
    LIMIT 1
)
SELECT COUNT(*) as grade_a_count
FROM assignments a
JOIN teacher_grading_counts t ON a.teacher_id = t.teacher_id
WHERE a.grade = 'A'
AND a.state = 'GRADED';