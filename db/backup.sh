pg_dump LTERV2 -f ~/Dropbox/database-development/db/backups/lter_db_backup_$(date +%m-%d-%Y).sql
pg_dump LTERV2 | ssh -C lter@www.how-imodel-it.com "psql popler"