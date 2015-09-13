SELECT
    cr.comlog_id,
    cr.registrant_first_name,
    cr.registrant_last_name,
    cl.client_name,
    COUNT(*) AS number_of_meetings
FROM communication_dpoh AS cd
    INNER JOIN communication_registrant AS cr ON cd.comlog_id == cr.comlog_id
    INNER JOIN client AS cl ON cr.client_num == cl.client_num
WHERE cd.dpoh_last_name == "Harper" AND cd.dpoh_first_name == "Stephen"
GROUP BY cr.registrant_first_name, cr.registrant_last_name
ORDER BY number_of_meetings DESC
