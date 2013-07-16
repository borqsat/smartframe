from smartserver.v0.impl.dbstore import store
from smartserver.v0.impl.dbstore import duration

@duration
def testUpdateSummary():
    for session in store._db['testsessions'].find({},{"sid":1}):
        store.updateTestsessionSummary(session['sid'])
        print "Updating %s" %session['sid']
        print "=======================================\n"
        
if __name__ == '__main__':
    testUpdateSummary()
