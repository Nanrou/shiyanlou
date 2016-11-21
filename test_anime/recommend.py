#coding:utf8

from random import choice
import MySQLdb

def recommend(user): 
    DB = MySQLdb.connect('127.0.0.1','root','password','recommend')
    cur = DB.cursor()
    
    love = []
    
    sql = 'select anime_id from user_anime where user_id=%s' % user
    cur.execute(sql)
    
    results = cur.fetchall()
    for result in results:
        love.append(result[0])
        
    sql = '''
        select style_id from
            (select user_id ,style_id from
                (select user_id ,anime_id as id from user_anime where user_id=%s) as s
                natural join anime natural join
                (select anime_id as id,style_id from anime_style) as n
                )as temp group by style_id order by count(user_id) desc limit 3;
        ''' % user
        
    cur.execute(sql)
    results=cur.fetchall()
    lis = []
    anime = {}
    for (result,) in results:
        lis.append(result)
    
    for l in lis:
        sql = 'select anime_id from anime_style where style_id=' +str(i)+';'
        cur.execute(sql)
        results = cur.fetchall()
        anime_lis = []
        for result in results:
            anime_lis.append(result[0])
        anime[str(l)] = anime_lis
        
    s = set(anime[str(lis[0])])&set(anime[str(lis[1])])&set(anime[str(lis[2])])
    
    loveSet = set(love)
    
    if loveSet > s:
        s = set(anime[str(lis[0])])
        
    set_lis = []
    for i in s:
        set_lis.append(i)
        
    res = choice(set_lis)
    
    while res in love:
        res = choice(set_lis)
        
    dic = {}
    sql = 'select name,brief from anime where id = ' + str(res) + ';'
    cur.execute(sql)
    result = cur.fetchall()
    dic['name']=result[0][0]
    dic['brief']=result[0][1]
    
    cur.close()
    DB.close()
    
    return dic