import flask
from flask import request
import datetime
from flask_api import status
import random

app = flask.Flask(__name__)
app.config["DEBUG"] = True


# Functions to randomly give True / False - acting as PaymentGateways

def cheap():  # cheap payment gateway
    n = random.randint(1, 30)
    if n == 3 or n == 9 or n == 6:
        return False
    return True


def expensive():  # expensive payment gateway
    n = random.randint(1, 30)
    if n == 3 or n == 9:
        return False
    return True


def premium():  # premium payment gateway
    n = random.randint(1, 30)
    if n == 3:
        return False
    return True


def process(cnumber, cholder, amt, exp, scode):  # make calls to appropriate Payment Gateway passing all details
    amt = float(amt)
    resp = False

    if amt <= 20:  # for amount less than or equal 20
        resp = cheap()
        return resp, "using CheapPaymentGateway"

    elif 500 >= amt >= 21:  # for amount between 21 and 500 (inclusive)
        try:  # try expensive if there
            resp = expensive()
            return resp, "using ExpensivePaymentGateway"

        except:  # else go for cheap
            resp = cheap()
            return resp, "using CheapPaymentGateway"

    elif amt > 500:  # for amount more than 500
        i = 0
        while not resp and i < 3:
            resp = premium()
            if resp:
                return resp, "using PremiumPaymentGateway"
            i += 1
        return resp, "using PremiumPaymentGateway"


@app.route('/', methods=['GET'])
def ProcessPayment(SecurityCode=None):  # default SecurityCode is None
    try:  # try appropriate logic else 500
        if 'CreditCardNumber' in request.args:  # if not provided raise 400
            CreditCardNumber = request.args['CreditCardNumber']
        else:
            return "Error: No CreditCardNumber field provided. Please specify CreditCardNumber.", status.HTTP_400_BAD_REQUEST

        if 'CardHolder' in request.args:  # if not provided raise 400
            CardHolder = request.args['CardHolder']
        else:
            return "Error: No CardHolder field provided. Please specify CardHolder.", status.HTTP_400_BAD_REQUEST

        if 'ExpirationDate' in request.args:  # if not provided raise 400
            try:  # for invalid format
                ExpirationDate = datetime.datetime.strptime(request.args.get('ExpirationDate'), "%y-%m")
            except:
                return "Error: invalid Expiration Data format", status.HTTP_400_BAD_REQUEST

            if ExpirationDate < datetime.datetime.now():  # for expired card
                return "Error: ExpirationDate has passed.", status.HTTP_400_BAD_REQUEST
        else:
            return "Error: No ExpirationDate field provided. Please specify an ExpirationDate.", status.HTTP_400_BAD_REQUEST

        if 'Amount' in request.args:  # if not provided raise 400
            Amount = request.args['Amount']
            try:  # if not decimal raise 400
                float(Amount)
            except:
                return "Error: invalid amount", status.HTTP_400_BAD_REQUEST

            if float(Amount) < 0:  # if negative raise 400
                return "Error: invalid amount(negative)", status.HTTP_400_BAD_REQUEST
        else:
            return "Error: No Amount field provided. Please specify an Amount.", status.HTTP_400_BAD_REQUEST

        if 'SecurityCode' in request.args:
            SecurityCode = request.args['SecurityCode']
            if not (SecurityCode.isdigit()):
                return "invalid security code", status.HTTP_400_BAD_REQUEST
            if not (len(SecurityCode) == 3):
                return "long/short security code", status.HTTP_400_BAD_REQUEST

        result = process(CreditCardNumber, CardHolder, Amount, ExpirationDate, SecurityCode)
        # Use Payment Gateway and get the result
        # result[1] shows the payment gateway used for transaction
        if result[0]:  # if True
            return "Payment Processed " + result[1], status.HTTP_200_OK
        else:  # if False
            return "Payment Failed " + result[1], status.HTTP_502_BAD_GATEWAY

    except:
        return "Some Error Occurred", status.HTTP_500_INTERNAL_SERVER_ERROR


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


app.run()

# run test.api to run test the app

#######################
# Hope it makes sense!#
# - Naazneen Jatu #####
#######################
