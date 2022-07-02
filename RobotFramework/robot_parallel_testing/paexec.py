import os
import random
import subprocess
import time
import webbrowser


# config
baseFolder = 'data_tests'
suiteFile = 'suite.robot'
usernamesFile = 'user_list.txt'
testUsersPassword = 'secret'

# clean up base folder
os.system('del /f ' + baseFolder)
os.mkdir(baseFolder)

# no output to console please
FNULL = open(os.devnull, 'w')

# load list of usernames
f = open(usernamesFile, 'r')
lines = f.readlines()
f.close()

# spawn subprocess for each user
userPathes = []
processes = set()
for line in lines:
    user = line.strip()
    userPath = baseFolder + '/' + user
    userPathes.append((user, userPath))
    os.mkdir(userPath)
    cmdParts = [
        'robot',
        # abitrary amount of variables can be added here
        '--variable', 'USER:' + user,
        '--variable', 'PASSWORD:' + testUsersPassword,
        # use -t argument to execute only the test named 'Login Test' from the suite
        '../../' + suiteFile,
    ]
    processes.add(subprocess.Popen(cmdParts, cwd=userPath, stdout=FNULL))
    print('Spawned ' + user)

    # random timeout to simulate more realistic user behavior
    time.sleep(random.randint(0, 4))

# wait until all subprocesses finished
for proc in processes:
    proc.wait()

# collect output and open log files of failed tests
for username, path in userPathes:
    f = open(path + '/output.xml')
    content = f.read()
    f.close()
    if 'status="FAIL"' in content:
        print(username + '\t' + 'Failed')
        webbrowser.open(path + '/report.html')
    else:
        print(username + '\t' + 'OK')