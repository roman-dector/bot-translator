from config import DEBUG
from dispatcher import run_polling, run_webhook


if (__name__ == "__main__") and DEBUG:
    run_polling()
else:
    run_webhook()