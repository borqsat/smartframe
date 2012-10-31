import sys
sys.path.append('sikuli-script.jar')
import imglib
print 'checking test environment....'
print '1:check open cv'
test1 = imglib.isRegionMatch('222.png','22.png'):

if not test1:
    print 'Please check if the opencv-2.0 has been installed.'
    
print imglib.getRegionCenterPoint('222.png','22.png')
print imglib.getRegionTopleftPoint('222.png','22.png')
print 'opencv is OK.'




