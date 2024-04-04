from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

person=0
def calc():
    with open('log.txt', 'r') as file:
        ins_count = 0
        outs_count = 0
        for line in file:
            parts = line.strip().split(',')
            if len(parts) >= 3:
                action = parts[2].strip().lower()  # Convert to lowercase for case insensitivity
                if action == 'in':
                    ins_count += 1
                elif action == 'out':
                    outs_count += 1
    person = ins_count-outs_count
    return person


# Define a password for accessing the log entries
PASSWORD = "myweb"

# Define a route for entering the password
@app.route('/')
def enter_password():
    return render_template('index.html',page=1)

# Define a route for handling the password submission
@app.route('/authenticate', methods=['POST'])
def authenticate():
    password = request.form.get('password')
    if password == PASSWORD:
        page = int(request.args.get('page', 1))  # Get the page parameter or default to page 1
        log_content, more_entries, read_previous = parse_log_file('log.txt', page)
        person = calc()
        return render_template('log.html', log_content=log_content, more_entries=more_entries, read_previous=read_previous, page=page,person=person)
    else:
        return render_template('index.html',page=1, message="Incorrect password, please try again.")

@app.route('/references')
def references():
    return render_template('references.html')
@app.route('/about')
def about():
    return render_template('about.html')
def index():
    return render_template('index.html')
# Define a route to upload the log file
@app.route('/upload_log', methods=['POST'])
def upload_log():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    
    if file:
        # Save the uploaded log file
        file.save('log.txt')
        return 'Log file uploaded successfully'

# Define a route to display the log file
@app.route('/p')
def log():
    page = int(request.args.get('page', 1))  # Get the page parameter or default to page 1
    log_content, more_entries, read_previous = parse_log_file('log.txt', page)
    person = calc()
    return render_template('log.html', log_content=log_content, more_entries=more_entries, read_previous=read_previous, page=page,person=person)

def parse_log_file(log_file_path, page, page_size=20):
    log_data = []
    with open(log_file_path, 'r') as file:
        lines = file.readlines()
        start_idx = (page - 1) * page_size
        end_idx = min(start_idx + page_size, len(lines))
        for line in lines[start_idx:end_idx]:
            parts = line.strip().split(',')
            log_data.append({
                'name': parts[0],
                'datetime': parts[1],
                'action': parts[2]
            })
        more_entries = end_idx < len(lines)
        read_previous = page > 1  # Check if there are entries to read in the previous page
    return log_data, more_entries, read_previous

if __name__ == '__main__':
    app.run(debug=True)

