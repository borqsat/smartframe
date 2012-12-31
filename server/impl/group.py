from dbstore import store

##########################Group Roles########################
ROLES = ['system','owner','admin','member']
ROLES_IDX = {'system':0,'owner':1, 'admin':2, 'member':3}

def __getRoleById(gid,uid):
    rdata = store.getUserRole(gid,uid)
    if rdata.has_key('uid'):
        return rdata['role']
    else:
        return None

def createGroup(uid, groupname, info):
    rdata = store.createGroup(groupname,info)
    if rdata.has_key('gid'):
        store.addGroupMember(rdata['gid'],uid, ROLES_IDX['owner'])
        return {'results':rdata}
    else:
        return {'errors':rdata}

def getGroupInfo(uid, gid):
    role = __getRoleById(gid, uid)
    if (role is None) or (role > ROLES_IDX['member']):
        return {'errors':{'code':'00','msg':'Permission Denied!'}}

    rdata = store.getGroupInfo(gid)
    if rdata.has_key('gid'):
        for d in rdata['members']:
            d['role'] = ROLES[d['role']]
        return {'results':rdata}
    else:
        return {'errors':rdata}

def addGroupMembers(uid, gid,members):
    role = __getRoleById(gid, uid)
    if (role is None) or (role > ROLES_IDX['admin']):
        return {'errors':{'code':'00','msg':'Permission Denied!'}}

    for d in members:
        store.addGroupMember(gid, d['uid'], ROLES_IDX[d['role']])
    return {'results':1}

def setGroupMembers(uid, gid,members):
    role = __getRoleById(gid, uid)
    if (role is None) or (role > ROLES_IDX['admin']):
        return {'errors':{'code':'00','msg':'Permission Denied!'}}

    for d in members:
        store.setGroupMember(gid, d['uid'], ROLES_IDX[d['role']])
    return {'results':1}

def delGroupMembers(uid, gid,members):
    role = __getRoleById(gid, uid)
    if (role is None) or (role > ROLES_IDX['admin']):
        return {'errors':{'code':'00','msg':'Permission Denied!'}}

    for d in members:
        store.delGroupMember(gid,d['uid'])
    return {'results':1}