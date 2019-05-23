import logging

from diagbot import DiagBot

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def main():
    DiagBot(token='Hello')


if __name__ == '__main__':
    main()
