import subprocess
subprocess.Popen("pyinstaller admin.py database.py --noconsole --add-data 'logo.ico:.' --icon='logo.ico' --onefile --name MyMarket",shell=True)