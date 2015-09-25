SELECT *, count(*) as infra_count
FROM (
	SELECT cd.comlog_id, cd.dpoh_last_name, cd.dpoh_first_name, sm.subject_matter
	FROM communication_dpoh as cd INNER JOIN subject_matter as sm 
		ON cd.comlog_id = sm.comlog_id
	WHERE sm.subject_matter = "Infrastructure"
) as v
GROUP BY v.dpoh_last_name, v.dpoh_first_name
ORDER BY infra_count DESC;