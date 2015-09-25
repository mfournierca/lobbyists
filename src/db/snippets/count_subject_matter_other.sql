select count(*)
from (
select distinct(comlog_id) from subject_matter where subject_matter = "Other"
);
