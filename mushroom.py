from flask import Flask,render_template,request,redirect
from flask_mysqldb import MySQL
import pickle
import numpy as np

app=Flask(__name__)
model=pickle.load(open('model.pkl','rb'))

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='tin85may1#'
app.config['MYSQL_DB']='mushroom'
#conn = sqlite3.connect('user_data.db') 
mysql=MySQL(app)
@app.route('/') 
def home():
    return render_template("home.html")
@app.route('/Types')
def types():
    return render_template("types.html")
@app.route('/Health_tip')
def health_tip():
    return render_template("health_tip.html")
@app.route('/Quality_check',methods=['GET', 'POST'])
def quality_check():
    if request.method == 'POST':
        a = request.form['cap-shape']
        b = request.form['cap-surface']
        c = request.form['cap-color']
        d = request.form['bruises']
        e= request.form['odor']
        f=request.form['gill-attachment']
        g=request.form['gill-spacing']
        h=request.form['gill-size']
        i=request.form['gill-color']
        j=request.form['stalk-shape']
        k=request.form['stalk-surface-above-ring']
        l=request.form['stalk-surface-below-ring']
        m=request.form['stalk-color-above-ring']
        n=request.form['stalk-color-below-ring']
        o=request.form['veil-type']
        p=request.form['veil-color']
        q=request.form['ring-number']
        r=request.form['ring-type']
        s=request.form['spore-print-color']
        t=request.form['population']
        u=request.form['habitat']
        conn=mysql.connection.cursor()
        #conn.execute("CREATE TABLE mushroomtable(id int NOT NULL AUTO_INCREMENT,cap_shape TEXT NOT NULL,cap_surface TEXT NOT NULL,cap_color TEXT NOT NULL,bruises TEXT NOT NULL,odor TEXT NOT NULL,gill_attachment TEXT NOT NULL,gill_spacing TEXT NOT NULL,gill_size TEXT NOT NULL,gill_color TEXT NOT NULL,stalk_shape TEXT NOT NULL,stalk_surf_a TEXT NOT NULL,stalk_surf_b TEXT NOT NULL,stalk_color_a TEXT NOT NULL,stalk_color_b  TEXT NOT NULL,veil_type TEXT NOT NULL,veil_color TEXT NOT NULL,ring_number TEXT NOT NULL,ring_type TEXT NOT NULL,spore_print_color TEXT NOT NULL,population TEXT NOT NULL,habitat TEXT NOT NULL,PRIMARY KEY(id));")
        conn.execute("INSERT INTO mushroomtable(cap_shape,cap_surface,cap_color,bruises,odor,gill_attachment,gill_spacing,gill_size, gill_color,stalk_shape,stalk_surf_a,stalk_surf_b,stalk_color_a,stalk_color_b,veil_type,veil_color,ring_number,ring_type,spore_print_color,population,habitat) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u))
        mysql.connection.commit()
        conn.close()
        return redirect('/result')
    return render_template("quality_check.html")
@app.route('/values')
def values():
    conn=mysql.connection.cursor()
    conn.execute("SELECT * FROM mushroomtable;")
    details=conn.fetchall()
    return render_template('values.html',details=details)
@app.route('/result')
def result():
    conn=mysql.connection.cursor()
    conn.execute("SELECT cap_shape,cap_surface,cap_color,bruises,odor,gill_attachment,gill_spacing,gill_size, gill_color,stalk_shape,stalk_surf_a,stalk_surf_b,stalk_color_a,stalk_color_b,veil_type,veil_color,ring_number,ring_type,spore_print_color,population,habitat FROM mushroomtable WHERE id=(SELECT MAX(id) FROM mushroomtable);")
    tup1=conn.fetchall()
    print(tup1)
    to_predict=[]
    for t in tup1:
        for i in t:
            to_predict.append(i)
    print(to_predict)
    capshape=[]
    if to_predict[0]=='x':
        capshape=[1,0,0,0,0,0]
    elif to_predict[0]=='f':
        capshape=[0,1,0,0,0,0]
    elif to_predict[0]=='k':
        capshape=[0,0,1,0,0,0]
    elif to_predict[0]=='b':
         capshape=[0,0,0,1,0,0]
    elif to_predict[0]=='s':
        capshape=[0,0,0,0,1,0]
    else:
        capshape=[0,0,0,0,0,1]
    capsurface=[]
    if to_predict[1]=='y':
        capsurface=[1,0,0,0]
    elif to_predict[1]=='s':
        capsurface=[0,1,0,0]
    elif to_predict[1]=='f':
        capsurface=[0,0,1,0]
    else:
        capsurface=[0,0,0,1]
    capcolor=[]
    if to_predict[2]=='n':
        capcolor=[1,0,0,0,0,0,0,0,0,0]
    elif to_predict[2]=='g':
        capcolor=[0,1,0,0,0,0,0,0,0,0]
    elif to_predict[2]=='e':
        capcolor=[0,0,1,0,0,0,0,0,0,0]
    elif to_predict[2]=='y':
        capcolor=[0,0,0,1,0,0,0,0,0,0]
    elif to_predict[2]=='w':
        capcolor=[0,0,0,0,1,0,0,0,0,0]
    elif to_predict[2]=='b':
        capcolor=[0,0,0,0,0,1,0,0,0,0]
    elif to_predict[2]=='p':
        capcolor=[0,0,0,0,0,0,1,0,0,0]
    elif to_predict[2]=='c':
        capcolor=[0,0,0,0,0,0,0,1,0,0]
    elif to_predict[2]=='u':
        capcolor=[0,0,0,0,0,0,0,0,1,0]
    else:
        capcolor=[0,0,0,0,0,0,0,0,0,1]
    bruises=[]
    if to_predict[3]=='f':
        bruises=[1,0]
    else:
        bruises=[0,1]
    odor=[]
    if to_predict[4]=='n':
        odor=[1,0,0,0,0,0,0,0,0]
    elif to_predict[4]=='f':
        odor=[0,1,0,0,0,0,0,0,0]
    elif to_predict[4]=='s':
        odor=[0,0,1,0,0,0,0,0,0]
    elif to_predict[4]=='y':
        odor=[0,0,0,1,0,0,0,0,0]
    elif to_predict[4]=='l':
        odor=[0,0,0,0,1,0,0,0,0]
    elif to_predict[4]=='a':
        odor=[0,0,0,0,0,1,0,0,0]
    elif to_predict[4]=='p':
        odor=[0,0,0,0,0,0,1,0,0]
    elif to_predict[4]=='c':
        odor=[0,0,0,0,0,0,0,1,0]
    else:
        odor=[0,0,0,0,0,0,0,0,1]
    gill_attach=[]
    if to_predict[5]=='f':
        gill_attach=[1,0]
    else:
        gill_attach=[0,1]
    gill_space=[]
    if to_predict[6]=='c':
        gill_space=[1,0]
    else:
        gill_space=[0,1]
    gill_size=[]
    if to_predict[7]=='b':
         gill_size=[1,0]
    else:
        gill_size=[0,1]
    gill_color=[]
    if to_predict[8]=='b':
        gill_color=[1,0,0,0,0,0,0,0,0,0,0,0]
    elif to_predict[8]=='p':
        gill_color=[0,1,0,0,0,0,0,0,0,0,0,0]
    elif to_predict[8]=='w':
        gill_color=[0,0,1,0,0,0,0,0,0,0,0,0]
    elif to_predict[8]=='n':
        gill_color=[0,0,0,1,0,0,0,0,0,0,0,0]
    elif to_predict[8]=='g':
        gill_color=[0,0,0,0,1,0,0,0,0,0,0,0]
    elif to_predict[8]=='h':
        gill_color=[0,0,0,0,0,1,0,0,0,0,0,0]
    elif to_predict[8]=='u':
        gill_color=[0,0,0,0,0,0,1,0,0,0,0,0]
    elif to_predict[8]=='k':
        gill_color=[0,0,0,0,0,0,0,1,0,0,0,0]
    elif to_predict[8]=='e':
        gill_color=[0,0,0,0,0,0,0,0,1,0,0,0]
    elif to_predict[8]=='y':
        gill_color=[0,0,0,0,0,0,0,0,0,1,0,0]
    elif to_predict[8]=='o':
        gill_color=[0,0,0,0,0,0,0,0,0,0,1,0]
    else:
        gill_color=[0,0,0,0,0,0,0,0,0,0,0,1]
    stalkshape=[]
    if to_predict[9]=='t':
        stalkshape=[1,0]
    else:
        stalkshape=[0,1]
    stalksurfa=[]
    if to_predict[10]=='s':
        stalksurfa=[1,0,0,0]
    elif to_predict[10]=='k':
        stalksurfa=[0,1,0,0]
    elif to_predict[10]=='f':
        stalksurfa=[0,0,1,0]
    else:
        stalksurfa=[0,0,0,1]
    stalksurfb=[]
    if to_predict[11]=='s':
        stalksurfb=[1,0,0,0]
    elif to_predict[11]=='k':
        stalksurfb=[0,1,0,0]
    elif to_predict[11 ]=='f':
        stalksurfb=[0,0,1,0]
    else:
        stalksurfb=[0,0,0,1]
    colora=[]
    if to_predict[12]=='w':
        colora=[1,0,0,0,0,0,0,0,0]
    elif to_predict[12]=='p':
        colora=[0,1,0,0,0,0,0,0,0]
    elif to_predict[12]=='g':
        colora=[0,0,1,0,0,0,0,0,0]
    elif to_predict[12]=='n':
        colora=[0,0,0,1,0,0,0,0,0]
    elif to_predict[12]=='b':
        colora=[0,0,0,0,1,0,0,0,0]
    elif to_predict[12]=='o':
        colora=[0,0,0,0,0,1,0,0,0]
    elif to_predict[12]=='e':
        colora=[0,0,0,0,0,0,1,0,0]
    elif to_predict[12]=='c':
        colora=[1,0,0,0,0,0,0,1,0]
    else:
        colora=[0,0,0,0,0,0,0,0,1]
    
    colorb=[]
    if to_predict[13]=='w':
        colorb=[1,0,0,0,0,0,0,0,0]
    elif to_predict[13]=='p':
        colorb=[0,1,0,0,0,0,0,0,0]
    elif to_predict[13]=='g':
        colorb=[0,0,1,0,0,0,0,0,0]
    elif to_predict[13]=='n':
        colorb=[0,0,0,1,0,0,0,0,0]
    elif to_predict[13]=='b':
        colorb=[0,0,0,0,1,0,0,0,0]
    elif to_predict[13]=='o':
        colorb=[0,0,0,0,0,1,0,0,0]
    elif to_predict[13]=='e':
        colorb=[0,0,0,0,0,0,1,0,0]
    elif to_predict[13]=='c':
        colorb=[1,0,0,0,0,0,0,1,0]
    else:
        colorb=[0,0,0,0,0,0,0,0,1]
    veil_type=[]
    if to_predict[14]=='t':
        veil_type=[1]
    else:veil_type=[0]
    veilcolor=[]
    if to_predict[15]=='w':
        veilcolor=[1,0,0,0]
    elif to_predict[15]=='o':
        veilcolor=[0,1,0,0]
    elif to_predict[15]=='n':
        veilcolor=[0,0,1,0]
    else:veilcolor=[0,0,0,1]
    ringno=[]
    if to_predict[16]=='o':
        ringno=[1,0,0]
    elif to_predict[16]=='t':
        ringno=[0,1,0]
    else:ringno=[0,0,1]
    ringtype=[]
    if to_predict[17]=='p':
        ringtype=[1,0,0,0,0]
    elif to_predict[17]=='e':
        ringtype=[0,1,0,0,0]
    elif to_predict[17]=='l':
        ringtype=[0,0,1,0,0]
    elif to_predict[17]=='f':
        ringtype=[0,0,0,1,0]
    else:ringtype=[0,0,0,0,1]
        
    spore=[]
    if to_predict[18]=='w':
        spore=[1,0,0,0,0,0,0,0,0]
    elif to_predict[18]=='n':
        spore=[0,1,0,0,0,0,0,0,0]
    elif to_predict[18]=='k':
        spore=[0,0,1,0,0,0,0,0,0]
    elif to_predict[18]=='h':
        spore=[0,0,0,1,0,0,0,0,0]
    elif to_predict[18]=='r':
        spore=[0,0,0,0,1,0,0,0,0]
    elif to_predict[18]=='o':
        spore=[0,0,0,0,0,1,0,0,0]
    elif to_predict[18]=='b':
        spore=[0,0,0,0,0,0,1,0,0]
    elif to_predict[18]=='y':
        spore=[0,0,0,0,0,0,0,1,0]
    else:spore=[0,0,0,0,0,0,0,0,1]
        
    population=[]
    if to_predict[19]=='v':
        population=[1,0,0,0,0,0]
    elif to_predict[19]=='y':
        population=[0,1,0,0,0,0]
    elif to_predict[19]=='s':
        population=[0,0,1,0,0,0]
    elif to_predict[19]=='n':
        population=[0,0,0,1,0,0]
    elif to_predict[19]=='a':
        population=[0,0,0,0,1,0]
    else:population=[0,0,0,0,0,1]
        
    habitat=[]
    if to_predict[20]=='d':
        habitat=[1,0,0,0,0,0,0]
    elif to_predict[20]=='g':
        habitat=[0,1,0,0,0,0,0]
    elif to_predict[20]=='p':
        habitat=[0,0,1,0,0,0,0]
    elif to_predict[20]=='l':
        habitat=[0,0,0,1,0,0,0]
    elif to_predict[20]=='u':
        habitat=[0,0,0,0,1,0,0]
    elif to_predict[20]=='m':
        habitat=[0,0,0,0,0,1,0]
    else:habitat=[0,0,0,0,0,0,1]
    print(capshape)
    print(capsurface)
    print("datas are copied to list")    
    capshape.extend(capsurface)
    print(capshape)
    capshape.extend(capcolor)
    capshape.extend(bruises)
    capshape.extend(odor)
    capshape.extend(gill_attach)
    capshape.extend(gill_space)
    capshape.extend(gill_size)
    capshape.extend(gill_color)
    capshape.extend(stalkshape)
    capshape.extend(stalksurfa)
    capshape.extend(stalksurfb)
    capshape.extend(colora)
    capshape.extend(colorb)
    capshape.extend(veil_type)
    capshape.extend(veilcolor)
    capshape.extend(ringno)
    capshape.extend(ringtype)
    capshape.extend(spore)
    capshape.extend(population)
    capshape.extend(habitat)
    print(capshape)
    array=np.reshape(capshape,(-1,112))
    output=model.predict(array)
    output=output.item()
    if output=='e':
        actual='edible'
    else:actual='poisoness'

    return render_template('result.html',result=actual)
    
@app.route('/Visualization')
def visualization():
    return render_template("visualization.html")


if __name__=="__main__":
    app.run(port=8000)

