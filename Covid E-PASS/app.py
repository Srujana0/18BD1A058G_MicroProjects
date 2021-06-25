from flask import Flask,render_template,request
from twilio.rest import Client
import requests
account_sid='AC9ea8e4ce8c9e173e603a9511ed335cde'
auth_token='0a401fc7a1601760e2c015ddfd332a5a'
client=Client(account_sid,auth_token)
app=Flask(__name__,static_url_path='/static')
@app.route('/')
def registration_form():
    return render_template('index.html')
@app.route('/login',methods=['POST','GET'])
def login_registration_dtls():
    first_name=request.form['fname']
    last_name=request.form['lname']
    email_id=request.form['email']
    source_st=request.form['source_state']
    source_dt = request.form['source']
    destination_st=request.form['dest_state']
    destination_dt = request.form['destination']
    phoneNumber=request.form['phoneNumber']
    date=request.form['trip']
    full_name=first_name+","+last_name
    r=requests.get('https://api.covid19india.org/v4/data.json')
    json_data=r.json()
    cnt=json_data[destination_st]['districts'][destination_dt]['total']['confirmed']
    pop = json_data[destination_st]['districts'][destination_dt]['meta']['population']
    travel_pass=((cnt/pop)*100)
    if travel_pass<30 and request.method=='POST':
        status='CONFIRMED'
        client.messages.create(to="whatsapp:+918096602111",
                               from_="whatsapp:+14155238886",
                               body="Hello "+" "+full_name+" "+"Your Travel From "+" "+source_dt+" "+"To"+" "+destination_dt+" "+"Has"+
              " "+status+" On"+" "+date+" "+", Apply later")
        return render_template('user_registration_dlts.html',var=full_name,var1=email_id,
                               var3=source_st,var4=source_dt,var5=destination_st,var6=destination_dt,var7=phoneNumber,
                               var8=date,var9=status)
    else:
        status = 'Not Confirmed'
        client.messages.create(to="whatsapp:+918096602111",
                               from_="whatsapp:+14155238886",
                               body="Hello " + " " + full_name + "  " + "your travel from" + source_dt + " " + "To" + " " + destination_dt + " "
                                    + "Has" + " " + status + " On" + " " + date + " " + ", Apply later")
        return render_template('user_registration_dlts.html', var=full_name, var1=email_id,
                               var3=source_st, var4=source_dt, var5=destination_st, var6=destination_dt,
                               var7=phoneNumber, var8=date, var9=status)
if __name__ == "__main__":
        app.run(port=9001, debug=True)




