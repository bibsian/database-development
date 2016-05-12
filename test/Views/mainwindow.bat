REM Creates pyfiles from qtdesigner ui files

echo trying to update mainwindow
C:\Users\MillerLab\Envs\lter\Scripts\python.exe C:\Users\MillerLab\Envs\lter\Lib\site-packages\PyQt4\uic\pyuic.py C:\Users\MillerLab\Dropbox\database-development\test\Views\ui_mainrefactor.ui -o C:\Users\MillerLab\Dropbox\database-development\test\Views\ui_mainrefactor.py
echo main window updated

cp C:\Users\MillerLab\Dropbox\database-development\test\Views\ui_mainrefactor.py C:\Users\MillerLab\Dropbox\database-development\test\ui_mainrefactor.py
echo main window copied

C:\Users\MillerLab\Envs\lter\Scripts\python.exe C:\Users\MillerLab\Envs\lter\Lib\site-packages\PyQt4\uic\pyuic.py C:\Users\MillerLab\Dropbox\database-development\test\Views\ui_dialog_session.ui -o C:\Users\MillerLab\Dropbox\database-development\test\Views\ui_dialog_session.py
echo session dialog updated

cp C:\Users\MillerLab\Dropbox\database-development\test\Views\ui_dialog_session.py C:\Users\MillerLab\Dropbox\database-development\test\ui_dialog_session.py
echo session dialog copied

C:\Users\MillerLab\Envs\lter\Scripts\python.exe C:\Users\MillerLab\Envs\lter\Lib\site-packages\PyQt4\uic\pyuic.py C:\Users\MillerLab\Dropbox\database-development\test\Views\ui_dialog_site.ui -o C:\Users\MillerLab\Dropbox\database-development\test\Views\ui_dialog_site.py
echo site dialog updated

cp C:\Users\MillerLab\Dropbox\database-development\test\Views\ui_dialog_site.py C:\Users\MillerLab\Dropbox\database-development\test\ui_dialog_site.py
echo site dialog copied

C:\Users\MillerLab\Envs\lter\Scripts\python.exe C:\Users\MillerLab\Envs\lter\Lib\site-packages\PyQt4\uic\pyuic.py C:\Users\MillerLab\Dropbox\database-development\test\Views\ui_dialog_main.ui -o C:\Users\MillerLab\Dropbox\database-development\test\Views\ui_dialog_main.py
echo main dialog updated

cp C:\Users\MillerLab\Dropbox\database-development\test\Views\ui_dialog_main.py C:\Users\MillerLab\Dropbox\database-development\test\ui_dialog_main.py
echo main dialog copied

C:\Users\MillerLab\Envs\lter\Scripts\python.exe C:\Users\MillerLab\Envs\lter\Lib\site-packages\PyQt4\uic\pyuic.py C:\Users\MillerLab\Dropbox\database-development\test\Views\ui_dialog_taxa.ui -o C:\Users\MillerLab\Dropbox\database-development\test\Views\ui_dialog_taxa.py
echo taxa dialog updated

cp C:\Users\MillerLab\Dropbox\database-development\test\Views\ui_dialog_taxa.py C:\Users\MillerLab\Dropbox\database-development\test\ui_dialog_taxa.py
echo taxa dialog copied

C:\Users\MillerLab\Envs\lter\Scripts\python.exe C:\Users\MillerLab\Envs\lter\Lib\site-packages\PyQt4\uic\pyuic.py C:\Users\MillerLab\Dropbox\database-development\test\Views\ui_dialog_time.ui -o C:\Users\MillerLab\Dropbox\database-development\test\Views\ui_dialog_time.py
echo time dialog updated

cp C:\Users\MillerLab\Dropbox\database-development\test\Views\ui_dialog_time.py C:\Users\MillerLab\Dropbox\database-development\test\ui_dialog_time.py
echo time dialog copied

C:\Users\MillerLab\Envs\lter\Scripts\python.exe C:\Users\MillerLab\Envs\lter\Lib\site-packages\PyQt4\uic\pyuic.py C:\Users\MillerLab\Dropbox\database-development\test\Views\ui_dialog_obs.ui -o C:\Users\MillerLab\Dropbox\database-development\test\Views\ui_dialog_obs.py
echo obs dialog updated

cp C:\Users\MillerLab\Dropbox\database-development\test\Views\ui_dialog_obs.py C:\Users\MillerLab\Dropbox\database-development\test\ui_dialog_obs.py
echo obs dialog copied

C:\Users\MillerLab\Envs\lter\Scripts\python.exe C:\Users\MillerLab\Envs\lter\Lib\site-packages\PyQt4\uic\pyuic.py C:\Users\MillerLab\Dropbox\database-development\test\Views\ui_dialog_covariate.ui -o C:\Users\MillerLab\Dropbox\database-development\test\Views\ui_dialog_covariate.py
echo covariate dialog updated

cp C:\Users\MillerLab\Dropbox\database-development\test\Views\ui_dialog_covariate.py C:\Users\MillerLab\Dropbox\database-development\test\ui_dialog_covariate.py
echo covariate dialog copied

C:\Users\MillerLab\Envs\lter\Scripts\python.exe C:\Users\MillerLab\Envs\lter\Lib\site-packages\PyQt4\uic\pyuic.py C:\Users\MillerLab\Dropbox\database-development\test\Views\ui_dialog_climatesite.ui -o C:\Users\MillerLab\Dropbox\database-development\test\Views\ui_dialog_climatesite.py
echo climate site dialog updated

cp C:\Users\MillerLab\Dropbox\database-development\test\Views\ui_dialog_climatesite.py C:\Users\MillerLab\Dropbox\database-development\test\ui_dialog_climatesite.py
echo climate site dialog copied


