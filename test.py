import requests
import os
from lxml import etree
import json



#
# headers = {
#     'authority': 'music.163.com',
#             'user-agent': UserAgent().random,
#             'content-type': 'application/x-www-form-urlencoded',
#             'accept': '*/*',
#             'origin': 'https://music.163.com',
#             'sec-fetch-site': 'same-origin',
#             'sec-fetch-mode': 'cors',
#             'sec-fetch-dest': 'empty',
#             'referer': 'https://music.163.com/song?id=1426301364',
#             'accept-language': 'zh-CN,zh;q=0.9',
#             'cookie': '_iuqxldmzr_=32; _ntes_nnid=5f8ee04e745645d13d3f711c76769afe,1593048942478; _ntes_nuid=5f8ee04e745645d13d3f711c76769afe; WM_TID=XqvK2%2FtWaSBEUBRBEEN7XejGE%2FL0h6Vq; WM_NI=iN6dugAs39cIm2K2R9ox28GszTm5oRjcvJCcyIuaI1dccEVSjaHEwhc8FuERfkh3s%2FFP0zniMA5P4vqS4H3TJKdQofPqezDPP4IR5ApTjuqeNIJNZkCvHMSY6TtEkCZUS3k%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeb2e57dbababf88b879a8b08fa2d84f869f9fbaaa50a3f599a5d650939b8dadd52af0fea7c3b92aab92fa85f86d83adfddae243afee85d3d133ada8fed9c679ba8ca3d6ee5aaabdbaabc269bb97bb82cc3ba8bdada6d559aabf88a6f664a1e88a96c85aa6b5a8d4f2258690009bed638f9ffbb1b77eb38dfca9b2608a95acb2ee6e94afab9bc75c94ec87b3b84bb48ca696f46f8e9786afd96181aa88aed253f68cbca6ea499a8b9dd4ea37e2a3; JSESSIONID-WYYY=tI8MIKMCRBuyCYnUJMCyUTlp%2Fufv5xIfCquvp7PJ4%2BuXod%5CXH%5CB0icDZw8TNlwHUHOW%2B2t%2BCuXyC4VZ%5C19OrzaDE%5Ck0F0dAZQh7KcVxUoHKpqUdiVzPu8NxCK9cJRG%5C%5CPTvtqxjFerd1%2BBa4%2F%5C8PESa4pvvRaQF6jljjsibX%5CrcPsH0I%3A1593347447142',
# }
#
#

#
# NETEASE_P2 = "010001"
# NETEASE_P3 = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629e" \
#              "c4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe" \
#              "4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
# NETEASE_P4 = "0CoJUm6Qyw8W8jud"
#
#
# def add_to_16(text):
#     if len(text.encode('utf-8')) % 16:
#         add = 16 - (len(text.encode('utf-8')) % 16)
#     else:
#         add = 0
#     text = text + ('\0' * add)
#     return text.encode('utf-8')
#
#
# def function_a(a):
#     b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
#     c = ""
#     for d in range(0, a):
#         e = random.randint(0, len(b)-1)
#         c += b[e]
#     return c
#
#
# def function_b(text, key):
#     '''
#     AES
#     :param a: text
#     :param b: key
#     :return:
#     '''
#     BS = AES.block_size
#     if isinstance(text,str):
#         text = text.encode('utf-8')
#     pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode('utf-8')
#     text = pad(text)
#     key = key.encode("utf-8")
#     IV = b'0102030405060708'
#     encryptor = AES.new(key,AES.MODE_CBC,iv=IV)
#     cipher_text = encryptor.encrypt(text)
#     encrypted = base64.b64encode(cipher_text).decode("utf-8")
#     return encrypted
#
#
# def function_d(json_param,NETEASE_P2,NETEASE_P3,NETEASE_P4):
#     key2 = "l6Brr86UeZ6C3Bsw" # 默认使用此字符串
#     encText = function_b(json_param, NETEASE_P4)
#     encText = function_b(encText,key2)
#     return encText
#
#
# def get_json(url, params, encSecKey):
#     data = {
#         "params": params,
#         "encSecKey": encSecKey
#     }
#     params = (
#         ('csrf_token', ''),
#     )
#     res = requests.post(url, headers=headers, data=data,params=params)
#     return res
#
#


board_id = {
    "云音乐飙升榜": "19723756",
    "云音乐新歌榜": "3779629",
    "网易原创歌曲榜": "2884035",
    "云音乐热歌榜": "3778678",
    "云音乐说唱榜": "991319590"
}


def save_mp3():
    url = "https://music.163.com/song/media/outer/url?id=27759605.mp3"
    headers = {
        "authority":"music.163.com",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
        "cookie":"_ntes_nnid=1f87e183c7eba533da9d8036c26fe3da,1597888217651; _ntes_nuid=1f87e183c7eba533da9d8036c26fe3da; UM_distinctid=1743484aed4555-0113b4830d2127-4353761-1fa400-1743484aed5bda; vinfo_n_f_l_n3=e82858abf55d990d.1.0.1598608944128.0.1598608961896; _ntes_newsapp_install=false; _iuqxldmzr_=32; WM_TID=X0322mUil9tARBQABUMqNQUk%2BqZXAxMc; playerid=99185480; WM_NI=1LG9uCt8MrPu%2BwmE87eZb%2FAW2EVox7tdUWKypzLtlMbeYSLIekEc8mIQ8C1b8FFM2mZhtUQAeJOsoRX04EJoxEKrO5hM71FgdmhXuNbpBShoIDtNsQH8cYuInO4V61kOUlM%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeb7d15d94ec9896c77cf5968ba6c54a879a9abaae469ca88495b66df8b68789c72af0fea7c3b92af39489daf849b8e88393d37fe9a9a3a6bb3da786aed0c45df29b9a90fb3db8bc9bb8ca73b4a68495ef47a2bb97b4cf43a7b58b84bb678b8ff8a4b46afc9a8aaeb1679ab8bcb6d44ba7968194ee5a9cf0fca6c965bc9b8593ce3fac93f9d2c56da8b3a8b9f846a2b08eb4eb658b9cbcaff25b8ce8adbaf843ae91fcb7b53ba9919b8dd037e2a3; JSESSIONID-WYYY=MpN7VMEJSGxZ6jNbVCoFrZCRfDpfqlZ%2BmcVu6R9Qi9%2FIxZ1cpFV73SRq1CnuFnmfi9gn9VB5VCbuYsUzkCNOqphWtWC3cah246xdMkO8nuUgeBA9GJD%2Fim8jzIT7cJ%2Fm7ApicDSj8lN7%2FjjWInwv%2B5F48BrCzQlyH9CzFZBHVUXI1sO4%3A1599443367066"

    }
    r = requests.get(url,params=None,headers=headers)

    print(r.is_redirect)
    print(r.history)
    mp3_url = r.history[0].headers["location"]
    for r in r.history:
        print(r.headers["Location"])


# if __name__ == '__main__':
#     list_url = "https://music.163.com/discover/toplist?id=19723756"
#     res = requests.get(list_url)
#     song_list = etree.HTML(res.text).xpath("//textarea[@id='song-list-pre-data']//text()")[0]
#     song_list_json = json.loads(song_list)
#     for song in song_list_json:
#         print("name: ",song["name"])
#         print("artists: ", song["artists"])
#         print("publishTime: ",song["publishTime"])
#         print("commentThreadId: ",song["commentThreadId"])
#         print("id",song["id"])
#         print("alias: ", song["alias"])
#     save_mp3()

def filter_same(_str):
    _list = list(_str)
    n = len(_list)
    if n <= 1:
        print(_str)
        return
    list1 = []
    for i in range(n - 1):
        if _list[i] != _list[i + 1] or _list[i] != "\n":
            list1.append(_list[i])
    list1.append(_list[-1])
    str1 = ''.join(list1)
    return str1

print(filter_same("111\n\n\n111"))