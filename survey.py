# Handler for root path
class survey:        
    currentFolderIndex = 0

    def GET(self) :

        # Set up web page form
        survey_form = form.form()
        survey_form.question("devices", [(1,'just 1'),(2,'2 - 3'),(3,'4 or more')], "How many cameras do you own?")
        survey_form.question("devices2", [(1,'just 1'),(2,'2 - 3'),(3,'4 or more')], "How many cameras do you own?")
        survey_form.question("trick", [('yes', 'I sure am'),('no', 'I would never!')], "Are you just making up answers to get a quick payment?", "yes")

        # Set up page text
        text = text_object()
        text.title = "Image Survey"
        text.step1_desc = "Please answer a few questions before we start:"
        text.step2_desc = "Select all images that you want in your photo album"
        text.step3_desc = "Drag and drop images to order them the way you'd like them to be ordered in a slide show"

        # Get images in imagefolder
        imgdir = cycleFolder()
        imgs = ["/static/%s/%s" % (imgdir, i) for i in os.listdir("static/%s" % imgdir)]
        return render.survey(imgs, text, survey_form)


    def POST(self) :
        pass


    # Switch between folders on each reload
    def cycleFolder() :
        self.currentFolderIndex = (self.currentFolderIndex + 1) % 3
        folders = ["Beach", "Bird", "Other"]
        return "images/%s/" % folders[self.currentFolderIndex]

# Set up web page text fields
class text_object(object):
    pass
