from bson.objectid import ObjectId
from flask import Flask, render_template, request, url_for, redirect, session, flash
from flask_wtf import FlaskForm
from forms import ScenarioForm, RegisterForm, LoginForm
import json, datetime
import os, threading, subprocess, time
import pymongo, bcrypt
from pymongo import MongoClient
from models import ModelUsers, ModelRecords 


cluster = MongoClient("mongodb+srv://admin:KesummWHH5yr68c@cluster0.mi5o8.mongodb.net/web_simulation?retryWrites=true&w=majority")
db = cluster["web_simulation"]
users = db["users"]
records = db["records"]

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SESSION_COOKIE_SAMESITE']='Lax'

@app.route('/login', methods = ['POST','GET'])
def login():
    form = LoginForm()
    if 'username' in session:
        return redirect(url_for('dashboard'))    

    if form.validate_on_submit():
        login_user = users.find_one({"username":form.username.data})
        if login_user:
            if bcrypt.checkpw(form.password.data.encode('utf-8'),login_user['password']):
                session['username'] = login_user['username']
                session['email'] = login_user['email']
                return redirect(url_for('dashboard')) 
            else:
                flash("Invalid username/password combination!", "danger")                
        else:
            flash("Invalid username/password combination!", "danger")        
    return render_template("login.html", form=form)

@app.route('/register', methods= ['POST','GET'])
def register():
    form = RegisterForm()
    model = ModelUsers()
    if form.validate_on_submit():
        #check existing user
        existing_user = users.find_one({"username":form.username.data})
        existing_email = users.find_one({"email":form.email.data})
        print(existing_email, existing_user)
        #verify with existing usernames and emails in the mongoDB: users
        valid = True
        if existing_user != None:
            valid=False
            flash("This username has already existed.", "warning")  

        if existing_email != None:
            valid=False  
            flash("This email address has already existed.", "warning")   
        if valid:    
            hasspass = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt()) 
            session['hasspass'] = hasspass
            # users.insert({"username": form.username.data, "email": form.email.data, "password": hasspass})            
            post = model.userProfile()
            users.insert(post)
            session['username'] = form.username.data
            session['email'] = form.email.data
            del session['hasspass']
            return redirect(url_for("dashboard"))

    return render_template("register.html", form=form)    

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        user_records = records.find({"username":session['username']})
        return render_template("dashboard.html", user_records=user_records)    
    return redirect(url_for("index"))    

@app.route('/', methods = ['POST', 'GET'])
def index():
    form = ScenarioForm()
    messages_error = [""]
   # session.clear()
    if request.method == "POST" :
        valid = True
        print("Submitted")
        network = form.network.data
        num_devices = form.num_devices.data
        dist_devices_gateway = form.dist_devices_gateway.data
        if num_devices<1 :
            valid =False    
        if network != "LoRaWAN" :
            packet_size = form.packet_size_wifi.data
            print("Packet size, WiFi = "+str(packet_size), type(packet_size))
            if packet_size<1 or packet_size>1500 :
                valid = False
                print("WiFI-False")
            if dist_devices_gateway<0 or dist_devices_gateway>10 :
                valid = False    
                messages_error[0] = "Distance must not be over 10 meters."
        else :
            packet_size = form.packet_size_lorawan.data
            print("Packet size, LoRaWAN = "+str(packet_size), type(packet_size))
            if packet_size<1 or packet_size>230 :
                valid = False
                print("LoRaWAN-False")
            if dist_devices_gateway<0 or dist_devices_gateway>8000 :
                valid = False
                messages_error[0] = "Distance must not be over 8000 meters."   
        if form.validate() or valid :       
            session['network'] = form.network.data
            session['traffic_direction'] = form.traffic_dir.data
            session['traffic_profile'] = form.traffic_profile.data
            session['packet_size'] = str(packet_size)
            load_freq = form.load_freq.data
            session['load_freq'] = str(load_freq)
            session['mean_load'] = str(form.mean_load.data)
            session['fps'] = str(form.fps.data)
            session['number_devices'] = str(form.num_devices.data)
            session['distance_devices_gateway'] = str(form.dist_devices_gateway.data)
            session['simulation_time'] = str(form.simulation_time.data)
            hidden_devices = form.hidden_devices.data
            session['hidden_devices'] = dict(form.hidden_devices.choices).get(hidden_devices)
            sf = form.sf.data
            session['sf'] = dict(form.sf.choices).get(sf)
            #In case of LoRaWAN manager chosen, for the moment set sf = 7
            session['propagation_delay_model'] = dict(form.prop_delay.choices).get(form.prop_delay.data)
            session['propagation_loss_model'] =  dict(form.prop_loss.choices).get(form.prop_loss.data)
            session['cyclic_redundacy_check'] = form.cyclic_redundacy_check.data
            session['low_data_rate_optimization'] = form.low_data_rate_optimization.data
            session['implicit_header_mode'] = form.implicit_header_mode.data
            mcs = form.mcs.data
            session['mcs'] = dict(form.mcs.choices).get(mcs)
            #In case of ideal Wi-Fi manager chosen, for the moment set mcs = 5
            if mcs=='12':
                mcs='5'
            session['bandwidth'] = str(form.bandwidth.data)
            session['spatial_streams'] = form.spatial_streams.data
            tx = form.tx.data
            session['tx'] = str(tx)
            rx = form.rx.data
            session['rx'] = str(rx)
            tx_factor = form.tx_factor.data
            session['tx_factor'] = str(tx_factor)
            rx_factor = form.rx_factor.data
            session['rx_factor'] = str(rx_factor)
            voltage = form.voltage.data
            session['voltage'] = str(voltage)
            session['battery_capacity'] = str(form.battery_cap.data)

            #Copy all varaibles to environment varaibles to use in the shell script
            #principal variables for both Wi-Fi and LoRaWAN
            os.environ['NETWORK']=session['network']
            os.environ['DISTANCE']=session['distance_devices_gateway'] 
            os.environ['SIMULATION_TIME']=session['simulation_time'] 
            os.environ['NUMDEVICES']=session['number_devices'] 
            os.environ['TRAFFICDIR']=session['traffic_direction']
            os.environ['TRAFFICPROF']=session['traffic_profile']
            #print(os.environ['TRAFFICPROF'])
            os.environ['PACKETSIZE']=session['packet_size']
            os.environ['LOADFREQ']=session['load_freq'] 
            os.environ['FPS']=session['fps'] 
            os.environ['MEANLOAD']= str(session['mean_load'])
            os.environ['HIDDENDEVICES']=hidden_devices
            #advanced varaibles for both Wi-Fi and LoRaWAN
            os.environ['PROPDELAY']=session['propagation_delay_model']
            os.environ['PROPLOSS']=session['propagation_loss_model']
            os.environ['BANDWIDTH']=session['bandwidth']
            os.environ['TX']=session['tx']
            os.environ['RX']=session['rx']
            os.environ['TXFACTOR']=session['tx_factor']
            os.environ['RXFACTOR']=session['rx_factor']
            os.environ['VOLTAGE']=session['voltage']
            os.environ['BATTERYCAP']=session['battery_capacity'] 
            #advanced varables for Wi-Fi only
            os.environ['MCS']=mcs
            os.environ['SPATIALSTREAMS']=session['spatial_streams'] 
            #advanced variables for LoRaWAN only
            os.environ['CYCLREDUNDCHK']=session['cyclic_redundacy_check']
            os.environ['LOWDATAOPT']=session['low_data_rate_optimization']
            os.environ['IMPLICITHEADER']=session['implicit_header_mode']
            os.environ['SF']=sf
            output="#"
            latency="#"
            #Create class of a thread
            class myThread (threading.Thread):
                def __init__(self, threadID, output, latency) :
                    threading.Thread.__init__(self)
                    self.threadID = threadID
                    self.output = output
                    self.latency = latency
                def run(self):
                    print("Start Thread",self.threadID)
                    self.output, self.latency=simulationCall(self.threadID)
                    print("Exit Thread",self.threadID)
            
            def simulationCall(threadID):
                if threadID==1 :
                    print(os.environ['NETWORK'])
                    if os.environ['TRAFFICPROF'] == "cbr":
                        if os.environ['NETWORK'] == "Wi-Fi 802.11ac":
                            output = subprocess.check_output('cd static/ns-wifi; ./waf --run "scratch/script-cbr.cc --distance=$DISTANCE --simulationTime=$SIMULATION_TIME --nWifi=$NUMDEVICES --trafficDirection=$TRAFFICDIR --payloadSize=$PACKETSIZE --dataRate=$MEANLOAD --hiddenStations=$HIDDENDEVICES --MCS=$MCS --channelWidth=$BANDWIDTH --propDelay=$PROPDELAY --propLoss=$PROPLOSS --spatialStreams=$SPATIALSTREAMS --batteryCap=$BATTERYCAP --voltage=$VOLTAGE" 2> log.txt', shell=True, text=True,stderr=subprocess.DEVNULL)
                            latency = subprocess.check_output('cd static/ns-wifi; cat "log.txt" | grep -e "client sent 1023 bytes" -e "server received 1023 bytes from" > "log-parsed.txt"; python3 get_latencies.py "log-parsed.txt"', shell=True, text=True,stderr=subprocess.DEVNULL)
                            subprocess.check_output('cd static/ns-wifi; rm "log.txt"; rm "log-parsed.txt"', shell=True, text=True,stderr=subprocess.DEVNULL)
                    elif os.environ['TRAFFICPROF'] == "vbr":
                        if os.environ['NETWORK'] == "Wi-Fi 802.11ac":
                            output = subprocess.check_output('cd static/ns-wifi; ./waf --run "scratch/script-vbr.cc --distance=$DISTANCE --simulationTime=$SIMULATION_TIME --nWifi=$NUMDEVICES --trafficDirection=$TRAFFICDIR --fps=$FPS --hiddenStations=$HIDDENDEVICES --MCS=$MCS --channelWidth=$BANDWIDTH --propDelay=$PROPDELAY --propLoss=$PROPLOSS --spatialStreams=$SPATIALSTREAMS --batteryCap=$BATTERYCAP --voltage=$VOLTAGE" 2> log.txt', shell=True, text=True,stderr=subprocess.DEVNULL)
                            latency = subprocess.check_output('cd static/ns-wifi; cat "log.txt" | grep -e "client sent 1023 bytes" -e "server received 1023 bytes from" > "log-parsed.txt"; python3 get_latencies.py "log-parsed.txt"', shell=True, text=True,stderr=subprocess.DEVNULL)
                            subprocess.check_output('cd static/ns-wifi; rm "log.txt"; rm "log-parsed.txt"', shell=True, text=True,stderr=subprocess.DEVNULL)                    
                    elif os.environ['TRAFFICPROF'] == "periodic":
                        if os.environ['NETWORK'] == "Wi-Fi 802.11ac":
                            #print(os.environ['MCS'])
                            output = subprocess.check_output('cd static/ns-wifi; ./waf --run "scratch/script-periodic.cc --distance=$DISTANCE --simulationTime=$SIMULATION_TIME --nWifi=$NUMDEVICES --trafficDirection=$TRAFFICDIR --payloadSize=$PACKETSIZE --period=$LOADFREQ --hiddenStations=$HIDDENDEVICES --MCS=$MCS --channelWidth=$BANDWIDTH --propDelay=$PROPDELAY --propLoss=$PROPLOSS --spatialStreams=$SPATIALSTREAMS --batteryCap=$BATTERYCAP --voltage=$VOLTAGE" 2> log.txt', shell=True, text=True,stderr=subprocess.DEVNULL)
                            latency = subprocess.check_output('cd static/ns-wifi; cat "log.txt" | grep -e "client sent 1023 bytes" -e "server received 1023 bytes from" > "log-parsed.txt"; python3 get_latencies.py "log-parsed.txt"', shell=True, text=True,stderr=subprocess.DEVNULL)
                            subprocess.check_output('cd static/ns-wifi; rm "log.txt"; rm "log-parsed.txt"', shell=True, text=True,stderr=subprocess.DEVNULL)
                        elif os.environ['NETWORK'] == "LoRaWAN":
                            output = subprocess.check_output('cd static/ns-lora; ./waf --run "scratch/script-periodic.cc --distance=$DISTANCE --simulationTime=$SIMULATION_TIME --nSta=$NUMDEVICES --payloadSize=$PACKETSIZE --period=$LOADFREQ --SF=$SF --channelWidth=$BANDWIDTH --propDelay=$PROPDELAY --propLoss=$PROPLOSS --batteryCap=$BATTERYCAP --voltage=$VOLTAGE" 2> log.txt', shell=True, text=True,stderr=subprocess.DEVNULL)
                            output = output + "Energy consumption: " + subprocess.check_output("cd static/ns-lora; cat 'log.txt' | grep -e 'LoraRadioEnergyModel:Total energy consumption' | tail -1 | awk 'NF>1{print $NF}' | sed 's/J//g'", shell=True, text=True,stderr=subprocess.DEVNULL)
                            latency = subprocess.check_output('cd static/ns-lora; cat "log.txt" | grep -e "GatewayLorawanMac:Receive()" -e "EndDeviceLorawanMac:Send(" > "log-parsed.txt"; python3 get_latencies.py "log-parsed.txt"', shell=True, text=True,stderr=subprocess.DEVNULL)
                
                            subprocess.check_output('cd static/ns-lora; rm "log.txt"; rm "log-parsed.txt"', shell=True, text=True,stderr=subprocess.DEVNULL)
                            
                    print(output)
                    return output, latency
            #Call NS-3 simulation by python shell script according network type
            try:
                model = ModelRecords()
                if(network!='LoRaWAN') :
                    #Create a new thread to connect to the simulation NS-3
                    thread1 = myThread(1,output, latency)
                    #Start a thread
                    thread1.start()
                    #wait for all threads to finish
                    thread1.join()
                    output, latency = thread1.output, thread1.latency
                    lines = output.splitlines()
                    line = lines[0]
                    i = 0
                    while "Total" not in line:
                        i = i + 1
                        line = lines[i]
                    energy = lines[i].split()[-1]
                    battery_lifetime = lines[i+1].split()[-1]
                    throughput = lines[i+2].split()[-1]
                    success_rate = lines[i+3].split()[-1]

                    session['energy_consumption'] = energy
                    session['throughput'] = throughput
                    session['latency'] = str(float(latency) * 1000) # To get in ms
                    session['success_rate'] = success_rate
                    session['battery_lifetime'] = battery_lifetime
                    #If a user has already login, save input parameters and results in JSON. 
                    if 'username' in session:
                        if form.traffic_profile.data == 'periodic':   
                            post = model.wifiPeriodicRec()           
                        else:
                            post = model.wifiStochasticRec()
                else :
                    #Create a new thread to connect to the LoRa simulation NS-3
                    thread1 = myThread(1,output, latency)
                    #Start a thread
                    thread1.start()
                    #wait for all threads to finish
                    thread1.join()
                    output, latency = thread1.output, thread1.latency

                    lines = output.splitlines()
                    line = lines[0]
                    i = 0
                    while "Success" not in line:
                        i = i + 1
                        line = lines[i]
                    success_rate = round(float(lines[i].split()[-1]), 2)
                    throughput = round(float(lines[i+1].split()[-1]), 2)
                    energy = float(lines[i+2].split()[-1])
                    capacity = (float(session['battery_capacity']) / 1000.0) * float(session['voltage']) * 3600
                    battery_lifetime = round(((capacity / energy) * float(session['simulation_time'])) / 86400 / 365, 2)
                    energy = round(energy, 2)
                    session['energy_consumption'] = energy
                    session['throughput'] = throughput
                    session['success_rate'] = success_rate
                    session['battery_lifetime'] = battery_lifetime
                    #If a user has already login, save input parameters and results in JSON. 
                    if 'username' in session:
                        post = model.lorawanRec()
                #Insert a record of parameters and results according to an account of a user to a collection "records", if this user has already login
                if 'username' in session:
                    records.insert_one(post)  

                jResults = {
                    "throughput": throughput,
                    "latency":  str(float(latency) * 1000), # To get in ms
                    "success_rate": success_rate,
                    "energy_consumption": energy,
                    "battery_lifetime": battery_lifetime
                }
               
                return render_template("results.html", jResults=jResults)
            except Exception as e:
                print('error:', e)    
                flash("No access at the simulation!", "warning")             
    print("Messages error distance ="+messages_error[0])   
    return render_template("index.html", form=form, messages_error=messages_error)

"""
@app.route('/results')
def results():
    return render_template("results.html")
"""
@app.route('/documents')
def documents():
    return render_template("documents.html")

@app.route('/api/<id>')    
def api(id):
    objID = ObjectId(id)
    user_record = records.find_one({"_id": objID})
    if user_record != None:
        record_json = json.dumps(user_record, indent=4, default=str)
        print(record_json)
        return render_template("result_records.html",user_record=user_record)
    return "No record found."     

@app.route('/delete/<id>')
def delete(id):
    objID = ObjectId(id)
    try:
        records.delete_one({"_id": objID})
    except Exception as e:
        print('error: ',e)   
        flash("Cannot delete this record!", "danger")
    return redirect(url_for('dashboard')) 

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    #session.pop('username',None)
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__" :
    app.run(debug=True, reloader_interval=20)