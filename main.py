import json
import logging
import urllib
import urllib2
import webapp2
import configuration


TOKEN = '244650362:AAFbxcGVlhjA0luZdY1ZRmXLNtUGHi_zFkk'

MY_URL = "https://peyvandgaller1ybot.herokuapp.com/"

BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'

# config = configuration.Configuration('config/syslog.json')
# config.configuration['log_file'] = "sample_data/syslog"
# config.save()


config = configuration.Configuration("telebot.json")


def set_enabled(chat_id, yes):
    config.configuration[chat_id] = yes
    config.save()

def get_enabled(chat_id):
    if config.configuration[chat_id]:
        return config.configuration[chat_id]
    return False

# ================================

class MeHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getMe', timeout=60))))


class GetUpdatesHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getUpdates', timeout=60))))


class SetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        url = self.request.get('url')
        if url:
            self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'setWebhook', urllib.urlencode({'url': url}), timeout=60))))


class WebhookHandler(webapp2.RequestHandler):
    def post(self):
        body = json.loads(self.request.body)
        logging.info('request body:')
        logging.info(body)
        self.response.write(json.dumps(body))

        update_id = body['update_id']
        message = body['message']
        message_id = message.get('message_id')
        date = message.get('date')
        text = message.get('text')
        fr = message.get('from')
        chat = message['chat']
        chat_id = chat['id']

        if not text:
            logging.info('no text')
            return

        def reply(msg):
            resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                'chat_id': str(chat_id),
                'text': msg,
                'disable_web_page_preview': 'true',
                'reply_to_message_id': str(message_id),
            })).read()
            logging.info('send response:')
            logging.info(resp)

        if text.startswith('/'):
            if text == '/start':
                reply('Bot enabled')
                set_enabled(chat_id, True)
            elif text == '/stop':
                reply('Bot disabled')
                set_enabled(chat_id, False)
            else:
                reply('What command?')

        # CUSTOMIZE FROM HERE

        elif 'who are you' in text:
            reply('telebot starter kit, created by yukuku: https://github.com/yukuku/telebot')
        elif 'what time' in text:
            reply('look at the top-right corner of your screen!')
        else:
            if get_enabled(chat_id):
                resp1 = json.load(urllib2.urlopen('http://www.simsimi.com/requestChat?lc=en&ft=1.0&req=' + urllib.quote_plus(text.encode('utf-8'))))
                back = resp1.get('res')
                if not back:
                    reply('okay...')
                elif 'I HAVE NO RESPONSE' in back:
                    reply('you said something with no meaning')
                else:
                    reply(back)
            else:
                logging.info('not enabled for chat_id {}'.format(chat_id))


app = webapp2.WSGIApplication([
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
], debug=True)

def set_webhook():
    url = MY_URL + "/webhook/"
    if url:
        print(BASE_URL + 'setWebhook', urllib.urlencode({'url': url}))
        urllib2.urlopen(BASE_URL + 'setWebhook', urllib.urlencode({'url': url}))

def main():
    from paste import httpserver
    set_webhook()
    httpserver.serve(app, host='0.0.0.0', port='8080')


if __name__ == '__main__':
    main()
