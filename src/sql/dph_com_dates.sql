SELECT 
	DISTINCT(cr.com_date)
FROM communication_dpoh dpoh
	INNER JOIN communication_registrant cr ON cr.comlog_id == dpoh.comlog_id
WHERE dpoh.dpoh_last_name == "Harper" AND dpoh.dpoh_first_name == "Stephen"
ORDER BY cr.com_date
LIMIT 50