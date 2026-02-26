"""
Run this ONCE to create the SQLite database and seed demo data.
    python init_db.py

Credentials from seed data:
  Admin   → username: admin       password: Test@1234
  Company → email: infosys@gmail.com  password: 123
  User    → email: rahul@gmail.com    password: 123
"""

import sqlite3
import hashlib
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'campustocareer.db')

def md5(text):
    return hashlib.md5(text.encode()).hexdigest()

SCHEMA = """
CREATE TABLE IF NOT EXISTS tbladmin (
    ID          INTEGER PRIMARY KEY AUTOINCREMENT,
    AdminName   TEXT,
    UserName    TEXT,
    MobileNumber INTEGER,
    Email       TEXT,
    Password    TEXT,
    AdminRegdate DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tbluser (
    ID           INTEGER PRIMARY KEY AUTOINCREMENT,
    FullName     TEXT,
    Email        TEXT,
    MobileNumber INTEGER,
    StudentID    TEXT,
    Gender       TEXT,
    Address      TEXT,
    Age          INTEGER,
    DOB          TEXT,
    Image        TEXT,
    Password     TEXT,
    UserRegdate  DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tblcompany (
    ID             INTEGER PRIMARY KEY AUTOINCREMENT,
    CompanyName    TEXT,
    ContactPerson  TEXT,
    CompanyUrl     TEXT,
    CompanyAddress TEXT,
    MobileNumber   INTEGER,
    CompanyEmail   TEXT,
    CompanyLogo    TEXT,
    Password       TEXT,
    CompanyRegdate DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tblvacancy (
    ID              INTEGER PRIMARY KEY AUTOINCREMENT,
    CompanyID       INTEGER,
    JobTitle        TEXT,
    MonthlySalary   TEXT,
    JobDescriptions TEXT,
    NoofOpenings    TEXT,
    JobLocation     TEXT,
    ApplyDate       TEXT,
    LastDate        TEXT,
    JobpostingDate  DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tblapplyjob (
    ID           INTEGER PRIMARY KEY AUTOINCREMENT,
    UserId       INTEGER,
    JobId        INTEGER,
    Resume       TEXT,
    ApplyDate    DATETIME DEFAULT CURRENT_TIMESTAMP,
    Message      TEXT,
    Remark       TEXT,
    Status       TEXT,
    ResponseDate DATETIME
);

CREATE TABLE IF NOT EXISTS tbleducation (
    ID                  INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID              INTEGER,
    SecondaryBoard      TEXT,
    SecondaryBoardyop   TEXT,
    SecondaryBoardper   TEXT,
    SecondaryBoardcgpa  TEXT,
    SSecondaryBoard     TEXT,
    SSecondaryBoardyop  TEXT,
    SSecondaryBoardper  TEXT,
    SSecondaryBoardcgpa TEXT,
    GraUni              TEXT,
    GraUniyop           TEXT,
    GraUnidper          TEXT,
    GraUnicgpa          TEXT,
    PGUni               TEXT,
    PGUniyop            TEXT,
    PGUniper            TEXT,
    PGUnicgpa           TEXT,
    ExtraCurriculars    TEXT,
    OtherAchivement     TEXT
);

CREATE TABLE IF NOT EXISTS tblmessage (
    ID           INTEGER PRIMARY KEY AUTOINCREMENT,
    AppID        INTEGER,
    Message      TEXT,
    Status       TEXT,
    ResponseDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    IsRead       TEXT
);

CREATE TABLE IF NOT EXISTS tblpage (
    ID              INTEGER PRIMARY KEY AUTOINCREMENT,
    PageType        TEXT,
    PageTitle       TEXT,
    PageDescription TEXT,
    Email           TEXT,
    MobileNumber    INTEGER,
    UpdationDate    DATETIME
);
"""

def seed(conn):
    cur = conn.cursor()

    # Admin  (password = Test@1234)
    cur.execute("SELECT COUNT(*) FROM tbladmin")
    if cur.fetchone()[0] == 0:
        cur.execute("""INSERT INTO tbladmin (AdminName,UserName,MobileNumber,Email,Password)
                       VALUES (?,?,?,?,?)""",
                    ('Admin','admin',7898799720,'admin@campus.com', md5('Test@1234')))

    # Companies (password = 123)
    cur.execute("SELECT COUNT(*) FROM tblcompany")
    if cur.fetchone()[0] == 0:
        p123  = md5('123')
        ptest = md5('test')
        companies = [
            ('Infosys Pvt Ltd','Sanjana Jha','www.infosys.com','H-123, Bangalore',8956232528,'infosys@gmail.com','',p123),
            ('HCL Pvt Ltd','Sneha','www.hcl.com','G-123, Sector-63, Noida',8989898989,'hcl@gmail.com','',p123),
            ('TCS Pvt Ltd','Sudhir Sharma','www.tcs.com','Mumbai HQ',8889898989,'support@tcs.com','',p123),
            ('Religare Pvt Ltd','Mahesh Kumar','www.religare.com','H-321 Sector 4 Noida',8956247994,'religare@gmail.com','',p123),
            ('HSBC','Anuj Kumar','hsbc.com','New Delhi',2345235423,'anuj@hsbc.com','',ptest),
            ('Amazon India','Amit Kumar','amazon.in','Bangalore India',1425362514,'info@amazon.in','',ptest),
        ]
        cur.executemany("""INSERT INTO tblcompany
            (CompanyName,ContactPerson,CompanyUrl,CompanyAddress,MobileNumber,CompanyEmail,CompanyLogo,Password)
            VALUES (?,?,?,?,?,?,?,?)""", companies)

    # Users (password = 123)
    cur.execute("SELECT COUNT(*) FROM tbluser")
    if cur.fetchone()[0] == 0:
        p123  = md5('123')
        ptest = md5('test')
        users = [
            ('Rahul Saxena','rahul@gmail.com',8989898989,'567945','Male','H-456 Mayur Vihar',26,'1990-05-01','',p123),
            ('Farha Akthar','farha@gmail.com',2525252525,'5657767','Female','',0,'','',p123),
            ('Akash Jain','jain@gmail.com',6544646544,'667886768','Male','',0,'','',p123),
            ('Ginni Mishra','ginni@gmail.com',3636363663,'7877878','Female','NA',0,'2001-10-07','',p123),
            ('Anuj Kumar','ak@gmail.com',6174512546,'HGH32321','Male','',0,'','',ptest),
            ('ABC Test','abctest@gmail.com',123458900,'2275462354','Male','NA',24,'2000-01-02','',ptest),
            ('John Deo','johnde12@gmail.com',1425632145,'10809125','Male','NA',35,'1990-02-03','',ptest),
        ]
        cur.executemany("""INSERT INTO tbluser
            (FullName,Email,MobileNumber,StudentID,Gender,Address,Age,DOB,Image,Password)
            VALUES (?,?,?,?,?,?,?,?,?,?)""", users)

    # Vacancies
    cur.execute("SELECT COUNT(*) FROM tblvacancy")
    if cur.fetchone()[0] == 0:
        vacancies = [
            (2,'Software Engineer/Senior Software Engineer C++','10K-25K',
             'Experience in C++, VC++, Windows or Linux. Strong programming and analytical skills. Image/Video Processing knowledge preferred.',
             '10','Noida','15-02-2024','16-12-2024'),
            (2,'Software Engineer, Senior Software Engineer, Module Lead','25k-35k',
             'Blue Prism Professionals role. Designing process solutions, configuring workflows, supporting existing processes.',
             '25','Noida','10-02-2024','31-12-2024'),
            (1,'SQL Server Database Administrator','15k-35k',
             'SQL Server DBA responsible for implementation, configuration, maintenance. 3-5 years experience required.',
             '10','Jhandewalan, Delhi','10-02-2024','31-12-2024'),
            (1,'Python Developer','10K-25K',
             'Good knowledge of Python, data structures, algorithms. Aggregate of 65 in Academics. Computer Science graduate.',
             '52','H-125 Bangalore','10-02-2024','31-12-2024'),
            (3,'Software Developer (Java/.Net/PHP)','25k-35k',
             'Full stack developer role. Design, implement and deliver new features. Strong architecture and design skills required.',
             '3','H-476 Noida Sector-12','10-02-2024','31-12-2024'),
            (3,'SQL QEUFM Software','10K-25K',
             'Python and data structures expertise needed. CS graduate with 65+ aggregate. Algorithm design skills required.',
             '12','K-12345 Sector 234 Bangalore','10-02-2024','31-12-2024'),
            (4,'Software Engineer/Senior Software Engineer C++','15k-35k',
             'C++ developer with strong programming, software design and architecture skills. Research in image/video processing a plus.',
             '10','H-321 Sector 4 Noida','10-02-2024','31-12-2024'),
            (5,'Web Developer','$25-30k',
             'PHP (Must), MySQL (Must). Knowledge of HTML, Bootstrap, and CSS required.',
             '2','New Delhi','10-02-2024','31-12-2024'),
            (5,'PHP Developer','125641',
             'Bachelor in CS. Knowledge of Laravel, CodeIgniter. Frontend: CSS3, JS, HTML5. OOP PHP, scalable apps.',
             '2','Noida','10-02-2024','31-12-2024'),
            (6,'WordPress Developer','2000-3000 USD',
             'WordPress Developer: Theme Customization, Plugin Development.',
             '6','Bangalore India','17-02-2024','30-08-2024'),
        ]
        cur.executemany("""INSERT INTO tblvacancy
            (CompanyID,JobTitle,MonthlySalary,JobDescriptions,NoofOpenings,JobLocation,ApplyDate,LastDate)
            VALUES (?,?,?,?,?,?,?,?)""", vacancies)

    # Applications
    cur.execute("SELECT COUNT(*) FROM tblapplyjob")
    if cur.fetchone()[0] == 0:
        apps = [
            (1,1,'resume1.pdf','Comes with original documents','Sorted'),
            (1,2,'resume2.pdf','','Rejected'),
            (2,2,'resume3.pdf','Come with your original documents','Sorted'),
            (2,3,'resume4.pdf','','Sorted'),
            (1,1,'resume5.pdf','',''),
            (1,4,'resume6.pdf','This is sample text for testing.','Rejected'),
            (1,7,'resume7.pdf','',''),
            (5,8,'resume8.doc','',''),
            (6,8,'resume9.doc','',''),
            (6,9,'resume10.doc','Your application is sort listed.','Sorted'),
            (6,1,'resume11.pdf','Your are selected for this position. CONGRATS','Selected'),
            (7,10,'resume12.pdf','Congrats, Your are selected for the job.','Selected'),
        ]
        cur.executemany("""INSERT INTO tblapplyjob (UserId,JobId,Resume,Message,Status) VALUES (?,?,?,?,?)""", apps)

    # Education
    cur.execute("SELECT COUNT(*) FROM tbleducation")
    if cur.fetchone()[0] == 0:
        edu = [
            (1,'CBSE','2010','80','8','CBSE','2012','76','7.6','B.Tech','2016','75','7.5','NA','NA','NA','NA','NA','NA'),
            (5,'CBSE','2010','80','8','CBSE','2012','76','7.6','B.Tech','2016','75','7.5','NA','NA','NA','NA','NA','NA'),
            (6,'CBSE','2015','91','9','CBSE','2017','85','8','LPU','2021','75','7','LPU','2023','75','7','NA','NA'),
            (7,'CBSE','2008','85','8','CBSE','2010','90','9','BITS Pilani','2014','74','7','BITS Pilani','2016','85','8','NA','NA'),
        ]
        cur.executemany("""INSERT INTO tbleducation
            (UserID,SecondaryBoard,SecondaryBoardyop,SecondaryBoardper,SecondaryBoardcgpa,
             SSecondaryBoard,SSecondaryBoardyop,SSecondaryBoardper,SSecondaryBoardcgpa,
             GraUni,GraUniyop,GraUnidper,GraUnicgpa,
             PGUni,PGUniyop,PGUniper,PGUnicgpa,ExtraCurriculars,OtherAchivement)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", edu)

    # Pages (About + Contact)
    cur.execute("SELECT COUNT(*) FROM tblpage")
    if cur.fetchone()[0] == 0:
        cur.execute("""INSERT INTO tblpage (PageType,PageTitle,PageDescription,Email,MobileNumber) VALUES
            ('aboutus','About Us',
             'We are a professional placement services organization. Campus to Career is a prominent Recruitment Firm offering out-of-the-box campus recruitment solutions to institutes and colleges. With a vision to explore and harness the talents of young leaders, we have come up with a concept of campus recruitment and promotion of institutes and colleges looking to place their fresh candidates.',
             NULL, NULL)""")
        cur.execute("""INSERT INTO tblpage (PageType,PageTitle,PageDescription,Email,MobileNumber) VALUES
            ('contactus','Contact Us','H-126, By-Pass Road, New Delhi India','info@campus.com',8988858695)""")

    # Messages
    cur.execute("SELECT COUNT(*) FROM tblmessage")
    if cur.fetchone()[0] == 0:
        msgs = [
            (4,'Application sorted. Ready for next round.','Sorted','1'),
            (6,'Application rejected.','Rejected','1'),
            (11,'Your application is sort listed.','Sorted','1'),
            (11,'Congrats, you are selected for this position!','Selected','1'),
            (12,'You are sort listed for the next round.','Sorted','1'),
            (12,'Congrats, you are selected for the job!','Selected','1'),
        ]
        cur.executemany("INSERT INTO tblmessage (AppID,Message,Status,IsRead) VALUES (?,?,?,?)", msgs)

    conn.commit()
    print("✅ Database created and seeded successfully!")
    print("\nLogin credentials:")
    print("  Admin   → username: admin         | password: Test@1234")
    print("  Company → email: infosys@gmail.com | password: 123")
    print("  User    → email: rahul@gmail.com   | password: 123")


if __name__ == '__main__':
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("🗑️  Old database removed.")
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    seed(conn)
    conn.close()
