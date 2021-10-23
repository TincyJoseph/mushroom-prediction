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
    
    value=label.fit_transform(to_predict)
    value=np.reshape(value,(-1,21))
    output=model.predict(value)
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

