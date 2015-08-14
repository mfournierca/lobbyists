SELECT dpoh_last_name AS first_name, dpoh_first_name AS last_name
FROM communication_dpoh
WHERE comlog_id == 77595
UNION ALL
SELECT registrant_first_name AS first_name, registrant_last_name AS last_name
FROM communication_registrant
WHERE comlog_id == 77595
