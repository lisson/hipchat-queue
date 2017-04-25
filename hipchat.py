import requests
import simplejson

class Hipchat(object):
    def __init__(self, url, ukey, ikey,rid):
        self.url = url
        self.user_key = ukey
        self.room_key = ikey
        self.room_id = rid
        self.header = {'content-type': 'application/json', "Authorization": ("Bearer {}".format(self.user_key))}
        self.notification_header = {'content-type': 'application/json', "Authorization": ("Bearer {}".format(self.room_key))}

    def register_webhook(self, target_url, pattern):
        # Where will the webhook send POST request to?
        request_url = "{}/v2/room/{}/webhook".format(self.url,self.room_id);
        payload = {"url":target_url,
                    "pattern": pattern,
                    "event":"room_message"}
        # We're suppose to use Create Room Webhook which requires PUT.
        # It doesn't work, but the deprecated API still works.
        r = requests.post(request_url, headers=self.header, data=simplejson.dumps(payload))
        print r.text

    def delete_webhook(self, webhook_id):
        r = requests.delete("{}/v2/room/{}/webhook/{}".format(self.url, self,room_id), headers=self.header)
        if (r.status_code == "204"):
            print "Removed webhook {}".format(webhook_id)

    def get_webhooks(self):
        request_url = "{}/v2/room/{}/webhook".format(self.url,self.room_id);
        print request_url
        r = requests.get(request_url, headers=self.header)
        if (r.status_code == 200):
            return r
        return None

    def delete_all_webhook(self):
        r = self.get_webhooks()
        json = r.json()
        for i in json['items']:
            request_url = "{}/v2/room/{}/webhook/{}".format(self.url,self.room_id, i['id']);
            r = requests.delete(request_url, headers=self.header)
            if (r.status_code == 204):
                print "Removed webhook {}".format(i['id'])
        return

    def send_message(self, message):
        request_url = "{}/v2/room/{}/notification".format(self.url,self.room_id);
        payload = {"message":message,
                    "notify": "false",
                    "message_format":"text"}
        requests.post(request_url, headers=self.notification_header, data=simplejson.dumps(payload))
        return
