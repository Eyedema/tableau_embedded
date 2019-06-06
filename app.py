from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user
from urllib.parse import urlparse, urljoin

app = Flask(__name__)
app.secret_key = "F5e9d824e9!"
login_manager = LoginManager(app)
users = ['rossi', 'bianchi', 'verdi']


class User(UserMixin):

    def __init__(self, id):
        self.id = id
        self.name = users[int(id)]
        #self.password = self.name + "_secret"
    
    def set_token(self, token):
        self.token = token
        
    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name)



@app.route("/")
def home():
    return redirect(url_for("welcome"))

@app.route("/welcome")
#@login_required
def welcome():
    return render_template("welcome.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] not in users or request.form['password'] == None:
            error = 'Invalid Credentials. Please try again.'
        else:
            user = User([i for i,x in enumerate(users) if x == request.form['username']][0])
            login_user(user)

            next = request.args.get('next')
            if not is_safe_url(next):
                return Flask.abort(400)
            return redirect(url_for('welcome'))
    return render_template('login.html', error=error)

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__=="__main__":
    app.run(debug=True)
