#####################################################
#ICS MINI-PROJECT(Concept of Dual Signature)
#####################################################

from flask import Flask,redirect,url_for,request
import random

app=Flask(__name__)

p,q = 7,17
e,d = 0,0

def gcd(a,b):
    while b!=0:
        c=a%b
        a=b
        b=c
    return a

def mod(a,b,c):
	ans = a
	for i in range(1,b):
			ans = (ans*a)%c
	return (ans)%c

def encrypt(m,e,n):
    return mod(m,e,n)

def decrypt(c):
	global d
	n = p*q
	return mod(c,d,n)

def encode(phi_n):
	global e
	for i in range(2,phi_n):
		if gcd(i,phi_n) == 1:
			e = i
			break
	return e

def decode(phi_n):
	global e,d
	for i in range(1,phi_n):
		if (e*i)%phi_n == 1:
			d = i
			break
	return d
   
def RSA(data):
	global e,d
	n = p*q
	phi_n=(p-1)*(q-1)
	e = encode(phi_n)
	d = decode(phi_n)
	return encrypt(data,e,n)


@app.route('/success/<name>')
def success(name):
    '<html><body></body></html>'
    return 'The digital Signature generated is %s' % name

@app.route('/dual_signature',methods=['POST','GET'])
def dual_signature():
    if request.method=='POST':
        ccard=int(request.form['creditcard'])
        cccv=int(request.form['cvv'])
        cexpiry=int(request.form['expiry'])
        orderid1=int(request.form['orderid'])
        productid=int(request.form['productid'])
        ordercost1=int(request.form['ordercost'])
        PI=ccard+cccv+cexpiry
        print('PI: ',PI)
        OI=orderid1+productid+ordercost1
        print('OI: ',OI)
        PIMD=hash(PI)
        print('PIMD: ',PIMD)
        OIMD=hash(OI)
        print('OIMD: ',OIMD)
        PO=PIMD+OIMD
        print('P0: ',PO)
        POMD=hash(PO)
        print('POMD: ',POMD)
        digital_sign = RSA(POMD)
        print('Digital Sign: ',digital_sign)
        merchant(OI,PIMD,digital_sign)
        return redirect(url_for('success',name=digital_sign))
    else:
        ccard=int(request.args.get('creditcard'))    
        cccv=int(request.args.get('cvv'))
        cexpiry=int(request.args.get('expiry'))
        orderid=int(request.args.get('orderid'))
        productid=int(request.args.get('productid'))
        ordercost=int(request.args.get('ordercost'))
        PI=ccard+cccv+cexpiry
        OI=orderid+productid+ordercost
        PIMD=hash(PI)
        OIMD=hash(OI)
        PO=PIMD+OIMD
        POMD=hash(PO)
        digital_sign=RSA(POMD)
        #print(digital_sign)
        #merchant(OI,PIMD,digital_sign)
        return redirect(url_for('success',name=digital_sign))

def merchant(OI,PIMD,DigiSign):
	OIMD = hash(OI)
	PO = PIMD+OIMD
	POMD = hash(PO)
	POMD1 = decrypt(DigiSign)
	print('POMD: ',POMD)
	print('POMD1: ',POMD1)

	if (POMD == POMD1):
		print('POMD is verified successfully.')
	else:
		print('POMD failed to verify.')

if __name__=='__main__':
    app.run(debug=True)