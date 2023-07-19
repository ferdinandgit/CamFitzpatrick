python --version 3>NUL
if errorlevel 1 goto errorNoPython

pip install virtualenv 
python -m venv CamFitzpatrickvenv
.\CamFitzpatrickvenv\Scripts\pip3 install -r requirements.txt

goto:eof

:errorNoPython
echo Error Python not installed
