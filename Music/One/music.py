import requests
from lxml import etree
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}


def kugou(name):
    url = 'https://songsearch.kugou.com/song_search_v2?keyword={}&page=1&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0'.format(str(name))
    response = requests.get(url=url, headers=headers).content.decode('utf-8')
    one_dic = json.loads(response)
    all_musics = one_dic['data']['lists']
    music = []
    if len(all_musics) >= 10:
        for one_music in all_musics[:10]:
            data = {}
            data['music'] = one_music['FileName'].replace('<', '').replace('em', '').replace('/', '').replace('>', '')
            data['singer'] = one_music['SingerName']
            data['ord_hash'] = one_music['FileHash']
            data['hq_hash'] = one_music['HQFileHash']
            music.append(data)
    else:
        for one_music in all_musics:
            data = {}
            data['music'] = one_music['FileName'].replace('<', '').replace('em', '').replace('/', '').replace('>', '')
            data['singer'] = one_music['SingerName']
            data['ord_hash'] = one_music['FileHash']
            data['hq_hash'] = one_music['HQFileHash']
            music.append(data)
    for one_music in music:
        url = 'https://wwwapi.kugou.com/yy/index.php?r=play/getdata&hash={}'.format(one_music['ord_hash'])
        response = requests.get(url=url, headers=headers).content.decode('utf-8')
        one_music['one_link'] = json.loads(response, strict=False)['data']['play_url']
        del one_music['ord_hash']
        if one_music['hq_hash']:
            url = 'https://wwwapi.kugou.com/yy/index.php?r=play/getdata&hash={}'.format(one_music['hq_hash'])
            response = requests.get(url=url, headers=headers).content.decode('utf-8')
            one_music['two_link'] = json.loads(response)['data']['play_url']
            if not one_music['two_link']:
                del one_music['two_link']
            else:
                one_music['one_link'] = one_music['two_link']
                del one_music['two_link']
            del one_music['hq_hash']
        else:
            del one_music['hq_hash']
    i = 0
    i_list = []
    for one_music in music:
        if one_music['one_link'] == '':
            i_list.append(i)
        i += 1
    while i_list:
        del music[i_list.pop()]
    return music


def qianqian(name):
    url = 'http://music.taihe.com/search?key={}'.format(str(name))
    response = requests.get(url=url, headers=headers).content.decode('utf-8')
    tree = etree.HTML(response)
    li_list = tree.xpath('//div[@monkey="song-list"]/ul/li')
    music = []
    if len(li_list) > 10:
        for li in li_list[:10]:
            one_music = {}
            song_title = li.xpath('./div/span[@class="song-title"]/a/em/text()')
            if song_title:
                one_music['music'] = song_title[0]
            else:
                song_title = li.xpath('./div/span[@class="song-title"]/a/text()')
                if song_title:
                    one_music['music'] = song_title[0]
                else:
                    continue
            song_id = li.xpath('./div/span[@class="song-title"]/a/@href')
            if song_id:
                one_music['id'] = song_id[0].split('/')[-1]
            else:
                continue
            singer = li.xpath('./div/span[@class="singer"]/span/@title')
            if singer:
                one_music['singer'] = singer[0]
            music.append(one_music)
    else:
        for li in li_list:
            one_music = {}
            song_title = li.xpath('./div/span[@class="song-title"]/a/em/text()')
            if song_title:
                one_music['music'] = song_title[0]
            else:
                song_title = li.xpath('./div/span[@class="song-title"]/a/text()')
                if song_title:
                    one_music['music'] = song_title[0]
                else:
                    continue
            song_id = li.xpath('./div/span[@class="song-title"]/a/@href')
            if song_id:
                one_music['id'] = song_id[0].split('/')[-1]
            else:
                continue
            singer = li.xpath('./div/span[@class="singer"]/span/@title')
            if singer:
                one_music['singer'] = singer[0]
            music.append(one_music)
    for one_music in music:
        id = one_music['id']
        url = 'http://musicapi.taihe.com/v1/restserver/ting?method=baidu.ting.song.playAAC&format=jsonp&songid={}&from=web'.format(str(id))
        try:
            response = requests.get(url=url, headers=headers).content.decode('utf-8')
            all_dic = json.loads(response)
        except Exception as e:
            pass
        else:
            music_url = all_dic['bitrate']['show_link']
            one_music['one_link'] = music_url
        finally:
            del one_music['id']
    n_list = []
    n = 0
    for one_music in music:
        try:
            url = one_music['one_link']
        except Exception as e:
            n_list.append(n)
        n += 1
    while n_list:
        n = n_list.pop()
        music.remove(music[n])
    return music


def migu(name):
    url = 'http://music.migu.cn/v3/search?keyword={}'.format(str(name))
    response = requests.get(url=url, headers=headers).content.decode('utf-8')
    tree = etree.HTML(response)
    div_list = tree.xpath('//div[@id="js_songlist"]/div')
    music = []
    if len(div_list) > 10:
        for div in div_list[:10]:
            one_music = {}
            song_name = div.xpath('./div[3]/span[1]/a/@title')
            if song_name:
                one_music['music'] = song_name[0]
            else:
                continue
            id = div.xpath('./div[3]/span[1]/a/@href')
            if id:
                one_music['id'] = id[0].split('/')[-1]
            else:
                continue
            singer = div.xpath('./div[@class="song-singer"]/a/text()')
            if singer:
                one_music['singer'] = singer[0]
            music.append(one_music)
    else:
        for div in div_list:
            one_music = {}
            song_name = div.xpath('./div[3]/span[1]/a/@title')
            if song_name:
                one_music['music'] = song_name[0]
            else:
                continue
            id = div.xpath('./div[3]/span[1]/a/@href')
            if id:
                one_music['id'] = id[0].split('/')[-1]
            else:
                continue
            singer = div.xpath('./div[@class="song-singer"]/a/text()')
            if singer:
                one_music['singer'] = singer[0]
            music.append(one_music)
    for one_music in music:
        id = one_music['id']
        url = 'http://music.migu.cn/v3/api/music/audioPlayer/getPlayInfo?copyrightId={}'.format(str(id))
        response = requests.get(url=url, headers=headers).content.decode('utf-8')
        all_dic = json.loads(response)
        try:
            music_url = all_dic['walkmanInfo']['playUrl']
        except Exception as e:
            one_music['one_link'] = ''
        else:
            one_music['one_link'] = music_url
        del one_music['id']
    i = 0
    i_list = []
    for one_music in music:
        if one_music['one_link'] == '':
            i_list.append(i)
        i += 1
    while i_list:
        del music[i_list.pop()]
    return music

