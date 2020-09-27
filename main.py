
from tkinter import *
import numpy as np
from tkcalendar import *
from tkinter import messagebox
import tkinter.font as font
import datetime
from datetime import date

#import time
import urllib.request
import matplotlib.pyplot as plt
import tkcalendar
import tkinter.simpledialog

import sqlite3

root = Tk()
root.geometry("1100x600+50+50")
root.title("Store managment system")
myFont = font.Font(family='Helvetica')
#root.configure(bg = 'blue')

# Python program to convert the currency 
# of one country to that of another country  

import requests 
  
class Currency_convertor: 
    # empty dict to store the conversion rates 
    rates = {}  
    def __init__(self, url): 
        data = requests.get(url).json() 
  
        # Extracting only the rates from the json data 
        self.rates = data["rates"]  
  
    # function to do a simple cross multiplication between  
    # the amount and the conversion rates 
    def convert(self, from_currency, to_currency, amount): 
        
        if from_currency != 'EUR' : 
            amount = amount / self.rates[from_currency] 
  
        # limiting the precision to 2 decimal places 
        amount = round(amount * self.rates[to_currency], 2) 
        return amount

# url = str.__add__('http://data.fixer.io/api/latest?access_key=', '2b8863535c463f1a9762ef78532d54e9')   


def connect():
    try:
        urllib.request.urlopen('http://google.com', timeout=1) #Python 3.x
        return True
    except:
        return False



def goBack(frame, func):
    frame.destroy()
    func()
def goMenu(frame):
    frame.destroy()
    menu()

def menu():
    def getData():

        def showModels():
            detailed()
        
        def showGraph():

            conn = sqlite3.connect('store.db')
            c = conn.cursor()
            data_q = []
            data_p = []
            now = datetime.date.today()
            for i in range(1, 13):
                c.execute("SELECT sum(quantity), sum(overall) FROM Sell WHERE year = ? and  month = ?", (int(now.year) - 2000, i))
                data_monthly = c.fetchall()
                data_monthly = data_monthly[0]
                if data_monthly[0] is None:
                    data_q.append(0)
                    data_p.append(0)
                else:
                    data_q.append(data_monthly[0])
                    data_p.append(data_monthly[1])
           
            
            names = ['Jan', 'Feb', 'Mart', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dect']
            values = data_q
            values2 = data_p
            plt.figure(figsize=(12, 12))
            
            plt.subplot(2, 1, 1)
            plt.bar(names, values, color = 'peru', edgecolor = 'blue')
            plt.xlabel("Month")
            plt.ylabel("Sold")
            plt.suptitle('Sale')
            plt.subplot(2, 1, 2)
            plt.bar(names, values2, color = 'peru', edgecolor = 'blue')
            plt.xlabel("Month")
            plt.ylabel("Sold")
            plt.suptitle('Sale')
            plt.show()



        def showDatePicker(frame, wh):
            dateF = Toplevel(frame)
            today = date.today()
            d2 = today.strftime("%m/%d/%y")
            d2 = d2.split('/')
            cal = Calendar(dateF, selectmode = 'day', year = int(d2[2]), month = int(d2[0]), day = int(d2[1]))
            cal.pack()
            choose = Button(dateF, text = 'Choose', command = lambda : grabDate(cal.get_date(), dateF, wh))
            choose.pack()
            cansel = Button(dateF, text = 'Cansel', command = lambda: dateF.destroy())
            cansel.pack()
        def grabDate(date, window, wh):
            window.destroy()

            if wh == 'from':
                fromD_entry.delete(0, END)
                fromD_entry.insert(0, date)
            else:
                toD_entry.delete(0, END)
                toD_entry.insert(0, date)

        frame.destroy()
        main_frame = Frame(root)
        main_frame.pack(fill=BOTH, expand = 1)
        # for scroolbar

        canvas = Canvas(main_frame)
        canvas.pack(side = LEFT, expand = 1, fill = BOTH)
        
        scrollbary = Scrollbar(main_frame, orient = VERTICAL, command = canvas.yview)
        scrollbary.pack(side = LEFT, fill = Y)

        scrollbarx = Scrollbar(main_frame, orient = HORIZONTAL, command = canvas.xview)
        scrollbarx.pack(side = BOTTOM, fill = X)

        canvas.configure(yscrollcommand = scrollbary.set, xscrollcommand = scrollbarx.set)
        canvas.bind('<Configure>', lambda e:  canvas.configure(scrollregion = canvas.bbox('all')))

        frameGet = Frame(canvas, padx = 100, pady = 5)
        canvas.create_window((0, 0), window = frameGet, anchor = "sw")
        frameE = Frame(canvas, padx = 100, pady = 5)
        canvas.create_window((0, 0), window = frameE, anchor = "nw")

        global from_date, to_date
        today = date.today() 
        today = str(today).split('-')
        from_date = datetime.datetime(int(today[0]), int(today[1]), 1)
        from_date = from_date.strftime("%m/%d/%y")
        to_date = datetime.datetime(int(today[0]), int(today[1]), int(today[2]))
        to_date = to_date.strftime("%m/%d/%y")

        def sqlDaily(date = ""):
            if date.find('/'):
                date = date.split('/')
            elif date.find(','):
                date = date.split('.')
                date[0], date[1] = date[1], date[0]

            conn = sqlite3.connect('store.db')
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            if len(date) != 1:
                c.execute('SELECT model, price, currency, to_amd, type, size, quantity, color, info  FROM Purchase WHERE( year = ? AND month = ? AND day = ?) LIMIT 100',
                (int(date[2]), int(date[0]), int(date[1]))
                )
            else:
                c.execute('SELECT model, price, currency, to_amd, type, size, quantity, color, info  FROM Purchase')

            data = [dict(row) for row in c.fetchall()]

            same = []
            allk = set()
            for i in range(len(data)):
                if i in allk:
                    continue
                k = set([i])
                for j in range(i+1, len(data)):
                    if data[i]['model'] == data[j]['model'] and data[i]['size'] == data[j]['size'] and data[i]['price'] == data[j]['price'] and data[i]['type'] == data[j]['type'] and data[i]['color'] == data[j]['color'] and data[i]['info'] == data[j]['info']:
                        k.add(j)
                        allk.add(j)
                same.append(k)
            i = 0
            while i < len(same):

                if len(same[i]) == 1:
                    same.pop(i)
                else:
                    i += 1

            for i in range(len(same)):
                same[i] = list(same[i])

            for i in range(len(same)):
                for j in range(1, len(same[i])):
                    data[same[i][0]]['quantity'] += data[same[i][j]]['quantity'] 

            for i in range(len(same)):
                same[i].pop(0)

            alist = []
            for i in range(len(same)):
                for j in range(len(same[i])):
                    alist.append(same[i][j])

            if len(alist) > 1:
                alist.sort(reverse = True)
                same = alist
            else:
                same = alist

            for i in same:
                del data[i]

            if len(date) != 1:
                c.execute('SELECT model, price, currency, to_amd, type, size, quantity, color, info  FROM Sell WHERE( year = ? AND month = ? AND day = ?) LIMIT 100',
                (int(date[2]), int(date[0]), int(date[1]))
                )
            else:
                c.execute('SELECT model, price, currency, to_amd, type, size, quantity, color, info  FROM Sell')

            data_sell = [dict(row) for row in c.fetchall()]

            same_sell = []
            alls = set()
            for i in range(len(data_sell)):
                if i in alls:
                    continue
                s = set([i])
                for j in range(i+1, len(data_sell)):
                    if data_sell[i]['model'] == data_sell[j]['model'] and data_sell[i]['size'] == data_sell[j]['size'] and data_sell[i]['price'] == data_sell[j]['price'] and data_sell[i]['type'] == data_sell[j]['type'] and data_sell[i]['color'] == data_sell[j]['color'] and data_sell[i]['info'] == data_sell[j]['info']:
                        s.add(j)
                        alls.add(j)
                same_sell.append(s)

            i = 0
            while i < len(same_sell):
                if len(same_sell[i]) == 1:
                    same_sell.pop(i)   
                else:
                    i += 1

            for i in range(len(same_sell)):
                same_sell[i] = list(same_sell[i])

            for i in range(len(same_sell)):
                for j in range(1, len(same_sell[i])):
                    data_sell[same_sell[i][0]]['quantity'] += data_sell[same_sell[i][j]]['quantity'] 
            
            for i in range(len(same_sell)):
                same_sell[i].pop(0)

            alist = []
            for i in range(len(same_sell)):
                for j in range(len(same_sell[i])):
                    alist.append(same_sell[i][j])

            if len(alist) > 1:
                alist.sort(reverse = True)
                same_sell = alist
            else:
                same_sell = alist

            for i in same_sell:
                del data_sell[i]

            pModel = dict()
            sModel = dict()

            for i in range(len(data_sell)):
                sModel[data_sell[i]['model']] = []

            for i in range(len(data)):
                pModel[data[i]['model']] = []

            for i in range(len(data)):
                c.execute('SELECT SUM(quantity) FROM Purchase WHERE model = ? AND size = ? AND color = ?',
                 (data[i]['model'], data[i]['size'], data[i]['color'])
                 )
                p = list(c.fetchone())
                if p[0] is None:
                    p[0] = 0
                c.execute('SELECT SUM(quantity) FROM Sell WHERE model = ? AND size = ? AND color = ?',
                 (data[i]['model'], data[i]['size'], data[i]['color'])
                 )
                s = list(c.fetchone())
                if s[0] is None:
                    s[0] = 0
                pModel[data[i]['model']].append([data[i]['size'], data[i]['color'], p[0], p[0] - s[0]])

            data = [list(row.items()) for row in data]
            
            
            for i in range(len(data_sell)):
                c.execute('SELECT SUM(quantity) FROM Purchase WHERE model = ? AND size = ? AND color = ?',
                 (data_sell[i]['model'], data_sell[i]['size'], data_sell[i]['color'])
                 )
                p = list(c.fetchone())
                if p[0] is None:
                    p[0] = 0
                c.execute('SELECT SUM(quantity) FROM Sell WHERE model = ? AND size = ? AND color = ?',
                 (data_sell[i]['model'], data_sell[i]['size'], data_sell[i]['color'])
                 )
                s = list(c.fetchone())
                if s[0] is None:
                    s[0] = 0
                sModel[data_sell[i]['model']].append([data_sell[i]['size'], data_sell[i]['color'], p[0], p[0] - s[0]])

            for i in pModel.keys():
                for j in sModel.keys():
                    if i == j and len(pModel[i]) != len(sModel[j]):
                        for k in sModel[j]:
                            if k not in pModel[i]:
                                pModel[i].append(k)
                        for k in pModel[i]:
                            if k not in sModel[j]:
                                sModel[j].append(k)

            data_sell = [list(row.items()) for row in data_sell]

            return (data_sell, data, sModel, pModel)

        def sql(from_date, to_date):
            if to_date.find('/') != -1:
                to = to_date.split('/')
            else:
                to = to_date.split('.')
                to[0], to[1] = to[1], to[0]
            if from_date.find('/') != -1:
                fr = from_date.split('/')
            else:
                fr = from_date.split('.')            
                fr[0], fr[1] = fr[1], fr[0]

            conn = sqlite3.connect('store.db')
            c = conn.cursor()

            c.execute('SELECT  SUM(quantity) FROM Purchase WHERE( (year BETWEEN ? AND ?) AND (month BETWEEN ? AND ?) AND (day BETWEEN ? AND ?)) LIMIT 1000',
             (int(fr[2]), int(to[2]), int(fr[0]), int(to[0]), int(fr[1]), int(to[1]))
             )
            
            data = c.fetchall()
            if data == []:
                data.append((None))

            c.execute('SELECT  SUM(quantity) FROM Sell WHERE( (year BETWEEN ? AND ?) AND (month BETWEEN ? AND ?) AND (day BETWEEN ? AND ?)) LIMIT 1000',
             (int(fr[2]), int(to[2]), int(fr[0]), int(to[0]), int(fr[1]), int(to[1]))
             )
            data_sell = c.fetchall()
            start = fr
            end = to
            start_date = datetime.date(int(start[2]), int(start[0]), int(start[1]))
            end_date = datetime.date(int(end[2]), int(end[0]), int(end[1]))
            delta = datetime.timedelta(days = 1)
            daily = []
            daily_sell = []
            while start_date <= end_date:
                price = 0
                to_daily = [(0, 0)]
                count = 0
                c.execute("SELECT quantity, to_amd FROM Purchase WHERE day = ? AND month = ? AND year = ?", 
                    (int(start_date.day), int(start_date.month), int(start_date.year))
                    )
                pr = c.fetchall()
                if len(pr) != 0:
                    for i in pr:
                        price += i[0] * i[1]
                        count += i[0]
                price = round(price, 2)
                  
                to_daily = [(count, price)]
                daily.append(to_daily)

                price_sell = 0
                to_daily_sell = [(0, 0)]
                count_sell = 0

                c.execute("SELECT quantity, to_amd FROM Sell WHERE day = ? AND month = ? AND year = ?", 
                    (int(start_date.day), int(start_date.month), int(start_date.year))
                    )
                pr_sell = c.fetchall()
                if len(pr_sell) != 0:
                    for i in pr_sell:
                        price_sell += i[0] * i[1]
                        count_sell += i[0]
                price_sell = round(price_sell, 2)
              
                to_daily_sell = [(count_sell, price_sell)]

                daily_sell.append(to_daily_sell)

                start_date += delta
            
            for i in range(len(daily_sell)):
                x = list(daily_sell[i])
                x.append((daily[i][0][0], daily[i][0][1]))
                daily_sell[i] = x

            pr = 0
            for i in daily_sell:
                pr += i[0][1]

            x = list(data_sell[0])
            if x[0] is None:
                x[0] = 0
            x.append(pr)
            pr = 0
            if data[0][0] is not None:
                x.append(data[0][0])
            else:
                x.append(0)
            for i in daily:
                pr += i[0][1]

            x.append(pr)
            data_sell.pop(0)
            data_sell.append(x)

            return (data_sell, daily_sell)

        global dataP

        currentFrom = [from_date]
        currentTo = [to_date]
        def get_fd(d, currentFrom = currentFrom, currentTo = currentTo):
            if len(d.get()) != 0:
                correctDate = False
                
                try:

                    if d.get().find('/') != -1:
                        a = d.get().split('/')
                    else:
                        a = d.get().split('.')
                        a[0], a[1] = a[1], a[0]
                    checkDateFrom = datetime.datetime(int(a[2]) + 2000, int(a[0]), int(a[1])) 
                    correctDate = True

                except:
                    correctDate = False

                if currentTo[0].find('/') != -1:
                    a = currentTo[0].split('/')
                else:
                    a = currentTo[0].split('.')
                    a[0], a[1] = a[1], a[0]

                checkDateTo = datetime.datetime(int(a[2]) + 2000, int(a[0]), int(a[1]))

                if correctDate and checkDateFrom <= checkDateTo:

                    from_date = d.get()
                    currentFrom[0] = from_date
                    dataP = sql(currentFrom[0], currentTo[0])
                    (dataP, currentFrom[0], currentTo[0])
                else:
                    for widget in frameE.winfo_children():
                        widget.destroy()
                    noData_label = Label(frameE, text = 'NO DATA')
                    noData_label.pack()
            
        
        def get_td(d, currentFrom = currentFrom, currentTo = currentTo):
            if len(d.get()) != 0:
                correctDate = False

                try:

                    if d.get().find('/') != -1:
                        a = d.get().split('/')
                    else:
                        a = d.get().split('.')
                        a[0], a[1] = a[1], a[0]

                    checkDateTo = datetime.datetime(int(a[2]) + 2000, int(a[0]), int(a[1]))
                    correctDate = True
                except:
                    correctDate = False

                if currentFrom[0].find('/') != -1:
                    a = currentFrom[0].split('/')
                else:
                    a = currentFrom[0].split('.')
                    a[0], a[1] = a[1], a[0]

                checkDateFrom = datetime.datetime(int(a[2]) + 2000, int(a[0]), int(a[1]))
                if correctDate and checkDateFrom <= checkDateTo:
                    to_date = d.get()
                    currentTo[0] = to_date
                    dataP = sql(currentFrom[0], currentTo[0])
                    show(dataP, currentFrom[0], currentTo[0])
                else:
                    for widget in frameE.winfo_children():
                        widget.destroy()
                    noData_label = Label(frameE, text = 'NO DATA')
                    noData_label.pack()
                    noData_label.config(font=("Arial", 12))
            

        
        fd = StringVar()
        
        fromD = Button(frameGet,  command = lambda : showDatePicker(frameGet, 'from'), text = "From")
        fromD.grid(row = 0, column = 0, pady = 10)
        fromD['font'] = myFont
        fromD_entry = Entry(frameGet, textvariable = fd)
        fromD_entry.insert(0, from_date)
        fromD_entry.grid(row = 0, column = 1, pady = 10)
        fd.trace("w", lambda name, index, mode, d = fd : get_fd(d))

        td = StringVar()
        toD = Button(frameGet, command = lambda : showDatePicker(frameGet, 'to'), text = "To")
        toD.grid(row = 0, column = 2, pady = 10)
        toD['font'] = myFont
        toD_entry = Entry(frameGet, textvariable = td)
        toD_entry.insert(0, to_date)
        toD_entry.grid(row = 0, column = 3, pady = 10)
        td.trace("w", lambda name, index, mode, d = td : get_td(d))
        

        back = Button(frameGet, command = lambda : goBack(main_frame, menu), text = "Back")
        back.grid(row = 0, column = 4, pady = 10)
        back['font'] = myFont

        dataP = sql(from_date, to_date)

        def show(dataP, start, end):    

            for widget in frameE.winfo_children():
                widget.destroy()

            if dataP[1] == []:
                noData_label = Label(frameE, text = 'No Data')
                noData_label.pack()
                noData_label.config(font=("Arial", 12))
                return

            total_rows = len(dataP[0])
            total_cols = len(dataP[0][0])
            
            models = Button(frameGet, text = 'Models', command = showModels)
            models.grid(row = 0, column = 5)
            models['font'] = myFont
            graph = Button(frameGet, text = 'Graph', command = showGraph)
            graph.grid(row = 0, column = 6)
            graph['font'] = myFont

            for j in range(total_cols):
                e = Entry(frameE, width = 13)
                e.grid(row = 2, column = j + 1, pady = 2)
                e.insert(0, str(dataP[0][0][j]))
            overall_left_q = Entry(frameE, width = 13)
            overall_left_q.grid(row = 2, column = j + 2, pady = 2)
            overall_left_q.insert(0, str(dataP[0][0][2] - dataP[0][0][0]))
            overall_profit = Entry(frameE, width = 13)
            overall_profit.grid(row = 2, column = j + 3, pady = 2)
            overall_profit.insert(0, str(dataP[0][0][1] - dataP[0][0][3]))

            if start.find('/') != -1:
                start = start.split('/')
            else:
                start = start.split('.')
                start[0], start[1] = start[1], start[0]
            if end.find('/') != -1:
                end = end.split('/')
            else:
                end = end.split('.')
                end[0], end[1] = end[1], end[0]

            start_date = datetime.date(int(start[2]) + 2000, int(start[0]), int(start[1]))
            end_date = datetime.date(int(end[2]) + 2000, int(end[0]), int(end[1]))
            delta = datetime.timedelta(days = 1)
            count = 0

            if end_date.year - start_date.year > 2:
                return

            while start_date <= end_date:
                e = Entry(frameE, width = 10)
                e.grid(row = count + 3, column = 0, pady = 2)
                e.insert(0, start_date.strftime("%m/%d/%y"))
                detailed_b = Button(frameE, text = 'Detailed', command = lambda date = start_date.strftime("%m/%d/%y"): detailed(date) )
                detailed_b.grid(row = count + 3, padx = 6, column = 7, pady = 2)
                detailed_b['font'] = myFont
                start_date += delta
                count += 1

            total_rows = len(dataP[1])
            total_cols = len(dataP[1][0][0])
            for i in range(total_rows):
                for j in range(total_cols):
                    pr = Entry(frameE, width = 13)
                    pr.grid(row = i + 3, column = j + 1, padx = 6, pady = 2)
                    pr.insert(0, str(dataP[1][i][0][j]))
                    prs = Entry(frameE, width = 13)
                    prs.grid(row = i + 3, column = j + 3, padx = 6, pady = 2)
                    prs.insert(0, str(dataP[1][i][1][j]))
                    if j == 0:
                        profit = Entry(frameE, width = 13)
                        profit.grid(row = i + 3, column = j + 6, padx = 6, pady = 2)
                        profit.insert(0, str(dataP[1][i][0][1] - dataP[1][i][1][1]))
                        left_quantity = Entry(frameE, width = 13)
                        left_quantity.grid(row = i + 3, padx = 6, column = j + 5, pady = 2)
                        left_quantity.insert(0, str(dataP[1][i][1][0] - dataP[1][i][0][0]))
                        
                        

        show(dataP, from_date, to_date)
        date_label = Label(frameGet, text = 'Date')
        date_label.grid(row = 1, column = 0 ,padx = (0, 0))
        date_label.config(font=("Arial", 12))
        allQuantity_label = Label(frameGet, text = 'Bought', wraplength=58)
        allQuantity_label.grid(row = 1, column = 3, padx = (0, 0))
        allQuantity_label.config(font=("Arial", 12))
        allBuyPrice_label = Label(frameGet, text = 'Price')
        allBuyPrice_label.grid(row = 1, column = 4, padx = (0, 0))
        allBuyPrice_label.config(font=("Arial", 12))

        allSoldQuantity_label = Label(frameGet, text = 'Sold',  wraplength=58)
        allSoldQuantity_label.grid(row = 1, column = 1, padx = (0, 10))
        allSoldQuantity_label.config(font=("Arial", 12))
        allSoldPrice_label = Label(frameGet, text = 'Price')
        allSoldPrice_label.grid(row = 1, column = 2, padx = (5, 40))
        allSoldPrice_label.config(font=("Arial", 12))

        leftQuantity_label = Label(frameGet, text = 'Left')
        leftQuantity_label.grid(row = 1, column = 5, padx = (50,40))
        leftQuantity_label.config(font=("Arial", 12))
        profit_label = Label(frameGet, text = 'Profit', padx = 2)
        profit_label.grid(row = 1, column = 6, padx = (60, 0))
        profit_label.config(font=("Arial", 12))
        

        def detailed(date = ""):
            detailed_window = Toplevel(root)
            detailed_window.geometry("1280x720")
            ### 
            main_frame = Frame(detailed_window)
            main_frame.pack(fill=BOTH, expand = 1)
            # for scroolbar

            canvas = Canvas(main_frame)
            canvas.pack(side = LEFT, expand = 1, fill = BOTH)
            
            scrollbary = Scrollbar(main_frame, orient = VERTICAL, command = canvas.yview)
            scrollbary.pack(side = LEFT, fill = Y)

            scrollbarx = Scrollbar(main_frame, orient = HORIZONTAL, command = canvas.xview)
            scrollbarx.pack(side = BOTTOM, fill = X)

            canvas.configure(yscrollcommand = scrollbary.set, xscrollcommand = scrollbarx.set)
            canvas.bind('<Configure>', lambda e:  canvas.configure(scrollregion = canvas.bbox('all')))

            frameK = Frame(canvas, pady = 5)
            canvas.create_window((0, 0), window = frameK, anchor = "sw")

            dataP = sqlDaily(date)
            sell = Label(frameK, text = "Sell", pady = 20)
            sell.grid(row = 2, column = 3)
            sell.config(font=("Arial", 14))
            date_label = Label(frameK, text = date)
            date_label.grid(row = 1, column = 0, padx = 10)
            date_label.config(font=("Arial", 12))
            model_label = Label(frameK, text = 'Model')
            model_label.grid(row = 1, column = 1, padx = 10)
            model_label.config(font=("Arial", 12))
            price_label = Label(frameK, text = 'Price')
            price_label.grid(row = 1, column = 2, padx = 10)
            price_label.config(font=("Arial", 12))
            priceAll_label = Label(frameK, text = 'Overall price')
            priceAll_label.grid(row = 1, column = 3, padx = 10)
            priceAll_label.config(font=("Arial", 12))
            currency_label = Label(frameK, text = 'Currency')
            currency_label.grid(row = 1, column = 4, padx = 10)
            currency_label.config(font=("Arial", 12))
            inAmd_label = Label(frameK, text = "In AMD")
            inAmd_label.grid(row = 1, column = 5, padx = 20)
            inAmd_label.config(font=("Arial", 12))
            type_label = Label(frameK, text = 'Type')
            type_label.grid(row = 1, column = 6, padx = 10)
            type_label.config(font=("Arial", 12))
            size_label = Label(frameK, text = 'Size')
            size_label.grid(row = 1, column = 7, padx = 10)
            size_label.config(font=("Arial", 12))
            quantity_label = Label(frameK, text = 'Quantity', padx = 10)
            quantity_label.grid(row = 1, column = 8, padx = 10)
            quantity_label.config(font=("Arial", 12))
            color_label = Label(frameK, text = 'Color')
            color_label.grid(row = 1, column = 9, padx = 10)
            color_label.config(font=("Arial", 12))
            add_label = Label(frameK, text = "Additional info")
            add_label.grid(row = 1, column = 10, padx = 10)
            add_label.config(font=("Arial", 12))

            for i in range(len(dataP[0])):
                e = Entry(frameK)
                e.grid(row = i + 3, column = 3)
                e.insert(0, dataP[0][i][1][1] * dataP[0][i][6][1])
                for j in range(len(dataP[0][i])):
                    if j == 0:
                        b = Button(frameK, text = dataP[0][i][j][1], command = lambda m = dataP[0][i][j][1], mD = dataP[2]: modelinfo(m, mD))
                        b.grid(row = i + 3, column = 1)
                    elif j == 1:
                        e = Entry(frameK)
                        e.grid(row = i + 3, column = j + 1)
                        e.insert(0, dataP[0][i][j][1])
                    else:
                        e = Entry(frameK)
                        e.grid(row = i + 3, column = j + 2)
                        e.insert(0, dataP[0][i][j][1])

            for i in range(len(dataP[1])):
                e = Entry(frameK)
                e.grid(row = len(dataP[0]) + i + 4, column = 3)
                e.insert(0, dataP[1][i][1][1] * dataP[1][i][6][1])
                for j in range(len(dataP[1][i])):
                    if j == 0:
                        b = Button(frameK, text = dataP[1][i][j][1], command = lambda m = dataP[1][i][j][1], mD = dataP[3]: modelinfo(m, mD))
                        b.grid(row = len(dataP[0]) + i + 4, column = j + 1)
                    elif j == 1:
                        e = Entry(frameK)
                        e.grid(row = len(dataP[0]) + i + 4, column = j + 1)
                        e.insert(0, dataP[1][i][j][1])
                    else:
                        e = Entry(frameK)
                        e.grid(row = len(dataP[0]) + i + 4, column = j + 2)
                        e.insert(0, dataP[1][i][j][1])
            purchase = Label(frameK, text = "Purchase", pady = 20)
            purchase.grid(row = len(dataP[0]) + 3, column = 3)
            purchase.config(font=("Arial", 14))

            def modelinfo(m, mD):
                
                model_window = Toplevel(root)
                model_window.geometry("800x300")
                ### 
                main_frame = Frame(model_window)
                main_frame.pack(fill=BOTH, expand = 1)
                # for scroolbar

                canvas = Canvas(main_frame)
                canvas.pack(side = LEFT, expand = 1, fill = BOTH)
                
                scrollbary = Scrollbar(main_frame, orient = VERTICAL, command = canvas.yview)
                scrollbary.pack(side = LEFT, fill = Y)

                scrollbarx = Scrollbar(main_frame, orient = HORIZONTAL, command = canvas.xview)
                scrollbarx.pack(side = BOTTOM, fill = X)

                canvas.configure(yscrollcommand = scrollbary.set, xscrollcommand = scrollbarx.set)
                canvas.bind('<Configure>', lambda e:  canvas.configure(scrollregion = canvas.bbox('all')))

                modelW = Frame(canvas, pady = 5)
                canvas.create_window((0, 0), window = modelW, anchor = "sw")

                model_label = Label(modelW, text = 'Model: ' + m)
                model_label.grid(row = 0, column = 0)
                color_label = Label(modelW, text = 'Color')
                color_label.grid(row = 0, column = 1)
                size_label = Label(modelW, text = 'Size')
                size_label.grid(row = 0, column = 2)
                all_label = Label(modelW, text = 'Was')
                all_label.grid(row = 0, column = 3)
                left_label = Label(modelW, text = 'Left')
                left_label.grid(row = 0, column = 4)

                allWas = 0
                allLeft = 0
                for i in range(len(mD[m])):
                    allWas += mD[m][i][2]
                    allLeft += mD[m][i][3]
                    for j in range(len(mD[m][i])):
                        e = Entry(modelW)
                        e.grid(row = i + 1, column = j + 1, pady = 5)
                        e.insert(0, mD[m][i][j])
                        
                allWas_label = Label(modelW, text = 'Overall was ' + str(allWas))
                allWas_label.grid(row = len(mD[m]) + 2, column = 0)
                allLeft_label = Label(modelW, text = 'Left ' + str(allLeft))
                allLeft_label.grid(row = len(mD[m]) + 2, column = 1)

    def addData():
    
        frame.destroy()
        frameAdd = Frame(root, padx = 100, pady = 100)
        frameAdd.pack()
        
        def getDate(d):
            if d.find('/') != -1:
                x = d.split('/')
            else:
                x = d.split('.')
                x[0], x[1] = x[1], x[0]
            day = x[1]
            month = x[0]
            year = x[2]
            if (len(day) == 2) and day[0] == 0:
                    day = day[1]
            if len(month) == 2 and month[0] == 0:
                month = month[1]
            return (month, day, year)

        def submit(wh, curr, date, to_amd): #where
            if wh == 1:
                wh_s = 'Purchase'
            else:
                wh_s = 'Sell'
            data = normalizeInput(quantity_entry.get(), color_entry.get(), size_entry.get(), model_entry.get(), price_entry.get())
            if len(to_amd) != len(data[0]):
                for i in range(len(data[0]) - len(to_amd)):
                    to_amd.append(to_amd[0])
            if date[0] and date[1] and date[2]:
                response = messagebox.askquestion("Add ?", "Confirm")
                if response == 'yes':
                    conn = sqlite3.connect('store.db')
                    c = conn.cursor()
                    for i in range(len(data[0])):
                        if wh_s == 'Purchase':
                            c.execute("INSERT INTO Purchase (year, month, day, model, price, currency, to_amd, type, size, quantity, color, info, overall) "
                                    " VALUES(:year, :month, :day, :model, :price, :currency, :to_amd, :type, :size, :quantity, :color, :info, :overall)", 
                                {
                                    'year' : int(date[2]),
                                    'month' :   int(date[0]),
                                    'day' : int(date[1]),
                                    'model' : data[3][i],
                                    'price' : float(data[4][i]),
                                    'currency' : curr,
                                    'to_amd': to_amd[i],
                                    'type' :  type_entry.get(),
                                    'size' : data[2][i],
                                    'quantity' : data[0][i],
                                    'color' : data[1][i],
                                    'info' :  add_entry.get(),  
                                    'overall' : int(data[0][i]) * float(data[4][i]),

                                }
                            )
                        else:
                            c.execute("INSERT INTO Sell (year, month, day, model, price, currency, to_amd, type, size, quantity, color, info, overall) "
                                    " VALUES(:year, :month, :day, :model, :price, :currency, :to_amd, :type, :size, :quantity, :color, :info, :overall)", 
                                {
                                    'year' : int(date[2]),
                                    'month' :   int(date[0]),
                                    'day' : int(date[1]),
                                    'model' : data[3][i],
                                    'price' : float(data[4][i]),
                                    'currency' : curr,
                                    'to_amd': to_amd[i],
                                    'type' :  type_entry.get(),
                                    'size' : data[2][i],
                                    'quantity' :data[0][i],
                                    'color' : data[1][i],
                                    'info' :  add_entry.get(),
                                    'overall' : int(data[0][i]) * float(data[4][i]),

                                }
                            )
                    
                    conn.commit()
                    conn.close()
                    getL()
                    model_entry.delete(0, END)
                    #date_ch_label.delete(0, END)
                    type_entry.delete(0, END)
                    price_entry.delete(0, END)
                    size_entry.delete(0, END)
                    color_entry.delete(0, END)
                    quantity_entry.delete(0, END)
                    quantity_entry.insert(0, "1")
                    add_entry.delete(0, END)
                    
        dateB = Button(frameAdd, text = 'Date', command = lambda: showDatePicker(frameAdd))
        dateB.grid(row = 0, column = 1, padx = 20)
        dateB['font'] = myFont

        def reset():
            model_entry.delete(0, END)
            type_entry.delete(0, END)
            price_entry.delete(0, END)
            size_entry.delete(0, END)
            color_entry.delete(0, END)
            quantity_entry.delete(0, END)
            quantity_entry.insert(0, 1)
            add_entry.delete(0, END)
            curr.set("AMD")

        resetB = Button(frameAdd, text = 'Reset', command = reset)
        resetB.grid(row = 11, column = 0)
        resetB['font'] = myFont
            
        global r, date_ch_label, submit_btn, model_entry, type_entry, price_entry, size_entry, color_entry, quantity_entry, add_entry
        global day, month, year
        r = StringVar()
        c = StringVar()
        p = StringVar()
        q = StringVar()
        s = StringVar()
        dv = StringVar()

        date_ch_label = Entry(frameAdd, textvariable = dv, width = 10)
        date_ch_label.grid(row = 0, column = 2)
        today = date.today() 
        d3 = today.strftime("%m/%d/%y")
        date_ch_label.insert(0, d3)

        model_entry = Entry(frameAdd, textvariable = r, width = 30)
        model_entry.grid(row = 1, column = 1, padx = 20)
        type_entry = Entry(frameAdd, width = 30)
        type_entry.grid(row = 2, column = 1, padx = 20)
        size_entry = Entry(frameAdd, textvariable = s, width = 30)
        size_entry.grid(row = 3, column = 1)
        color_entry = Entry(frameAdd, textvariable = c, width = 30)
        color_entry.grid(row = 4, column = 1)
        price_entry = Entry(frameAdd, textvariable = p, width = 30)
        price_entry.grid(row = 5, column = 1, padx = 20)
        quantity_entry = Entry(frameAdd, textvariable = q, width = 30)
        quantity_entry.grid(row = 7, column = 1, padx = 20)
        quantity_entry.insert(0, 1)
        add_entry = Entry(frameAdd, width = 30)
        add_entry.grid(row = 8, column = 1, padx = 20, ipady = 3)

        currs = ['AMD', "RUB", "USD", "CNY"]
        curr = StringVar()
        curr.set("AMD")
        curr.trace_add('write', lambda *args: getCurrency())

        
        
        def getL():
            lst = set()
            conn = sqlite3.connect('store.db')
            cb = conn.cursor()
            if sop.get() == 2:
                cb.execute("SELECT model FROM Sell")
            else:
                cb.execute("SELECT model FROM Purchase")
            models = cb.fetchall()
            
            conn.close()
            for i in models:
                lst.add(i[0])
            if len(lst) == 0:
                lst.add("")
            setm = OptionMenu(frameAdd, mo, *lst)
            setm.grid(row = 1, column = 3)

        def getModel():
            model_entry.delete(0, END)
            model_entry.insert(0, mo.get())

       

        def getCurrency():
            if connect():
                currency = curr.get()
            else:
                setc.configure(state="disabled")
                currency = "AMD"
            return currency

        currency_label = Label(frameAdd, text = 'Currency')
        currency_label.grid(row = 6, column = 0)  
        currency_label.config(font=("Arial", 12)) 
        setc = OptionMenu(frameAdd, curr, *currs)
        setc.grid(row = 6, column = 1)
        if not connect():
            setc.configure(state="disabled")

        date_label = Label(frameAdd, text = 'Date')
        date_label.grid(row = 0, column = 0)
        date_label.config(font=("Arial", 12))
        model_label = Label(frameAdd, text = 'Model')
        model_label.grid(row = 1, column = 0)
        model_label.config(font=("Arial", 12))
        type_label = Label(frameAdd, text = 'Type')
        type_label.grid(row = 2, column = 0)
        type_label.config(font=("Arial", 12))
        size_label = Label(frameAdd, text = 'Size')
        size_label.grid(row = 3, column = 0)
        size_label.config(font=("Arial", 12))
        color_label = Label(frameAdd, text = 'Color')
        color_label.config(font=("Arial", 12))
        color_label.grid(row = 4, column = 0)
        price_label = Label(frameAdd, text = 'Price')
        price_label.grid(row = 5, column = 0)
        price_label.config(font=("Arial", 12))
        quantity_label = Label(frameAdd, text = 'Quantity')
        quantity_label.grid(row = 7, column = 0)
        quantity_label.config(font=("Arial", 12))
        add_label = Label(frameAdd, text = "Additional info")
        add_label.config(font=("Arial", 12))
        add_label.grid(row = 8, column = 0, padx = 20)
        
        sop = IntVar()
        sop.set('2')
        def sub_op(op):
            return op

        

        Radiobutton(frameAdd, text = 'Purchase', command=getL, variable = sop, value = 1).grid(row = 9, column = 0)
        Radiobutton(frameAdd, text = 'Sell', command=getL, variable = sop, value = 2).grid(row = 9, column = 1)
        def toAmd(amount):
            to_amd = []
            amount = amount.split()
            for i in amount:
                currency = getCurrency()
                if currency != "AMD":
                    try:
                        url = str.__add__('http://data.fixer.io/api/latest?access_key=', '2b8863535c463f1a9762ef78532d54e9')   
                        curs = Currency_convertor(url) 
                        to_amd.append(curs.convert(getCurrency(), "AMD", float(i)))
                    except:
                        to_amd.append(float(i))
                else:
                    to_amd.append(float(i))
                    #to_amd = amount
            return to_amd
            
        submit_btn = Button(frameAdd, text = "Add to database", command = lambda: submit(sop.get(), getCurrency(), getDate(dv.get()), toAmd(p.get())), state = DISABLED)
        submit_btn.grid(row = 10, column = 0, columnspan = 3, pady = 10, padx = 10, ipadx = 100)
        submit_btn['font'] = myFont

        r.trace("w", lambda name, index, mode, m=r, c = c: autofill(m, c, sop.get()))
        dv.trace("w", lambda name, index, mode, q = q, p = p, d = dv, m = r, c = c, s = s: submit_ver(p, q, d, m, c, s))
        p.trace("w", lambda name, index, mode, q = q, p = p, d = dv, m = r, c = c, s = s: submit_ver(p, q, d, m, c, s))
        c.trace("w", lambda name, index, mode, q = q, p = p, d = dv, m = r, c = c, s = s: submit_ver(p, q, d, m, c, s))
        s.trace("w", lambda name, index, mode, q = q, p = p, d = dv, m = r, c = c, s = s: submit_ver(p, q, d, m, c, s))
        q.trace("w", lambda name, index, mode, q = q, p = p, d = dv, m = r, c = c, s = s: submit_ver(p, q, d, m, c, s))

        mo = StringVar()

        lst = set()
        conn = sqlite3.connect('store.db')
        cb = conn.cursor()
        if sop.get() == 2:
            cb.execute("SELECT model FROM Sell")
        else:
            cb.execute("SELECT model FROM Purchase")
        models = cb.fetchall()
            
        conn.close()
        for i in models:
            lst.add(i[0])
        if len(lst) == 0:
            lst.add("")

        mo.trace_add('write', lambda *args: getModel())
        setm = OptionMenu(frameAdd, mo, *lst)
        setm.grid(row = 1, column = 3)

        back = Button(frameAdd, command = lambda : goBack(frameAdd, menu), text = "Back")
        back.grid(row = 11, column = 2)
        back['font'] = myFont

        def autofill(m, c, fr):
            if m.get() == "":
                mo.set("")
            submit_ver(p, q, dv, r, c, s)
            if m.get() != "":
                conn = sqlite3.connect('store.db')
                c = conn.cursor()
                if fr == 1:
                    c.execute("SELECT info, price, type FROM Purchase WHERE model = :model", {'model' : m.get()})
                else:
                    c.execute("SELECT info, price, type FROM Sell WHERE model = :model", {'model' : m.get()})
                res = c.fetchall()

                if len(res) >= 1:
                    add_entry.delete(0, END)
                    type_entry.delete(0, END)
                    price_entry.delete(0, END)
                    try:
                        add_entry.insert(0, res[len(res) - 1][0])
                        price_entry.insert(0, res[len(res) - 1][1])
                        type_entry.insert(0, res[len(res) - 1][2])
                            
                    except:
                        pass
        
        def normalizeInput(q, c, s, m, p):
            q = q.split()
            s = s.split()
            p = p.split()
            if c.find(',') == -1:
                c = c.split()
            else:
                c = c.split(',')
                if c[len(c) - 1] == "":
                    c.pop(len(c) - 1)
                for i in range(len(c)):
                    c[i] = c[i].strip()
            if m.find(',') == -1:
                m = m.split()
            else:
                m = m.split(',')
                if m[len(m) - 1] == "":
                    m.pop(len(m) - 1)
                for i in range(len(m)):
                    m[i] = m[i].strip()

            if len(q) == len(p) == len(c) == len(s) == len(m) and len(q) != 0:
                return (q, c, s, m, p)

            if 0 in [len(q), len(p), len(m)]:
                return "error"

            if (len(c) > len(q) or len(s) > len(q)) and len(q) != 1:
                return 'error'
            elif (len(c) > len(q) or len(s) > len(q)) and len(q) == 1:
                if len(c) == 0:
                    c.append("")
                if len(s) == 0:
                    s.append("")
                for i in range(max(len(c), len(s)) - len(q)):
                    if len(q) < max(len(c), len(s)):
                        q.append(q[0])
                    if min(len(c), len(s)) < max(len(c), len(s)):
                        if len(s) == min(len(c), len(s)):
                            s.append(s[0])
                        else:
                            c.append(c[0])
            else:
                if len(c) == 0:
                    c.append("")
                if len(s) == 0:
                    s.append("")

                if len(c) == len(s) and len(c) == 1:
                    for i in range(len(q) - min(len(c), len(s))):
                        if len(c) < len(q):
                            c.append(c[0])
                        if len(s) < len(q):
                            s.append(s[0])

            if len(q) > 1 and len(p) + len(m) == 2 and max(len(c), len(s)) <= 1:
                return 'error'

            if len(q) == len(m) and len(m) == len(p):
                return (q, c, s, m, p)
            elif 1 not in [len(q), len(m), len(p)]:
                return 'error'
            elif len(q) != 1 and ((len(c) > 1 and len(q) != len(c)) or (len(s) > 1 and len(s) != len(q))):
                return 'error'
            elif sum(1 for i in [len(q), len(p), len(m)] if i == 1) == 2 or (len(q) == 1 and len(p) == len(m)) or (len(p) == 1 and len(q) == len(m)) or (len(m) == 1 and len(p) == len(q)):
                for i in range(max(len(q), len(m), len(p)) - min(len(q), len(m), len(p))):
                    if len(q) < max(len(q), len(m), len(p)):
                        q.append(q[0])
                    if len(m) < max(len(q), len(m), len(p)):
                        m.append(m[0])
                    if len(p) < max(len(q), len(m), len(p)):
                        p.append(p[0])
                    if len(c) < max(len(q), len(m), len(p)):
                        c.append(c[0])
                    if len(s) < max(len(q), len(m), len(p)):
                        s.append(s[0])

            if min([len(q), len(c), len(s), len(m), len(p)]) != max([len(q), len(c), len(s), len(m), len(p)]):

                return 'error'
            
            return (q, c, s, m, p)

        

        def submit_ver(p, q, d, m, c, s):
            try:
                getDate(d.get())
                
                if d.get().find('/') != -1:
                    a = d.get().split('/')
                else:
                    a = d.get().split('.')
                    a[0], a[1] = a[1], a[0]
                checkDate = datetime.datetime(int(a[2]) + 2000,int(a[0]),int(a[1]))
                
                check = normalizeInput(q.get(), c.get(), s.get(), m.get(), p.get())
                
                if check == 'error':
                    submit_btn['state'] = 'disabled'

                flag = True
                for qc in check[0]:
                    if not qc.isdigit():
                        flag = False          
                for qc in check[1]:
                    if any(i.isdigit() for i in qc):
                        flag = False
                if len(d.get()) > 0 and m.get() != "" and flag and len(check[0]) >= 1:
                    submit_btn['state'] = 'active'
                else:
                    submit_btn['state'] = 'disabled'
                
            except:
                submit_btn['state'] = 'disabled'


        def showDatePicker(frame):
            dateF = Toplevel(frame)
            today = date.today()
            d2 = today.strftime("%m/%d/%y")
            d2 = d2.split('/')
            cal = Calendar(dateF, selectmode = 'day', year = int(d2[2]), month = int(d2[0]), day = int(d2[1]))
            cal.pack()
            def showDate():
                date = cal.get_date()
                if date.find('/') != -1:
                    x = date.split('/')
                else:
                    x = date.split('.')
                    x[0], x[1] = x[1], x[0]

                day = x[1]
                if (len(day) == 1):
                    day = '0' + day 
                month = x[0]
                if (len(month) == 1):
                    month = '0' + month
                year = x[2]
                dateF.destroy()
                date_ch_label.delete(0, END)
                date_ch_label.insert(0, date)

            choose = Button(dateF, text = 'Choose', command = showDate).pack()
            cansel = Button(dateF, text = 'Cansel', command = lambda: dateF.destroy()).pack()     

    def deleteData():
        
        def delete(id, wh):
            response = messagebox.askquestion("Delete ?", "Confirm")
            if response == 'yes':
                conn = sqlite3.connect('store.db')
                c = conn.cursor()
                if wh == "Sell":
                    c.execute("DELETE FROM Sell WHERE id = :id", {'id' : id})
                else:
                    c.execute("DELETE FROM Purchase WHERE id = :id", {'id' : id})
                main_frame.destroy()
                conn.commit()
                deleteData()
                conn.close()

        def sqlD():
            date = datetime.date.today()
            week_ago = date - datetime.timedelta(days=7)
            
            
            conn = sqlite3.connect('store.db')
            c = conn.cursor()
            c.execute('SELECT *  FROM Purchase WHERE( year BETWEEN ? and ? AND month BETWEEN ? and ? AND day BETWEEN ? and ?) LIMIT 100',
             (int(week_ago.year) - 2000, int(date.year) - 2000, int(week_ago.month), int(date.month), int(week_ago.day), int(date.day))
             )
            data = c.fetchall()

            c.execute('SELECT *  FROM Sell WHERE( year BETWEEN ? and ? AND month BETWEEN ? and ? AND day BETWEEN ? and ?) LIMIT 100',
             (int(week_ago.year) - 2000, int(date.year) - 2000, int(week_ago.month), int(date.month), int(week_ago.day), int(date.day))
             )
            data_sell = c.fetchall()
            conn.close()

            return (data_sell, data)
        
        #frame.destroy()
        main_frame = Frame(root)     
        main_frame.pack(fill=BOTH, expand = 1)
        # for scroolbar

        canvas = Canvas(main_frame)
        canvas.pack(side = LEFT, expand = 1, fill = BOTH)
        
        scrollbary = Scrollbar(main_frame, orient = VERTICAL, command = canvas.yview)
        scrollbary.pack(side = LEFT, fill = Y)

        scrollbarx = Scrollbar(main_frame, orient = HORIZONTAL, command = canvas.xview)
        scrollbarx.pack(side = BOTTOM, fill = X)

        canvas.configure(yscrollcommand = scrollbary.set, xscrollcommand = scrollbarx.set)
        canvas.bind('<Configure>', lambda e:  canvas.configure(scrollregion = canvas.bbox('all')))

        frameDel = Frame(canvas, padx = 100, pady = 5)
        canvas.create_window((0, 0), window = frameDel, anchor = "sw")


        sell = Label(frameDel, text = "Sell", pady = 20)
        sell.grid(row = 2, column = 3)
        sell.config(font=("Arial", 14))

        date_label = Label(frameDel, text = "Date")
        date_label.grid(row = 1, column = 1, padx = 10)
        date_label.config(font=("Arial", 12))
        model_label = Label(frameDel, text = 'Model')
        model_label.grid(row = 1, column = 2, padx = 10)
        model_label.config(font=("Arial", 12))
        price_label = Label(frameDel, text = 'Price')
        price_label.grid(row = 1, column = 3, padx = 10)
        price_label.config(font=("Arial", 12))
        currency_label = Label(frameDel, text = 'Currency')
        currency_label.grid(row = 1, column = 4, padx = 10)
        currency_label.config(font=("Arial", 12))
        inAmd_label = Label(frameDel, text = "In AMD")
        inAmd_label.grid(row = 1, column = 5, padx = 20)
        inAmd_label.config(font=("Arial", 12))
        type_label = Label(frameDel, text = 'Type')
        type_label.grid(row = 1, column = 6, padx = 10)
        type_label.config(font=("Arial", 12))
        size_label = Label(frameDel, text = 'Size')
        size_label.grid(row = 1, column = 7, padx = 10)
        size_label.config(font=("Arial", 12))
        quantity_label = Label(frameDel, text = 'Quantity', padx = 10)
        quantity_label.grid(row = 1, column = 8, padx = 10)
        quantity_label.config(font=("Arial", 12))
        color_label = Label(frameDel, text = 'Color')
        color_label.grid(row = 1, column = 9, padx = 10)
        color_label.config(font=("Arial", 12))
        add_label = Label(frameDel, text = "Addidional info")
        add_label.grid(row = 1, column = 10, padx = 10)
        add_label.config(font=("Arial", 12))

        dataP = sqlD()

        for i in range(len(dataP[0])):
            d = ""
            for j in range(1, len(dataP[0][i])):
                if j <= 3:
                    d += str(dataP[0][i][j]) + '/'
                    if j == 3:
                        e = Entry(frameDel)
                        e.grid(row = i + 3, column = j - 2)
                        e.insert(0, d)
                else:
                    e = Entry(frameDel)
                    e.grid(row = i + 3, column = j - 2)
                    e.insert(0, dataP[0][i][j])
                delete_b = Button(frameDel, text = 'Delete', command = lambda id = dataP[0][i][0], wh = "Sell": delete(id, wh) )
                delete_b.grid(row = i + 3, padx = 6, column = 0, pady = 2)
                delete_b['font'] = myFont

        for i in range(len(dataP[1])):
            d = ""
            for j in range(1, len(dataP[1][i])):
                if j <= 3:
                    d += str(dataP[1][i][j]) + '/'
                    if j == 3:
                        e = Entry(frameDel)
                        e.grid(row = len(dataP[0]) + i + 4, column = j - 2)
                        e.insert(0, d)
                else:    
                    e = Entry(frameDel)
                    e.grid(row = len(dataP[0]) + i + 4, column = j - 2)
                    e.insert(0, dataP[1][i][j])
                delete_b = Button(frameDel, text = 'Delete', command = lambda id = dataP[1][i][0], wh = "Purchase": delete(id, wh) )
                delete_b.grid(row = len(dataP[0]) + 4 + i, padx = 6, column = 0, pady = 2)
                delete_b['font'] = myFont
                
        purchase = Label(frameDel, text = "Purchase", pady = 20)
        purchase.grid(row = len(dataP[0]) + 3, column = 3)
        purchase.config(font=("Arial", 14))

       

        back = Button(frameDel, command = lambda : goBack(main_frame, menu), text = "BAck")
        back.grid(row = 0, column = 4)
        back['font'] = myFont

        


    frame = Frame(root)
    frame.place(relx = 0.5, rely = 0.5, anchor = 'c')

    getDataB = Button(frame, text = "Show", command = getData, padx = 43, pady = 20, anchor = "center", bg='#0052cc', fg='#ffffff', activeforeground = "black", activebackground = "green")
    getDataB.grid(row = 0, column = 1, pady = 10)
    getDataB['font'] = myFont

    addDataB = Button(frame, text = "Add", command = addData, padx = 50, pady = 20, anchor = "center", bg='#0052cc', fg='#ffffff', activeforeground = "black", activebackground = "yellow")
    addDataB.grid(row = 1, column = 1, pady = 10)
    addDataB['font'] = myFont

    deleteDataB = Button(frame, text = "Delete", command = deleteData, padx = 43, pady = 20, anchor = "center", bg='#0052cc', fg='#ffffff', activeforeground = "black", activebackground = "red")
    deleteDataB.grid(row = 2, column = 1, pady = 10)
    deleteDataB['font'] = myFont

if __name__ == "__main__":
    menu()

root.mainloop()
