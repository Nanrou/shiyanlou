'''
from flask import Flask
app = Flask(__name__)
@app.route('/')
def index():
    return 'Hello'
if __name__ == '__main__':
    app.run(port=8000)
'''
import MySQLdb
db = MySQLdb.connect('127.0.1.1','root','password','recommend')
cursor = db.cursor()

aa = cursor.execute('select * from anime')
print aa

info = cursor.fetchmany(aa)
for i in info:
    print i
    
cursor.close()
db.close()