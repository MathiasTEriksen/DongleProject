<<<<<<< HEAD
'''
this file upload.py creates a web server which is used to upload files to the
pi that can later be used to program PSU boards using the button.py script.
This file creates one page for uploads, at psu-programmer.local, which is
used to upload hex files, and one page at psu-programmer.local/folder, which
can be used to see which file is currently the active write file, and to
change which file is the active write file.
'''

'''
imports
'''

import os
import shutil
import glob
from werkzeug.utils import secure_filename
# using flask to setup and run app
from flask import Flask,flash,request,redirect,send_file,render_template

'''
setup Variables
'''

# uploads will be stored in .../DongleProject/uploads
UPLOAD_FOLDER = 'uploads/'
# only allowed to upload hex files
ALLOWED_EXTENSIONS = {'hex'}
# setting up flask, html templates in .../DongleProject/templates
app = Flask(__name__, template_folder='templates')
# configuring upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

'''
functions
'''

# make_tree function will be used to create a list of files in uploads folder
def make_tree(path):
    tree = dict(name=os.path.basename(path), children=[])
    try: lst = os.listdir(path)
    except OSError:
        pass
    else:           
        for name in lst:
            fn = os.path.join(path, name)
            if os.path.isdir(fn):
                tree['children'].append(make_tree(fn))
            else:
                tree['children'].append(dict(name=name))
    return tree

# allowed_file is used to only allow upload of hex files                                                                             
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# save_active_file writes the filename in active.json file
def save_active_file(file_content):
    active = open('active.json', 'w')
    active.write(file_content)
    active.close()
    pass

'''
upload file funtionality
'''

# url for this page is psu-programmer.local
@app.route('/', methods=['GET', 'POST'])                                      
def upload_file():
    # will be activated when a button is pressed
    if request.method == 'POST':
        # if Proceed button on page is pushed redirect to /folder page
        if request.form.get("Proceed"):                                      
            return redirect('/folder')
        # print no file to terminal and return to page if no file is selected
        if 'file' not in request.files:                                      
            print('no file')                                                 
            return redirect(request.url)                                     
        file = request.files['file']
        # if there is no filename print to terminal and return to page
        if file.filename == '':                                              
            print('no filename')                                             
            return redirect(request.url)
        # if file is allowed(hex) and has a name save to uploads folder
        if file and allowed_file(file.filename):                             
            filename = secure_filename(file.filename)                        
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))   
            print("saved file successfully")
            # redirect to psu-programmer/folder
            return redirect('/folder')                                       
    # render the web page                                                                         
    return render_template('upload_file.html')                               
                                                                             
'''
activate file functionality
'''

# url is psu-programmer.local/folder for this page
@app.route('/folder', methods=['GET', 'POST'])                               
def dirtree():
    # path for make_tree function is uploads folder
    path = os.path.expanduser(u'/home/pi/DongleProject/uploads')             
    # open active.json file and read the filename of last activated file
    active = open('active.json', 'r')
    active_file = active.read()
    active.close()
    # if activate button is clicked                                                                    
    if request.method == 'POST':
        # get the selected file from the drop down and put it in select cariable
        select = request.form.get('file')
        # path to selected file in uploads folder
        Path =  ('/home/pi/DongleProject/uploads/' + select)   
        # copy selected file over to rpipdi folder for writing
        shutil.copy(Path, '/home/pi/DongleProject/rpipdi' )
        # rename the selected file to be Hexfile.hex that used for writing in button.py
        os.chdir('rpipdi')
        os.rename('/home/pi/DongleProject/rpipdi/' + select, 'Hexfile.hex')
        # return to correct working directory
        os.chdir('/home/pi/DongleProject')
        # use save active file function to save the name of the activated file
        save_active_file(select)
        # make this the active filename that will be rendered in the web page
        active = open('active.json', 'r')
        active_file = active.read()
        active.close()
    # render web page, passing the given arguments                                                                         
    return render_template('dirtree.html', current_file=active_file,         
                           tree=make_tree(path))                             
'''
run app
'''

if __name__ == "__main__":
    # run the app on default port with debug activated, ip is psu-programmer.local
    app.run(host='0.0.0.0', port=80, debug=True)
=======
########################IMPORTS###############################################
                                                                             #   
import os                                                                    # using os for file organization within code
import shutil                                                                # using shutil to copy + paste files
import glob                                                                  # using glob for to find most recently added files
from werkzeug.utils import secure_filename                                   # using secure_filename to secure my filenames
from flask import Flask,flash,request,redirect,send_file,render_template     # using flask to create a web server
                                                                             #
########################SETUP VARIABLES#######################################
                                                                             #
UPLOAD_FOLDER = 'uploads/'                                                   # /home/pi/webapp/uploads will be used to store uploads
ALLOWED_EXTENSIONS = {'hex'}                                                 # we will only be allowing hex files to be uploaded
                                                                             # 
app = Flask(__name__, template_folder='templates')                           # we will be using flask for our web server, and
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER                                  # /home/pi/webapp/templates for our html templates
                                                                             # configuring the upload folder
########################FUNCTION DEFINITIONS##################################
                                                                             #   
def make_tree(path):                                                         # the make_tree function allows us to create a
    tree = dict(name=os.path.basename(path), children=[])                    # list of items in a directory that we use in a
    try: lst = os.listdir(path)                                              # html loop in order to get a list of all the files
    except OSError:                                                          # in our uploads directory
        pass                                                                 #
    else:                                                                    #
        for name in lst:                                                     #
            fn = os.path.join(path, name)                                    #
            if os.path.isdir(fn):                                            #
                tree['children'].append(make_tree(fn))                       #
            else:                                                            #
                tree['children'].append(dict(name=name))                     #
    return tree                                                              #
                                                                             #
def allowed_file(filename):                                                  # 
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS          # allow the upload of .hex files
                                                                             #
########################UPLOAD FILE FUNCTIONALITY#############################
                                                                             #
@app.route('/', methods=['GET', 'POST'])                                     # the url is just psu-programmer.local 
def upload_file():                                                           # using both GET and POST
    if request.method == 'POST':                                             # if a button on page is pushed, proceed
        if request.form.get("Proceed"):                                      # if the pushed button is the 'Proceed'
            return redirect('/folder')                                       # button, redirect to psu-programmer.local/folder
        if 'file' not in request.files:                                      # if there is no file selected, and 'upload' is 
            print('no file')                                                 # pushed, stay on page, print 'no file' to terminal
            return redirect(request.url)                                     #
        file = request.files['file']                                         # if there is no filename, stay on page and 
        if file.filename == '':                                              # print 'no filename'
            print('no filename')                                             #
            return redirect(request.url)                                     #
        if file and allowed_file(file.filename):                             # if the file is allowed (.hex) and has a name
            filename = secure_filename(file.filename)                        # secure filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))   # add th file to upload folder
            print("saved file successfully")                                 # 
            print(filename)                                                  # print out name of file
            return redirect('/folder')                                       # redirect to psu-programmer.local/folder page
                                                                             #
    return render_template('upload_file.html')                               # render this template
                                                                             #
########################ACTIVATE FILE FUNCTIONALITY###########################
                                                                             #                                
@app.route('/folder', methods=['GET', 'POST'])                               # url is psu-programmer/folder for this page
def dirtree():                                                               #
    path = os.path.expanduser(u'/home/pi/webapp/uploads')                    # the path for creation of the tree is '/home/pi/webapp/uploads
                                                                             #
    list_of_files = glob.glob('/home/pi/webapp/CurrentFile/*')               # using the glob module to create a list of files that have been
    try:latest_path = max(list_of_files, key=os.path.getctime)               # placed in current_files directory
    except ValueError:                                                       # try to find the most recently added file in the directory
        latest_file = 'none'                                                 # if the directory is empty, there would be a ValueError, so 
        pass                                                                 # if this happens we want to skip, and say there is no current
    else:                                                                    # write file
        latest_file = os.path.basename(latest_path)                          # if the directory is not empty, we will put the name of the most
                                                                             # recent hex file into latest_file 
    if request.method == 'POST':                                             # 
        select = request.form.get('file')                                    # if the submit button is pressed
        Path =  ('/home/pi/webapp/uploads/' + select)                        # select will be the file currently slected from the list
                                                                             # create a variable for the path to the currently selected file
        shutil.copy(Path, '/home/pi/webapp/CurrentFile/')                    # within the uploads folder
        print(str(select) + ' is now active')                                # copy the hex file into our current file folder, as this is going
        shutil.copy(Path, '/home/pi/')                                       # to be the new active write file, print out _ is now active
                                                                             # copy the file to /home/pi as well, where it will be used as 
        list_of_files = glob.glob('/home/pi/webapp/CurrentFile/*')           # the write file in button.py
        latest_path = max(list_of_files, key=os.path.getctime)               # make this file the new file in the latest_file variable
        latest_file = os.path.basename(latest_path)                          #
                                                                             #
    return render_template('dirtree.html', current_file=latest_file,         # render this page with these parameters, using make_tree to 
                           tree=make_tree(path))                             # create the file list in the uploads directory, and current_file
                                                                             # as the value for the currently active file
########################RUN APP###############################################
                                                                             # 
if __name__ == "__main__":                                                   # run the app on port 80 (default port), with debug active
    app.run(host='0.0.0.0', port=80, debug=True)                             # site url : psu-programmer.local
                                                                             # 
##############################################################################    
>>>>>>> 0b5fcece0d7cc2a11f516a99befd8f8b01e44ef6
