pg_dump LTERV2 -f ~/Desktop/git/database-development/db/backups/lter_db_backup_$(date +%m-%d-%Y).sql
pg_dump LTERV2 | ssh -C lter@www.how-imodel-it.com "psql popler_test"

pg_dump popler__ -f ~/Desktop/git/database-development/db/backups/popler_backup_$(date +%m-%d-%Y).sql
pg_dump popler__ | ssh -C lter@www.how-imodel-it.com "psql popler"