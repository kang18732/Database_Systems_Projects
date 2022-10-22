import random                   # random과 string 라이브러리는 임의의 13자리 수 계좌번호를 생성하기 위해 필요
import string
import pymysql as pms
from getpass import getpass     # 비밀번호를 입력받을 때 비밀번호가 노출되지 않게 해주는 getpass 함수를 가지는 라이브러리

print("Accessing Bank Database ... ")
pw = getpass("Enter password: ")        # mysql에 접속하기 위해 비밀번호를 미리 입력받음.

connection = pms.connect(
    host='localhost',
    port=3306,
    user='root',
    password=pw,
    charset='utf8mb4',
    db='Bank'                   # 생성한 Bank 데이터베이스에 접근.
)

try:
    with connection.cursor() as cursor:
        sql = """CREATE TABLE IF NOT EXISTS ADMIN (
        AdminSsn CHAR(13) NOT NULL,
        Name VARCHAR(20) NOT NULL,
        Address VARCHAR(30),
        Phone CHAR(11),
        PRIMARY KEY (AdminSsn)
        )"""
        cursor.execute(sql)

        sql = """CREATE TABLE IF NOT EXISTS USER (
        Phone CHAR(11),
        NumOfAccounts INT NOT NULL default 0,
        Ssn CHAR(13) NOT NULL,
        Name VARCHAR(20) NOT NULL,
        Address VARCHAR(30),
        ASsn CHAR(13) NOT NULL,
        PRIMARY KEY (Ssn),
        FOREIGN KEY (ASsn) REFERENCES ADMIN(AdminSsn)
        )"""
        cursor.execute(sql)

        sql = """CREATE TABLE IF NOT EXISTS ACCOUNT (
        AccNum CHAR(13) NOT NULL,
        Password CHAR(4) NOT NULL,
        DepositLimit INT NOT NULL,
        WithdrawLimit INT NOT NULL,
        Dormant BOOLEAN NOT NULL default 0,
        AccountType VARCHAR(10) NOT NULL,
        AccSsn CHAR(13) NOT NULL,
        AdSsn CHAR(13) NOT NULL,
        PRIMARY KEY (AccNum),
        FOREIGN KEY (AccSsn) REFERENCES USER(Ssn) ON DELETE CASCADE,
        FOREIGN KEY (AdSsn) REFERENCES ADMIN(AdminSsn)
        )"""
        cursor.execute(sql)

        sql = """CREATE TABLE IF NOT EXISTS TRANSACTION (
        Date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        Amount INT NOT NULL,
        TransType VARCHAR(10) NOT NULL,
        TNum INT NOT NULL AUTO_INCREMENT,
        TSsn CHAR(13) NOT NULL,
        TAdSsn CHAR(13) NOT NULL,
        TAccNum CHAR(13) NOT NULL,
        PRIMARY KEY (TNum, TAccNum),
        FOREIGN KEY (TSsn) REFERENCES USER(Ssn) ON DELETE CASCADE,
        FOREIGN KEY (TAdSsn) REFERENCES ADMIN(AdminSsn),
        FOREIGN KEY (TAccNum) REFERENCES ACCOUNT(AccNum) ON DELETE CASCADE
        )"""
        cursor.execute(sql)
        connection.commit()

        print("\nDatabase Access Authorized.\n")

        while True:
            print("---------------------------------")
            print("1. Register User")
            print("2. Register Admin")
            print("3. Login as User")
            print("4. Login as Admin")
            print("5. Exit")
            start = input("Choose an instruction: ")

            if start == '1':
                while True:
                    print("---------------------------------")
                    print("Registering User...")
                    name = input("Name: ")                          # Name 입력 받음.
                    if len(name) > 20:                              # Name은 최대 20자리여야함.
                        print("---------------------------------")
                        print("Name must be within 20 characters.")
                        continue
                    ssn = input("Ssn (13 digits): ")                # Ssn 입력 받음.
                    if not (len(ssn) == 13 and ssn.isdigit()):      # Ssn은 13자리 숫자여야함.
                        print("---------------------------------")
                        print("Ssn must be a 13 digit number.")
                        continue
                    phone = input("Phone Number (11 digits): ")     # Phone 입력 받음.
                    if not (len(phone) == 11 and phone.isdigit()):  # Phone은 11자리 숫자여야함.
                        print("---------------------------------")
                        print("Phone number must be a 11 digit number.")
                        continue
                    address = input("Address: ")                    # Address 입력 받음.
                    if len(address) > 30:                           # Address는 최대 30자리여야함.
                        print("---------------------------------")
                        print("Address must be within 30 characters.")
                        continue

                    # ADMIN에서 튜플 하나를 무작위로 선정하고 튜플의 AdminSsn 값을 가져오는 SQL문.
                    sql = "SELECT AdminSsn FROM ADMIN ORDER BY rand() LIMIT 1"
                    cursor.execute(sql)
                    adssn = cursor.fetchall()
                    # USER 테이블에 튜플을 INSERT할 때 위에서 가져온 AdminSsn값을 튜플의 ASsn값으로 지정.
                    # USER 테이블에 INSERT한 튜플이 ADMIN 테이블의 튜플 하나를 참조하게 됨.
                    sql = "INSERT INTO USER(Name, Ssn, Phone, Address, ASsn) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(sql, (name, ssn, phone, address, adssn))
                    print("---------------------------------")
                    print("Register complete.")
                    connection.commit()
                    break
            elif start == '2':
                while True:
                    print("---------------------------------")
                    print("Registering Admin...")
                    ssn = input("Ssn (13 digits): ")                # AdminSsn 입력받음.
                    if not (len(ssn) == 13 and ssn.isdigit()):      # AdminSsn은 13자리 숫자여야함.
                        print("---------------------------------")
                        print("Ssn must be a 13 digit number.")
                        continue
                    name = input("Name: ")                          # Name 입력 받음.
                    if len(name) > 20:                              # Name은 최대 20자리여야함.
                        print("---------------------------------")
                        print("Name must be within 20 characters.")
                        continue
                    address = input("Address: ")                    # Address 입력 받음.
                    if len(address) > 30:                           # Address는 최대 30자리여야함.
                        print("---------------------------------")
                        print("Address must be within 30 characters.")
                        continue
                    phone = input("Phone Number (11 digits): ")     # Phone 입력 받음.
                    if not (len(phone) == 11 and phone.isdigit()):  # Phone은 11자리 숫자여야함.
                        print("---------------------------------")
                        print("Phone number must be a 11 digit number.")
                        continue
                    # ADMIN 테이블에 입력받은 정보들이 담긴 새로운 튜플 삽입.
                    sql = "INSERT INTO ADMIN(AdminSsn, Name, Address, Phone) VALUES (%s, %s, %s, %s)"
                    cursor.execute(sql, (ssn, name, address, phone))
                    print("---------------------------------")
                    print("Register complete.")
                    connection.commit()
                    break
            elif start == '3':
                print("---------------------------------")
                ssn = input("Enter Ssn: ")                      # 사용자로부터 Ssn을 입력 받음.
                sql = "SELECT Ssn FROM USER WHERE Ssn = %s"     # 사용자가 입력한 Ssn과 일치하는 Ssn을 갖는 튜플을 찾아서 Ssn값 반환.
                cursor.execute(sql, ssn)
                select = cursor.fetchall()
                if not select:                                  # 비어있는 row가 반환되면 사용자가 입력한 Ssn이 존재하지 않는다는 것이므로
                    print("---------------------------------")  # 등록되지 않은 사용자라는 메시지를 출력하고 다시 메뉴로 복귀.
                    print("You are not a registered user.")
                    continue
                sql = "SELECT Name FROM USER WHERE Ssn = %s"    # 사용자가 입력한 Ssn을 갖는 튜플의 Name값을 반환.
                cursor.execute(sql, ssn)
                select = cursor.fetchall()
                print("---------------------------------")
                print(f"Welcome, {select[0][0]}")               # Name값을 이용해 사용자를 맞이하는 문장 출력.
                while True:
                    print("---------------------------------")
                    print("1. Create Account")
                    print("2. Select Account")
                    print("3. Update User Info")
                    print("4. View User Info")
                    print("5. Delete User")
                    print("6. Exit")
                    login_user = input("Choose an instruction: ")

                    if login_user == '1':   # 계좌 생성
                        # 로그인한 사용자의 Ssn을 갖는 튜플에서 NumOfAccounts를 가져옴으로써 사용자의 계좌 수를 알아낸다.
                        sql = "SELECT NumOfAccounts FROM USER WHERE Ssn = %s"
                        cursor.execute(sql, ssn)
                        numOfAccounts = cursor.fetchall()
                        if numOfAccounts[0][0] >= 10:                   # 계좌 수가 10개 이상이면 계정 생성을 막는다.
                            print("---------------------------------")
                            print("You can only have 10 accounts maximum.")
                            continue
                        while True:
                            print("---------------------------------")
                            print("Creating account...")

                            # Password를 입력 받음. Password는 4자리 숫자여야함.
                            password = getpass("Password (4 digits): ")
                            if not(len(password) == 4 and password.isdigit()):
                                print("---------------------------------")
                                print("Password must be 4 digits.")
                                continue
                            # DepositLimit 입력 받음. DepositLimit은 숫자여야함.
                            depositLimit = input("Deposit Limit (for a single transaction): ")
                            if not depositLimit.isdigit():
                                print("---------------------------------")
                                print("Deposit Limit must be a number.")
                                continue
                            # WithdrawLimit 입력 받음. WithdrawLimit은 숫자여야함.
                            withdrawLimit = input("Withdrawal Limit (for a single transaction): ")
                            if not withdrawLimit.isdigit():
                                print("---------------------------------")
                                print("Withdrawal Limit must be a number.")
                                continue
                            # AccountType 입력 받음. AccountType은 'checking' 혹은 'savings' 둘 중 하나만 가능함.
                            accountType = input("Account Type (Type 'checking' or 'savings'): ")
                            if not (accountType == "checking" or accountType == "savings"):
                                print("---------------------------------")
                                print("Account Type must be either 'checking' or 'savings'.")
                                continue

                            while True:     # 중복되지 않는 계좌번호가 나올 때까지 while문 반복.
                                # 임의의 13자리 숫자로 된 문자열을 반환해주는 함수. 이 함수로 계좌번호를 생성한다.
                                accnum = ''.join(random.choice(string.digits) for _ in range(13))
                                # 임의로 생성한 계좌번호(AccNum)가 이미 ACCOUNT 테이블에 존재하는지 확인하는 sql문.
                                sql = "SELECT EXISTS (SELECT * FROM ACCOUNT WHERE AccNum = %s)"
                                cursor.execute(sql, accnum)
                                if not cursor.fetchall()[0][0]:     # 존재하지 않으면 while문 빠져나옴.
                                    break

                            # 로그인한 사용자의 ASsn을 반환. ASsn은 ADMIN의 AdminSsn을 참조하는 Foreign Key이다.
                            sql = "SELECT ASsn FROM USER WHERE Ssn = %s"
                            cursor.execute(sql, ssn)
                            adssn = cursor.fetchall()

                            sql = """INSERT INTO ACCOUNT(AccNum, Password, DepositLimit, WithdrawLimit,
                                    AccountType, AccSsn, AdSsn) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                            cursor.execute(sql, (accnum, password, depositLimit, withdrawLimit, accountType, ssn,
                                                 adssn))

                            # ACCOUNT 테이블에 튜플을 생성하면 사용자의 계좌가 하나 늘어난 것이므로 사용자의 NumOfAccounts 업데이트.
                            sql = "UPDATE USER SET NumOfAccounts = NumOfAccounts + 1 WHERE Ssn = %s"
                            cursor.execute(sql, ssn)
                            print("---------------------------------")
                            print("Account successfully created.")
                            print(f"Your account number: {accnum}")
                            connection.commit()
                            break
                    elif login_user == '2':
                        print("---------------------------------")
                        sql = "SELECT AccNum, DepositLimit, WithdrawLimit, Dormant, AccountType FROM ACCOUNT WHERE " \
                              "AccSsn = %s"
                        cursor.execute(sql, ssn)
                        select = cursor.fetchall()
                        print("{:<15} {:<20} {:<20} {:<15} {:<20}".format("Account Number", "Deposit Limit",
                                                                          "Withdrawal Limit", "Status", "Account Type"))
                        for row in select:      # Dormant값이 0이면 Active, 1이면 Dormant인 상태.
                            if row[3] == 0:
                                status = "Active"
                            else:
                                status = "Dormant"
                            print("{:<15} {:<20} {:<20} {:<15} {:<20}".format(row[0], row[1], row[2], status, row[4]))
                        print("---------------------------------")

                        accnum = input("Enter account number: ")        # 계좌번호를 입력 받음.
                        sql = "SELECT AccNum FROM ACCOUNT WHERE AccNum = %s"  # 입력한 계좌번호와 일치하는 AccNum 찾아서 반환.
                        cursor.execute(sql, accnum)
                        select = cursor.fetchall()
                        if not select:                                  # 일치하는 AccNum이 없으면 직전 메뉴로 복귀.
                            print("---------------------------------")
                            print("Wrong account number.")
                            continue
                        password = getpass("Enter password: ")          # 비밀번호를 입력 받음.
                        sql = "SELECT Password FROM ACCOUNT WHERE Accnum = %s"  # 선택한 계좌의 Password를 반환.
                        cursor.execute(sql, accnum)
                        select = cursor.fetchall()
                        if password != select[0][0]:            # 입력한 비밀번호가 계좌의 Password와 일치하지 않으면 직전 메뉴로 복귀.
                            print("---------------------------------")
                            print("Wrong password.")
                            continue
                        while True:                             # 비밀번호가 계좌의 Password와 일치하면 다음 메뉴로 진행.
                            print("---------------------------------")
                            print("1. Deposit")
                            print("2. Withdrawal")
                            print("3. Check Balance")
                            print("4. View Transactions")
                            print("5. Update Account Info")
                            print("6. Delete Account")
                            print("7. Exit")
                            trans = input("Choose instruction: ")

                            # TRANSACTION의 튜플 중에서 입력받은 계좌번호와 TAccNum이 일치하고 TransType(거래 종류)가 Deposit(입금)에
                            # 해당하는 튜플들을 골라 Amount(금액)의 합산을 구함.
                            sql = "SELECT SUM(Amount) FROM TRANSACTION WHERE TAccNum = %s AND TransType = 'Deposit'"
                            cursor.execute(sql, accnum)
                            deposit = cursor.fetchall()[0][0]
                            # TRANSACTION의 튜플 중에서 입력받은 계좌번호와 TAccNum이 일치하고 TransType(거래 종류)가 Withdrawal(출금)에
                            # 해당하는 튜플들을 골라 Amount(금액)의 합산을 구함.
                            sql = "SELECT SUM(Amount) FROM TRANSACTION WHERE TAccNum = %s AND TransType = 'Withdrawal'"
                            cursor.execute(sql, accnum)
                            withdraw = cursor.fetchall()[0][0]

                            balance = 0                         # 입금과 출금 모두 없다면 balance(잔액)은 0.
                            if deposit and withdraw:            # 입금과 출금 둘다 존재하면 balance는 입금 금액에서 출금 금액을 뺀 값.
                                balance = deposit - withdraw
                            elif deposit:                       # 입금만 존재하고 출금 기록은 없다면 balance는 입금 금액의 합산임.
                                balance = deposit

                            if trans == "1":
                                print("---------------------------------")
                                deposit = input("Enter deposit amount: ")       # Amount(입금 금액)을 입력 받음.
                                if not deposit.isdigit():                       # 숫자가 아니라면 continue.
                                    print("---------------------------------")
                                    print("Deposit amount must be a number.")
                                    continue
                                sql = "SELECT DepositLimit FROM ACCOUNT WHERE AccNum = %s"  # 계좌의 입금 한도 확인
                                cursor.execute(sql, accnum)
                                depositLimit = cursor.fetchall()[0][0]
                                if int(deposit) > depositLimit:                 # 입금 금액이 한도를 초과하면 continue.
                                    print("---------------------------------")
                                    print("Deposit amount exceeds Deposit Limit.")
                                    continue

                                # ASsn은 USER가 참조하는 ADMIN의 AdminSsn. TRANSACTION의 TAdSsn은 ADMIN을 참조하는 Foreign
                                # Key인데, TAdSsn을 USER의 ASsn으로 지정함으로써 TRANSACTION과 USER 모두 같은 ADMIN을 가리키게 함.
                                sql = "SELECT ASsn FROM USER WHERE Ssn = %s"
                                cursor.execute(sql, ssn)
                                adssn = cursor.fetchall()
                                sql = "INSERT INTO TRANSACTION (Amount, TransType, TSsn, TAdSsn, TAccNum) VALUES" \
                                      "(%s, %s, %s, %s, %s)"
                                # 입금이므로 TransType은 Deposit
                                cursor.execute(sql, (deposit, "Deposit", ssn, adssn, accnum))
                                connection.commit()
                            elif trans == "2":
                                print("---------------------------------")
                                withdraw = input("Enter withdrawal amount: ")       # Amount(출금 금액)을 입력 받음.
                                if not withdraw.isdigit():                          # 숫자가 아니라면 continue.
                                    print("---------------------------------")
                                    print("Withdrawal amount must be a number.")
                                    continue
                                sql = "SELECT WithdrawLimit FROM ACCOUNT WHERE AccNum = %s"     # 계좌의 출금 한도 확인
                                cursor.execute(sql, accnum)
                                withdrawLimit = cursor.fetchall()[0][0]
                                if balance - int(withdraw) < 0:                     # 출금 금액이 balance보다 크면 continue.
                                    print("---------------------------------")
                                    print("Withdrawal amount exceeds balance.")
                                    continue
                                if int(withdraw) > withdrawLimit:                   # 입금 금액이 한도를 초과하면 continue.
                                    print("---------------------------------")
                                    print("Withdrawal amount exceeds Withdraw Limit.")
                                    continue

                                # ASsn은 USER가 참조하는 ADMIN의 AdminSsn. TRANSACTION의 TAdSsn은 ADMIN을 참조하는 Foreign
                                # Key인데, TAdSsn을 USER의 ASsn으로 지정함으로써 TRANSACTION과 USER 모두 같은 ADMIN을 가리키게 함.
                                sql = "SELECT ASsn FROM USER WHERE Ssn = %s"
                                cursor.execute(sql, ssn)
                                adssn = cursor.fetchall()
                                sql = """INSERT INTO TRANSACTION (Amount, TransType, TSsn, TAdSsn, TAccNum) VALUES
                                        (%s, %s, %s, %s, %s)"""
                                # 출금이므로 TransType은 Withdrawal
                                cursor.execute(sql, (withdraw, "Withdrawal", ssn, adssn, accnum))
                                connection.commit()
                            elif trans == "3":
                                print("---------------------------------")
                                print(f"Balance: {balance}")
                            elif trans == "4":
                                print("---------------------------------")
                                # 선택한 계좌의 AccNum과 TRANSACTION 튜플들의 TAccNum을 비교하고 일치하면 금액, 거래종류, 거래일시를 가져옴.
                                sql = "SELECT Amount, TransType, Date FROM TRANSACTION WHERE TAccNum = %s"
                                cursor.execute(sql, accnum)
                                select = cursor.fetchall()
                                print("{:<10} {:<20} {:<25}".format("Amount", "Transaction Type", "Date"))
                                for row in select:
                                    print("{:<10} {:<20} {:<25}".format(row[0], row[1], str(row[2])))
                            elif trans == "5":
                                while True:
                                    print("---------------------------------")
                                    print("1. Update Password")
                                    print("2. Update Deposit Limit")
                                    print("3. Update Withdrawal Limit")
                                    print("4. Update Account Type")
                                    print("5. Exit")
                                    update_account = input("Choose instruction: ")

                                    if update_account == '1':
                                        password = getpass("Password (4 digits): ")         # Password 입력 받음.
                                        if not (len(password) == 4 and password.isdigit()):   # 4자리 숫자가 아니면 continue.
                                            print("---------------------------------")
                                            print("Password must be 4 digits.")
                                            continue
                                        # ACCOUNT 테이블에서 선택한 계좌에 해당하는 튜플 찾아서 Password를 변경함.
                                        sql = "UPDATE ACCOUNT SET Password = %s WHERE AccNum = %s"
                                        cursor.execute(sql, (password, accnum))
                                        print("---------------------------------")
                                        print("Password updated.")
                                    elif update_account == '2':
                                        # DepositLimit 입력 받음. 숫자가 아니면 continue.
                                        depositLimit = input("Deposit Limit (for a single transaction): ")
                                        if not depositLimit.isdigit():
                                            print("---------------------------------")
                                            print("Deposit Limit must be a number.")
                                            continue
                                        # ACCOUNT 테이블에서 선택한 계좌에 해당하는 튜플 찾아서 DepositLimit을 변경함.
                                        sql = "UPDATE ACCOUNT SET DepositLimit = %s WHERE AccNum = %s"
                                        cursor.execute(sql, (depositLimit, accnum))
                                        print("---------------------------------")
                                        print("Deposit Limit updated.")
                                    elif update_account == '3':
                                        # WithdrawLimit 입력 받음. 숫자가 아니면 continue.
                                        withdrawLimit = input("Withdrawal Limit (for a single transaction): ")
                                        if not withdrawLimit.isdigit():
                                            print("---------------------------------")
                                            print("Withdrawal Limit must be a number.")
                                            continue
                                        # ACCOUNT 테이블에서 선택한 계좌에 해당하는 튜플 찾아서 WithdrawLimit을 변경함.
                                        sql = "UPDATE ACCOUNT SET WithdrawLimit = %s WHERE AccNum = %s"
                                        cursor.execute(sql, (withdrawLimit, accnum))
                                        print("---------------------------------")
                                        print("Withdrawal Limit updated.")
                                    elif update_account == '4':
                                        # AccountType 입력 받음. 'checking' 혹은 'savings'가 아니면 continue.
                                        accountType = input("Account Type (Type 'checking' or 'savings'): ")
                                        if not (accountType == "checking" or accountType == "savings"):
                                            print("---------------------------------")
                                            print("Account Type must be either 'checking' or 'savings'.")
                                            continue
                                        # ACCOUNT 테이블에서 선택한 계좌에 해당하는 튜플 찾아서 AccountType을 변경함.
                                        sql = "UPDATE ACCOUNT SET AccountType = %s WHERE AccNum = %s"
                                        cursor.execute(sql, (accountType, accnum))
                                        print("---------------------------------")
                                        print("Account Type updated.")
                                    elif update_account == '5':
                                        connection.commit()     # mysql에 반영하고 while문 빠져나옴.
                                        break
                                    else:
                                        print("---------------------------------")
                                        print("Not valid instruction.")
                            elif trans == "6":
                                print("---------------------------------")
                                # ACCOUNT 테이블에서 선택한 계좌에 해당하는 튜플 찾아서 삭제.
                                sql = "DELETE FROM ACCOUNT WHERE AccNum = %s"
                                cursor.execute(sql, accnum)
                                # USER 테이블에서 로그인한 사용자에 해당하는 튜플 찾아서 NumOfAccounts를 1만큼 감소시킴.
                                sql = "UPDATE USER SET NumOfAccounts = NumOfAccounts - 1 WHERE Ssn = %s"
                                cursor.execute(sql, ssn)
                                print("Account deleted.")
                                connection.commit()
                                break
                            elif trans == "7":
                                break
                            else:
                                print("---------------------------------")
                                print("Not valid instruction.")
                    elif login_user == '3':
                        while True:
                            print("---------------------------------")
                            print("1. Update Phone Number")
                            print("2. Update Address")
                            print("3. Update Name")
                            print("4. Exit")
                            update_user = input("Choose instruction: ")

                            if update_user == "1":
                                print("---------------------------------")
                                phone = input("Enter phone number: ")               # Phone 입력 받음.
                                if not (len(phone) == 11 and phone.isdigit()):      # 11자리 숫자가 아니면 continue.
                                    print("---------------------------------")
                                    print("Phone number must be a 11 digit number.")
                                    continue
                                # USER 테이블에서 로그인한 사용자에 해당하는 튜플을 찾아서 Phone을 변경함.
                                sql = "UPDATE USER SET Phone = %s WHERE Ssn = %s"
                                cursor.execute(sql, (phone, ssn))
                                print("---------------------------------")
                                print("Phone number updated.")
                            elif update_user == "2":
                                print("---------------------------------")
                                address = input("Enter address: ")                  # Address 입력 받음.
                                if len(address) > 30:                               # 30자리 초과하면 continue.
                                    print("---------------------------------")
                                    print("Address must be within 30 characters.")
                                    continue
                                # USER 테이블에서 로그인한 사용자에 해당하는 튜플을 찾아서 Address를 변경함.
                                sql = "UPDATE USER SET Address = %s WHERE Ssn = %s"
                                cursor.execute(sql, (address, ssn))
                                print("---------------------------------")
                                print("Address updated.")
                            elif update_user == "3":
                                print("---------------------------------")
                                name = input("Enter name: ")                        # Name 입력 받음.
                                if len(name) > 20:                                  # 20자리 초과하면 continue.
                                    print("---------------------------------")
                                    print("Name must be within 20 characters.")
                                    continue
                                # USER 테이블에서 로그인한 사용자에 해당하는 튜플을 찾아서 Name을 변경함.
                                sql = "UPDATE USER SET Name = %s WHERE Ssn = %s"
                                cursor.execute(sql, (name, ssn))
                                print("---------------------------------")
                                print("Name updated.")
                            elif update_user == "4":
                                connection.commit()     # mysql에 반영하고 while문 빠져나옴.
                                break
                            else:
                                print("---------------------------------")
                                print("Invalid instruction.")
                    elif login_user == '4':
                        print("---------------------------------")
                        # USER 테이블에서 로그인한 사용자에 해당하는 튜플을 찾아서 이름, 주민번호, 계좌 수, 전화번호, 주소를 가져옴.
                        sql = "SELECT Name, Ssn, NumOfAccounts, Phone, Address FROM USER WHERE Ssn = %s"
                        cursor.execute(sql, ssn)
                        print("{:<25} {:<15} {:<20} {:<13} {:<35}".format("Name", "Ssn", "Number of Accounts",
                                                                          "Phone Number", "Address"))
                        info = cursor.fetchall()[0]
                        print("{:<25} {:<15} {:<20} {:<13} {:<35}".format(info[0], info[1], info[2], info[3], info[4]))
                    elif login_user == '5':
                        print("---------------------------------")
                        # USER 테이블에서 로그인한 사용자에 해당하는 튜플을 찾아서 삭제함.
                        sql = "DELETE FROM USER WHERE Ssn = %s"
                        cursor.execute(sql, ssn)
                        print("User deleted.")
                        connection.commit()
                        break
                    elif login_user == '6':
                        break
                    else:
                        print("---------------------------------")
                        print("Not valid instruction.")
            elif start == '4':
                print("---------------------------------")
                adssn = input("Enter Ssn: ")        # 관리자의 AdminSsn을 입력으로 받아서 adssn에 저장.
                # ADMIN 테이블에서 adssn과 일치하는 AdminSsn을 갖는 튜플이 있다면 그 튜플의 AdminSsn 반환.
                sql = "SELECT AdminSsn FROM ADMIN WHERE AdminSsn = %s"
                cursor.execute(sql, adssn)
                select = cursor.fetchall()
                if not select:                      # AdminSsn 일치하는 튜플 없다면 등록된 관리자가 아니므로 continue.
                    print("---------------------------------")
                    print("You are not a registered admin.")
                    continue
                # ADMIN 테이블에서 로그인한 관리자에 해당하는 튜플에서 Name을 가져옴.
                sql = "SELECT Name FROM ADMIN WHERE AdminSsn = %s"
                cursor.execute(sql, adssn)
                select = cursor.fetchall()
                print("---------------------------------")
                print(f"Welcome, {select[0][0]}")           # Name을 이용해서 관리자를 맞이하는 문구 출력.
                while True:
                    print("---------------------------------")
                    print("1. View Managing Users")
                    print("2. Update Admin Info")
                    print("3. View Admin Info")
                    print("4. Delete Admin")
                    print("5. Exit")
                    login_admin = input("Choose instruction: ")

                    if login_admin == '1':
                        while True:
                            print("---------------------------------")
                            # USER 테이블에서 ASsn이 관리자의 AdminSsn과 일치하는 튜플들을 찾아서 이름, 주민번호, 계좌 수, 전화번호, 주소 가져옴.
                            sql = "SELECT Name, Ssn, NumOfAccounts, Phone, Address FROM USER WHERE ASsn = %s"
                            cursor.execute(sql, adssn)

                            select = cursor.fetchall()
                            print("{:<25} {:<15} {:<20} {:<13} {:<35}".format("Name", "Ssn", "Number of Accounts",
                                                                              "Phone Number", "Address"))
                            for row in select:
                                print("{:<25} {:<15} {:<20} {:<13} {:<35}".format(row[0], row[1], row[2], row[3],
                                                                                  row[4]))
                            print("---------------------------------")
                            print("1. Select User")
                            print("2. Delete User")
                            print("3. Exit")
                            select_user = input("Choose instruction: ")
                            if select_user == '1':
                                print("---------------------------------")
                                user_ssn = input("Enter User Ssn to select user: ")     # 관리하는 사용자의 Ssn을 입력 받음.
                                # 입력받은 사용자의 Ssn을 가지는 튜플이 USER 테이블에 존재하는지 확인.
                                sql = "SELECT EXISTS (SELECT * FROM USER WHERE Ssn = %s)"
                                cursor.execute(sql, user_ssn)
                                if not cursor.fetchall()[0][0]:                 # 존재하지 않으면 continue.
                                    print("---------------------------------")
                                    print("User does not exist.")
                                    continue
                                while True:
                                    print("---------------------------------")
                                    print("1. View Accounts")
                                    print("2. View Transactions")
                                    print("3. Set Account Status (Dormant or Active)")
                                    print("4. Delete Account")
                                    print("5. Exit")
                                    admin_user = input("Choose instruction: ")

                                    if admin_user == '1':
                                        print("---------------------------------")
                                        # ACCOUNT 테이블에서 선택한 사용자에 해당하는 튜플들을 골라서
                                        # 계좌번호, 입금한도, 출금한도, 휴면 여부, 계좌 종류를 가져옴.
                                        sql = """SELECT AccNum, DepositLimit, WithdrawLimit, Dormant, AccountType
                                                FROM ACCOUNT WHERE AccSsn = %s"""
                                        cursor.execute(sql, user_ssn)

                                        select = cursor.fetchall()
                                        print("{:<15} {:<20} {:<20} {:<15} {:<20}".format("Account Number",
                                                                                          "Deposit Limit",
                                                                                          "Withdrawal Limit",
                                                                                          "Status", "Account Type"))
                                        # Dormant(휴면 여부)가 0이면 Active, 1이면 Dormant로 표시.
                                        for row in select:
                                            if row[3] == 0:
                                                status = "Active"
                                            else:
                                                status = "Dormant"
                                            print("{:<15} {:<20} {:<20} {:<15} {:<20}".format(row[0], row[1], row[2],
                                                                                              status, row[4]))
                                    elif admin_user == '2':
                                        print("---------------------------------")
                                        # TRANSACTION 테이블에서 선택한 사용자에 해당하는 튜플들을 골라서
                                        # 계좌번호, 금액, 거래 종류, 거래 일시를 가져옴.
                                        sql = "SELECT TAccNum, Amount, TransType, Date FROM TRANSACTION WHERE TSsn = %s"
                                        cursor.execute(sql, user_ssn)

                                        select = cursor.fetchall()
                                        print("{:<20} {:<10} {:<20} {:<25}".format("Account Number", "Amount",
                                                                                   "Transaction Type", "Date"))
                                        for row in select:
                                            print("{:<20} {:<10} {:<20} {:<25}".format(row[0], row[1], row[2],
                                                                                       str(row[3])))
                                    elif admin_user == '3':
                                        print("---------------------------------")
                                        # 휴면 여부 설정하기 전 사용자가 가지고 있는 계좌 목록을 계좌번호와 최근 거래일시와 함께 출력함.

                                        # ACCOUNT 테이블에서 선택한 사용자에 해당하는 튜플들을 골라서 계좌번호를 가져옴.
                                        sql = "SELECT AccNum FROM ACCOUNT WHERE AccSsn = %s"
                                        cursor.execute(sql, user_ssn)
                                        accounts = cursor.fetchall()
                                        # 각 계좌의 계좌번호와 마지막 거래 시간을 출력.
                                        print("{:<20} {:<20}".format("Account Number", "Last Transaction"))
                                        for account in accounts:
                                            # TRANSACTION 테이블에서 각 계좌의 계좌번호와 거래일시를 가져옴. 거래는 TNum이 클수록
                                            # 나중에 이루어진 것이므로 DESC과 LIMIT 1을 통해 TNum이 가장 큰 하나만 가져옴.
                                            sql = "SELECT TAccNum, Date FROM TRANSACTION WHERE TAccNum = %s " \
                                                  "ORDER BY TNum DESC LIMIT 1"
                                            cursor.execute(sql, account[0])
                                            select = cursor.fetchall()
                                            if select:
                                                row = select[0]
                                                print("{:<20} {:<20}".format(row[0], str(row[1])))
                                            else:   # 거래가 아직 안 이루어졌다면 No Transaction 출력.
                                                print("{:<20} {:<20}".format(account[0], "No Transaction"))
                                        print("---------------------------------")
                                        acc_num = input("Enter Account Number: ")       # 계좌번호 입력 받음.
                                        if not (len(acc_num) == 13 and acc_num.isdigit()):
                                            print("---------------------------------")
                                            print("Account Number must be a 13 digit number.")
                                            continue
                                        # ACCOUNT 테이블에서 관리자가 선택한 사용자의 계좌들 중에서 입력받은 계좌가 존재하는지 확인.
                                        sql = "SELECT EXISTS (SELECT * FROM ACCOUNT WHERE AccSsn = %s AND " \
                                              "AccNum = %s)"
                                        cursor.execute(sql, (user_ssn, acc_num))
                                        if not cursor.fetchall()[0][0]:                 # 존재하지 않으면 continue.
                                            print("---------------------------------")
                                            print("Account does not exist.")
                                            continue
                                        status = input("Enter status (0 for Active, 1 for Dormant): ")
                                        if not (status == '0' or status == '1'):
                                            print("---------------------------------")
                                            print("Type only 0 or 1.")
                                            continue

                                        # ACCOUNT 테이블에서 계좌를 찾아 계좌의 휴면 여부를 0 또는 1의 int값으로 설정.
                                        sql = "UPDATE ACCOUNT SET Dormant = %s WHERE AccNum = %s"
                                        cursor.execute(sql, (int(status), acc_num))
                                        print("---------------------------------")
                                        print("Account Status Updated.")
                                        connection.commit()
                                    elif admin_user == '4':
                                        print("---------------------------------")
                                        acc_num = input("Enter Account Number: ")           # 계좌번호 입력 받음.
                                        if not (len(acc_num) == 13 and acc_num.isdigit()):
                                            print("---------------------------------")
                                            print("Account Number must be a 13 digit number.")
                                            continue
                                        # ACCOUNT 테이블에서 관리자가 선택한 사용자의 계좌들 중에서 입력받은 계좌가 존재하는지 확인.
                                        sql = "SELECT EXISTS (SELECT * FROM ACCOUNT WHERE AccSsn = %s AND " \
                                              "AccNum = %s)"
                                        cursor.execute(sql, (user_ssn, acc_num))
                                        if not cursor.fetchall()[0][0]:
                                            print("---------------------------------")
                                            print("Account does not exist.")
                                            continue

                                        # ACCOUNT 테이블 내에서 해당 계좌를 삭제.
                                        sql = "DELETE FROM ACCOUNT WHERE AccNum = %s"
                                        cursor.execute(sql, acc_num)
                                        # USER 테이블에서 관리자가 선택한 사용자를 찾아 계좌 수를 하나 줄임.
                                        sql = "UPDATE USER SET NumOfAccounts = NumOfAccounts - 1 WHERE Ssn = %s"
                                        cursor.execute(sql, user_ssn)
                                        print("---------------------------------")
                                        print("Account Deleted.")
                                        connection.commit()
                                    elif admin_user == '5':
                                        break
                                    else:
                                        print("---------------------------------")
                                        print("Not valid instruction.")
                            elif select_user == '2':
                                print("---------------------------------")
                                user_ssn = input("Enter User Ssn to delete user: ")         # 삭제할 사용자 Ssn 입력받음.
                                # USER 테이블 내에 입력받은 Ssn을 가지는 사용자가 존재하는지 확인.
                                sql = "SELECT EXISTS (SELECT * FROM USER WHERE Ssn = %s)"
                                cursor.execute(sql, user_ssn)
                                if not cursor.fetchall()[0][0]:
                                    print("---------------------------------")
                                    print("User does not exist.")
                                    continue

                                # USER 테이블에서 해당 사용자를 삭제.
                                sql = "DELETE FROM USER WHERE Ssn = %s"
                                cursor.execute(sql, user_ssn)
                                print("---------------------------------")
                                print("User Deleted.")
                                connection.commit()
                            elif select_user == '3':
                                break
                            else:
                                print("---------------------------------")
                                print("Not valid instruction.")
                    elif login_admin == '2':
                        while True:
                            print("---------------------------------")
                            print("1. Update Phone Number")
                            print("2. Update Address")
                            print("3. Update Name")
                            print("4. Exit")
                            update_admin = input("Choose instruction: ")

                            if update_admin == "1":
                                print("---------------------------------")
                                phone = input("Enter phone number: ")               # 전화번호를 입력받음.
                                if not (len(phone) == 11 and phone.isdigit()):      # 전화번호는 11자리 숫자여야함.
                                    print("---------------------------------")
                                    print("Phone number must be a 11 digit number.")
                                    continue
                                # ADMIN 테이블에서 해당 관리자 찾아서 Phone(전화번호)를 변경함.
                                sql = "UPDATE ADMIN SET Phone = %s WHERE AdminSsn = %s"
                                cursor.execute(sql, (phone, adssn))
                                print("---------------------------------")
                                print("Phone number updated.")
                            elif update_admin == "2":
                                print("---------------------------------")
                                address = input("Enter address: ")                  # 주소를 입력받음.
                                if len(address) > 30:                               # 주소는 30자리를 초과하면 안됨.
                                    print("---------------------------------")
                                    print("Address must be within 30 characters.")
                                    continue
                                # ADMIN 테이블에서 해당 관리자 찾아서 Address(주소)를 변경함.
                                sql = "UPDATE ADMIN SET Address = %s WHERE AdminSsn = %s"
                                cursor.execute(sql, (address, adssn))
                                print("---------------------------------")
                                print("Address updated.")
                            elif update_admin == "3":
                                print("---------------------------------")
                                name = input("Enter name: ")                        # 이름을 입력받음.
                                if len(name) > 20:                                  # 이름은 20자리를 초과하면 안됨.
                                    print("---------------------------------")
                                    print("Name must be within 20 characters.")
                                    continue
                                # ADMIN 테이블에서 해당 관리자 찾아서 Name(이름)을 변경함.
                                sql = "UPDATE ADMIN SET Name = %s WHERE AdminSsn = %s"
                                cursor.execute(sql, (name, adssn))
                                print("---------------------------------")
                                print("Name updated.")
                            elif update_admin == "4":
                                connection.commit()
                                break
                            else:
                                print("---------------------------------")
                                print("Invalid instruction.")
                    elif login_admin == '3':
                        print("---------------------------------")
                        # ADMIN 테이블에서 해당 관리자 찾아서 이름, 사원번호, 전화번호, 주소 가져옴.
                        sql = "SELECT Name, AdminSsn, Phone, Address FROM ADMIN WHERE AdminSsn = %s"
                        cursor.execute(sql, adssn)
                        print("{:<25} {:<15} {:<13} {:<35}".format("Name", "Ssn", "Phone Number", "Address"))
                        info = cursor.fetchall()[0]
                        print("{:<25} {:<15} {:<13} {:<35}".format(info[0], info[1], info[2], info[3]))
                    elif login_admin == '4':
                        print("---------------------------------")
                        sql = "SELECT COUNT(*) FROM ADMIN"          # ADMIN 테이블에 있는 튜플의 개수를 반환.
                        cursor.execute(sql)
                        count = cursor.fetchall()[0][0]
                        if count == 1:                              # 한 개밖에 없다면 continue.
                            print("There should be at least 1 Admin.")
                            continue

                        while True:     # 관리자가 삭제되면 그가 관리하던 모든 튜플들의 관리자가 바뀌어야 하므로 새로운 관리자를 찾아서 지정.
                            # ADMIN 테이블 내에서 무작위로 관리자를 뽑아 AdminSsn을 가져옴.
                            sql = "SELECT AdminSsn FROM ADMIN ORDER BY rand() LIMIT 1"
                            cursor.execute(sql)
                            new_admin = cursor.fetchall()[0][0]
                            if adssn != new_admin:
                                break

                        # USER, ACCOUNT, TRANSACTION 테이블에서 참조하는 관리자가 삭제되는 튜플들의 관리자를 변경해줌.
                        sql = "UPDATE USER SET ASsn = %s WHERE ASsn = %s"
                        cursor.execute(sql, (new_admin, adssn))
                        sql = "UPDATE ACCOUNT SET AdSsn = %s WHERE AdSsn = %s"
                        cursor.execute(sql, (new_admin, adssn))
                        sql = "UPDATE TRANSACTION SET TAdSsn = %s WHERE TAdSsn = %s"
                        cursor.execute(sql, (new_admin, adssn))
                        # ADMIN 테이블에서 해당 관리자를 찾아 삭제.
                        sql = "DELETE FROM ADMIN WHERE AdminSsn = %s"
                        cursor.execute(sql, adssn)
                        print("Admin Deleted.")
                        connection.commit()
                        break
                    elif login_admin == '5':
                        break
                    else:
                        print("---------------------------------")
                        print("Not valid instruction.")
            elif start == '5':
                break
            else:
                print("---------------------------------")
                print("Not valid instruction.")

        connection.commit()
finally:
    connection.close()
