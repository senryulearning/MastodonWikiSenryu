#追加ライブラリ
import urllib
import xml.etree.ElementTree as elementtree
import MeCab
import random

WIKI_URL = u"http://wikipedia.simpleapi.net/api?keyword="

class CreateResult:
   senryu = ''
   furigana = ''
   errormessage = ''
   word = ''
   url = ''

def createSenryu(serch_word):
    utftext =  serch_word.encode('utf-8')
    urlencode = urllib.parse.quote(utftext, '')
    request = urllib.request.Request(WIKI_URL + urlencode)
    result =  CreateResult()

    with urllib.request.urlopen(request) as response:
        XmlData = response.read()

    if len(XmlData) == 0:
        result.errormessage = 'Wikipediaに該当ページがありませんでした。'
        return result

    root = elementtree.fromstring(XmlData)

    if len(root) == 0:
        result.errormessage = 'Wikipediaに該当ページがありませんでした。'
        return result

    result.url = root[0][2].text
    result.word = root[0][3].text

    tagger = MeCab.Tagger('-Ochasen')
    nodes = tagger.parseToNode(root[0][4].text)

    bunsetsulist = []
    PoemPartslist = []

    kamigolist = []
    nakashichilist = []
    shimogolist = []

    spellCount = 0

    while nodes:
        #長文のため分割したいが、いい方法が思い浮かばず保留
        splitData =  nodes.feature.split(',')
        SplitLength =  len(splitData)
        if SplitLength <= 7:
            bunsetsulist = []
            spellCount= 0
            nodes = nodes.next
            continue

        furigana = splitData[7]
        furiganaCount =  mojiCount(furigana)
        spellCount +=  furiganaCount
        bunsetsulist.append(nodes)

        if splitData[0] in '記号':
            bunsetsulist = []
            spellCount= 0
            nodes = nodes.next
            continue

        if splitData[0] in '助詞' and len(bunsetsulist) == 1:
            bunsetsulist = []
            spellCount= 0
            nodes = nodes.next
            continue

        if splitData[0] in '助動詞' and len(bunsetsulist) == 1:
            bunsetsulist = []
            spellCount= 0
            nodes = nodes.next
            continue

        if splitData[1] in '非自立' and len(bunsetsulist) == 1:
            bunsetsulist = []
            spellCount= 0
            nodes = nodes.next
            continue

        if splitData[1] in '接尾' and len(bunsetsulist) == 1:
            bunsetsulist = []
            spellCount= 0
            nodes = nodes.next
            continue

        if splitData[5] in '未然レル接続' and (furiganaCount == 5 or furiganaCount == 7):
            bunsetsulist = []
            spellCount= 0
            nodes = nodes.next
            continue

        if splitData[0] in '接頭詞' and (furiganaCount == 5 or furiganaCount == 7):
            bunsetsulist = []
            spellCount= 0
            nodes = nodes.next
            continue

        if furigana in '*':
            bunsetsulist = []
            spellCount= 0
            nodes = nodes.next
            continue

        if is_sokuon(furigana[-1]) and (furiganaCount == 5 or furiganaCount == 7):
            bunsetsulist = []
            spellCount= 0
            nodes = nodes.next
            continue

        if spellCount == 5:
            gobiindex = len (bunsetsulist)
            if IsKire(bunsetsulist[gobiindex - 1]) == True:
                kamigolist.append(list(bunsetsulist))
                shimogolist.append(list(bunsetsulist))
            else:
                kamigolist.append(list(bunsetsulist))

        if  spellCount == 7:
            nakashichilist.append(list(bunsetsulist))
            bunsetsulist = []
            spellCount= 0
            if furiganaCount == 7 :
                 nodes = nodes.next
            continue

        if spellCount > 7:
            bunsetsulist = []
            spellCount= 0
            if furiganaCount > 7 :
                 nodes = nodes.next
            continue

        nodes = nodes.next

    furigana = ''
    senryu = ''
    bunsho = []
    create = False

    for count in range(10):

        #長文のため分割したいが、いい方法が思い浮かばず保留
        furigana = ''
        senryu = ''
        bunsho = []
        create = False

        if len(kamigolist) == 0 or len(nakashichilist) == 0 or len(shimogolist) == 0:
            result.errormessage = '句の素材がたりず、生成できませんでした。'
            return result

        kamigo = random.choice(kamigolist)
        nakashichi = random.choice(nakashichilist)
        shimogo = random.choice(shimogolist)

        kamigofurigana = ''
        nakahachifurigana = ''
        simogofurigana = ''

        for spell in kamigo:
            senryu += spell.surface
            kamigofurigana += spell.feature.split(',')[7]
            bunsho.append(spell)

        for spell in nakashichi:
            senryu += spell.surface
            nakahachifurigana += spell.feature.split(',')[7]
            bunsho.append(spell)

        for spell in shimogo:
            senryu += spell.surface
            simogofurigana += spell.feature.split(',')[7]
            bunsho.append(spell)

        furigana += kamigofurigana
        furigana += nakahachifurigana
        furigana += simogofurigana

        #'上五と下五が同じの場合は作り直し'
        if kamigofurigana == simogofurigana:
            continue

        #'中七に上五が含まれている場合は作り直し'
        if nakahachifurigana.find(kamigofurigana) != -1:
            continue

        #'中七に下五が含まれている場合は作り直し'
        if nakahachifurigana.find(simogofurigana) != -1:
            continue

        #上五、中七、下五すべての末で切れている場合は作り直し
        Kamigokire = IsKire(kamigo[len(kamigo)  - 1])
        Nakahachikire = IsKire(nakashichi[len(nakashichi) - 1])
        Shimogokire = IsKire(shimogo[len(shimogo) - 1])
        if Kamigokire and Nakahachikire and Shimogokire:
            continue

        #動詞が2つ以上ある場合は作り直し
        doshicount = 0
        for spell in bunsho:
            splitData =  spell.feature.split(',')
            if splitData[0] in '動詞':
                doshicount+= 1

        if doshicount >= 2:
            continue

        create = True
        break

    if create == False:
        result.errormessage = '川柳が作成できませんでした。別の単語を入力してください。'
        return result

    result.senryu = senryu
    result.furigana = furigana
    return result

def IsKire(nodes):
    splitData =  nodes.feature.split(',')

    if splitData[5] in '基本形':
        return True

    elif splitData[0] in '名詞':
        return True

    else:
        return False

def mojiCount(furigana):
    mojicount = 0
    for moji in furigana:
        if is_youon(moji) == False:
            mojicount += 1

    return mojicount

def is_youon(moji):
    youon = ['ぁ',
     'ぃ',
     'ぅ',
     'ぇ',
     'ぉ',
     'ゃ',
     'ゅ',
     'ょ',
     'ァ',
     'ィ',
     'ゥ',
     'ェ',
     'ォ',
     'ャ',
     'ュ',
     'ョ']

    return moji in youon

def is_sokuon(moji):
    sokuon = ['っ','ッ']

    return moji in sokuon


