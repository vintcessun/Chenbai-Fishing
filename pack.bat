@call conda activate tensor
pyinstaller -i icon.ico -F -c --uac-admin --add-data model;imgs run.py