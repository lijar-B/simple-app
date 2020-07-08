import streamlit as st
from PIL import Image
#EDA Pkgs
import pandas as pd
import matplotlib.pyplot as plt 
import matplotlib
matplotlib.use('Agg')
# from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator



#DB
import sqlite3
conn = sqlite3.connect('o.db')
c = conn.cursor()

#Functons
def create_ohntable():
    c.execute('CREATE TABLE IF NOT EXISTS ohntable(category TEXT,title TEXT,content TEXT,postdate DATE)')

def add_data(category,title,content,postdate):
    c.execute('INSERT INTO ohntable(category,title,content,postdate) VALUES (?,?,?,?)',(category,title,content,postdate))
    conn.commit()

def view_all_notes():
    c.execute('SELECT * FROM ohntable')
    data = c.fetchall()
    return data

def view_all_titles():
    c.execute('SELECT DISTINCT title FROM ohntable')
    data = c.fetchall()
    return data

def get_blog_by_title(title):
    c.execute('SELECT * FROM ohntable WHERE title="{}"'.format(title))
    data = c.fetchall()
    return data

def get_blog_by_category(category):
    c.execute('SELECT * FROM ohntable WHERE category="{}"'.format(category))
    data = c.fetchall()
    return data

def delete_data(title):
    c.execute('DELETE FROM ohntable WHERE title="{}"'.format(title))
    conn.commit()

def readingTime(mytext):
    total_words = len([token for token in mytext.split(" ")])
    estimatedTime = total_words/200.0
    return estimatedTime

#Layout Templates
html_temp = """
<div style="background-color:{};padding:10px;border-radius:10px">
<h1 style="color:{};text-align:center;">Ohn's Blog! </h1>
</div>
"""
title_temp ="""
<div style="background-color:#fb5ec5;padding:10px;border-radius:10px;margin:10px;">
<h4 style="color:white;text-align:center;">{}</h1>
<h6>{}</h6>
<br/>
<br/> 
<p style="text-align:justify">{}</p>
</div>
"""
content_temp ="""
<div style="background-color:#fb5ec5;padding:10px;border-radius:5px;margin:10px;">
<h4 style="color:white;text-align:center;">{}</h1>
<h6>{}</h6> 
<h6>{}</h6>
<br/>
<br/>
<p style="text-align:justify">{}</p>
</div>
"""
head_message_temp ="""
<div style="background-color:#fb5ec5;padding:10px;border-radius:5px;margin:10px;">
<h4 style="color:white;text-align:center;">{}</h1>
<h6>{}</h6> 
<h6>Post Date: {}</h6> 
</div>
"""
full_message_temp ="""
<div style="overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
<p style="text-align:justify;color:black;padding:10px">{}</p>
</div>
"""

def main():
    #A Simple CRUD Blog
    st.title ("Ohn's Blog! ")

    menu = ["Ohn's Home", "View Ohn's Posts", "Add Ohn's Posts", "Ohn's Search", "Ohn's Manager"]
    choice = st.sidebar.selectbox("Ohn's Menu", menu)

    if choice == "Ohn's Home":
        st.subheader("Ohn's Home")
        # img = Image.open("us.jpg")
        # st.image(img, width=300)
        # vid_file = open("ohn.mp4", "rb").read()
        # st.video(vid_file)
       
        result = view_all_notes()
        
        for i in result:
            b_category = i[0]
            b_title = i[1]
            b_content = str(i[2])[0:20]
            b_post_date = i[3]
            st.markdown(title_temp.format(b_title,b_category,b_content,b_post_date),unsafe_allow_html=True)

    elif choice == "View Ohn's Posts":
        st.subheader("Here are your posts my Love!")
        all_titles =[i[0] for i in view_all_titles()]
        postlist = st.selectbox("Ohn's Post", all_titles)
        post_result = get_blog_by_title(postlist)
        for i in post_result:
            b_category = i[0]
            b_title = i[1]
            b_content = str(i[2])[:]
            b_post_date = i[3]
            st.text("Reading Time: {} min".format(readingTime(b_content)))
            st.markdown(head_message_temp.format(b_title,b_category,b_post_date),unsafe_allow_html=True)
            st.markdown(full_message_temp.format(b_content),unsafe_allow_html=True)



    elif choice == "Add Ohn's Posts":
        st.subheader("Add contents")
        create_ohntable()
        blog_category = st.text_input("Enter category", max_chars=50)
        blog_title = st.text_input("Enter Post Title")
        blog_content = st.text_area("Post Here",height=200)
        blog_post_date = st.date_input("Date")
        if st.button("Add"):
            add_data(blog_category,blog_title,blog_content,blog_post_date)
            st.success("Post:{} saved".format(blog_title))




    elif choice == "Ohn's Search":
        st.subheader("Search Posts my Love!")
        search_term = st.text_input("search")
        search_choice = st.radio("Search by...",("title", "category"))
        if st.button("Search"):
            if search_choice == "title":
                content_result =get_blog_by_title(search_term)
            elif search_choice == "category":
                content_result = get_blog_by_category(search_term)
            for i in content_result:
                b_category = i[0]
                b_title = i[1]
                b_content = str(i[2])[:]
                b_post_date = i[3]
                st.text("Reading Time: {}".format(readingTime(b_content)))
                st.markdown(head_message_temp.format(b_title,b_category,b_post_date),unsafe_allow_html=True)
                st.markdown(full_message_temp.format(b_content),unsafe_allow_html=True)

    elif choice == "Ohn's Manager":
        st.subheader("Manage Posts")
        unique_titles =[i[0] for i in view_all_titles()]
        delet_blog_by_title = st.selectbox("Post Title", unique_titles)
        result = view_all_notes()
        clean_db = pd.DataFrame(result,columns=["category", "Title","Posts","Post Date"])
        
        if st.button("Delete"):
            delete_data(delet_blog_by_title)
            st.warning("Deleted: '{}'".format(delet_blog_by_title))

        if st.checkbox("Metrics"):
            new_df = clean_db
            new_df['Length'] = new_df['Posts'].str.len()
            st.dataframe(new_df)

            st.subheader("category Stats")
            new_df['category'].value_counts().plot(kind='bar')
            st.pyplot()

            st.subheader("category Stats")
            new_df['category'].value_counts().plot.pie(autopct="%1.1f%%")
            st.pyplot()

        
if __name__ == '__main__':
    main()





# import streamlit as st
# from PIL import Image
# #EDA Pkgs
# import pexpect
# import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib
# matplotlib.use('Agg')
# # from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator



# #DB
# import sqlite3
# conn = sqlite3.connect('data.db')
# c = conn.cursor()

# #Functons
# def create_table():
#     c.execute('CREATE TABLE IF NOT EXISTS blogtable(author TEXT,title TEXT,article TEXT,postdate DATE)')

# def add_data(author,title,article,postdate):
#     c.execute('INSERT INTO blogtable(author,title,article,postdate) VALUES (?,?,?,?)',(author,title,article,postdate))
#     conn.commit()

# def view_all_notes():
#     c.execute('SELECT * FROM blogtable')
#     data = c.fetchall()
#     return data

# def view_all_titles():
#     c.execute('SELECT DISTINCT title FROM blogtable')
#     data = c.fetchall()
#     return data

# def get_blog_by_title(title):
#     c.execute('SELECT * FROM blogtable WHERE title="{}"'.format(title))
#     data = c.fetchall()
#     return data

# def get_blog_by_author(author):
#     c.execute('SELECT * FROM blogtable WHERE author="{}"'.format(author))
#     data = c.fetchall()
#     return data

# def delete_data(title):
#     c.execute('DELETE FROM blogtable WHERE title="{}"'.format(title))
#     conn.commit()

# def readingTime(mytext):
#     total_words = len([token for token in mytext.split(" ")])
#     estimatedTime = total_words/200.0
#     return estimatedTime

# #Layout Templates
# html_temp = """
# <div style="background-color:{};padding:10px;border-radius:10px">
# <h1 style="color:{};text-align:center;">Simple Blog </h1>
# </div>
# """
# title_temp ="""
# <div style="background-color:#fb5ec5;padding:10px;border-radius:10px;margin:10px;">
# <h4 style="color:white;text-align:center;">{}</h1>
# <img src="https://www.w3schools.com/howto/img_avatar2.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;" >
# <h6>Author:{}</h6>
# <br/>
# <br/> 
# <p style="text-align:justify">{}</p>
# </div>
# """
# article_temp ="""
# <div style="background-color:#464e5f;padding:10px;border-radius:5px;margin:10px;">
# <h4 style="color:white;text-align:center;">{}</h1>
# <h6>Author:{}</h6> 
# <h6>Post Date: {}</h6>
# <img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;width: 50px;height: 50px;border-radius: 50%;" >
# <br/>
# <br/>
# <p style="text-align:justify">{}</p>
# </div>
# """
# head_message_temp ="""
# <div style="background-color:#464e5f;padding:10px;border-radius:5px;margin:10px;">
# <h4 style="color:white;text-align:center;">{}</h1>
# <img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;">
# <h6>Author:{}</h6> 
# <h6>Post Date: {}</h6> 
# </div>
# """
# full_message_temp ="""
# <div style="background-color:silver;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
# <p style="text-align:justify;color:black;padding:10px">{}</p>
# </div>
# """



# def main():
#     #A Simple CRUD Blog
#     st.title ("Ohn's Blog! ")

#     menu = ["Ohn's Home", "Ohn's Posts", "Add Ohn's Posts", "Ohn's Search", "Ohn's Manager"]
#     choice = st.sidebar.selectbox("Ohn's Menu", menu)

#     if choice == "Ohn's Home":
#         st.subheader("Ohn's Home")
#         st.subheader("Upload Picture")
#         uploaded_file = st.file_uploader("Choose an image..", type="jpg")
#         if uploaded_file is not None:
#             image = Image.open(uploaded_file)
#             st.image(image, caption='Uploaded Image', use_column_width=True)
#             st.write("")
#         result = view_all_notes()
        
#         for i in result:
#             b_author = i[0]
#             b_title = i[1]
#             b_article = str(i[2])[0:60]
#             b_post_date = i[3]
#             st.markdown(title_temp.format(b_title,b_author,b_article,b_post_date),unsafe_allow_html=True)

#     elif choice == "Ohn's Posts":
#         st.subheader("Here are your articles my Love!")
#         all_titles =[i[0] for i in view_all_titles()]
#         postlist = st.selectbox("Ohn's Post", all_titles)
#         post_result = get_blog_by_title(postlist)
#         for i in post_result:
#             b_author = i[0]
#             b_title = i[1]
#             b_article = str(i[2])[:]
#             b_post_date = i[3]
#             st.text("Reading Time: {} min".format(readingTime(b_article)))
#             st.markdown(head_message_temp.format(b_title,b_author,b_post_date),unsafe_allow_html=True)
#             st.markdown(full_message_temp.format(b_article),unsafe_allow_html=True)



#     elif choice == "Add Ohn's Posts":
#         st.subheader("Add Articles")
#         create_table()
#         blog_author = st.text_input("Enter Author Name", max_chars=50)
#         blog_title = st.text_input("Enter Post Title")
#         blog_article = st.text_area("Post Article Here",height=200)
#         blog_post_date = st.date_input("Date")
#         if st.button("Add"):
#             add_data(blog_author,blog_title,blog_article,blog_post_date)
#             st.success("Post:{} saved".format(blog_title))




#     elif choice == "Ohn's Search":
#         st.subheader("Search Posts my Love!")
#         search_term = st.text_input("search")
#         search_choice = st.radio("Search by...",("title", "author"))
#         if st.button("Search"):
#             if search_choice == "title":
#                 article_result =get_blog_by_title(search_term)
#             elif search_choice == "author":
#                 article_result = get_blog_by_author(search_term)
#             for i in article_result:
#                 b_author = i[0]
#                 b_title = i[1]
#                 b_article = str(i[2])[:]
#                 b_post_date = i[3]
#                 st.text("Reading Time: {}".format(readingTime(b_article)))
#                 st.markdown(head_message_temp.format(b_title,b_author,b_post_date),unsafe_allow_html=True)
#                 st.markdown(full_message_temp.format(b_article),unsafe_allow_html=True)

#     elif choice == "Ohn's Manager":
#         st.subheader("Manage Posts")
#         unique_titles =[i[0] for i in view_all_titles()]
#         delet_blog_by_title = st.selectbox("Post Title", unique_titles)
#         result = view_all_notes()
#         clean_db = pd.DataFrame(result,columns=["Author", "Title","Posts","Post Date"])
        
#         if st.button("Delete"):
#             delete_data(delet_blog_by_title)
#             st.warning("Deleted: '{}'".format(delet_blog_by_title))

#         if st.checkbox("Metrics"):
#             new_df = clean_db
#             new_df['Length'] = new_df['Posts'].str.len()
#             st.dataframe(new_df)

#             st.subheader("Author Stats")
#             new_df['Author'].value_counts().plot(kind='bar')
#             st.pyplot()

#             st.subheader("Author Stats")
#             new_df['Author'].value_counts().plot.pie(autopct="%1.1f%%")
#             st.pyplot()




# if __name__ == '__main__':
#     main()