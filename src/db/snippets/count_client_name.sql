SELECT client_name, com_date,  COUNT(client_name) as count_client_name
FROM dpoh_com_details
WHERE dpoh_first_name == "Stephen" AND dpoh_last_name == "Harper"
GROUP BY client_name
ORDER BY count_client_name DESC