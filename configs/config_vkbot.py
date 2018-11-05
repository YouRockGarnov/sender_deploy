from flask import request
from tools.debug import getDEBUG
from tools.log import logger, logged

@logged
def get_token():
    if getDEBUG():
        logger.info('DEBUG = True')
        return 'bddeddc0f08b56addc83768d464cea4246ecb5e1b2c9b5df894900aeb84dcec396cc77eae7a5b6062bd6f'

    logger.info('URL: {0}'.format(request.url_root))
    if request.url_root == 'http://tattoo-release.herokuapp.com/':
        logger.info('Я взял этот токен - 41da...')
        return '41da46788fcebab7d73426c8a015f829ec9b21b6680136e4e474df7dc980d4219c66eebcb6292c5ec405b'
    else:
        logger.info('Я взял этот токен - bdde...')
        return 'bddeddc0f08b56addc83768d464cea4246ecb5e1b2c9b5df894900aeb84dcec396cc77eae7a5b6062bd6f'

confirmation_token = '6d75c23e'
main_url = 'https://tattoo-sender.herokuapp.com'