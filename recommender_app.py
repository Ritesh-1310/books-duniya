# importing neccessary libraries
import os
import pandas as pd
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#reading csv file, taking user input and listing the tags
df = pd.read_csv("unique.csv")
def combined_features(row):
    return str(row['Title'])+" "+str(row['Description'])+" "+str(row['Author'])
df["combined_features"] = df.apply(combined_features, axis =1)

# flask database
app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
# postgres://books_dunia_user:LLFBfpdR8ytXssimRQ011Akocxap3tmw@dpg-cgop7fou9tun42q6ske0-a.oregon-postgres.render.com/books_dunia

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=True)
    author = db.Column(db.String(200), nullable=True)
    price = db.Column(db.String(50), nullable=True)
    rating = db.Column(db.String(20), nullable=True)
    image = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


#listing the name of the books
title_arr=list(df["Title"])
price_arr=list(df["Price"])
rating_arr=list(df["Rating"])
author_arr=list(df["Author"])
url_arr=list(df["LINK"])
comb_arr=list(df["combined_features"])


#implementing the Jaccard similarity
def Jaccard_Similarity(doc1, doc2): 
    
    # List the unique words in a document
    words_doc1 = set(doc1.lower().split()) 
    words_doc2 = set(doc2.lower().split())
    
    # Find the intersection of words list of doc1 & doc2
    intersection = words_doc1.intersection(words_doc2)

    # Find the union of words list of doc1 & doc2
    union = words_doc1.union(words_doc2)
        
    # Calculate Jaccard similarity score 
    # using length of intersection set divided by length of union set
    return float(len(intersection)) / len(union)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        # delete whole table/db
        db.session.query(Todo).delete()
        db.session.commit()

        # user input
        title = request.form['title']
        s = title
        # s=input("Enter your book description : ")
        s=s.lower()

        #removing the unneccesary words
        s=s+' ' 
        arr=['books','book','best','recommend','for','in','market','of','seller','by','buy','author','written','show','other','the','me','all','what','are','world','get','rating']
        x=""
        y=""
        for i in range(0,len(s)):
            if(s[i]!=' '):
                x=x+s[i]
            else:
                if(arr.count(x)==0):
                    y=y+x+' '
                x=""
        s=y
        df

        # calling the Jaccard_Similarity for calculating the similarity
        similar=[]
        add=0 # variable to check whether atleast one recommendation is there or not
        for item in comb_arr:
            similar.append(Jaccard_Similarity(item,s))
            jc=Jaccard_Similarity(item,s)
            add=add+jc


        #storing the deatils of each book in an array
        reco=[]
        for i in range(0,len(title_arr)):
            #print(title_arr[i]+"  "+str(similar[i]))
            pair=((similar[i],title_arr[i],price_arr[i],author_arr[i],rating_arr[i],url_arr[i]))
            reco.append(pair)

        #printing the recommended books
        l=[]
        ans=[]
        reco.sort(reverse=True)
        count=0
        # if add==0:
        #     print("No relevant recommendation !!")
        if add!=0:
            # print("Your search matched with the following books ")
            for item in reco:
                if(item[0]>0):
                    l=[]
                    l.append(item[1])
                    l.append(item[3])
                    l.append(item[2])
                    l.append(item[4])
                    l.append(item[5])
                    ans.append(l)
                    
        ans.sort(key=lambda x:x[3],reverse=True)
        # print("Title  Author  Price   Rating  Url")
        i=1
        for item in ans:
            # for item1 in item:
                # print(item1, end=",")
            todo = Todo(title=item[0], author=item[1], price=item[2], rating=item[3], image=item[4])
            db.session.add(todo)
            db.session.commit()
                # i=i+1
            # print(end="\n")

    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)



@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
