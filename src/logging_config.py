import logging
import os

# Configure logging
os.makedirs("logs", exist_ok=True)
with open('logs/logs.txt', 'w', encoding='utf-8'):
    pass
logging.basicConfig(filename='logs/logs.txt', level=logging.INFO, encoding='utf-8')