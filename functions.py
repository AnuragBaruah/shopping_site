##funtions
import csv, pickle, random, pdfkit

def roundOff(n):
    i = int(n)
    p = n + 0.5
    if n >= p:
        return i + 1
    else:
        return i


def billhtml(name, billData, mode, ip):
    with open('BILL/billbackbone1.txt', 'r') as f:
        p1 = f.read()
    p1 += name
    with open('BILL/billbackbone2.txt', 'r') as f:
        p1 += f.read()
    info = ''
    for i in billData:
        if i[0] == 'Total':
            break
        else:
            info += f"""
<tr>
    <td>
        <div class="cart-info">
            <div>
                <p>{i[0]}</p>
            </div>
        </div>
    </td>
    <td>
        <small>{i[1]}</small>
    </td>
    <td>
        {i[2]}
    </td>
</tr>
"""
    info += f"""
</table>

        <div class="total-price">
            <table>
                <tr>
                    <td>
                        Subtotal
                    </td>
                    <td>
                            {billData[-1][1]}
                    </td>
                </tr>
                <tr>
                    <td>
                        GST
                    </td>
                    <td>
                        {roundOff(float(billData[-1][1])*0.12)}
                    </td>
                </tr>
                <tr>
                    <td>
                        Net Price
                    </td>
                    <td>
                        {roundOff(float(billData[-1][1])*1.12)}
                    </td>
                </tr>
                <tr>
                    <td>
                        Mode Of Payment
                    </td>
                    <td>
                        {mode}
                    </td>
                </tr>
            </table>
        </div>
    </div>
"""
    path = f'BILL/{ip}.html'
    with open(path, 'w') as f:
        f.write(p1 + info)
    return path

def createBill(data, mode, ip):
    with open('DATABASE/machinedata.csv', 'r') as f:
        ip_email = list(csv.reader(f))
    for i in ip_email:
        if ip == i[0]:
            logged_in = i[1]
            break
    with open('DATABASE/accounts.csv', 'r') as f:
        accdata = list(csv.reader(f))
    for i in range(len(accdata)):
        if logged_in == accdata[i][0]:
            name = accdata[i][1]
    path1 = billhtml(name, data, mode, ip)
    path2 = f'HTML/BILL/{ip}.pdf'
    try:
        pdfkit.from_file(path1, path2)
    except:
        pass
    with open('DATABASE/sales.dat', 'ab') as f:
        pickle.dump([logged_in, data], f)
    return path2



 
def getBillData(ip, addr):
    with open('DATABASE/machinedata.csv', 'r') as f:
        ip_email = list(csv.reader(f))
    for i in ip_email:
        if ip == i[0]:
            logged_in = i[1]
            break
    with open('DATABASE/accounts.csv', 'r') as f:
        accdata = list(csv.reader(f))
    for i in range(len(accdata)):
        if logged_in == accdata[i][0]:
            accdata[i][-1], accdata[i][-2], accdata[i][-3], accdata[i][1] = addr[-1], addr[-2], addr[-3], addr[0]
    with open('DATABASE/accounts.csv', 'w', newline = '') as f:
        w = csv.writer(f)
        w.writerows(accdata)
    pdt_qty = FetchCart(ip)
    billData = []; total = 0
    for i in pdt_qty:
        sub = float(i[0][2])*int(i[1])
        total += sub
        billData.append([i[0][0], i[1], sub])
    billData.append(['Total', total])
    return billData
            
    

def addtocart(ip, product_index, quantity):
    logged_in = None
    with open('DATABASE/machinedata.csv', 'r') as f:
        ip_email = list(csv.reader(f))
    for i in ip_email:
        if ip == i[0]:
            logged_in = i[1]
            break
    if logged_in == None:
        return 'noaccount'
    else:
        with open('DATABASE/accounts.csv', 'r') as f:
            accountsData = list(csv.reader(f))
        for i in range(len(accountsData)):
            if logged_in == accountsData[i][0]:
                products = accountsData[i][3].split('.')
                quantities = accountsData[i][4].split('.')
                if product_index in products:
                    quantities[products.index(product_index)] = quantity
                    ##quantities[products.index(product_index)] = int(quantity) + int(quantities[products.index(product_index)])
                else:
                    products.append(str(product_index))
                    quantities.append(str(quantity))
                accountsData[i][3] = '.'.join(products).strip('...........')
                accountsData[i][4] = '.'.join(quantities).strip('...........')
        with open('DATABASE/accounts.csv', 'w', newline = '') as f:
            w = csv.writer(f)
            w.writerows(accountsData)
        return 'cart'
        

def RowWiseProducts(rawlist):
    L = []; products = []
    for i in rawlist:
        L.append(i)
        if (rawlist.index(i) + 1)%4 == 0 or i == rawlist[-1]:
            products.append(L)
            L = []
    rows = ''
    for row in products:
        cols = ''
        for item in row:
            imgN = 3
            cols += f"""
                        
                            <div class="col-4">
                                <a href="individualproducts{item[8]}">
                                    <img src="{item[imgN]}">
                                    <h4>{item[0]}</h4>
                                    <p style="color: black;">Rs. {item[2]}</p>
                                </a>
                            </div>
                        
                        """
        rows +=f"""<div class="row">{cols}</div>"""
    return rows


def SortFilter(ip, sort, filt):
    with open(f'HTML/PRODUCTS/{ip}productsshowing.dat', 'rb') as f:
        unfiltered = pickle.load(f)
        heading = pickle.load(f)
    if filt == 'None':
        filt = 9.9e+20
    else:
        filt = int(filt)
    products = []
    for i in unfiltered:
        if float(i[2]) < filt:
            products.append(i)
    if products == []:
        return [], 'None of the products matches your criteria'
    else:
        if sort == 'H':
            for i in range(len(products)):
                for j in range(len(products) - 1 - i):
                    if float(products[j][2]) < float(products[j+1][2]):
                        products[j], products[j+1] = products[j+1], products[j]

        elif sort == 'L':
            for i in range(len(products)):
                for j in range(len(products) - 1 - i):
                    if float(products[j][2]) > float(products[j+1][2]):
                        products[j], products[j+1] = products[j+1], products[j]
        else:
            pass

        if heading[0] != 'N':
            heading = 'Showing products filtered and sorted'
        return products, heading
        

def getTags(string):
    probabletags = string.lower().split(' ')
    with open('DATABASE/tagsused.dat', 'rb') as f:
        tagsused = pickle.load(f)
    tags = []
    for i in probabletags:
        if i in tagsused:
            tags.append(i)
    return tags

def FetchProducts(tags, products_raw):
    products = []
    for i in products_raw:
        if len(tags) == 0:
            yes = False
        else: yes = True
        for j in tags:
            if j not in i[1]:
                yes = False
                break
        if yes:
            products.append(i)
    return products



def LoginAccount(ip, email):
    with open('DATABASE/machinedata.csv','r') as f:
        loggedList = list(csv.reader(f))
    needAppend = True
    for i in range(len(loggedList)):
        if ip == loggedList[i][0]:
            loggedList[i][1] = email
            needAppend = False
            break
    if needAppend:
        loggedList.append([ip,email])
    with open('DATABASE/machinedata.csv', 'w', newline = '') as f:
        w = csv.writer(f)
        w.writerows(loggedList)


def RemoveFromCart(product_index, ip):
    with open('DATABASE/machinedata.csv', 'r') as f:
        ip_email = list(csv.reader(f))
    for i in ip_email:
        if ip == i[0]:
            logged_in = i[1]
            break
    with open('DATABASE/accounts.csv', 'r') as f:
        accountsData = list(csv.reader(f))
    for i in range(len(accountsData)):
        if logged_in == accountsData[i][0]:
            products = accountsData[i][3].split('.')
            quantities = accountsData[i][4].split('.')
            quantities.pop(products.index(product_index))
            products.remove(product_index)
            accountsData[i][3] = '.'.join(products)
            accountsData[i][4] = '.'.join(quantities)
    with open('DATABASE/accounts.csv', 'w', newline = '') as f:
        w = csv.writer(f)
        w.writerows(accountsData)



def FetchCart(ip):
    
    with open('DATABASE/machinedata.csv', 'r') as f:
        ip_email = list(csv.reader(f))
    logged_in = None
    for i in ip_email:
        if ip == i[0]:
            logged_in = i[1]
            break

    if logged_in == None:
        return ['']
    else:
        with open('DATABASE/accounts.csv', 'r') as f:
            accountsData = list(csv.reader(f))
        for i in accountsData:
            if logged_in == i[0]:
                products = i[3].split('.')
                quantities = i[4].split('.')

        with open('DATABASE/products.csv', 'r') as f:
            products_data = list(csv.reader(f))
        real_info = []

        if products != ['']:
            for i in products:
                real_info.append([products_data[int(i)], quantities[products.index(i)]])
            return real_info
        else:
            return ['']
                

                    
