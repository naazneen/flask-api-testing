import unittest
from api import app


class MyTestCase(unittest.TestCase):
    tester = app.test_client()

    def test_home_CardNumber(self):
        response = self.tester.get('/?CardHolder="Hana"&ExpirationDate=21-03&Amount=40')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data,b"Error: No CreditCardNumber field provided. Please specify CreditCardNumber.")

    def test_home_CardHolder(self):
        response = self.tester.get('/?CreditCardNumber=1200147852365478&ExpirationDate=21-03&Amount=40')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data,b"Error: No CardHolder field provided. Please specify CardHolder.")

    def test_home_Expiration_NotGiven(self):
        response = self.tester.get('/?CreditCardNumber=1200147852365478&CardHolder="Hana"&Amount=40')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Error: No ExpirationDate field provided. Please specify an ExpirationDate.")

    def test_home_Expiration_Expired(self):
        response = self.tester.get('/?CreditCardNumber=1200147852365478&CardHolder="Hana"&ExpirationDate=19-03&Amount=40')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Error: ExpirationDate has passed.")

    def test_home_Expiration_WrongFormat(self):
        response = self.tester.get(
            '/?CreditCardNumber=1200147852365478&CardHolder="Hana"&ExpirationDate=20/03&Amount=40')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Error: invalid Expiration Data format")

    def test_home_Amount_Invalid(self):
        response = self.tester.get(
            '/?CreditCardNumber=1200147852365478&CardHolder="Hana"&ExpirationDate=21-03&Amount=d40')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Error: invalid amount")

    def test_home_Amount_Negative(self):
        response = self.tester.get(
            '/?CreditCardNumber=1200147852365478&CardHolder="Hana"&ExpirationDate=21-03&Amount=-40')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Error: invalid amount(negative)")

    def test_home_Amount_NotGiven(self):
        response = self.tester.get(
            '/?CreditCardNumber=1200147852365478&CardHolder="Hana"&ExpirationDate=21-03')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Error: No Amount field provided. Please specify an Amount.")

    def test_home_Security_More(self):
        response = self.tester.get(
            '/?CreditCardNumber=1200147852365478&CardHolder="Hana"&ExpirationDate=21-03&Amount=40&SecurityCode=1234')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"long/short security code")

    def test_home_Security_Invalid(self):
        response = self.tester.get(
            '/?CreditCardNumber=1200147852365478&CardHolder="Hana"&ExpirationDate=21-03&Amount=40&SecurityCode=S34')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"invalid security code")

    def test_cheap(self):
        response = self.tester.get('/?CreditCardNumber=1200147852365478&CardHolder="Hana"&ExpirationDate=21-03&Amount=4')
        if response.data == b"Payment Failed using CheapPaymentGateway":
            #print("here")
            self.assertEqual(response.status_code, 502)
        elif response.data == b"Payment Processed using CheapPaymentGateway":
            #print("there")
            self.assertEqual(response.status_code, 200)

    def test_expensive(self):
        response = self.tester.get(
            '/?CreditCardNumber=1200147852365478&CardHolder="Hana"&ExpirationDate=21-03&Amount=40')
        if response.data == b"Payment Failed using ExpensivePaymentGateway" or response.data == b"Payment Failed using CheapPaymentGateway":
            # print("here")
            self.assertEqual(response.status_code, 502)
        elif response.data == b"Payment Processed using ExpensivePaymentGateway" or response.data == b"Payment Processed using CheapPaymentGateway":
            # print("there")
            self.assertEqual(response.status_code, 200)

    def test_premium(self):
        response = self.tester.get(
            '/?CreditCardNumber=1200147852365478&CardHolder="Hana"&ExpirationDate=21-03&Amount=500')
        if response.data == b"Payment Failed using PremiumPaymentGateway":
            # print("here")
            self.assertEqual(response.status_code, 502)
        elif response.data == b"Payment Processed using PremiumPaymentGateway":
            # print("there")
            self.assertEqual(response.status_code, 200)

    def test_404(self):
        response = self.tester.get(
            '/card/?id=0')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, b"<h1>404</h1><p>The resource could not be found.</p>")



if __name__ == '__main__':
    unittest.main()
