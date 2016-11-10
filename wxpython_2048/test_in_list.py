'''
i = 1
vlist = [1,1,3,5,4,4]
print vlist,len(vlist)
t = 1
score = 0

while i<len(vlist):
    print '--------------------'
    print 'This is %s time.' % t
    t += 1
    print 'now is vlist[%s] and vlist[%s]' % (i-1,i)
    if vlist[i-1] == vlist[i]:
        del vlist[i]
        vlist[i-1] *=2
        score += vlist[i-1]
        i += 1
    i += 1
    print 'i=%s' % i
    print 'score = %s' % score
    print 'len(vlist) = %s' % len(vlist)
    print '--------------------\n'
'''

#vlist = [1,1,3,5,4,4]
vlist=[2,2]
print vlist,len(vlist)
t = 1
score = 0
i = len(vlist)-1
print i
while i>0:
    print '--------------------'
    print 'This is %s time.' % t
    t += 1
    print 'now is vlist[%s] and vlist[%s]' % (i-1,i)
    
    if vlist[i-1] == vlist[i]:
        del vlist[i]
        vlist[i-1] *=2
        score += vlist[i-1]                        
        i -= 1
    i -= 1
    print 'i=%s' % i
    print 'score = %s' % score
    print 'len(vlist) = %s' % len(vlist)
    print 'vlist = %s' % vlist
    print '--------------------\n'