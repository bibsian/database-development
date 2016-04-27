REM Creates pyfile from qtdesigner ui files
echo trying to update mainwindow
C:\Users\MillerLab\Envs\lter\Scripts\python.exe C:\Users\MillerLab\Envs\lter\Lib\site-packages\PyQt4\uic\pyuic.py C:\Users\MillerLab\Dropbox\database-development\test\Views\ui_mainrefactor.ui -o C:\Users\MillerLab\Dropbox\database-development\test\Views\ui_mainrefactor.py
echo updated main

REM Copying files to test directory
cp C:\Users\MillerLab\Dropbox\database-development\test\Views\ui_mainrefactor.py C:\Users\MillerLab\Dropbox\database-development\test\ui_mainrefactor.py

echo tyring to update session dialog
C:\Users\MillerLab\Envs\lter\Scripts\python.exe C:\Users\MillerLab\Envs\lter\Lib\site-packages\PyQt4\uic\pyuic.py C:\Users\MillerLab\Dropbox\database-development\test\Views\ui_dialog_session.ui -o C:\Users\MillerLab\Dropbox\database-development\test\Views\ui_dialog_session.py
echo updated session dialog

REM Copying files to test directory
cp C:\Users\MillerLab\Dropbox\database-development\test\Views\ui_dialog_session.py C:\Users\MillerLab\Dropbox\database-development\test\ui_dialog_session.py