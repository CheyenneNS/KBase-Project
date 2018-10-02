from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)
app.debug = True   # need this for autoreload as and stack trace
UPLOAD_FOLDER = '/Users/nelsonchey/Desktop/KbaseProject/Environments/site/files'
ALLOWED_EXTENSIONS = set(['txt'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/process')
def interactive():
    return render_template('interactive.html')

@app.route('/background_process')
def background_process():
    

    var = request.args.get('variable', 0, type=str)
    arrayFragStrs = np.asarray(readFile(var))

    if 30 > countLines(var): 

        unscrambledString = list(assemble(stringFrag))
        unfragmentedString = str(unscrambledString[0])
        #print(unfragmentedString)
        return(unfragmentedString)

    else:
        unscrambledString = listMatch(stringFrag)
        unfragmentedString = toString(unscrambledString)
        #print(unfragmentedString)
        return(unfragmentedString)

    
    decodedString = urllib.parse.unquote_plus(unfragmentedString)

    return jsonify(result=decodedString)

def readFile(file):
	contents = None

	with open(file, 'r') as fileOpen:
		contents = fileOpen.read().splitlines()
		fileOpen.close()

		return(contents)

def assemble(str_list, min=3, max=15):

    if len(str_list) < 2:
        return set(str_list)

    output = set()
    string = str_list.pop()

    for i, match in enumerate(str_list):
        matches = set()

        if match in string:
            matches.add(string)

        elif match in candidate:
            matches.add(candidate)

        for n in range(min, max + 1):
            if match[:n] == string[-n:]:
                matches.add(string + match[n:])

            if match[-n:] == string[:n]:
                matches.add(match[:-n] + string)

        for word in matches:
            output.update(assemble(str_list[:i] + str_list[i + 1:] + [word]))

    return(output)



def overlap(string1, string2):

    overlaps = []

    for i in range(len(string2)):
        for j in range(len(string1)):
            if string1.endswith(string2[:i + 1], j):
                overlaps.append((i, j))

    return max(overlaps) if overlaps else (0, -1) 


def listMatch(lst):

    overlaps = defaultdict(list)

    while len(lst) > 1:
        overlaps.clear()

        for string1 in lst:
            for string2 in lst:
                if string1 == string2:
                    continue

                amount, start = overlap(string1, string2)
                overlaps[amount].append((start, string1, string2))

        maximum = max(overlaps)

        if maximum == 0:
            break

        start, string1, string2 = choice(overlaps[maximum])  
        lst.remove(string1)
        lst.remove(string2)
        lst.append(string1[:start] + string2)

    return(lst)


# Descramble function is the main function used for allocating which string assembly method to use, decoding unfragmented string from url,
# and writing output to file


# @app.route('/')
# def hello_world():
#     return "Hello world"

if __name__ == '__main__':
   app.run()