#!/usr/bin/env python
# -*- coding: utf-8 -*-

import vk_api
import twitter
import facebook
import pprint
import ConfigParser


pp = pprint.PrettyPrinter(indent=4)


class xpost():
    
    def __init__(self, vkToken):
        self.vk = vk_api.VkApi(token = vkToken, app_id = 5046122, scope=73728)

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
                
    def editVk(self, postId, text):
        return self.vk.method('wall.edit', {'post_id': postId, 'message': text})
    
    def postTwi(self):
        pass
    
    def postFb(self):
        pass
    
    def repostFromVk(self):
        pass
        

def main():
    config = ConfigParser.ConfigParser()
    config.read('lynXpost.cfg')

    x = xpost(vkToken = config.get('vkontakte', 'token'))

    for post in x.readVk(3):
        print "postID: ", post['id'], "text: ", post['text']
        if "#lynXpost" in post['text']:
            x.editVk(post['id'], post['text'].replace("#lynXpost", "")) 
        if 'attachments' in post:
            print "photos: ",
            for attachment in  post['attachments']:
                print attachment['text'], ": ", attachment['url']
        print "--------------------------------------------------------------"

if __name__ == '__main__':
    main()
