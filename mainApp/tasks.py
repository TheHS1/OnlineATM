from celery import shared_task
from scripts import processCheck
from .models import *
from onlineATM.celery import app

@app.task
def procCheck(checkPK, imagePath):
    checkTransaction = checkTransactions.objects.get(id=checkPK)
    data = processCheck.getCheckInfo(imagePath)
    sender_id = int(data['sender_account'])
    sender_info = data['sender_info']
    recorded_date = data['date']
    spelled_amount = data['spelled_amount']
    recipient = data['recipient']
    memo = data['memo']
    sender = Accounts.objects.get(id=sender_id)
    amt = checkTransaction.transaction.amount

    if all(value != '' for value in data.values()):
        if float(data['numerical_amount']) == float(amt) and float(amt) > 0.0:
            if sender.balance >= amt:
                sender.balance -= amt
                checkTransaction.transaction.destination.balance += amt
                checkTransaction.transaction.source = sender;
                checkTransaction.sender_info = sender_info
                checkTransaction.spelled_amount = spelled_amount
                checkTransaction.recipient_name = recipient
                checkTransaction.memo = memo
                checkTransaction.transaction.save()
                checkTransaction.save()
                sender.save()
                checkTransaction.transaction.destination.save()
            else:
                checkTransaction.transaction.delete()
                checkTransaction.delete()
        else:
            checkTransaction.transaction.error = True
            checkTransaction.transaction.source = sender;
            checkTransaction.sender_info = sender_info
            checkTransaction.spelled_amount = spelled_amount
            checkTransaction.recipient_name = recipient
            checkTransaction.memo = memo
            checkTransaction.save()
            checkTransaction.transaction.save()
    else:
            checkTransaction.transaction.error = True
            checkTransaction.transaction.source = sender;
            checkTransaction.sender_info = sender_info
            checkTransaction.spelled_amount = spelled_amount
            checkTransaction.recipient_name = recipient
            checkTransaction.memo = memo
            checkTransaction.save()
            checkTransaction.transaction.save()
        




