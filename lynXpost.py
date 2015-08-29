#!/usr/bin/env python
# -*- coding: utf-8 -*-

import vk_api
import twitter
import facebook
import pprint

pp = pprint.PrettyPrinter(indent=4)


class xpost():
    
    '''
    get vk token: https://oauth.vk.com/authorize?client_id=5046122&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=73728&response_type=token&v=5.37
    '''
    def __init__(self):
        self.vk = vk_api.VkApi(token = '', app_id = 5046122, scope=73728)
        try:
            self.vk.authorization()
        except vk_api.AuthorizationError as error_msg:
            print(error_msg)
            return

    def readVk(self, msgCount = 1):
        items = []
        response = self.vk.method('wall.get', {'count': msgCount})
        if response['items']:
            for i in response['items']:
                item = {}
                if i['text']:
                    item['text'] = i['text']
                    item['id'] = i['id']
                    if 'attachments' in i:
                        item['attachments'] = []
                        for attachment in i['attachments']:
                            if attachment['type'] == 'photo':
                                photo =  attachment['photo']
                                pNum = max(map(lambda key: int(key.split('_')[1]) if 'photo' in key else 0, photo.keys()))
                                item['attachments'].append({'text': photo['text'], 'url': photo['photo_' + str(pNum)]})
                    items.append(item)
        return items
                

    def postTwi(self):
        pass
    
    def postFb(self):
        pass
    
    def repostFromVk(self):
        pass
        

def main():
    x = xpost()
    for post in x.readVk(4):
        print "postID: ", post['id'], "text: ", post['text'] 
        if 'attachments' in post:
            print "photos: ",
            for attachment in  post['attachments']:
                print attachment['text'], ": ", attachment['url']
        print "--------------------------------------------------------------"

if __name__ == '__main__':
    main()
