from config import DEBUG
from dispatcher import run_polling, run_webhook


if (__name__ == "__main__") and (DEBUG == "True"):
    run_polling()
elif (__name__ == "__main__"):
    run_webhook()

