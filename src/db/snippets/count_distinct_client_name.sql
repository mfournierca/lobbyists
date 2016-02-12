SELECT comlog_id, client_name, com_date, COUNT(client_name) as count_client_name
FROM (
	SELECT DISTINCT comlog_id, client_name, com_date
	FROM dpoh_com_details
	WHERE dpoh_last_name == 'Harper' AND dpoh_first_name ==  'Stephen'
)
GROUP BY client_name
ORDER BY count_client_name DESC