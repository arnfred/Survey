""" Small backend for survey page """

import os
import web
import json
import csv
import random
from string import ascii_uppercase, digits
import form
import hashlib
import time

# Handler for root path
class survey:        
    render = web.template.render('templates/')

    def GET(self) :
	
		# Get images in imagefolder
        imgdir = cycleFolder()

        # Set up web page form
        survey_form = form.form()
        survey_form.question("age", [('0to10','Under 10 years old'),('10to20','Between 10 and 19'),('20to30','Between 20 and 29'), ('30to40','Between 30 and 39'), ('over40', 'Over 40')], "How old are you?")
        survey_form.question("gender", [('male','Male'),('female','Female'),('other', 'Other')], "What is your gender?")
        survey_form.question("nb_devices", [(0,'None'),(1,'One'),(2,'More than one')], "How many cameras do you own?")
        survey_form.question("smartphone_p", [('yes','Yes'),('no','No')], "Do you own a smart-phone?")
        survey_form.question("nb_years", [("0to5","Less than 5 years ago"),("5to10",'Between 5 and 10 years'),("10plus", "More than 10 years ago"),("NA","I don't have a camera")], "How many years approximately is it since you had your first digital camera?")
        survey_form.question("nb_images_day", [("0to20","Less than 20"),("20to100",'Between 20 and 100 photos'), ("over100", "More than 100")], "How many images approximately do you take on average every month?")
        survey_form.question("nb_images_library", [("0to1000","Less than 1000"),("1000to5000",'Between 1000 and 5000 photos'),("over5000",'Over 5000 photos')], "How many images approximately does your photo library have?")
        survey_form.question("verify", [('yes', 'Yes'),('no', 'No')], "Did you provide false answers in the previous questions?")

        # Set up page text
        sections = page_object()
        sections.page_title = "Slideshow Survey"
        sections.keys = ["intro1", "intro2", "intro3", "step1", "step2", "done"]

        # Title for each step
        sections.title = {
                "intro1" : "Slideshow Survey",
                "intro2" : "Description of the task",
                "intro3" : "Personal questions",
                "step1" : "Step1: Select photos",
                "step2" : "Step2: Sequence photos",
                "done" : "Finished",
                }
				
        def step1_select() :
            d = "unassigned"
            print(imgdir)
            if imgdir == "images/baby" :
                d = """This is Josh. You want to make a slideshow about him. Imagine that he is your son/younger brother etc. Select any images that you would like to include in the slideshow by clicking on them (a red border will appear). There is no restriction on the number of images that you can select. Then explain in the textbox why you selected these particular images."""
            elif imgdir == "images/girl" :
                d = """This is Jess. You want to make a slideshow about her. Imagine that she is your daughter/sister etc. Select any images that you would like to include in the slideshow by clicking on them (a red border will appear). There is no restriction on the number of images that you can select. Then explain in the textbox why you selected these particular images."""
            elif imgdir == "images/female" :
                d = """This is Jill. You want to make a slideshow about her. Imagine that she is your best friend/girlfriend/ sister/daughter etc. Select any images that you would like to include in the slideshow by clicking on them (a red border will appear). There is no restriction on the number of images that you can select. Then explain in the textbox why you selected these particular images."""
            elif imgdir == "images/male" :
                d = """This is Jack. You want to make a slideshow about him. Imagine that he is your best friend/boyfriend/ brother/son etc. Select any images that you would like to include in the slideshow by clicking on them (a red border will appear). There is no restriction on the number of images that you can select. Then explain in the textbox why you selected these particular images."""
            elif imgdir == "images/couple" :
                d = """This is Jack and Jill. You want to make a slideshow about them. Imagine that they are your best friends. Select any images that you would like to include in the slideshow by clicking on them. Selected images will have a red border around them (a red border will appear). There is no restriction on the number of images that you can select. Then explain in the textbox why you selected these particular images."""
            print(d)
            return d

        # Description for each step
        sections.desc = {
                "intro1" : """<p>Welcome to ADSC's slideshow creation survey! This is an experiment conducted by the PhotoWork group.</p>
<p>You will be shown 60 photos of a person and you will be asked to create a slideshow about him/her. You will have to select any number of photos that you like and you will have to arrange them into a slideshow, about this particular person.<br/><br/>
We expect you to spend 10 to 15 minutes for this task. If the quality of your work is adequate, you will be awarded 0.2$ from the Microworkers crowdsourcing platform. If you are really committed and the quality of your work is very good, you will get a BONUS of 0.2$ (total 0.4$).</p>
<p>Click NEXT for a thorough description of the task.</p>""",

				"intro2" : """<img src="/static/description.jpg" />""",
                "intro2-bak" : """<p>Your aim is to <span class='underline'>create a slideshow for a specific person</span>. <br/><br/>
Imagine that <span class='underline'>this person is important toy you</span> (e.g. your best friend, girlfriend/boyfriend, daughter/son etc.) and you would like to create a slideshow about him/her.<br/><br/>
Think about the following scenario: Some friends are visiting and you would like to show them photos of this person, so, you compile a slideshow about him/her.<br/><br/>
The task has 3 sections:</p>
<img class="content" src='/static/pic.png'/>
<h4>Step1: Select photos</h2>
<p>You will be presented with 60 images. All images will portray a specific person (or a couple) in various moments or activities. Your aim is to <span class='underline'>choose any</span> images that you think are appropriate to be used in a slideshow. There is no restriction on the number of images that you can select. Select any photos that you like by simply clicking on them. A <span class='red'>red border</span> will appear around each image that you have clicked. This means that it is selected. If you click again on them, you will deselect them and the <span class="red">red border</span> will disappear. <span class='bold'>Remember that your aim is to use these photos in order to create a slideshow for this person</span>. Once you are ready, click Next.</p>
<h4>Step2: Sequence photos</h2>
<p>You will be presented with the images that you selected in Step1. Your aim is to <span class='underline'>rearrange the photos into a sequence</span> that you think is good for describing the person depicted. You can just drag the images and rearrange their order. Remember that your aim is to create a good sequence (according to your personal taste) that is appropriate for representing this particular person. Once you are done, click Next</p>
<h4>Step3: Finished!</h2>
<p>Once you have finished, a unique code will be generated for you. Write down this code! You will need it in order to get paid for the task that you have just performed. Go to the MicroWorkers website and use this code in order to redeem your 1$ payment!</p>
<p>If you are ready, click Next and the test will begin!</p>""",

                "intro3" : """<p>Before you will continue to the test, we would like to know some more things about you, which is necessary for our survey. Please take some time to answer the following questions (it's totally anonymous).</p>""",

                "step1" : "<p>%s</p><img src='/static/%s.jpg' />" % (step1_select(), imgdir),

                "step2" : """<p><span class='underline'>This is the most important part of the work!</span><br/><br/>These are the images that you have selected in Step1. <span class='underline'>Drag the photos and arrange them into a sequence</span> (slideshow) that you think is good for describing the person depicted. Then explain in the textbox why you selected this particular sequence of photos.<br/><br/> We expect you to spend 5 minutes in this task. <br/><br/><span class='underline'>The quality of your work in this stage will determine your paiment and your bonus! All results will be individually analysed. Good quality of work and committeed workers will get a bonus of up to 0.2$ (total 0.4$).</span></p>""",

                "done" : """<p>Thank you for your participation in our slideshow survey!</p>""",
                }

        # Collect images
        imgs = [("/static/%s/%s" % (imgdir, i), "/static/%s/large/%s" % 
            (imgdir, i)) for i in os.listdir("static/%s/" % imgdir) if 
            i[-4:].lower() == ".jpg"]
        # Shuffle images to avoid bias			
        random.shuffle(imgs)
        return self.render.survey(imgs, sections, survey_form)


    def POST(self) :
        # Get data and decode it
        data = json.loads(web.data())

        # Make sure that the data is acceptable (what needs to be done here?)

        # Get data
        questions = "[%s]" % "; ".join(map(lambda d : str(d['value']), data['questions']))
        photo_order = "[%s]" % "; ".join(map(str,data['photo_order']))
			
        time_diffs = map(lambda td : "(%s: %s)" % (td['name'], td['time']), data['time_diffs'][1:])
        window_dimensions = [data['window_x'], data['window_y']]
        mw_id = data['mw_id']

        # Create voucher code
        #id = self.getRandPath("codes/")
        if mw_id != "" :
            salt = "ICECREAM"
            project = "slideshow"
            id_hash = hashlib.sha224(mw_id + project + salt).hexdigest()
        else :
            id_hash = "Invalid worker id"

        # Create file to mark voucher as used
        # open("codes/%s" % id, 'a').close()

        # Write data to csv
        with open('data.csv', 'ab') as f:
            writer = csv.writer(f)
            writer.writerow([mw_id, time.strftime("%c"), id_hash, str(data['collection']), photo_order, questions, "[%s]" % "; ".join(time_diffs), str(data['clicks']), "'%s'" % data['question_pick'].replace("\n"," "), "'%s'" % data['question_order'].replace("\n"," "), str(window_dimensions)])       # stringify data and save to file
        return id_hash


    def getRandPath(self, folder, size=6, chars=ascii_uppercase + digits) :
        condition = True
        while condition:
            name = ''.join(random.choice(chars) for x in range(size))
            condition = os.path.isdir(folder + name)
        return name

# Set up web page text fields
class page_object(object):
    pass


# Switch between folders on each reload
currentFolderIndex = 0
def cycleFolder() :
    global currentFolderIndex
    folders = ["female", "girl", "male", "couple", "baby"]
    currentFolderIndex = (currentFolderIndex + 1) % len(folders)
    return "images/%s" % folders[currentFolderIndex]

