import flask 
from flask import render_template, request, jsonify, session
from flask_session import Session
from web3 import Web3
import json

app = flask.Flask(__name__, template_folder='Templates')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

web3 = Web3(Web3.HTTPProvider('http://localhost:7545'))

with open("build/contracts/Crowdfunding.json") as f:
    cf_compiled = json.load(f)
cf_contract_address = "0xBE4d0b9104124c38D12638e1D8678C7D3b6fD3F3"
cf_contract_instance = web3.eth.contract(
    address=cf_contract_address,
    abi=cf_compiled["abi"]
)
tx_params = {
    'from': "0x4fD5d4Ba140C9068d1789D7FBeCBA67B11e76765",
    'gas': 2000000,  # Adjust gas limit as needed
}

@app.route('/')

@app.route('/main', methods=['GET', 'POST'])
def main():
    return(flask.render_template('admin-signin.html'))

import hashlib
import json
import datetime

@app.route('/createcampaignrequest', methods=['GET', 'POST'])
def createcampaignrequest():
    if flask.request.method == 'POST':
        
        projectgoal = request.form['projectgoal']
        fundgoal = request.form['fundgoal']
        campaignduration = request.form['campainduration']
        domain = request.form['domain']
        description = request.form['description']
        
        filename = request.form["filename"]
        
        try:
            tx_hash = cf_contract_instance.functions.createCampaign(projectgoal, fundgoal, campaignduration, domain, description, filename).transact(tx_params)
            receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
                
            out = {'status': 'success', 
                   'message': 'Campaign added successfully', 
                   'transactionstatus': receipt.status,
                   'gasused': receipt.cumulativeGasUsed,
                   'block':receipt.blockNumber
                }
            return jsonify('1')
        except Exception as e:
            return jsonify(e)
        
@app.route('/getallcampaigns', methods=['GET', 'POST'])
def getallcampaigns():
    try:
        tx_hash = cf_contract_instance.functions.getAllCampaigns().call()
        return jsonify(tx_hash)
    except Exception as e:
        return jsonify('0')

@app.route('/getallprojects', methods=['GET', 'POST'])
def getallprojects():
    try:
        tx_hash = cf_contract_instance.functions.getAllProjects().call()
        return jsonify(tx_hash)
    except Exception as e:
        return jsonify('0')

@app.route('/getallevents', methods=['GET', 'POST'])
def getallevents():
    try:
        tx_hash = cf_contract_instance.functions.getAllEvents().call()
        return jsonify(tx_hash)
    except Exception as e:
        return jsonify('0')

@app.route('/getallqueries', methods=['GET', 'POST'])
def getallqueries():
    try:
        tx_hash = cf_contract_instance.functions.getAllQuery().call()
        return jsonify(tx_hash)
    except Exception as e:
        return jsonify('0')
    
import os
@app.route('/posterupload', methods=['POST'])
def posterupload():
    if request.method == 'POST':
    
        file = request.files['image']
        uploadpath = 'static/posters'
        filename = file.filename
        file.save(os.path.join(uploadpath, filename))
        return jsonify("1")
    
@app.route('/createprojectrequest', methods=['GET', 'POST'])
def createprojectrequest():
    if flask.request.method == 'POST':
        projectname = request.form['projectname']
        description = request.form['description']
        category = request.form['category']
        owner = request.form['owner']
        contact = request.form['contact']
        email = request.form['email']
        phone = request.form['phone']
        timeline = request.form['timeline']
        targetaudience = request.form['targetaudience']
        riskandchallenges = request.form['riskandchallenges']
        
        try:
            tx_hash = cf_contract_instance.functions.storeProject(projectname, description, category, owner, contact, email, phone, timeline, targetaudience, riskandchallenges).transact(tx_params)
            receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            return jsonify('1')
        except Exception as e:
            return jsonify(e)


@app.route('/createeventrequest', methods=['GET', 'POST'])
def createeventrequest():
    if flask.request.method == 'POST':
        eventid = request.form['eventid']
        eventname = request.form['eventname']
        duration = request.form['duration']
        avenue = request.form['avenue']
        datetime = request.form['datetime']
        description = request.form['description']

        try:
            tx_hash = cf_contract_instance.functions.storeEvent(eventid, eventname, duration, avenue, datetime, description).transact(tx_params)
            receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            return jsonify('1')
        except Exception as e:
            return jsonify(e)


@app.route('/createbackerfund', methods=['GET', 'POST'])
def createbackerfund():
    if flask.request.method == 'POST':
        fundamount = request.form['fundamount']
        transactionid = request.form['transactionid']
        fundmode = request.form['fundmode']
        reason = request.form['reason']

    return jsonify("result")

@app.route('/createqueryrequest', methods=['GET', 'POST'])
def createqueryrequest():
    if flask.request.method == 'POST':
        description = request.form['description']
        role =  session.get("role")
        email = session.get("email")
        
        try:
            tx_hash = cf_contract_instance.functions.createQuery(description, role, email).transact(tx_params)
            receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            return jsonify('1')
        except Exception as e:
            return jsonify(e)

#Get data calls
@app.route('/gelallactivecampaigns', methods=['GET', 'POST'])
def gelallactivecampaigns():
    if flask.request.method == 'POST':
        
        return jsonify("result")

@app.route('/getallfundrequest', methods=['GET', 'POST'])
def getallfundrequest():
    if flask.request.method == 'POST':
        
        return jsonify("result")

@app.route('/getcampaigndetail', methods=['GET', 'POST'])
def getcampaigndetail():
    if flask.request.method == 'POST':
        campaignid = request.form['campaignid']
        
    return jsonify("result")

#querypages
@app.route('/adminquery', methods=['GET', 'POST'])
def adminquery():
    if flask.request.method == 'GET':
        return(flask.render_template('admin-query.html'))

@app.route('/addquery', methods=['GET', 'POST'])
def addquery():
    if flask.request.method == 'GET':
        return(flask.render_template('add-query.html'))
    
#event pages
@app.route('/createevent', methods=['GET', 'POST'])
def createevent():
    if flask.request.method == 'GET':
        return(flask.render_template('event-create.html'))
    
@app.route('/manageevent', methods=['GET', 'POST'])
def manageevent():
    if flask.request.method == 'GET':
        return(flask.render_template('event-manage.html'))
    
@app.route('/viewevent', methods=['GET', 'POST'])
def viewevent():
    if flask.request.method == 'GET':
        return(flask.render_template('event-view.html'))

#project pages
@app.route('/createproject', methods=['GET', 'POST'])
def createproject():
    if flask.request.method == 'GET':
        return(flask.render_template('project-create.html'))
    
@app.route('/manageproject', methods=['GET', 'POST'])
def manageproject():
    if flask.request.method == 'GET':
        return(flask.render_template('project-manage.html'))

#Fund pages
@app.route('/fundrequest', methods=['GET', 'POST'])
def fundrequest():
    if flask.request.method == 'GET':
        return(flask.render_template('fund-request.html'))
    

    
@app.route('/backerfundraise', methods=['GET', 'POST'])
def backerfundraise():
    if flask.request.method == 'GET':
        return(flask.render_template('backer-fund-raise.html'))
    
@app.route('/backerrefund', methods=['GET', 'POST'])
def backerrefund():
    if flask.request.method == 'GET':
        return(flask.render_template('backer-refund.html'))
    
@app.route('/backerprojectlist', methods=['GET', 'POST'])
def backerprojectlist():
    if flask.request.method == 'GET':
        return(flask.render_template('backer-project-list.html'))
    
@app.route('/backerviewcampaign', methods=['GET', 'POST'])
def backerviewcampaign():
    if flask.request.method == 'GET':
        return(flask.render_template('backer-view-campaign.html'))

@app.route('/backeraddfund', methods=['GET', 'POST'])
def backeraddfund():
    if flask.request.method == 'GET':
        return(flask.render_template('backeraddfund.html'))

#Campaign pages
@app.route('/createcampaign', methods=['GET', 'POST'])
def createcampaign():
    if flask.request.method == 'GET':
        return(flask.render_template('campaign-create.html'))
    
@app.route('/managecampaign', methods=['GET', 'POST'])
def managecampaign():
    if flask.request.method == 'GET':
        return(flask.render_template('campaign-manage.html'))


#Startup Pages

@app.route('/createstartupfund', methods=['GET', 'POST'])
def createstartupfund():
    if flask.request.method == 'POST':
        fundamount = request.form['fundamount']
        idea = request.form['idea']
    
   
    return jsonify("result")


    
@app.route('/startuprequestfund', methods=['GET', 'POST'])
def startuprequestfund():
    if flask.request.method == 'GET':
        return(flask.render_template('startuprequestfund.html'))
    
@app.route('/startupviewcampaign', methods=['GET', 'POST'])
def startupviewcampaign():
    if flask.request.method == 'GET':
        return(flask.render_template('startup-view-campaign.html'))
    
@app.route('/startupdashboard', methods=['GET', 'POST'])
def startupdashboard():
    if flask.request.method == 'GET':
        return(flask.render_template('startup-index.html'))
    
@app.route('/startupsignin', methods=['GET', 'POST'])
def startupsignin():
    if flask.request.method == 'GET':
        return(flask.render_template('startup-signin.html'))
    
@app.route('/startupsignup', methods=['GET', 'POST'])
def startupsignup():
    if flask.request.method == 'GET':
        return(flask.render_template('startup-signup.html'))
     
@app.route('/startupprojectlist', methods=['GET', 'POST'])
def startupprojectlist():
    if flask.request.method == 'GET':
        return(flask.render_template('startup-project-list.html'))  

@app.route('/startupsignupfun', methods=['GET', 'POST'])
def startupsignupfun():
    if flask.request.method == 'POST':
        email       = request.form['email']
        password    = request.form['password']
        username    = request.form['username']
        phone       = request.form['phone']
        
        
        try:
            tx_hash = cf_contract_instance.functions.registerStartup(username, email, phone, password).transact(tx_params)
            receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
                
            out = {'status': 'success', 
                   'message': 'Startup registered successfully', 
                   'transactionstatus': receipt.status,
                   'gasused': receipt.cumulativeGasUsed,
                   'block':receipt.blockNumber
                }
            return jsonify('1')
        except Exception as e:
            return jsonify('0')
    
@app.route('/startupsigninfun', methods=['GET', 'POST'])
def startupsigninfun():
    if flask.request.method == 'POST':
        email       = request.form['email']
        password    = request.form['password']
        try:
            tx_hash = cf_contract_instance.functions.loginStartup(email, password).call()
            session["role"]  = "startup"
            session["email"] = email
            return jsonify(tx_hash)
        except Exception as e:
            return jsonify('0')


#Backer Pages
@app.route('/backerdashboard', methods=['GET', 'POST'])
def backerdashboard():
    if flask.request.method == 'GET':
        return(flask.render_template('backer-index.html'))
    
@app.route('/backersignin', methods=['GET', 'POST'])
def backersignin():
    if flask.request.method == 'GET':
        return(flask.render_template('backer-signin.html'))
    
@app.route('/backersignup', methods=['GET', 'POST'])
def backersignup():
    if flask.request.method == 'GET':
        return(flask.render_template('backer-signup.html'))


@app.route('/backersignupfun', methods=['GET', 'POST'])
def backersignupfun():
    if flask.request.method == 'POST':
        email       = request.form['email']
        password    = request.form['password']
        username    = request.form['username']
        phone       = request.form['phone']
        
        try:
            tx_hash = cf_contract_instance.functions.registerBacker(username, email, phone, password).transact(tx_params)
            receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
                
            out = {'status': 'success', 
                   'message': 'Backer registered successfully', 
                   'transactionstatus': receipt.status,
                   'gasused': receipt.cumulativeGasUsed,
                   'block':receipt.blockNumber
                }
            return jsonify('1')
        except Exception as e:
            return jsonify('0')
    
@app.route('/backersigninfun', methods=['GET', 'POST'])
def backersigninfun():
    if flask.request.method == 'POST':
        email       = request.form['email']
        password    = request.form['password']
        
        try:
            tx_hash = cf_contract_instance.functions.loginBacker(email, password).call()
            session["role"]  = "backer"
            session["email"] = email
            return jsonify(tx_hash)
        except Exception as e:
            return jsonify('0')
        
#Admin Pages
@app.route('/adminsignin', methods=['GET', 'POST'])
def adminsignin():
    if flask.request.method == 'POST':
        email       = request.form['email']
        password    = request.form['password']
        
        if (email=='crowdfuncadmin@gmail.com' and password == 'AdminPassword'):
            return jsonify("1")
        else:
            return jsonify("0")

@app.route('/admindashboard', methods=['GET', 'POST'])
def admindashboard():
    if flask.request.method == 'GET':
        return(flask.render_template('campaigner-index.html'))
    
if __name__ == '__main__':
    app.run(debug=True)