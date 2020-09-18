from Cryptodome.Cipher import AES
import base64
import requests
import json
from lxml import etree
import re


class NetEaseSongCrawler:
    def __init__(self, song_id:str="21268932"):

        self.headers = {
            'authority': 'music.163.com',
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
            'content-type': 'application/x-www-form-urlencoded',
            'accept': '*/*',
            'origin': 'https://music.163.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://music.163.com/song?id=1426301364',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': '_iuqxldmzr_=32; _ntes_nnid=5f8ee04e745645d13d3f711c76769afe,1593048942478; _ntes_nuid=5f8ee04e745645d13d3f711c76769afe; WM_TID=XqvK2%2FtWaSBEUBRBEEN7XejGE%2FL0h6Vq; WM_NI=iN6dugAs39cIm2K2R9ox28GszTm5oRjcvJCcyIuaI1dccEVSjaHEwhc8FuERfkh3s%2FFP0zniMA5P4vqS4H3TJKdQofPqezDPP4IR5ApTjuqeNIJNZkCvHMSY6TtEkCZUS3k%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeb2e57dbababf88b879a8b08fa2d84f869f9fbaaa50a3f599a5d650939b8dadd52af0fea7c3b92aab92fa85f86d83adfddae243afee85d3d133ada8fed9c679ba8ca3d6ee5aaabdbaabc269bb97bb82cc3ba8bdada6d559aabf88a6f664a1e88a96c85aa6b5a8d4f2258690009bed638f9ffbb1b77eb38dfca9b2608a95acb2ee6e94afab9bc75c94ec87b3b84bb48ca696f46f8e9786afd96181aa88aed253f68cbca6ea499a8b9dd4ea37e2a3; JSESSIONID-WYYY=tI8MIKMCRBuyCYnUJMCyUTlp%2Fufv5xIfCquvp7PJ4%2BuXod%5CXH%5CB0icDZw8TNlwHUHOW%2B2t%2BCuXyC4VZ%5C19OrzaDE%5Ck0F0dAZQh7KcVxUoHKpqUdiVzPu8NxCK9cJRG%5C%5CPTvtqxjFerd1%2BBa4%2F%5C8PESa4pvvRaQF6jljjsibX%5CrcPsH0I%3A1593347447142',
        }

        self.song_id = song_id
        self.encSecKey = "7ca9b5ba8b13044f47ed74c388df912ac84758122acbedc64111f2ac83232b01d3ce16f7195a39c7e064b4c0240b5c1d52624dc13c22ec820d76dfe32db43e496aeacced5be3ca9108c78a85bb389f1edf8d8c9fced02024ba9490401b4ce062cc50764d0a24294e07bb229271391b5a3640e924ee1ed15435dc6e288f1fa873"
        self.iv = b'0102030405060708'
        self.NetEaseKey1 = b"0CoJUm6Qyw8W8jud"
        self.key2 = b"l6Brr86UeZ6C3Bsw"

    API_Search_Songs = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='

    API_Comments_Song = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?csrf_token='  # 音乐ID可替换

    API_Lyric_Songs = 'https://music.163.com/weapi/song/lyric?csrf_token='

    API_Download = "https://music.163.com/song/media/outer/url?id={song_id}.mp3"

    def encrypt(self, text, key):
        BS = AES.block_size
        if isinstance(text, str):
            text = text.encode('utf-8')
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode('utf-8')
        text = pad(text)
        IV = b'0102030405060708'
        encryptor = AES.new(key, AES.MODE_CBC, iv=IV)
        cipher_text = encryptor.encrypt(text)
        encrypted = base64.b64encode(cipher_text).decode("utf-8")
        return encrypted

    def getEncText(self,params):
        encText = self.encrypt(params, self.NetEaseKey1)
        encText = self.encrypt(encText, self.key2)
        return encText

    def lyrics_parse(self,lyrics_text):
        reg_pattern = "\[.+\]"
        pattern = re.compile(reg_pattern)
        lyrics = pattern.sub("",lyrics_text)
        lyrics = self.filter_line_feed(lyrics)
        return lyrics

    def filter_line_feed(self,_str):
        _list = list(_str)
        n = len(_list)
        if n <= 1:
            print(_str)
            return
        list1 = []
        for i in range(n - 1):
            if _list[i] != _list[i + 1] or _list[i] !="\n":
                list1.append(_list[i])
        list1.append(_list[-1])
        str1 = ''.join(list1)
        return str1


    def getLyrics(self):
        text = '{"id":"%s","lv":-1,"tv":-1,"csrf_token":""}'%(self.song_id)
        # text = '{"id":"%s","lv":-1,"tv":-1,"csrf_token":""}' % ("1459950258")
        params = (
            ('csrf_token', ''),
        )
        data = {
            'params': self.getEncText(text),
            'encSecKey': self.encSecKey
        }
        response = requests.post(self.API_Lyric_Songs, headers=self.headers, params=params, data=data)
        res_json = json.loads(response.text)
        lyrics_text = res_json["lrc"]["lyric"]
        print(self.lyrics_parse(lyrics_text))

    def get_one_page_comment(self,offset:int=0,limit:int=50):
        '''

        :param offset: 偏移量
        :param limit:  每次请求返回的评论数
        :return:
        '''
        text = '{"rid":"R_SO_4_%s","offset":"%s","total":"true","limit":"%s","csrf_token":""}'%(self.song_id,offset*50,limit)
        params = (
            ('csrf_token', ''),
        )

        data = {
            'params': self.getEncText(text),
            'encSecKey': self.encSecKey
        }
        response = requests.post(self.API_Comments_Song.format(self.song_id), headers=self.headers, params=params, data=data)
        print(response.text)

    def download_song(self):
        headers = {
            "authority": "music.163.com",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
            "cookie": "_ntes_nnid=1f87e183c7eba533da9d8036c26fe3da,1597888217651; _ntes_nuid=1f87e183c7eba533da9d8036c26fe3da; UM_distinctid=1743484aed4555-0113b4830d2127-4353761-1fa400-1743484aed5bda; vinfo_n_f_l_n3=e82858abf55d990d.1.0.1598608944128.0.1598608961896; _ntes_newsapp_install=false; _iuqxldmzr_=32; WM_TID=X0322mUil9tARBQABUMqNQUk%2BqZXAxMc; playerid=99185480; WM_NI=1LG9uCt8MrPu%2BwmE87eZb%2FAW2EVox7tdUWKypzLtlMbeYSLIekEc8mIQ8C1b8FFM2mZhtUQAeJOsoRX04EJoxEKrO5hM71FgdmhXuNbpBShoIDtNsQH8cYuInO4V61kOUlM%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeb7d15d94ec9896c77cf5968ba6c54a879a9abaae469ca88495b66df8b68789c72af0fea7c3b92af39489daf849b8e88393d37fe9a9a3a6bb3da786aed0c45df29b9a90fb3db8bc9bb8ca73b4a68495ef47a2bb97b4cf43a7b58b84bb678b8ff8a4b46afc9a8aaeb1679ab8bcb6d44ba7968194ee5a9cf0fca6c965bc9b8593ce3fac93f9d2c56da8b3a8b9f846a2b08eb4eb658b9cbcaff25b8ce8adbaf843ae91fcb7b53ba9919b8dd037e2a3; JSESSIONID-WYYY=MpN7VMEJSGxZ6jNbVCoFrZCRfDpfqlZ%2BmcVu6R9Qi9%2FIxZ1cpFV73SRq1CnuFnmfi9gn9VB5VCbuYsUzkCNOqphWtWC3cah246xdMkO8nuUgeBA9GJD%2Fim8jzIT7cJ%2Fm7ApicDSj8lN7%2FjjWInwv%2B5F48BrCzQlyH9CzFZBHVUXI1sO4%3A1599443367066"

        }
        r = requests.get(self.API_Download.format(song_id=self.song_id), params=None, headers=headers)
        print(r.is_redirect)
        print(r.history)
        for r in r.history:
            print(r.headers)


board_id = {
    "云音乐飙升榜": "19723756",
    "云音乐新歌榜": "3779629",
    "网易原创歌曲榜": "2884035",
    "云音乐热歌榜": "3778678",
    "云音乐说唱榜": "991319590",
    "云音乐电音榜": "1978921795",
    "抖音排行榜":"2250011882",
    "中国新乡村音乐排行榜":"3112516681",
    "云音乐民谣榜": "5059661515",
    "云音乐古风榜":"5059642708",
    "云贝推歌榜":"5201625538"
}


class NetEaseSongListCrawler:
    def __init__(self, board_id:str):
        self.board_id = board_id

    Song_List_Api = "https://music.163.com/discover/toplist?id={id}"

    def parse_song_list(self):
        list_url = self.Song_List_Api.format(id=self.board_id)
        res = requests.get(list_url)
        song_list = etree.HTML(res.text).xpath("//textarea[@id='song-list-pre-data']//text()")[0]
        song_list_json = json.loads(song_list)
        for song in song_list_json:
            print("name: ", song["name"])
            print("artists: ", song["artists"])
            print("publishTime: ", song["publishTime"])
            print("commentThreadId: ", song["commentThreadId"])
            print("id", song["id"])
            print("alias: ", song["alias"])

if __name__ == '__main__':
    song_crawler = NetEaseSongCrawler("20163335")
    song_crawler.getLyrics()
    song_crawler.download_song()