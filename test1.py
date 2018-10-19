from flask import Flask,redirect,url_for
app = Flask(__name__)

@app.route('/data')
def showdata():
   return 'show data'

@app.route('/map')
def map():
   return 'display map'

@app.route('/')
def hello():
   return 'home page'

@app.route('/<nme>')
def home(nme=None):
   if(nme == 'map'):
       return redirect(url_for(map))
   elif(nme=='data'):
       return redirect(url_for(showdata))
   else:
       return 'no such page exists'

if __name__ == '__main__':
   app.run(debug = True)