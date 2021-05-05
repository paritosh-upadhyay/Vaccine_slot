import requests as re
import urllib3
from datetime import datetime
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

urllib3.disable_warnings()


def check_vacine_status(hosturl, district_code):
    today_date = datetime.today().strftime('%d-%m-%Y')
    for district in district_code:
        url = '%s/api/v2/appointment/sessions/public/calendarByDistrict?district_id=%s&date=%s' % (
            hosturl, district, today_date)
        resp = re.get(url, headers=None, timeout=60, verify=False)
        body = resp.json()
        create_rport(body)


def create_rport(body):
    global content, content_flag, date_list
    #content = content + "<p>=============================" + body['centers'][0]['district_name'] + "================" \
     #                                                                                              "===================</p>"
    for center in body['centers']:
#        content = content + "<p>" + center['name'] + "</p>"
        for data in center['sessions']:
            date_list.append(str(data['date']))
            if data['min_age_limit'] < 45 and data['available_capacity'] > 0:
                content_flag = True
                content = content + "<p>On date " + str(data['date']) + " Vaccine " + data['vaccine'] + " " + \
                          str(data['available_capacity']) + " slot available in "+ center['name']  +\
                              " in district "+ center['district_name'] +" for 18 to 44. </p>"
            # else:
            #     content = content + "<p>On date " + str(data['date']) + " Vaccine " + data['vaccine'] +" " +\
            #           str(data['available_capacity']) + " Available for 45 above.</p>"

    #content = content + "<p>==========================================================================</p>"


def user_invitation(msg):
    try:
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = "paritosh.upadhyay008@gmail.com"  # Enter your address
        receiver_email = ['u.paritosh14@gmail.com', 'paritosh.upadhyay008@gmail.com']
        SUBJECT = "Vaccine available slot."
        INVITATION_SENDER_PASS = "p@r!to$h_1111"

        message = MIMEMultipart("alternative")
        message["Subject"] = SUBJECT
        message["From"] = sender_email
        message["To"] = ", ".join(receiver_email)
        part2 = MIMEText(msg, "html")
        message.attach(part2)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password=INVITATION_SENDER_PASS)
            server.sendmail(sender_email, receiver_email, message.as_string())

    except Exception as error:
        print(error)


def get_dictrict_id(url):
    global district_code
    resp = re.get(url, headers=None, timeout=60, verify=False)
    body = resp.json()
    for id in body['districts']:
        district_code.append(id['district_id'])


if __name__ == '__main__':
    host_url = "https://cdn-api.co-vin.in"
    up_district_url = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/34"
    content_flag = False
    date_list = list()
    #district_code= [363] # pune
    #district_code = [687, 677, 696] #It is varanasi , mirzapur , bhadohi
    district_code = list()
    get_dictrict_id(up_district_url)
    content = "<html><body>"
    check_vacine_status(host_url, district_code)
    content = content + "</html></body>"
    if content_flag:
        user_invitation(content)
    else:
        print("No slot")
    
