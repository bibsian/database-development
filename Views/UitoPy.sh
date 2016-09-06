#!bin/bash

python /Users/bibsian/.virtualenvs/lter/lib/python3.4/site-packages/PyQt4/uic/pyuic.py /Users/bibsian/Desktop/git/database-development/test/Views/ui_mainrefactor.ui -o /Users/bibsian/Desktop/git/database-development/test/Views/ui_mainrefactor.py

cp /Users/bibsian/Desktop/git/database-development/test/Views/ui_mainrefactor.py /Users/bibsian/Desktop/git/database-development/test/ui_mainrefactor.py

python /Users/bibsian/.virtualenvs/lter/lib/python3.4/site-packages/PyQt4/uic/pyuic.py /Users/bibsian/Desktop/git/database-development/test/Views/ui_dialog_session.ui -o /Users/bibsian/Desktop/git/database-development/test/Views/ui_dialog_session.py

cp /Users/bibsian/Desktop/git/database-development/test/Views/ui_dialog_session.py /Users/bibsian/Desktop/git/database-development/test/ui_dialog_session.py


python /Users/bibsian/.virtualenvs/lter/lib/python3.4/site-packages/PyQt4/uic/pyuic.py /Users/bibsian/Desktop/git/database-development/test/Views/ui_dialog_site.ui -o /Users/bibsian/Desktop/git/database-development/test/Views/ui_dialog_site.py
echo site dialog updated

cp /Users/bibsian/Desktop/git/database-development/test/Views/ui_dialog_site.py /Users/bibsian/Desktop/git/database-development/test/ui_dialog_site.py
echo site dialog copied

python /Users/bibsian/.virtualenvs/lter/lib/python3.4/site-packages/PyQt4/uic/pyuic.py /Users/bibsian/Desktop/git/database-development/test/Views/ui_dialog_sitechange.ui -o /Users/bibsian/Desktop/git/database-development/test/Views/ui_dialog_sitechange.py
echo site change dialog updated

cp /Users/bibsian/Desktop/git/database-development/test/Views/ui_dialog_sitechange.py /Users/bibsian/Desktop/git/database-development/test/ui_dialog_sitechange.py
echo site change dialog copied

python /Users/bibsian/.virtualenvs/lter/lib/python3.4/site-packages/PyQt4/uic/pyuic.py /Users/bibsian/Desktop/git/database-development/test/Views/ui_dialog_main.ui -o /Users/bibsian/Desktop/git/database-development/test/Views/ui_dialog_main.py
echo main dialog updated

cp /Users/bibsian/Desktop/git/database-development/test/Views/ui_dialog_main.py /Users/bibsian/Desktop/git/database-development/test/ui_dialog_main.py
echo main dialog copied

python /Users/bibsian/.virtualenvs/lter/lib/python3.4/site-packages/PyQt4/uic/pyuic.py /Users/bibsian/Desktop/git/database-development/test/Views/ui_dialog_taxa.ui -o /Users/bibsian/Desktop/git/database-development/test/Views/ui_dialog_taxa.py
echo taxa dialog updated

cp /Users/bibsian/Desktop/git/database-development/test/Views/ui_dialog_taxa.py /Users/bibsian/Desktop/git/database-development/test/ui_dialog_taxa.py
echo taxa dialog copied

python /Users/bibsian/.virtualenvs/lter/lib/python3.4/site-packages/PyQt4/uic/pyuic.py /Users/bibsian/Desktop/git/database-development/test/Views/ui_dialog_time.ui -o /Users/bibsian/Desktop/git/database-development/test/Views/ui_dialog_time.py
echo time dialog updated

cp /Users/bibsian/Desktop/git/database-development/test/Views/ui_dialog_time.py /Users/bibsian/Desktop/git/database-development/test/ui_dialog_time.py
echo time dialog copied

python /Users/bibsian/.virtualenvs/lter/lib/python3.4/site-packages/PyQt4/uic/pyuic.py /Users/bibsian/Desktop/git/database-development/test/Views/ui_dialog_obs.ui -o /Users/bibsian/Desktop/git/database-development/test/Views/ui_dialog_obs.py
echo obs dialog updated

cp /Users/bibsian/Desktop/git/database-development/test/Views/ui_dialog_obs.py /Users/bibsian/Desktop/git/database-development/test/ui_dialog_obs.py
echo obs dialog copied

python /Users/bibsian/.virtualenvs/lter/lib/python3.4/site-packages/PyQt4/uic/pyuic.py /Users/bibsian/Desktop/git/database-development/test/Views/ui_dialog_covariate.ui -o /Users/bibsian/Desktop/git/database-development/test/Views/ui_dialog_covariate.py
echo covariate dialog updated

cp /Users/bibsian/Desktop/git/database-development/test/Views/ui_dialog_covariate.py /Users/bibsian/Desktop/git/database-development/test/ui_dialog_covariate.py
echo covariate dialog copied

python /Users/bibsian/.virtualenvs/lter/lib/python3.4/site-packages/PyQt4/uic/pyuic.py /Users/bibsian/Desktop/git/database-development/test/Views/ui_dialog_climatesite.ui -o /Users/bibsian/Desktop/git/database-development/test/Views/ui_dialog_climatesite.py
echo climate site dialog updated

cp /Users/bibsian/Desktop/git/database-development/test/Views/ui_dialog_climatesite.py /Users/bibsian/Desktop/git/database-development/test/ui_dialog_climatesite.py
echo climate site dialog copied

python /Users/bibsian/.virtualenvs/lter/lib/python3.4/site-packages/PyQt4/uic/pyuic.py /Users/bibsian/Desktop/git/database-development/test/Views/ui_dialog_climateobs.ui -o /Users/bibsian/Desktop/git/database-development/test/Views/ui_dialog_climateobs.py
echo climate obs dialog updated

cp /Users/bibsian/Desktop/git/database-development/test/Views/ui_dialog_climateobs.py /Users/bibsian/Desktop/git/database-development/test/ui_dialog_climateobs.py
echo climate obs dialog copied

python /Users/bibsian/.virtualenvs/lter/lib/python3.4/site-packages/PyQt4/uic/pyuic.py /Users/bibsian/Desktop/git/database-development/test/Views/ui_dialog_table_preview.ui -o /Users/bibsian/Desktop/git/database-development/test/Views/ui_dialog_table_preview.py
echo preview dialog updated

cp /Users/bibsian/Desktop/git/database-development/test/Views/ui_dialog_table_preview.py /Users/bibsian/Desktop/git/database-development/test/ui_dialog_table_preview.py
echo preview dialog copied

echo trying to run bash script
bash /Users/bibsian/Desktop/git/database-development/test/update_source.sh
echo Update poplerGUI