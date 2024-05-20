from flask import *
import mysql.connector
from datetime import datetime
app=Flask(__name__)

app.secret_key='user' 

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Shukurmern@786",
  database="Todo_List"
)


mycursor = mydb.cursor(buffered=True)


@app.route('/home',methods=['POST','GET'])
def home0():
    return render_template('home.html')


@app.route('/reg',methods=['POST','GET'])
def home1():
    return render_template('reg.html')

@app.route('/regf',methods=['POST','GET'])
def home2():
    d=request.form
    if d['p']!=d['rp']:
         print("if")
         return render_template('reg.html',u=0)

    
    try:   
        now = datetime.now()
        f_d = now.strftime('%Y-%m-%d %H:%M:%S')
        print(f_d) 
        global mycursor
        global mydb
        s1="insert into users(name,email,created_at,updated_at,password) values(%s,%s,%s,%s,%s)"
        v=(d['u'],d['e'],f_d,f_d,d['p'])
        mycursor.execute(s1,v)
        mydb.commit()
        return render_template('login.html',u="Success")
    except: 
        print("except")   
        return render_template('reg.html',u=1)

  

@app.route('/login',methods=['POST','GET'])
def home3():
    print("sample1")
    return render_template('login.html')
    
    
@app.route('/loginf',methods=['POST','GET'])
def home4():
    print("sample2")
    d=request.form 
    global mycursor
    global mydb
    print(d['u'])
    s="select * from users where username=%s and password=%s"
    v=[d['u'],d['p']]
    mycursor.execute(s,v)
    r=mycursor.fetchall()
    print(r)
    if len(r)!=0:
        session['user']=d['u']
        return redirect(url_for('home8'))

    # for i in m:
    #     print(i[0],i[1])
    #     if d['u']==i[0] and d['p']==i[1]:
    #            session['user']=d['u']
    #            return render_template('add.html',u="Success")
        
    else:
             mydb.commit()
             return render_template('login.html',u=0)
        
     

@app.route('/add',methods=['POST','GET'])
def home5():
    return render_template('add.html',u="Success")




@app.route('/addf',methods=['POST','GET'])
def home6():
    global mycursor
    global mydb
    d=request.form['d']
    try:
        print("addf try")
        mycursor = mydb.cursor()
        u1=session['user']
        s='insert into todo values(%s,%s)'
        mycursor.execute(s,(u1,d))
        mydb.commit()
        return render_template('add.html',u="Success")

    except:
        print("addf except")
        return render_template('add.html',u="Failure")



# @app.route('/view',methods=['POST','GET'])
# def home7():
#     return render_template('view.html')



@app.route('/viewf',methods=['POST','GET'])
def home8():
    global mydb
    global mycursor
    u1=session["user"]
    s="select * from todo where username=%s"
    mycursor.execute(s,[u1])
    r=mycursor.fetchall()
    if len(r)==0:
        return render_template('view.html',u="You Dont Have Any think ToDo",user=u1)
    str1=""
    c=-1
    for i in r:
        c=c+1
        p=f"<input type='radio' name='{str(c)}' value='{str(i[1])}' >  <label for='{str(c)}'> {str(i[1])} </label>"
        str1=str1+p
   
    # print(str1)
    return render_template('view.html',u=str1,user=u1)
    

@app.route('/deletef',methods=['POST','GET'])
def home9():
        global mydb
        global mycursor
        u1=session["user"]
        u2=dict(request.form)
        u2=list(u2.values())[0]
        print(u2)
        s="delete from todo where username=%s and list=%s"
        v=[u1,u2]
        mycursor.execute(s,v)
        mydb.commit()
        return redirect(url_for('home8'))



    


app.run(debug=True)


