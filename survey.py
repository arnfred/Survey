# Main instance of survey

import web
import os
from web import form

# Set up stuff for web server
urls = (
    '/', 'survey'
)
render = web.template.render('templates/')
app = web.application(urls, globals())

# Set up form for survey
survey_form = form.Form( 
    form.Radio("devices", [(1,'just 1'),(2,'2 - 3'),(3,'4 or more')], form.notnull, description="How many cameras do you own?"),
    form.Radio("trick", [('yes', 'I sure am'),('no', 'I would never!')], description="Are you just making up answers to get a quick payment?", value='yes')
)

# Set up web page text fields
class text_object(object):
    pass
text = text_object()
text.title = "Image Survey"
text.step1_desc = "Please answer a few questions before we start ... "
text.step2_desc = "Select all images that you want in your photo album"
text.step3_desc = "Drag and drop images to order them the way you'd like them to be ordered in a slide show"

# This is such a cheap hack, but some times global state is just easier
currentFolderIndex = 0
def cycleFolder() :
    global currentFolderIndex
    currentFolderIndex = (currentFolderIndex + 1) % 3
    folders = ["Beach", "Bird", "Other"]
    return "images/%s/" % folders[currentFolderIndex]

# Handler for root path
class survey:        
    def GET(self):

        # Get images in imagefolder
        imgdir = cycleFolder()
        imgs = ["/static/%s/%s" % (imgdir, i) for i in os.listdir("static/%s" % imgdir)]
        return render.survey(imgs, text, survey_form)

if __name__ == "__main__":
    app.run()
