##THIS IS THE SERVER

import functions, htmlCreator, sendemail
import csv, pickle, random
import http.server
h = http.server.SimpleHTTPRequestHandler

class REQUEST_CLASS(h):
    def do_GET(self):
        ##GOING TO THE CHECKOUT PAGE FROM CART (PROCEED TO CHECKOUT)
        if 'checkout' in self.path:
            ip = self.client_address[0]
            self.path = htmlCreator.createCheckoutPage(ip)
            return h.do_GET(self)
        
        ##SHOWING PROBLEM WHEN ADD TO CART IS DONE WITHOUT LOGING IN
        if 'noaccountforcart' in self.path:
            self.path = 'HTML/RESPONSES/noaccountforcart.html'
            return h.do_GET(self)
        
        
        ##LOGIC FOR SEARCH / SHOWING PRODUCTS
        if 'usersearch' in self.path:
            ip = self.client_address[0]
            T = self.path.split('usersearch=')[1].split('&')
            nT = len(T)  ## nT = 3 >> {usersearch in real} 
            searchKeyword = T[0].replace('+', ' ') ## replacing + by single space ' '
            tags = functions.getTags(searchKeyword)
            with open('DATABASE/products.csv', 'r') as f:
                products_raw = list(csv.reader(f))
            #productsList = functions.FetchProducts(tags, products_raw)
            listStore = open(f'HTML/PRODUCTS/{ip}productsshowing.dat', 'wb') 
            if searchKeyword == '':
                heading = 'Showing All Available Products'
                self.path = htmlCreator.createProductPage(ip, products_raw, heading)
                pickle.dump(products_raw, listStore)
                pickle.dump(heading, listStore)
                listStore.close()
            else:
                productsList = functions.FetchProducts(tags, products_raw)
                heading = f'Showing all available products in the Category "{searchKeyword}"'
                if nT == 3:
                    heading = f'Showing available products related to the keyword "{searchKeyword}"'
                if productsList == []:
                    heading = f'None of the products match your criteria'
                self.path = htmlCreator.createProductPage(ip, productsList, heading)
                pickle.dump(productsList, listStore)
                pickle.dump(heading, listStore)
                listStore.close()
            return h.do_GET(self)

        ##SHOWING A PAGE FOR EACH PRODUCT
        if 'individualproducts' in self.path:
            index = int(self.path.split('individualproducts')[1])
            with open('DATABASE/products.csv', 'r') as f:
                product = list(csv.reader(f))[index]
            self.path = htmlCreator.createIndividualProductsPage(product)
            return h.do_GET(self)
        
        ##LOGIC FOR SHOWING CART
        if 'cart' in self.path and 'removecartproduct' not in self.path:
            ip = self.client_address[0]
            cart_data = functions.FetchCart(ip)
            if cart_data == ['']:
                self.path = 'HTML/CARTS/emptycart.html'
            else:
                path = htmlCreator.createCartPage(ip, cart_data)
                self.path = path
            return h.do_GET(self)

        ##LOGIC FOR REMOVING ITEMS FROM CART
        if 'removecartproduct' in self.path:
            ip = self.client_address[0]
            index = self.path.split('removecartproduct')[1]
            functions.RemoveFromCart(index, ip)
            cart_data = functions.FetchCart(ip)
            if cart_data == ['']:
                self.path = 'HTML/CARTS/emptycart.html'
            else:
                path = htmlCreator.createCartPage(ip, cart_data)
                self.path = path
            return h.do_GET(self)


        ##ULTIMATE STATEMENT
        return h.do_GET(self)


    def do_POST(self):
        ip = self.client_address[0]
        L = int(self.headers['content-length'])
        posted_data = str(self.rfile.read(L)).lstrip("b'").rstrip("'").split('&')

        ##OTP AUTHENTICATION
        if 'otpsubmit' in self.path:
            otp1 = posted_data[0][2:]
            with open('DATABASE/machinedata.csv', 'r') as f:
                ip_email = list(csv.reader(f))
            for i in ip_email:
                if ip == i[0]:
                    logged_in = i[1]
                    break
            with open(f'DATABASE/OTP/{logged_in}.dat', 'rb') as f:
                f.seek(0)
                otp2 = pickle.load(f)
            if otp1 == otp2:
                with open(f'DATABASE/TEMP/{ip}.dat', 'rb') as f:
                    name, addr1, addr2, addr3 = pickle.load(f)
                billData = functions.getBillData(ip, (name, addr1,addr2,addr3))
                billPath =  functions.createBill(billData, 'Online Payment', ip)
                sendemail.sendTHANK(logged_in)
                self.path = htmlCreator.thankyoupage(ip)
                return h.do_GET(self)
            else:
                self.path = 'HTML/OTPFORM/otpfailed.html'
                return h.do_GET(self)

        ##SENDING OTP AFTER ONLINE PAY
        if 'onlinepay' in self.path:
            cardno = posted_data[0][7:].replace('+', '')
            name = posted_data[1][5:].replace('+', ' ')
            exp = posted_data[2].split('+')[0] + '.' + posted_data[2].split('+')[2]
            cvv = posted_data[3][4:]
            ## The online payments part of the website is just an emulation.
            ## Hence, the data extracted is not used here.
            ## In real life these would be sent to the bank, and the bank would send otp.
            ## We here are just sending an OTP to the registered e-mail id for a complete emulation of the authentication process
            with open('DATABASE/machinedata.csv', 'r') as f:
                ip_email = list(csv.reader(f))
            for i in ip_email:
                if ip == i[0]:
                    logged_in = i[1]
                    break
            OTP = sendemail.sendOTP(logged_in, 5, 'One Time Password', 'The OTP for your online payment to Shop.Drop is')
            with open(f'DATABASE/OTP/{logged_in}.dat', 'wb') as f:
                pickle.dump(OTP, f)
            self.path = 'HTML/OTPFORM/otp.html'
            return h.do_GET(self)

            
        ##CHECKOUT FORM
        if 'checkout' in self.path:
            with open('DATABASE/machinedata.csv', 'r') as f:
                ip_email = list(csv.reader(f))
            for i in ip_email:
                if ip == i[0]:
                    logged_in = i[1]
                    break
            name = posted_data[0][13:].replace('+', ' ')
            addr1 = posted_data[1][6:].replace('+', ' ')
            addr2 = posted_data[2][6:].replace('+', ' ')
            addr3 = posted_data[3][6:].replace('+', ' ')
            payOpt = posted_data[4][-1]
            billData = functions.getBillData(ip, (name, addr1,addr2,addr3))
            with open(f'DATABASE/TEMP/{ip}.dat', 'wb') as f:
                pickle.dump([name,addr1,addr2,addr3], f)
            if payOpt == 'C':
               billPath =  functions.createBill(billData, 'Cash On Delivery', ip)
               sendemail.sendTHANK(logged_in)
               self.path = htmlCreator.thankyoupage(ip)
               return h.do_GET(self)
            else:
                self.path = 'HTML/PAYMENTS/checkoutpage.html'
                return h.do_GET(self)

        ##ADD TO CART
        if 'addtocart' in self.path:
            product_index = self.path.split('addtocart')[1]
            quantity = posted_data[0].split('=')[1]
            self.path = functions.addtocart(ip, product_index, quantity)
            cart_data = functions.FetchCart(ip)
            if cart_data == ['']:
                self.path = 'HTML/CARTS/emptycart.html'
            else:
                path = htmlCreator.createCartPage(ip, cart_data)
                self.path = path
            return h.do_GET(self)

        ##SORT AND FILTER
        if 'sortandfilter' in self.path:
            #print(posted_data)
            sort = posted_data[0].split('%3A+')[-1][0].strip()
            filt   = posted_data[1].split('+')[-1].strip()
            productsList, heading = functions.SortFilter(ip, sort, filt)
            self.path = htmlCreator.createProductPage(ip, productsList, heading)
            return h.do_GET(self)

        ##FORGOT PASSWORD
        if 'forgotpasswordform' in self.path:
            sent = False
            logged_in = posted_data[0][6:].replace('%40', '@')
            with open('DATABASE/accounts.csv', 'r') as f:
                allDetails = list(csv.reader(f))
            for i in range(len(allDetails)):
                if logged_in == allDetails[i][0]:
                    sent = True
                    newPass = sendemail.sendOTP(logged_in, 10, 'New Password', 'The new password for your account is')
                    allDetails[i][2] = newPass
                    break
            if sent:
                with open('DATABASE/accounts.csv', 'w', newline='') as f:
                    w = csv.writer(f)
                    w.writerows(allDetails)
                self.path = 'HTML/RESPONSES/passwordchanged.html'
                return h.do_GET(self)
            else:
                self.path = 'HTML/RESPONSES/loginError_accDNE.html'
                return h.do_GET(self)
            
        
        ##LOGIN AND SIGN UP
        if 'loginsignupform' in self.path:
            ##LOGIN
            if len(posted_data) == 2:
                email = posted_data[0][6:].replace('%40', '@')
                password = posted_data[1].lstrip('password=')
                with open('DATABASE/accounts.csv', 'r') as f:
                    accountsData = list(csv.reader(f))

                detectedAccount = None
                for i in accountsData:
                    if email == i[0]:
                        detectedAccount = i
                        break
                if detectedAccount == None:
                    self.path = 'HTML/RESPONSES/loginError_accDNE.html'
                    return h.do_GET(self)
                else:
                    if password == detectedAccount[2]:
                        ip = self.client_address[0]
                        functions.LoginAccount(ip, email)
                        self.path = 'HTML/RESPONSES/loginSuccessful.html'
                        return h.do_GET(self)
                    else:
                        self.path = 'HTML/RESPONSES/loginError_pwd_incorrect.html'
                        return h.do_GET(self)
                    
                    
                                
            ##SIGN UP
            elif len(posted_data) == 3:
                fullname = posted_data[0][9:].replace('+', ' ')
                email = posted_data[1][6:].replace('%40', '@')
                password = posted_data[2].lstrip('password=')

                with open('DATABASE/accounts.csv', 'r') as f:
                    accountsData = list(csv.reader(f))

                detectedAccount = None
                for i in accountsData:
                    if email == i[0]:
                        detectedAccount = i
                        break
                if detectedAccount == None:
                    with open('DATABASE/accounts.csv', 'r') as f:
                        d = list(csv.reader(f))
                    d.append([email, fullname, password, '', '', '', '', ''])
                    with open('DATABASE/accounts.csv', 'w', newline = '') as f:
                        w = csv.writer(f)
                        w.writerows(d)
                    ip = self.client_address[0]
                    functions.LoginAccount(ip, email)
                    self.path = 'HTML/RESPONSES/signupSuccessful.html'
                    return h.do_GET(self)
                else:
                    self.path = 'HTML/RESPONSES/signupError_accExists.html'
                    return h.do_GET(self)
                



def main():
    port = int(input('enter a free/valid port number'))
    s = http.server.HTTPServer(('192.168.43.163', port), REQUEST_CLASS)
    print('Server Running on port', port)
    s.serve_forever()

if __name__=='__main__':
    main()
