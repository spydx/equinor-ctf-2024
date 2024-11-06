# Writeup
by fluffyhake

## Solution
 Answers for security questions are found in the response when doing a password reset. We can change `klarz` password by using these answers. When we log in with the new password the flag is shown.

### Example

Resetting password with answers present in the response for `/get-secret-answers`: 
![Resetting the password](reset.png)


Logging in with our new password:
![Login screen](login_screen.png)



Flag is shown upon successful login:
![Flag](flag.png)



## Explanation

After registering a user we get a list of all admin users
![All admin users](all_admin_users.png)

On the webpage we see a option for resetting passwords. Let's explore it further.
We chose klarz as the target for the password reset.

![Forgot Password](forgot_password.png)

Usually during web challenges we use developer tools in the Network tab to keep an eye on all requests.

When submitting the username we see a request being sent to `/get-secret-answers`. Taking a look at the response we see the answers for our security questions.

![Questions](questions.png)

We are prompted to enter a new password after submitting these answers.

![Reset](reset.png)

Let's try our new password:
![Success-1](login_screen.png)


After logging in with the new password we get the flag!
![Flag](flag.png)


---

After the initial solve i tried with the other Admin user called iLoop. It results in the same outcome and the flag. iLoop has some other answers to the security questions:
![iLoop](iloop.png)