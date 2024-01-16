 ##HTML GENERATOR
import random, csv
from functions import getTags, FetchProducts, RowWiseProducts, FetchCart

def roundOff(n):
    i = int(n)
    p = n + 0.5
    if n >= p:
        return i + 1
    else:
        return i


def thankyoupage(ip):
    with open('HTML/THANKYOU/thank_you_page.html', 'r') as f:
        code = f.read()%(ip+'.pdf')
    path = f'HTML/THANKYOU/{ip}thankyou.html'
    with open(path, 'w') as f:
        f.write(code)
    return path

def createCheckoutPage(ip):
    current_cart = FetchCart(ip)
    amount = 0; netQty = 0
    for i in current_cart:
        amount += float(i[0][2])*int(i[1])
        netQty += int(i[1])
    with open('DATABASE/machinedata.csv', 'r') as f:
        ip_email = list(csv.reader(f))
    for i in ip_email:
        if ip == i[0]:
            logged_in = i[1]
            break
    with open('DATABASE/accounts.csv', 'r') as f:
        accountsData = list(csv.reader(f))
    for i in accountsData:
        if logged_in == i[0]:
            logged_in = i
    recvName = logged_in[1]
    addr1 = logged_in[5]
    addr2 = logged_in[6]
    addr3 = logged_in[7]

    theForm = f"""
<form method="POST" action="checkout">
    <div class="name-detail-1">
        <h3>Receiver's Name:</h2>
    </div>
    <div class="address-input">
        <input type="text" value="{recvName}" name="receivername" required>
    </div>
    <div class="address-detail-1">
        <h3>Address Line 1:</h2>
    </div>
    <div class="address-input">
        <input type="text" value="{addr1}" placeholder="Enter your address" name="addr1" required>
    </div>
    <div class="address-detail-2">
        <h3>Address Line 2:</h3>
    </div>
    <div class="address-input">
        <input type="text" value="{addr2}" placeholder="Enter your address" name="addr2" required>
    </div>
    <div class="address-detail-3">
        <h3>Address Line 3:</h3>
    </div>
    <div class="address-input">
        <input type="text" value="{addr3}" placeholder="Enter your address" name="addr3" required>
    </div>
    <br>
    <div class="payment-mode">
        <h3>Mode of payment:</h3>
    </div>
    <div class="payment-input">
        <input type="radio" id="option1" name="payoption" value="C" checked>
        <label for="COD">Cash on Delivery (COD)</label>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <input type="radio" id="option2" name="payoption" value="N">
        <label for="NetBanking">Net Banking</label>
    </div>

    <div class="payment-btn">
        <input type=submit value="Proceed">
    </div>
    </form>



    <br><br>

    <br>
    <footer>
        <span class="copyright">
            Copyright 2021 - Birla High School
        </span>   
    </footer>
</body>
</html>

"""
    code = ''
    with open('HTML/CHECKOUT/checkoutbackbone1.txt', 'r') as f:
        code += f.read().format(netQty)
    code += theForm
    path = f'HTML/CHECKOUT/{ip}.html'
    with open(path, 'w') as f:
        f.write(code)
    return path


def listEleRand(L, n):
    q = len(L)
    if n > q:
        n = q
    u = q - 1
    p = []
    while len(p) < n:
        while 1:
            i = random.randint(0, u)
            if L[i] not in p:
                p.append(L[i])
                break
    return p

def createIndividualProductsPage(product):    
    ##product variable is a single row from the database(products.csv) in the form of a list
    try:
        with open(f'DATABASE/product_descriptions/{product[-1]}.txt')as f:
            productDescription = f.read()
    except:
        productDescription = 'Information not available at the moment.'
        
    indP = f"""

<div class="test-container single-product">
        <div class="row">
            <div class="col-2">
                <img src="{product[4]}" width="100%" id="ProductImg">
                
                <div class="showcase-row">
                    <div class="showcase-col">
                        <img src="{product[4]}" width="100%" class="small-img">
                    </div>
                    <div class="showcase-col">
                        <img src="{product[5]}" width="100%" class="small-img">
                    </div>
                    <div class="showcase-col">
                        <img src="{product[6]}" width="100%" class="small-img">
                    </div>
                    <div class="showcase-col">
                        <img src="{product[7]}" width="100%" class="small-img">
                    </div>
                </div>


            </div>
            <div class="col-2">
                <!--<p>Products / Shirts</p>-->
                <h1>{product[0]}</h1>
                <h4>Rs. {product[2]}</h4>
                <form action="addtocart{product[-1]}" method="POST">
                <input type="number" value="1" min="1" class="quantity-changer" name="quantity">
                <input type="submit" value="Add To Cart" class="btn" style="border:none;">
                </form>
                <h3>
                    Product Description
                </h3>
                <p>{productDescription}</p>
            </div>
        </div>
    </div>


    <div class="test-container">
        <div class="row row-2">
            <h2>Similar Products</h2>
        </div>
    </div>

"""
    ##for finding the similar products
    tags = getTags(' '.join(product[1].lower().split('.')[:3]))
    with open(f'DATABASE/products.csv','r') as f:
        ALL = list(csv.reader(f))
    similarProducts = FetchProducts(tags, ALL)
    similarProducts.remove(product)
    similarProducts = listEleRand(similarProducts, 4)

    rows = RowWiseProducts(similarProducts)
    simP = f'<div class="test-container">{rows}</div>'

    code = ''
    with open('HTML/INDIVIDUALPRODUCTS/backbone1.txt') as f:
        code += f.read()
    code += indP + simP
    with open('HTML/INDIVIDUALPRODUCTS/backbone2.txt') as f:
        code += f.read()

    path = f'HTML/INDIVIDUALPRODUCTS/{product[-1]}.html'
    with open(path, 'w') as f:
        f.write(code)
    return path
    

    

    

def createProductPage(ip, rawlist, heading):
    path = 'HTML/PRODUCTS/' + ip + 'products.html'

    rows = RowWiseProducts(rawlist)

    code = ''
    with open('HTML/PRODUCTS/productsBackbone1.txt', 'r') as f:
        code += f.read()
    code += heading
    with open('HTML/PRODUCTS/productsBackbone1.1.txt', 'r') as f:
        code += f.read()
    code += rows
    with open('HTML/PRODUCTS/productsBackbone2.txt', 'r') as f:
        code += f.read()

    with open(path, 'w') as f:
        f.write(code)
    return path
    






def createCartPage(ip, cart_data):
    print('cart data for showing cart')
    path = 'HTML/CARTS/' + ip + 'cart.html'
    htmlFile = open(path, 'w')

    product_wise_entries = f"<tr><th>Product</th><th>Quantity</th><th>Total</th></tr>"
    subtotal = 0
    cart_net_quantity = 0
    for i in cart_data:
        product_name = i[0][0][:30]
        product_price = i[0][2]
        product_index = i[0][-1]
        product_quantity = i[1]
        product_img = i[0][random.randint(4,7)]
        total_price = int(product_price)*int(product_quantity)
        subtotal += total_price
        cart_net_quantity += int(product_quantity)
        product_wise_entries += f"""
                                                    <tr>
                                                        <td>
                                                            <div class="cart-info">
                                                                <img src="{product_img}">
                                                                <div>
                                                                    <p>{product_name}</p>
                                                                    <small>Price: Rs. {product_price}.00</small>
                                                                    <br>
                                                                    <a href="removecartproduct{product_index}">Remove</a>
                                                                </div>
                                                            </div>
                                                        </td>
                                                        <form method="POST">
                                                        <td>
                                                            <input type="number" value={product_quantity} min="1" disabled>
                                                        </td>
                                                        </form>
                                                        <td>
                                                            {total_price}
                                                        </td>
                                                    </tr>

                                                """
    

    code = f"""
<html>
<head>
    <meta charset="UTF-8">
    <title>Your Cart</title>
    <link rel="stylesheet" type="text/css" href="../styles.css">
    <script src="../Jquery.js"></script>
    <script src="https://kit.fontawesome.com/14040df3bb.js" crossorigin="anonymous"></script>
    <link rel="icon" href="../IMAGES/logo.png" type="image/x-icon">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@5.15.4/css/fontawesome.min.css">
</head>
<body>
    <nav>
        <div class="navigation">
            <a href="#" class="logo">
                <img src="../IMAGES/logo.png" width="125px">
            </a>
            <div class="cat-2">
            <ul class="centre-menu">
                <li><a href="../HOMEPAGE/homepage.html">Home</a></li>
                <li><a href="../HOMEPAGE/homepage.html?usersearch=">Products</a></li>
                <li><a href="">About Us</a></li>
            </ul>
            </div>
            <div class="right-menu">
                <!--<a href="#" class="user">
                    <i class="fas fa-user"></i>
                </a>-->
                <a href="cart" style="color: #0b9d8a">
                    <i class="fas fa-shopping-cart">
                    <span class="num-cart-product">{cart_net_quantity}</span>
                    </i>
                </a>
            </div>
        </div>
    </nav>
    <div class="form">
        <div class="login-form">
            <a href="#" class="form-cancel">
                <i class="fas fa-times"></i>
            </a>
            <strong>Log In</strong>
            <form method="POST" action="loginsignupform">
                <input type="email" placeholder="Enter your email address." name="email" required>
                <input type="password" placeholder="Enter your password." name="password" required>
                <input type="submit" value="Log In">
            </form>
            <div class="form-btns">
                <a href="#" class="forget">Forgot Your Password?</a>
                <a href="#" class="sign-up-btn">Create Account</a>
            </div>
        </div>


        <div class="sign-up-form">
            <a href="#" class="form-cancel">
                <i class="fas fa-times"></i>
            </a>
            <strong>Sign Up</strong>
            <form method="POST" action="loginsignupform">
                <input type="text" placeholder="Enter your full name" name="fullname" required>
                <input type="email" placeholder="Enter your email address." name="email" required>
                <input type="password" placeholder="Enter your password." name="password" required>
                <input type="submit" value="Sign Up">
            </form>
            <div class="form-btns">
                <a href="#" class="existing-account">Already have an account?</a>
            </div>
        </div> 
    </div> 
    <br><br><br><br>

    <div class="test-container cart-page">
        <table>
            {product_wise_entries}
        </table>
                                <div class="total-price">
                                    <table>
                                        <tr>
                                            <td>
                                                Subtotal
                                            </td>
                                            <td>
                                                Rs. {subtotal}.00
                                            </td>
                                        </tr>
                                        <tr>
                                            <td>
                                                GST
                                            </td>
                                            <td>
                                                Rs. {roundOff(subtotal * 0.12)}
                                            </td>
                                        </tr>
                                        <tr>
                                            <td>
                                                Net Price
                                            </td>
                                            <td>
                                                Rs. {roundOff(subtotal * 1.12)}
                                            </td>
                                        </tr>
                                    </table>
                                </div>
                                </div>
                                <div class="checkout-box">
                                <a href="checkout" class="checkout-btn">Proceed to Checkout</a>
                                </div>

                                <footer style="margin-top: 10%;">
                                <span class="copyright">
                                    Copyright 2021 - Birla High School
                                </span>   
                                </footer>

                                </body>
                                </html>

                                    

                """

    htmlFile.write(code)
    htmlFile.close()
    return path
