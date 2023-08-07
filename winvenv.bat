python --version 3>NUL
if errorlevel 1 goto errorNoPython

pip install virtualenv 
python -m venv CamFitzpatrickvenv
for /r .\windependencies %%F in (*.*) do .\CamFitzpatrickvenv\Scripts\pip install  %%F

goto:eof

s:errorNoPython
echo Error Python not installed

pause
