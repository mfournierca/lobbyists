SELECT comlog_id, max(subject_count)
FROM (
	SELECT comlog_id, subject_matter, count(subject_matter) as subject_count
	FROM subject_matter
	GROUP BY comlog_id
);