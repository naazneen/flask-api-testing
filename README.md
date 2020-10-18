# flask-process-payment
## Introduction
This is an api to redirect to the payment gateways base on the payment Amount in request.

## To run the app:
Go to root directory from cmd and type
```
python api.py
```
Open Brwoser and type:
http://127.0.0.1:5000/?CreditCardNumber=12000&CardHolder=%22Hana%22&ExpirationDate=21-03&Amount=4000

Change Amount and see different results.
Can also provide 3 digit Security Code.

## To test the app
Go to root directory from cmd and type
```
python test.api.py
```
