SELECT 
	comlog_id, 
	com_date, 
	registrant_last_name, 
	registrant_first_name, 
	dpoh_last_name, 
	dpoh_first_name,
	subject_matter
FROM dpoh_com_details
WHERE dpoh_last_name == "Harper"
ORDER BY com_date
LIMIT 50