#autor: Lenin Espinoza
from bs4 import BeautifulSoup
import urllib

# GET ALL THE CATEGORIES
soup = BeautifulSoup(urllib.urlopen("http://gdata.youtube.com/schemas/2007/educategories.cat"))


for category in soup.find_all("atom:category"):
	parent_category=None
	if category.find("yt:parentcategory")==None:
		parent_category=''
	else:
		parent_category=category.find("yt:parentcategory")['term']

	courses_url = "http://gdata.youtube.com/feeds/api/edu/courses?v=2&category=%s"%category["term"]
	
	# GET ALL THE COURSES FOR THIS CATEGORY
	courses_by_category_soup = BeautifulSoup(urllib.urlopen(courses_url))

	for course in courses_by_category_soup.find_all("entry"):
		courses_attributes=[course.id.get_text(),course.updated.get_text(),course.title.get_text(),course.summary.get_text(),category["term"]]
		
		print 'CATEGORY: '+category["label"].encode('utf-8')+' COURSE: '+course.title.get_text().encode('utf-8')
		
		lectures_url = "http://gdata.youtube.com/feeds/api/edu/lectures?v=2&course=" + course.find("yt:playlistid").get_text()
		
		# GET ALL THE LECTURES FOR THIS COURSE
		course_lectures_soup = BeautifulSoup(urllib.urlopen(lectures_url))
		print "LIST OF VIDEOS-LECTURES"
		print "======================="
		for lecture in course_lectures_soup.find_all("entry"):
			video_id=[y.next_element for y in lecture.findAll('yt:videoid')]

			print "https://www.youtube.com/embed/"+video_id[0]