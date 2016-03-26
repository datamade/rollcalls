PG_DB=openstates

define check_relation
 psql -d $(PG_DB) -c "\d $@" > /dev/null 2>&1 ||
endef

.PHONY : all
all : legislator_roles committees bills bill_actions bill_sponsors bill_votes bill_legislator_votes

2016-03-08-il-csv.zip :
	wget http://static.openstates.org/downloads/$@

%.csv : 2016-03-08-il-csv.zip
	unzip -j $< $@

% : il_%.csv
	$(check_relation) (\
          head -400 $< | csvsql --db postgresql://localhost/$(PG_DB) --tables $@ && \
	  cat $< | psql -d $(PG_DB) -c "COPY $@ FROM STDIN WITH CSV HEADER")

legislator_roles : il_legislator_roles.csv
bills : il_bills.csv
bill_votes : il_bill_votes.csv
bill_actions : il_bill_actions.csv
bill_sponsors : il_bill_sponsors.csv

legislator_roles : 
	$(check_relation) (\
	  head -400 $< | csvsql --db postgresql://localhost/$(PG_DB) --tables $@ && \
	  psql -d $(PG_DB) -c "ALTER TABLE $@ ALTER COLUMN term TYPE TEXT" && \
	  cat $< | psql -d $(PG_DB) -c "COPY $@ FROM STDIN WITH CSV HEADER")

bills bill_actions bill_sponsors bill_votes : 
	$(check_relation) (\
	  head -1000 $< | csvsql --db postgresql://localhost/$(PG_DB) --no-constraints --tables $@ && \
	  psql -d $(PG_DB) -c "ALTER TABLE $@ ALTER COLUMN session TYPE TEXT" && \
	  cat $< | psql -d $(PG_DB) -c "COPY $@ FROM STDIN WITH CSV HEADER")

matrix.csv : bill_votes bill_legislator_votes
	psql -d $(PG_DB) -c "COPY (SELECT bill_id, name, vote \
                                   FROM bill_votes INNER JOIN bill_legislator_votes \
                                   USING (vote_id) \
                                   WHERE motion='Third Reading' \
                                   AND vote_chamber='upper' \
                                   AND session='99th' \
                                   AND yes_count > 0 \
                                   AND no_count > 0 \
                                   ORDER BY bill_id, name) \
                                   TO STDOUT WITH CSV HEADER" | python rollcall.py > $@
