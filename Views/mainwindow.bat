REM Creates pyfiles from qtdesigner ui files

echo trying to update mainwindow
C:\Users\MillerLab\Envs\lter\Scripts\python.exe pyuic.py ui_mainrefactor.ui -o ui_mainrefactor.py
echo main window updated

C:\Users\MillerLab\Envs\lter\Scripts\python.exe pyuic.py  ui_dialog_session.ui -o ui_dialog_session.py
echo session dialog updated

C:\Users\MillerLab\Envs\lter\Scripts\python.exe pyuic.py ui_dialog_site.ui -o ui_dialog_site.py
echo site dialog updated

C:\Users\MillerLab\Envs\lter\Scripts\python.exe pyuic.py ui_dialog_main.ui -o ui_dialog_main.py
echo main dialog updated

C:\Users\MillerLab\Envs\lter\Scripts\python.exe pyuic.py ui_dialog_taxa.ui -o ui_dialog_taxa.py
echo taxa dialog updated

C:\Users\MillerLab\Envs\lter\Scripts\python.exe pyuic.py ui_dialog_time.ui -o ui_dialog_time.py
echo time dialog updated

C:\Users\MillerLab\Envs\lter\Scripts\python.exe pyuic.py ui_dialog_obs.ui -o ui_dialog_obs.py
echo obs dialog updated

C:\Users\MillerLab\Envs\lter\Scripts\python.exe pyuic.py ui_dialog_covariate.ui -o ui_dialog_covariate.py
echo covariate dialog updated

C:\Users\MillerLab\Envs\lter\Scripts\python.exe pyuic.py ui_dialog_climatesite.ui -o ui_dialog_climatesite.py
echo climate site dialog updated

