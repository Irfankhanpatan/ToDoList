from flask import *
import mysql.connector
from datetime import datetime, timedelta

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
         return render_template('reg.html',u="Password MissMatch")

    
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
        return render_template('login.html')
    except: 
        print("except")   
        return render_template('reg.html',u="Username Exists")

    
    # try:   
    #     now = datetime.now()
    #     f_d = now.strftime('%Y-%m-%d %H:%M:%S')
    #     print(f_d) 
    #     return render_template('reg.html',u=1) 
    #     global mycursor
    #     global mydb
    #     s1="insert into users(name,email,created_at,updated_at) values(%s,%s,%s,%s)"
    #     v=(d['u'],d['p'],d['e'],f_d,f_d)
    #     mycursor.execute(s1,v)
    #     mydb.commit()
    #     return render_template('login.html',u="Success")
    # except: 
    #     print("except") 
    #     return render_template('reg.html',u=1)

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
    s="select * from users where name=%s and password=%s"
    v=[d['u'],d['p']]
    mycursor.execute(s,v)
    r=mycursor.fetchall()
    print(r)
    if len(r)!=0:
        session['user']=r[0][1]
        session['id']=r[0][0]
        return redirect(url_for('view1f'))

    # for i in m:
    #     print(i[0],i[1])
    #     if d['u']==i[0] and d['p']==i[1]:
    #            session['user']=d['u']
    #            return render_template('add.html',u="Success")
        
    else:
             mydb.commit()
             flash("Invalid User")
             return render_template('login.html',u="Invalid Login")


@app.route('/viewf',methods=['POST','GET'])
def home8():
    global mydb
    global mycursor
    u1=session["id"]
    user=session['user']
    print(user)
    s="select * from todo where u_id=%s"
    mycursor.execute(s,[u1])
    r=mycursor.fetchall()
    if len(r)==0:
        return render_template('view.html',u="You Dont Have Any think ToDo",user=u1,u2=user)
    str1=""
    c=-1
    for i in r:
        c=c+1
        p=f"<input type='radio' name='{str(c)}' value='{str(i[1])}' >  <label for='{str(c)}'> {str(i[1])} </label>"
        str1=str1+p
   
    # print(str1)
    return render_template('view.html',u=str1,u2=user)



@app.route('/view1f',methods=['POST','GET'])
def view1f():
    global mydb
    global mycursor
    u1=session["id"]
    user=session['user']
    s=f"select * from todo where u_id={u1} and status='ic'"
    mycursor.execute(s)
    r=mycursor.fetchall()
    mydb.commit()
    if len(r)==0:
        return render_template('view1.html',p="You Dont Have Any thing to Show",u2=user)
    return render_template('view1.html',u=r,u2=user)



@app.route('/view2f',methods=['POST','GET'])
def view2f():
    global mydb
    global mycursor
    u1=session["id"]
    user=session['user']
    rq=dict(request.form)
    print(rq)
    rq=list(rq.values())[0]
    now = datetime.now()
    f_d = now.strftime('%Y-%m-%d %H:%M:%S')
    if rq=='1':
        s=f"select * from todo where u_id={u1} and deadline < '{f_d}'"
    elif rq=='2':
        s=f"select * from todo where u_id={u1} order by created_at asc"
    elif rq=='3':
        s=f"select * from todo where u_id={u1} order by created_at desc"
    elif rq=='4':
        s=f"select * from todo where u_id={u1} and status='c'"
    elif rq=='5':
        s=f"select * from todo where u_id={u1} and status='ic'"
    elif rq=='6':
        s=f"select * from todo where u_id={u1} and status='r'"

    mycursor.execute(s)
    r=mycursor.fetchall()
    mydb.commit()
    if len(r)==0:
        return render_template('view1.html',p="You Dont Have Any think Show",u2=user)

    return render_template('view1.html',u=r,u2=user)
    

@app.route('/add',methods=['POST','GET'])
def add(pp=0):
    global mydb
    global mycursor
    u1=session['id']
    s=f'select name from category where u_id={u1}'
    mycursor.execute(s)
    l=mycursor.fetchall()
    str1=''
    for i in l:
        i=i[0]
        str1=str1+f'<option value={i}>{i}</option>'
    # p=session["p"]
    # if p=='valid':
    #     session["p"]=""
    #     return render_template('add.html',l=str1,u="Successfully Added")
    try:
        if len(l)==0:
            return render_template('category.html',u='First Add Category To AddList')
        elif session['u']==1:
            session['u']=0
            return render_template('add.html',l=str1,u="Successfully Added")
        elif pp==1:
            return render_template('add.html',l=str1,u="Please Provide All Fields")

    except:
           return render_template('add.html',l=str1)
    session['u']=0
    return render_template('add.html',l=str1)


@app.route('/addf',methods=['POST','GET'])
def addf():
        d=request.form 
        global mycursor
        global mydb
        # session["p"]='valid'
        now = datetime.now()
        f_d = now.strftime('%Y-%m-%d %H:%M:%S')
        var=d['dt']
        if  len(d['dt'])<1 or len(d['t'])<1 or len(d['d'])<1:
                  u1=session['id']
                  s=f'select name from category where u_id={u1}'
                  mycursor.execute(s)
                  l=mycursor.fetchall()
                  str1=''
                  for i in l:
                        i=i[0]
                        str1=str1+f'<option value={i}>{i}</option>'
                  return render_template('add.html',l=str1,u="Please Fill All Fields")
                  
        var=var.split('T')
        var=" ".join(var)
        var=var+':00'
        print(var)
        # n1 = datetime.date(f_d)
        # n2 = datetime.date(var)
        # print(n1,n2)
        # if n2>n1:
        #     print("checked",var,f_d)
        #     return redirect(url_for('add'),pp=1)
        s="insert into todo(title,t_description,created_at,updated_at,deadline,u_id) values(%s,%s,%s,%s,%s,%s)"
        v=[d['t'],d['d'],f_d,f_d,var,session['id']]

        mycursor.execute(s,v)
        mydb.commit()
        flash("succesfully Added")
        session['u']=1
        return redirect(url_for('add'))

@app.route('/delete1f/<t_id>',methods=['POST','GET'])
def delete1f(t_id):
        print(t_id)
        global mydb
        global mycursor
        s=f'update todo set status="r" where t_id={t_id}'
        mycursor.execute(s)
        mydb.commit()
        return redirect(url_for('view1f'))

        # global mydb
        # global mycursor
        # u1=session["id"]
        # u2=dict(request.form)
        # print(u2)
        # u2=list(u2.values())[0]
        # s="delete from todo where u_id=%s and title=%s"
        # mycursor.execute(s,[u1,u2])
        # mydb.commit()
        # return redirect(url_for('home8'))

@app.route('/delete2f/<t_id>',methods=['POST','GET'])
def delete2f(t_id):
        print(t_id)
        global mydb
        global mycursor
        s=f'update todo set status="c" where t_id={t_id}'
        mycursor.execute(s)
        mydb.commit()
        return redirect(url_for('view1f'))

@app.route('/delete3f/<t_id>',methods=['POST','GET'])
def delete3f(t_id):
        print(t_id)
        global mydb
        global mycursor
        s=f'update todo set status="ic" where t_id={t_id}'
        mycursor.execute(s)
        mydb.commit()
        return redirect(url_for('view1f'))


@app.route('/cat',methods=['POST','GET'])
def cat():
    return render_template('category.html',u2=session['user']) 

@app.route('/catf',methods=['POST','GET'])
def catf():
        d=request.form 
        global mycursor
        global mydb
        now = datetime.now()
        f_d = now.strftime('%Y-%m-%d %H:%M:%S')
        s="insert into category(name,created_at,updated_at,u_id) values(%s,%s,%s,%s)"
        v=[d['c'],f_d,f_d,session['id']]
        mycursor.execute(s,v)
        mydb.commit()

        return render_template('category.html',u2=session['user'],u="Succesfully Added") 




app.run(debug=True)