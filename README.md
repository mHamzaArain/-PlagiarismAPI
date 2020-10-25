# Plagiarism API
 Plagiarism Check API using NLP 


| Resources                    | Protocol | Path      | Parameter                                                        | Status code                                                                         | Description |
|------------------------------|----------|-----------|------------------------------------------------------------------|-------------------------------------------------------------------------------------|-------------|
| Register<br>user             | POST     | /register | username: String<br>pw: String                                   | 200 OK<br>301 Invalid user                                                          |             |
| Detect similarities of Docks | POST     | /detect   | username: String<br>pw: String<br>text1: String<br>text2: String | 200 OK<br>301 Out of Tokens<br>302 Invalid username & password<br>303 Out of tokens |             |
| Refill Tokens of user        | POST     | /refill   | username: String<br>admin_pw: String<br>refillAmount: int        | 200 OK<br>301 Invalid username<br>302 Invalid admin_password                        |             |
