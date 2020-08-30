import subprocess
from flask import Flask, render_template, request, jsonify


app = Flask(__name__)




class AI:
    def __init__(self, path, id):
        self.path = path
        if path == 'human':
            self.human = 1
        else:
            self.human = 0
        self.id = id

    def send(self, message):
        value = str(message) + '\n'
        value = bytes(value, 'UTF-8')
        self.proc.stdin.write(value)
        self.proc.stdin.flush()

    def receive(self):
        return self.proc.stdout.readline().strip().decode()
   
    def init(self):
        if self.human == 0:
            self.proc = subprocess.Popen(self.path,
                                         stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE)
            self.send(self.id)
            self.name = self.receive()

    
    def action(self, a, b):
        if self.human == 1:
            value = [a, b]
        else:
            self.send(str(a) + ' ' + str(b))
            value = self.receive().split(' ')
        return int(value[0]), int(value[1])





def try_init(ai0, ai1):    
        ai0.init()
        ai1.init()
    



@app.route('/')
def index():
    return render_template("index.html")




@app.route('/start_game')
def start_game():
    global ai0, ai1
      
    a1 = ('human')
    b1 = ["./sample"]

    ai0, ai1 = AI(a1, 0), AI(b1, 1)
    try_init(ai0, ai1)
    return "游戏开始！"



@app.route('/send_message', methods=['GET'])
def send_message():
    message_get = ""
    message_get = request.args['message']

    global a, b
    global ai0
    
    tmp = message_get.split(" ")
    a = int(tmp[0])
    b = int(tmp[1])
    print(str(a) + " " + str(b))
   
    return "收到消息"    
      


@app.route('/change_to_json', methods=['GET'])
def change_to_json():
    global a, b    
    global ai1
  
    a, b = ai1.action(a, b)           
       
    message_back = "".join(str(a) + " " + str(b))
    message_json = {
        "message": message_back
    }

    return jsonify(message_json)
        
  


if __name__ == '__main__':   
    app.run(debug = true)
