#autor: Lenin Espinoza
from bs4 import BeautifulSoup
import urllib
import sqlite3

conn = sqlite3.connect('youtubeedu.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE category(
			term integer primary key not null,
            label text NOT NULL, 
            category_parent_id text,
            parent_category text)''')

cursor.execute('''CREATE TABLE course(
			id text primary key not null,
			title text NOT NULL, 
			summary text,
			category_id integer,
			FOREIGN KEY(category_id) REFERENCES category(term))''')

cursor.execute('''CREATE TABLE lecture(
			url_video text,
			course_id text,
			FOREIGN KEY(course_id) REFERENCES course(id))''')

cursor.close()

def insert_categories(term,label,category_parent_id,parent_category):
	conn = sqlite3.connect('youtubeedu.db')
	cursor = conn.cursor()
	cursor.execute('INSERT INTO category VALUES (?,?,?,?)',(term,label,category_parent_id,''))
	conn.commit()
	cursor.close()

def insert_courses(ids,title,summary,category_id):
	conn = sqlite3.connect('youtubeedu.db')
	cursor = conn.cursor()
	cursor.execute('INSERT INTO course VALUES (?,?,?,?)',(ids,title,summary,category_id))
	conn.commit()
	cursor.close()

def insert_lectures(url_video,course_id):
	conn = sqlite3.connect('youtubeedu.db')
	cursor = conn.cursor()
	cursor.execute('INSERT INTO lecture VALUES (?,?)',(url_video,course_id))
	conn.commit()
	cursor.close()


soup = BeautifulSoup(urllib.urlopen("http://gdata.youtube.com/schemas/2007/educategories.cat"))

for category in soup.find_all("atom:category"):
	parent_category_id=None
	if category.find("yt:parentcategory")==None:
		parent_category_id=''
	else:
		parent_category_id=category.find("yt:parentcategory")['term']

	#INSERT CATEGORIES
	insert_categories(category["term"],category["label"],parent_category_id, "")
	
	courses_url = "http://gdata.youtube.com/feeds/api/edu/courses?v=2&category=%s"%category["term"]

	#Get all the courses for this category
	courses_by_category_soup = BeautifulSoup(urllib.urlopen(courses_url))
	for course in courses_by_category_soup.find_all("entry"):
		
		#INSERT COURSES
		insert_courses(str(course.id.get_text()), course.title.get_text(), course.summary.get_text(),int(category["term"]))
		lectures_url = "http://gdata.youtube.com/feeds/api/edu/lectures?v=2&course=" + course.find("yt:playlistid").get_text()
		
		# Get all the lectures for this course
		course_lectures_soup = BeautifulSoup(urllib.urlopen(lectures_url))
		for lecture in course_lectures_soup.find_all("entry"):
			x=[y.next_element for y in lecture.findAll('yt:videoid')]
			
			#INSERT LECTURES
			insert_lectures("https://www.youtube.com/embed/"+x[0].encode('utf-8'),str(course.id.get_text()))
			