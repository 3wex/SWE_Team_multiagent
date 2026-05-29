import subprocess, sys
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'flask', 'flask_sqlalchemy', 'sqlalchemy'])
print('Installed')
