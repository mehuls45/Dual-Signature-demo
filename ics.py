#####################################################
#ICS MINI-PROJECT(Concept of Dual Signature)
#####################################################

from flask import Flask,redirect,url_for,request
import random
MAX = 1000000000000

app=Flask(__name__)

p=47
q=53
global d

def gcd(a,b):
    while b!=0:
        c=a%b
        a=b
        b=c
    return a

def modulus(p,q):
    for i in range(1,q):
        if (p*i)%q==1:
            return i
    return None

def coprimes(a):
    l_coprimes=[]
    for i in range(2,a):
        if gcd(a,i)==1 and modulus(i,a)!=None:
            l_coprimes.append(i)
    
    for j in l_coprimes:
        if j==modulus(j,a):
            l_coprimes.remove(j)
    
    return random.choice(l_coprimes)

def calcd():
	p,q=47,53
	n = p*q
    phi_n=(p-1)*(q-1)
    e=coprimes(phi_n)
    return modulus(e,phi_n)

def encrypt(m,e,n):
    c=(m**e)%n
    return c

def decrypt(c,d):
	p,q=47,53
	n = p*q
	d = calcd()
	m = (c**d)%n
	return m
   
def RSA(data):
    n = p*q
    phi_n=(p-1)*(q-1)
    e=coprimes(phi_n)
    d=modulus(e,phi_n)
    text=encrypt(data,e,n)
    return text


@app.route('/success/<name>')
def success(name):
    '<html><body></body></html>'
    return 'The digital Signature generated is %s' % name

@app.route('/dual_signature',methods=['POST','GET'])
def dual_signature():
    if request.method=='POST':
        print("INSIDE POST METHOD")
        ccard=request.form['creditcard']
        cccv=request.form['cvv']
        cname=request.form['name']
        orderid1=request.form['orderid']
        ordername1=request.form['ordername']
        ordercost1=request.form['ordercost']
        PI=ccard+cccv+cname
        print(PI)
        OI=orderid1+ordername1+ordercost1
        print(OI)
        PIMD=hash(PI)
        print(PIMD)
        OIMD=hash(OI)
        print(OIMD)
        PO=PIMD+OIMD
        print(PO)
        POMD=hash(PO)
        print(POMD)
        digital_sign=RSA(POMD)
        print(digital_sign)
        merchant(OI,PIMD,digital_sign)
        return redirect(url_for('success',name=digital_sign))
    else:
        ccard=request.args.get('creditcard')    
        cccv=request.args.get('cvv')
        cname=request.args.get('name')
        orderid=request.args.get('orderid')
        ordername=request.args.get('ordername')
        ordercost=request.args.get('ordercost')
        PI=ccard+cccv+cname
        OI=orderid+ordername+ordercost
        PIMD=hash(PI)
        OIMD=hash(OI)
        PO=PIMD+OIMD
        POMD=hash(PO)
        digital_sign=RSA(POMD)
        return redirect(url_for('success',name=digital_sign))

def merchant(OI,PIMD,DS):
	OIMD1 = hash(OI)
	PO1 = PIMD+OIMD1
	POMD1 = hash(PO1)
	POMDc = decrypt(DS)
	print('POMD1: ',POMD1)
	print('POMD: ',POMDc)

if __name__=='__main__':
    app.run(debug=True)