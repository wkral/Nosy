# By Jeff Winkler, http://jeffwinkler.net

import os,stat,time,sys,fnmatch


EXTENSIONS = ['*.py']
EXECUTABLE = 'nosetests'

'''
Watch for changes in all file types specified in 'EXTENSIONS'. 
If changes, run test executable in 'EXECUTABLE'. 
'''
def checkSum():
    ''' Return a long which can be used to know if any .py files have changed.'''
    val = 0
    for root, dirs, files in os.walk(os.getcwd()):
	for extension in EXTENSIONS:
            for f in fnmatch.filter(files, extension):
                stats = os.stat (os.path.join(root, f))
                val += stats [stat.ST_SIZE] + stats [stat.ST_MTIME]
    return val

val=0
try:
    while (True):
        if checkSum() != val:
            val=checkSum()
            os.system ('%s %s' % (EXECUTABLE, ' '.join(sys.argv[1:])))
        time.sleep(1)
except KeyboardInterrupt:
    print 'Goodbye'

