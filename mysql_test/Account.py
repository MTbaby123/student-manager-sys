#-*- coding:utf-8 -*-
import sqlite3
from xmlrpclib import SafeTransport

cx = sqlite3.connect('Account.db')
print "Opened database successfully";

#在该数据库下创建客户信息表
cx.execute('''CREATE TABLE Customer
   (id SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
   AccountID    SMALLINT UNSIGNED NOT NULL   UNIQUE KEY,
   Name           VARCHAR(30)    NOT NULL,
   Sex            SMALLINT UNSIGNED     NOT NULL,
   Birth          INT UNSIGNED ,
   PhoneNum         INT(11));''')
print "Table created successfully";

#在该数据库下创建资金信息表
cx.execute ('''CREATE TABLE Fund(
   id SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
   AccountID    SMALLINT UNSIGNED NOT NULL UNIQUE KEY,
   FundType         TEXT     ENUM('现金','微信支付','支付宝')  DEFAULT "现金",
   AvailableFunds        FLOAT       NOT NULL,
   FrozenFunds          FLOAT       NULL);''')
print "Table created successfully";

#在该数据库下创建资金流水信息表
cx.execute ('''CREATE TABLE FundFlow(
   AccountID    SMALLINT UNSIGNED NOT NULL UNIQUE KEY,
   ExecuteType         TEXT   ENUM('收入','支出') DEFAULT '支出' NOT NULL,
   FundType         TEXT    ENUM('现金','微信支付','支付宝')  DEFAULT "现金",
   ExecuteMoney        FLOAT       NOT NULL,
   ExecuteTime          INT      NOT NULL,
   ExecuteNum         SMALLINT UNSIGNED NOT NULL,
   Describe           TEXT   NULL);''')
print "Table created successfully";

#１，用户的插入，查询，修改，删除
#２，资金的查询，修改，删除
#３，流动资金的插入

def Insert_Cus():
    cu = cx.cursor()
    cus_id = input("请输入账户ID:")
    cu.execute("SELECT CusId FROM Customer WHERE CusId = %d;"%cus_id)
    row = cu.fetchone()
    if row:
        print "sorry,该账户已存在,请重新输入"
    else:
        cus_name = raw_input("请输入您的姓名:")
        cus_sex =input("请输入您的性别(1代表男生,2代表女生哦!):")
        cus_brith = input('请输入您的生日(如19900718):')
        cus_phone = input('请输入您的手机号:')
        sql1 = "INSERT INTO Customer(AccountID,Name,Sex,Birth,PhoneNum)"
        sql1 += " VALUES(%d,%s,%d,%d,%d);"%(cus_id,cus_name,cus_sex,cus_brith,cus_phone)
#        sql = "UPDATE Customer AS a INNER JOIN Fund AS b,FundFlow AS c ON a.AccountID=b.AccountID=c.AccountID SET a.AccountID = b.AccountID"
        cu.execute(sql1)
        cx.commit()
        print "恭喜你,账户注册成功!"
    cu.close()
def Search_Cus():
    cu = cx.cursor()
    search_id = input("请输入要查询账户ID:")
    sql2 = "SELECT AccountID,Name,Sex, Birth,PhoneNum FROM Customer "
    sql2 += "WHERE AccountID= %d;" % (search_id)
    cu.execute(sql2)
    row = cu.fetchone()
    if row: 
        print
        print "您的账户信息为:"
        print "账号  = ", row[0]
        print "姓名 = ", row[1]
        print "性别 = ", row[2]
        print "生日  = ",row[3]
        print "电话 = ",row[4], "\n"
    else:
        print "sorry,没有该账户信息！"
    cu.close()
def Modify_Cus():
    update_id = input("请输入要修改的账户ID:")
    Search_Cus()
    New_ID = input("请输入要修改用户的新账号:")
    New_name = raw_input("请输入新用户名:")
    New_brith =input("请输入要修改用户的新生日:")
    New_num = input("输入要修改用户的新号码:")
    sql3 = "UPDATE Customer SET AccountID = %d,Name = '%s',Birth = %d,PhoneNum = %d "
    sql3 += "WHERE AccountID = %d;"%(New_ID,New_name,New_brith,New_num)
    cu.execute(sql3)
    row = cu.fetchone()
    cx.commit()
    print "账户修改成功!"
    cu.close()


def Delete_Cus():
    del_id = input("请输入所要删除的账号:")
    sql4 = ("SELECT AccountID FORM Customer WHERE AccountID = %d;")%(del_id)
    row = fetchone()
    if row:
        sql5 = "DELETE FROM Customer WHERE AccountID = %d;"%del_id
        cx.execute(sql5)
        cx.commit()
        print "账户删除成功!"
    else:
        print "sorry,不存在该用户"

def Search_Fund():
    search_id = input('请输入要查询的账户ID:')
    sql6 = "SELECT AccountID,FundType,AvailableFunds, FrozenFunds FROM Fund"
    sql6 +=" WHERE AccountID= %d;" % (search_id)
    cx.execute(sql6)
    row = cx.fetchone()
    if row:
        print "账号 = ", row[0]
        print "资金类型 = ", row[1]
        print "可用资金 = ",row[2]
        print "冻结资金 = ", row[3], "\n"
    else:
        print "sorry,没有该用户信息"
def Modify_Fund():
    update_id = input("请输入要修改的账户ID:")
    sql7 = "SELECT AccountID,FundType,AvailableFunds,FrozenFunds FROM Fund "
    sql7 += "WHERE AccountID = %d;"%(update_id)
    cx.execute(sql7)
    row = cx.fetchone()
    if row:
        print "账号 = ", row[0]
        print "资金类型 = ", row[1]
        print "可用资金 = ",row[2]
        print "冻结资金 = ", row[3], "\n"
        New_type = raw_input("请输入新资金类型:")
        
def Delete_Fund():
    del_id = input('请输入要删除资金的ID:')
    sql8 = "SELECT AccountID FROM Fund WHERE AccountID = %d;"%(del_id)
    cx.execute(sql8)
    row = cx.fetchone()
    if row:
        sql9 = "DELETE FROM Fund WHERE AccountID = %d;"%(del_id)
        cx.execute(sql9)
        cx.commit()
        print "账户资金删除成功!"
    else:
        print "sorry,没有改账户资金信息"
    

def Insert_Fund():
    inert_id = raw_input("请输入要记账的用户ID:")
    sql10 = "SELECT AccountID FROM Customer WHERE AccountID =%d;"(inert_id)
    cx.execute(sql10)
    row = cx.fetchone()
    if row:
        Ex_Type = raw_input("请输入记账类型(支出or收入):")
        Fu_Type = raw_input("请输入支付类型(现金、支付宝、微信):")
        Ex_Money = input("金额:")
        Ex_Time = raw_input("时间(如20170315):")
        Ex_Num = input("流水号:")
        Describe = raw_input("备注:")
        sql11 = "INSERT INTO FundFlow(ExecuteType,FundType,ExecuteMoney,ExecuteTime,ExecuteNum,Describe)"
        sql11 += "VALUES ExecuteType='%s',FundType='%s',ExecuteMoney='%s',ExecuteTime='%s',ExecuteNum=%d,Describe='%s';"\
        %(Ex_Type,Fu_Type,Ex_Money,Ex_Time,Ex_Num,Describe)
        cx.execute(sql11)
        cx.commit()
        print "记账成功!"
    else:
        print "sorry,没有改用户"



def menu():
    print '1.进入用户信息系统'
    print '2.进入资金管理系统'
    print '3.进入资金流动系统'
    print '4.退出程序'
    
def Customer():
    print '欢迎进入账户信息管理系统!'
    print '1.注册账户'
    print '2.查询账户'
    print '3.修改账户信息'
    print '4.删除账户'
    print '5.返回主菜单'

def Fund():
    print '欢迎进入资金信息管理系统!'
    print '1.查询资金'
    print '2.修改资金信息'
    print '3.删除资金信息'
    print '4.返回主菜单'

def FundFlow():
    print '欢迎进入记账系统!'
    print '1.开始记账'
    print '2.返回主菜单'



while True:
    menu()
    print
    x = raw_input('请输入您的选择菜单号:')
    if x == '1':
        #进入用户信息系统
        Customer()
        Cus = raw_input('请输入选择菜单:')
        print
        if Cus == '1':
            Insert_Cus()
            continue
        if Cus == '2':
            Search_Cus()
        if Cus == '3':
            Modify_Cus()
        if Cus == '4':
            Delete_Cus()
        if Cus == '5':
            continue
        else:
            print "输入的选项不存在，请重新输入！"
            continue

    if x == '2':
        #资金信息管理系统
        Fund()
        Fund = raw_input('请输入选择菜单:')
        print
        if Fund == '1':
            Search_Fund()
            continue
        if Fund == '2':
            Modify_Fund()
            continue
        if Fund == '3':
            Delete_Fund()
            continue
        if Fund == '4':
            continue
        else:
            print "输入的选项不存在，请重新输入！"
            continue

    if x == '3':
        #进入记账系统
        FundFlow()
        Flow = raw_input('请输入选择菜单:')
        print
        if inf == '1':
            Insert_Fund()
            continue
        if inf == '2':
            continue
        else:
            print "输入的选项不存在，请重新输入！"
            continue

    if x == '4':
        print "谢谢使用！"
        exit()
    else:
        print "输入的选项不存在，请重新输入！"
        continue













