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