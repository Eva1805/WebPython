import requests
import json
from operator import itemgetter

ACCESS_TOKEN = '17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711'

def calc_age(uid):
    url_user = 'https://api.vk.com/method/users.get?v=5.71&access_token=%s&user_ids=%s' % (ACCESS_TOKEN, uid)

    info = json.loads(requests.get(url_user).text)
    user_id = info['response'][0]['id']
    url_friends = 'https://api.vk.com/method/friends.get?v=5.71&access_token=%s&user_id=%d&fields=bdate' % (ACCESS_TOKEN, user_id)
    info = json.loads(requests.get(url_friends).text)['response']['items']
    res_dict = {}
    for friend in info:
        if 'bdate' in friend:
            bdate = friend['bdate'].split('.')
            if len(bdate) > 2:
                res_dict[bdate[2]] = res_dict.get(bdate[2], 0) + 1
    res = []
    for key in res_dict.keys():
        age = 2018 - int(key)
        res.append((age, res_dict[key]))
    res = sorted(res, key=lambda tup:(-tup[1], tup[0]))
    # res = res[::-1]
    return res



if __name__ == '__main__':
    res = calc_age('reigning')
    print(res)
