import os
print 'Install...'
os.popen('sudo mv libcvaux.so.2.1 libcxcore.so.2.1 libhighgui.so.2.1 libcv.so.2.1 libcxts.so.2.1 libml.so.2.1 /usr/local/lib/')
os.popen('cd /usr/local/lib')
os.popen('sudo ln -s libcvaux.so.2.1 libcvaux.so')
os.popen('sudo ln -s libcv.so.2.1 libcv.so')
os.popen('sudo ln -s libcxcore.so.2.1 libcxcore.so')
os.popen('sudo ln -s libcxts.so.2.1 libcxts.so')
os.popen('sudo ln -s libhighgui.so.2.1 libhighgui.so')
os.popen('sudo ln -s libml.so.2.1 libml.so')
os.popen('sudo ldconfig')
print 'Install finished!'
