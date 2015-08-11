DROP VIEW IF EXISTS dpoh_com_details;
CREATE VIEW dpoh_com_details AS
SELECT 
	dpoh.comlog_id AS comlog_id, 
	cr.com_date AS com_date, 
	cr.registrant_last_name AS registrant_last_name, 
	cr.registrant_first_name AS registrant_first_name, 
	dpoh.dpoh_last_name AS dpoh_last_name, 
	dpoh.dpoh_first_name AS dpoh_first_name,
	client.client_name AS client_name,
	sm.subject_matter AS subject_matter
FROM communication_dpoh AS dpoh
	INNER JOIN subject_matter AS sm ON sm.comlog_id == dpoh.comlog_id
	INNER JOIN communication_registrant AS cr ON cr.comlog_id == dpoh.comlog_id
	INNER JOIN client ON cr.client_num == client.client_num;