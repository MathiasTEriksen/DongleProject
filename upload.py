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
