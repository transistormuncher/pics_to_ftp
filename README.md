# pics_to_ftp

### Scenario:
A company's field staff audits shops' compliance with company guidelines. The results are stored in a Postgresql database. In addition, pictures are taken as evidence and stored on an external server. Links to the pictures are stored in the database alongside the survey answers.
The company wants the survey results and the renamed pictures to be transferred to a third party FTP server on a daily basis. Hence, this script needs to

* retrieve the audit results from the database and transfer them to the FTP-Server
* retrieve the picture links from the database
* download all the pictures and rename them
* transfer all pictures to the FTP-Server
