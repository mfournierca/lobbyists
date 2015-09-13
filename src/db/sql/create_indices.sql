DROP INDEX IF EXISTS communication_dpoh.dpoh_comlog_id_index;
CREATE INDEX dpoh_comlog_id_index ON communication_dpoh (comlog_id);

DROP INDEX IF EXISTS communication_registrant.reg_comlog_id_index;
CREATE INDEX reg_comlog_id_index ON communication_registrant (comlog_id);

DROP INDEX IF EXISTS subject_matter.subject_comlog_id_index;
CREATE INDEX subject_comlog_id_index ON subject_matter (comlog_id);
