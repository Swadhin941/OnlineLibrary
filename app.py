from sklearn.metrics.pairwise import cosine_similarity
from importlib.resources import path
import os
from flask import Flask, jsonify, flash, request, render_template, send_file, session, redirect, url_for
from flask_mysqldb import MySQL
import stripe
import pandas as pd
import mysql.connector
import numpy as np
app = Flask(__name__)
app.secret_key = 'your secret key'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'log'
app.config['MYSQL_HOST'] = 'localhost'
Mysql = MySQL(app)
uploadpath = 'C:/xampp/htdocs/Final_project/'

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="log"
)




@app.route("/")
def home():
    return render_template('Home.html')

# Login Section


@app.route("/Login")
def Login():
    return render_template('Login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        email = request.args.get('email')
        password = request.args.get('password')
        val= (email, password)
        cursor = Mysql.connection.cursor()
        cursor.execute(''' SELECT * FROM accounts WHERE email = %s AND password = %s ''', (val))
        res = cursor.fetchall()
        cursor.close()
        if res:
            session['userid']= res[0][4]
            session['username']= res[0][1]
            return jsonify({'status': 201})
        else:
            return jsonify({'status': 402})


# Register Section
@app.route("/Register")
def Register():
    return render_template('Register.html')


#logout Section
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    location = request.args.get('location')
    session.clear()
    return jsonify({'location': location})

# All Book Page
@app.route('/allBook')
def allBook():
    cursor = Mysql.connection.cursor()
    cursor.execute("SELECT * FROM books")
    res = cursor.fetchall()
    cursor.close()
    return render_template('AllBook.html', book=res)

@app.route('/bookdetails')
def bookdetails():
    isbn = request.args.get('isbn')
    if session.get('userid') is None:
        return redirect(url_for('Login'))
    else:
        if isbn is None:
            isbn = session['isbn']
        cursor = Mysql.connection.cursor()
        val = (isbn,)
        cursor.execute("SELECT * FROM books WHERE isbn = %s", (val))
        res = cursor.fetchall()
        cursor.close()
        print(res[0])
        return render_template('BookDetails.html', book=res[0])
    

#rating Submission
@app.route('/rating')
def rating():
    isbn = request.args.get('isbn')
    rating = request.args.get('rating')
    userid = session['userid']
    rating= int (rating)
    cursor = Mysql.connection.cursor()
    cursor.execute('''SELECT * FROM rating WHERE userid = %s AND isbn = %s''',((userid,isbn,)))
    res= cursor.fetchall()
    if len(res)== 1:
        cursor.execute('''UPDATE rating SET rating = %s WHERE isbn = %s AND userid = %s''',((rating,isbn, userid )))
        Mysql.connection.commit()
    else:
        cursor.execute('''INSERT INTO rating( `userid`, `ISBN`, `rating`) VALUES (%s,%s,%s)''',((userid,isbn,rating)))
        Mysql.connection.commit()
    return jsonify({'okay':'done'})

#Customer Average Rating
@app.route('/customer')
def customer():
    isbn= request.args.get('isbn')
    print("Customer Average Rating")
    print(isbn)
    cursor= Mysql.connection.cursor()
    cursor.execute('''SELECT * FROM rating WHERE isbn=%s''',((isbn,)))
    res= cursor.fetchall()
    total =0
    for i in range(len(res)):
        total+=int(res[i][3])
    total= total/len(res)
    total= round(total/2)
    return jsonify({'rat': total})



#Blog posts
@app.route('/Blog')
def Blog():

    return render_template('Blog.html')

@app.route('/blog',methods= ['GET', 'POST'])
def BlogPost():
    cursor = Mysql.connection.cursor()
    cursor.execute("SELECT * FROM blog")
    result = cursor.fetchall()
    blogId=[]
    blogTitle=[]
    blogContent=[]
    for i in range(len(result)):
        blogId.append(result[i][0])
        blogTitle.append(result[i][1])
        blogContent.append(result[i][2])
    return jsonify({'blogId':blogId, 'blogTitle':blogTitle, 'blogContent':blogContent})

@app.route('/blogdetails')
def blogdetails():
    id = request.args.get('id')
    cursor = Mysql.connection.cursor()
    cursor.execute("SELECT * FROM blog WHERE id = %s", (()))
    res = cursor.fetchone()
    return render_template('BlogDetails.html', blog=res)



#Faq page
@app.route('/faq')
def faq():
    cursor = Mysql.connection.cursor()
    cursor.execute("SELECT * FROM faq")
    res= cursor.fetchall()
    return render_template('FAQ.html', faq= res)

#All the Function for cart system
@app.route('/addtocart', methods=['GET', 'POST'])
def addtocart():
    bookname = request.args.get('bookname')
    authorname = request.args.get('authorname')
    isbn = request.args.get('isbn')
    price = request.args.get('price')
    username = request.args.get('username')
    userid = request.args.get('userid')
    image = request.args.get('image')
    quantity = 1
    cursor = Mysql.connection.cursor()
    cursor.execute(
        '''SELECT * FROM quantity WHERE isbn= %s AND userid= %s''', ((isbn, userid,)))
    res = cursor.fetchall()
    if len(res) > 0:
        return jsonify({'message': 'Already added to the cart'})
    else:
        cursor.execute('''INSERT INTO quantity(userid, username, bookname, authorname, isbn, price, image, quantity) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)''', ((
            userid, username, bookname, authorname, isbn, price, image, quantity,)))
        Mysql.connection.commit()
        return jsonify({'message': "Successfully added to the cart"})


@app.route('/cart')
def cart():
    return render_template('Cart.html')


@app.route('/allcartbook')
def allcartbook():
    userid = request.args.get('userid')
    cursor = Mysql.connection.cursor()
    cursor.execute('''SELECT * FROM quantity WHERE userid = %s''', ((userid,)))
    res = cursor.fetchall()
    cartbook = []
    content = {}
    for i in range(len(res)):
        content = {'userid': res[i][1], 'username': res[i][2], 'bookname': res[i][3], 'authorname': res[i][4], 'isbn': res[i][5], 'price': res[i][6], 'image': res[i][7], 'quantity': res[i][8]}
        cartbook.append(content)
    return jsonify({'cartbook': cartbook})


@app.route('/incrementcart')
def incrementcart():
    userid = session['userid']
    quantity = request.args.get('quantity')
    isbn = request.args.get('isbn')
    cursor = Mysql.connection.cursor()
    cursor.execute('''UPDATE quantity SET quantity= %s WHERE isbn = %s AND userid = %s''', ((
        quantity, isbn, userid)))
    Mysql.connection.commit()
    cursor.execute('''SELECT quantity FROM quantity where isbn = %s AND userid = %s''',((isbn,userid,)))
    res = cursor.fetchall()
    return jsonify({'okay': res[0]})


@app.route('/decrementcart')
def decrementcart():
    userid = session['userid']
    quantity = request.args.get('quantity')
    isbn = request.args.get('isbn')
    cursor = Mysql.connection.cursor()
    cursor.execute('''UPDATE quantity SET quantity= %s WHERE isbn = %s AND userid = %s''', ((quantity, isbn, userid)))
    Mysql.connection.commit()
    return jsonify({'okay': 'done'})


@app.route('/deletecart')
def remove():
    userid = session['userid']
    isbn = request.args.get('isbn')
    cursor = Mysql.connection.cursor()
    cursor.execute('''DELETE FROM `quantity` WHERE userid= %s AND isbn= %s''',((userid,isbn)))
    Mysql.connection.commit()
    return jsonify({'delete':'success'})


#For User DashBoard
@app.route('/userdashBoard')
def userdashBoard():
    return render_template('Dashboard.html')

@app.route('/dashboard')
def dashboard():
    userid = session['userid']
    cursor = Mysql.connection.cursor()
    cursor.execute(''' SELECT * FROM downloadtest WHERE userid= %s ''',((userid,)))
    res = cursor.fetchall()
    category= []
    downloaded=[]
    for i in range(len(res)):
        category.append(res[i][2])
        downloaded.append(res[i][3])
    cursor.execute('''SELECT * FROM rating WHERE userid= %s''',((userid,)))
    result = cursor.fetchall()
    rating= []
    isbn=[]
    print(result)
    for i in range(len(result)):
        rating.append(result[i][3])
        isbn.append(result[i][2])
    cursor.execute('''SELECT bookname, isbn FROM books''')
    res = cursor.fetchall()
    bookname= []
    isbn1=[]
    for i in range(len(res)):
        bookname.append(res[i][0])
        isbn1.append(res[i][1])
    avgRating=[]
    for i in range(len(isbn1)):
        cursor.execute('''SELECT AVG(rating) FROM rating WHERE isbn= %s''',((isbn1[i],)))
        res = cursor.fetchall()
        if res[0][0] is None:
            avgRating.append(0)
        else:
            avgRating.append(float(res[0][0]))
    return jsonify({'category': category, 'downloaded': downloaded, 'rating': rating, 'bookname': bookname})

#WishList check
@app.route('/wishListCheck')
def wishListCheck():
    isbn = request.args.get('isbn')
    userid = session['userid']
    cursor = Mysql.connection.cursor()
    cursor.execute('''SELECT * FROM wishlist WHERE isbn= %s AND userid= %s''',((isbn,userid,)))
    res = cursor.fetchall()
    print(res)
    if len(res) > 0:
        return jsonify({'status': 200})
    else:
        return jsonify({'status': 404})

@app.route('/addWish')
def addWish():
    isbn= request.args.get('isbn')
    userid = session['userid']
    bookname= request.args.get('bookname')
    image= request.args.get('image')
    cursor = Mysql.connection.cursor()
    cursor.execute(''' INSERT INTO wishlist(userid, isbn, bookname, image) VALUES (%s,%s,%s,%s)''',((userid,isbn,bookname,image)))
    Mysql.connection.commit()
    return jsonify({'status': 200})  

@app.route('/wish')
def wish():
    userid = session['userid']
    cursor = Mysql.connection.cursor()
    cursor.execute('''SELECT * FROM wishlist WHERE userid= %s''',((userid,)))
    res = cursor.fetchall()
    isbn= []
    bookname= []
    image= []
    for i in range(len(res)):
        isbn.append(res[i][2])
        bookname.append(res[i][3])
        image.append(res[i][4])
    return render_template('Wishlist.html', isbn = isbn, bookname = bookname, image = image)
@app.route('/removeWish')
def removeWish():
    isbn = request.args.get('isbn')
    userid = session['userid']
    cursor = Mysql.connection.cursor()
    cursor.execute('''DELETE FROM `wishlist` WHERE userid= %s AND isbn= %s''',((userid,isbn)))
    Mysql.connection.commit()
    return redirect(url_for('wish'))

#Download Book
@app.route('/download')
def download():
    pdf = request.args.get('pdf')
    isbn = request.args.get('isbn')
    category = request.args.get('category')
    cursor = Mysql.connection.cursor()
    userid = session['userid']
    cursor.execute(''' SELECT * FROM download WHERE userid = %s AND isbn = %s ''', (userid, isbn))
    res = cursor.fetchall()
    # print(res)
    if(len(res)== 0):
        cursor.execute(''' INSERT INTO download (userid,isbn,category) VALUES(%s,%s,%s) ''',(userid,isbn,category))
        Mysql.connection.commit()
        cursor.execute(''' SELECT * FROM downloadtest WHERE userid = %s AND category = %s ''', (userid, category))
        result = cursor.fetchall()
        # print(result)
        if len(result) == 0:
            cursor.execute(''' INSERT INTO downloadtest ( userid, category, value) VALUES (%s,%s,%s) ''',(userid,category,1))
            Mysql.connection.commit()
        if len(result) >= 1:
            cursor.execute(''' UPDATE downloadtest SET value = %s WHERE userid = %s AND category = %s ''',(int(result[0][3])+1, userid,category))
            Mysql.connection.commit()

    path = uploadpath+pdf
    return send_file(path, as_attachment=True)


#Top Rated Books
@app.route('/topBook',methods=['GET', 'POST'])
def topBook():
    cursor = db.cursor()
    sql= '''SELECT * FROM books'''
    cursor.execute(sql)
    books= pd.DataFrame(cursor.fetchall())
    books.rename(columns={0:'Id',1:"Book-Title",2:'ISBN',3:'Category',4:"Book-Author",5:"Image",6:"Description",7:"FileName",8:"Price"},inplace=True)
    cursor.execute('''SELECT * FROM rating''')
    ratings= pd.DataFrame(cursor.fetchall())
    ratings.rename(columns={0:'Id',1:"User-ID",2:'ISBN',3:'Book-Rating'},inplace=True)
    pt = ratings.pivot_table(index= 'User-ID', columns=["ISBN"],values='Book-Rating')
    pt.fillna(0,inplace=True)
    book_score={}
    for i in pt.columns:
        one=0
        two=0
        three=0
        four=0
        five=0
        pre_ratings= pt[i]
        for j in range(len(pt.index)):
            pre_val= pre_ratings[pt.index[j]] #if ratings are greater then 5, divide by 2 here
            if pre_val == 1:
                one+=1
            elif pre_val == 2:
                two+=1
            elif pre_val == 3:
                three+=1
            elif pre_val == 4:
                four+=1
            elif pre_val == 5:
                five+=1
        book_score[i]= ((one*1)+(two*2)+(three*3)+(four*4)+(five*5))/(one+two+three+four+five)
    book_score = pd.DataFrame(book_score.items(), columns=['ISBN', "Frequency"])
    book_score= book_score.sort_values(by='Frequency', ascending=False)
    isbn=[]
    for i in book_score['ISBN']:
        isbn.append(i)
    bookName=[]
    bookImage=[]
    bookPrice=[]
    cur= Mysql.connection.cursor()
    for i in isbn:
        cur.execute(''' SELECT bookname, price, image FROM books WHERE isbn = %s''', ((i,)))
        res= cur.fetchall()
        bookName.append(res[0][0])
        bookImage.append(res[0][2])
        bookPrice.append(res[0][1])
    return jsonify({'books': bookName, 'isbn': isbn, 'image': bookImage, 'price': bookPrice})

#Recommended Books
@app.route('/recommend',methods=['GET','POST'])
def recommed():
    if session['userid'] is None:
        return jsonify({'len': 0})
    else:
        cur= Mysql.connection.cursor()
        cur.execute('''SELECT * FROM download WHERE userid = %s''',((session['userid'],)))
        result= cur.fetchall()
        if(len(result) < 3):
            return jsonify({'len':len(res)})
        else:
            cursor = db.cursor()
            sql= '''SELECT * FROM books'''
            cursor.execute(sql)
            books= pd.DataFrame(cursor.fetchall())
            books.rename(columns={0:'Id',1:"Book-Title",2:'ISBN',3:'Category',4:"Book-Author",5:"Image",6:"Description",7:"FileName",8:"Price"},inplace=True)
            cursor.execute('''SELECT * FROM downloadtest''')
            ratings= pd.DataFrame(cursor.fetchall())
            ratings.rename(columns={0:'Id',1:"User-ID",2:'Category',3:'Category-Values'},inplace=True)
            #Collaborative Filtering starts from here
            book_with_rating = ratings.merge(books, on='Category')
            pt = book_with_rating.pivot_table(index='User-ID', columns='Category', values='Category-Values')
            pt.fillna(0, inplace=True)
            similarity_distance = cosine_similarity(pt)
            s= np.where(pt.index == session['userid'] )[0][0]
            s1=sorted (list( enumerate( similarity_distance[s])), key= lambda x: x[1], reverse=True)[1:10]
            li=[]
            li1=[]
            for i in s1:
                li1.append(i[1])
                li.append(pt.index[i[0]])
            dst = pt[pt.index.isin(li)]
            book_score={}
            for i in dst.columns:
                books_val = dst[i]
                total=0
                count=0
                for j in range(len(dst.index)):
                    total+=books_val[dst.index[j]]* li1[j]
                    count+=1
                book_score[i]= total/count
            book_score = pd.DataFrame(book_score.items(), columns=["Category_Name", "Total Score of Category"])
            book_score = book_score.sort_values(by='Total Score of Category', ascending=False)
            category_name =[]
            print(book_score)
            for i in book_score['Category_Name']:
                category_name.append(i)
            isbn=[]
            cur = Mysql.connection.cursor()
            for i in range(len(li)):
                for j in range(len(category_name)):
                    cur.execute(''' SELECT isbn FROM download WHERE userid = %s AND category = %s''', ((li[i], category_name[j],)))
                    res = cur.fetchall()
                    if len(res)== 0:
                        continue
                    else:
                        isbn.append(res[0][0]) 
            isbnSet= set(isbn)
            isbn = list(isbnSet)
            # print(isbn)
            cur.execute(''' SELECT isbn FROM download WHERE userid = %s ''', ((session['userid'],)))
            res = cur.fetchall()
            userIsbn= []
            for i in range(len(res)):
                userIsbn.append(res[i][0])
            # print(userIsbn)
            recommendedList= [ i for i in isbn if i not in userIsbn]
            # print(recommendedList)
            bookName=[]
            bookPrice=[]
            bookImage=[]
            for i in recommendedList:
                cur.execute(''' SELECT bookname, price, image FROM books WHERE isbn = %s''', ((i,)))
                res = cur.fetchall()
                bookName.append(res[0][0])
                bookPrice.append(res[0][1])
                bookImage.append(res[0][2])
            print(bookName, bookPrice, bookImage)
            return jsonify({'books': bookName, 'price': bookPrice, 'image': bookImage,'isbn': recommendedList,'len': len(result)})





@app.route('/selectedbook',methods=['GET', 'POST'])
def selectedbook():
    isbn = request.args.get('isbn')
    session['isbn']= isbn
    return jsonify({'okay':'done'})


#Profile
@app.route('/profile')
def profile():
    userid = session['userid']
    cursor = Mysql.connection.cursor()
    cursor.execute('''SELECT category,isbn FROM download WHERE userid = %s''', ((userid,)))
    result = cursor.fetchall()
    category=[]
    value=[]
    for i in result:
        category.append(i[0])
        value.append(i[1])
    for i in range(len(value)):
        cursor.execute('''SELECT bookname FROM books WHERE isbn = %s''', ((value[i],)))
        res = cursor.fetchall()
        value[i]= res[0][0]
    return render_template('Profile.html',category=category,value=value)

#Admin 
@app.route('/ad')
def admin():
    return render_template('Admin.html')

@app.route('/admin')
def Admin():
    cursor = Mysql.connection.cursor()
    cursor.execute('''SELECT category FROM books''')
    result = cursor.fetchall()
    category= []
    for i in range(len(result)):
        category.append(result[i][0])
    category_set= list(set(category))
    number_of_books_in_category= []
    for i in range(len(category_set)):
        count= 0
        for j in range(len(category)):
            if category_set[i]== category[j]:
                count+=1
        number_of_books_in_category.append(count)
    cursor.execute(''' SELECT userid FROM rating ''')
    result = cursor.fetchall()
    userid = []
    for i in range(len(result)):
        userid.append(result[i][0])
    userid_set= list(set(userid))
    number_of_rating_of_user= []
    for i in range(len(userid_set)):
        count=0
        for j in range(len(userid)):
            if userid_set[i]== userid[j]:
                count+=1
        number_of_rating_of_user.append(count)
    username=[]
    category_set= set(category_set)
    uniqueCategory=[]
    userid_set= set(userid_set)
    uniqueUserId= []
    for i in category_set:
        uniqueCategory.append(i)
    for i in userid_set:
        uniqueUserId.append(i)
    # for i in range(len(uniqueUserId)):
    #     cursor.execute(''' SELECT username FROM accounts where userid = %s ''',((uniqueUserId[i])))
    #     result = cursor.fetchall()
    #     print(result)
    cursor.execute(''' SELECT * FROM books ''')
    result = cursor.fetchall()
    bookName= []
    categoryName=[]
    for i in range(len(result)):
        bookName.append(result[i][1])
        categoryName.append(result[i][3])
    
    return jsonify({'bookName': bookName, 'categoryName': categoryName, "uniqueUser": uniqueUserId,'userRating': number_of_rating_of_user, 'category': uniqueCategory , "numberOfBook": number_of_books_in_category})

if __name__ == '__main__':
    app.run(debug=True)
