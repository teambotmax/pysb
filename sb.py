# -*- coding: utf-8 -*-
from LineAPI.linepy import *
from LineAPI.akad.ttypes import Message
from LineAPI.akad.ttypes import ContentType as Type
from time import sleep
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, six, ast, pytz, urllib, urllib3, urllib.parse, traceback, atexit
from helper import helper
try:
    with open('token.txt','r') as lg:
        tkn = lg.read()
        ayam = LINE(tkn)
except:
    ayam = LINE()
    with open('token.txt','w') as lg:
        lg.write(ayam.authToken)
#===================================open codec===========================================#

plates = codecs.open("template.json","r","utf-8")
plate = json.load(plates)

#===================================Batas===============================================#
        
#=======[ BOTS START ]==========
ayamMid = ayam.profile.mid
ayamProfile = ayam.getProfile()
ayamSettings = ayam.getSettings()
ayamPoll = OEPoll(ayam)
botStart = time.time()
msg_dict = {}
#=============[ DATA STREAM ]=====================================================================================
with open('settings.json','r') as stg:settings = json.load(stg)
yam={"changepicture":False}
def setback():                                                                                                   
    with open('settings.json','w') as sb:json.dump(settings, sb, sort_keys=True, indent=4, ensure_ascii=False)
try:                                                                                                             
    with open("Log_data.json","r",encoding="utf_8_sig") as f:                                                    
        msg_dict = json.loads(f.read())                                                                          
except:                                                                                                          
    print("Couldn't Read Log Data")                                                                              
#=================================================================================================================
profile = ayam.getContact(ayamMid)
settings['myProfile']['displayName'] = profile.displayName
settings['myProfile']['pictureStatus'] = profile.pictureStatus
settings['myProfile']['statusMessage'] = profile.statusMessage
coverId = ayam.getProfileDetail()['result']['objectId']
settings['myProfile']['coverId'] = str(coverId)
setback()
def restartBot():
    print ("[ INFO ] BOT RESTART")
    python = sys.executable
    os.execl(python, python, *sys.argv)
def logError(text):
    ayam.log("[ ERROR ] {}".format(str(text)))
    tz = pytz.timezone("Asia/Jakarta")
    timeNow = datetime.now(tz=tz)
    timeHours = datetime.strftime(timeNow,"(%H:%M)")
    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    inihari = datetime.now(tz=tz)
    hr = inihari.strftime('%A')
    bln = inihari.strftime('%m')
    for i in range(len(day)):
        if hr == day[i]: hasil = hari[i]
    for k in range(0, len(bulan)):
        if bln == str(k): bln = bulan[k-1]
    time = "{}, {} - {} - {} | {}".format(str(hasil), str(inihari.strftime('%d')), str(bln), str(inihari.strftime('%Y')), str(inihari.strftime('%H:%M:%S')))
    with open("logError.txt","a") as error:
        error.write("\n[ {} ] {}".format(str(time), text))
def cTime_to_datetime(unixtime):
    return datetime.fromtimestamp(int(str(unixtime)[:len(str(unixtime))-3]))
def dt_to_str(dt):
    return dt.strftime('%H:%M:%S')
def delete_log():
    ndt = datetime.now()
    for data in msg_dict:
        if (datetime.utcnow() - cTime_to_datetime(msg_dict[data]["createdTime"])) > timedelta(1):
            if "path" in msg_dict[data]:
                ayam.deleteFile(msg_dict[data]["path"])
            del msg_dict[data]
def command(text):
    cmd = text.lower()
    return cmd
def ayamBot(op):
    try:
        if op.type == 0:return
        if op.type == 5 and settings["autoadd"]==True:
            print ("[ OP 5 ] Ada ADD !!")
            ayam.sendMentionV2(op.param1, "{}".format(settings["addmsg"]), [op.param1])
#=============================================================================
        if op.type == 13 and settings["autojoin"]==True:ayam.acceptGroupInvitation(op.param1)
        if op.type == 17 and settings["sapa"]==True:
            ayam.acceptGroupInvitation(op.param1)
            pesannya = {
                "type": "template",
                "altText": "{} Mengirim Sticker".format(str(ayam.getContact(ayamMid).displayName)),
                "baseSize": {
                    "height": 1040,
                    "width": 1040
                },
                "template": {
                    "type": "image_carousel",
                    "columns": [{
                        "imageUrl": "https://stickershop.line-scdn.net/stickershop/v1/sticker/177796075/IOS/sticker.png",
                        "action": {
                            "type": "uri",
                            "uri": "line://shop/detail/7384106",
                            "area": {
                                "x": 520,
                                "y": 0,
                                "width": 520,
                                "height": 1040
                            }
                        }
                    }]
                }
            }
            ayam.sendFlex(op.param1,pesannya)
            print ("Kam Showed")
        if op.type == 15 and settings["sapa"]==True or op.type == 19 and settings["sapa"]==True:
            ayam.acceptGroupInvitation(op.param1)
            pesannya = {
                "type": "template",
                "altText": "{} Mengirim Sticker".format(str(ayam.getContact(ayamMid).displayName)),
                "baseSize": {
                    "height": 1040,
                    "width": 1040
                },
                "template": {
                    "type": "image_carousel",
                    "columns": [{
                        "imageUrl": "https://stickershop.line-scdn.net/stickershop/v1/sticker/177796076/IOS/sticker.png",
                        "action": {
                            "type": "uri",
                            "uri": "line://shop/detail/7384106",
                            "area": {
                                "x": 520,
                                "y": 0,
                                "width": 520,
                                "height": 1040
                            }
                        }
                    }]
                }
            }
            ayam.sendFlex(op.param1,pesannya)
            print ("Bai Showed")
#===========================================================================================
        if op.type == 25:
            try:
                msg = op.message
                text = msg.text
                msg_id = msg.id
                receiver = msg.to
                sender = msg._from
                if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
                    if msg.toType == 0:
                        if sender != ayam.profile.mid:to = sender
                        else:to = receiver
                    elif msg.toType == 1:to = receiver
                    elif msg.toType == 2:to = receiver
                    if msg.contentType == 0:
                        if text is None:return
                        else:
                            cmd = command(text)#ThisMain
                            if cmd=='help':ayam.sendFlex(receiver, plate["mehelp"])
                            #[SELF MENU]
                            if cmd=='me':ayam.sendContact(to,sender);ayam.sendMessageMusic(to, title=ayam.getContact(sender).displayName, subText=str(ayam.getContact(sender).statusMessage), url='line.me/ti/p/~dev.line.me', iconurl="http://dl.profile.line-cdn.net/{}".format(ayam.getContact(sender).pictureStatus), contentMetadata={})
                            #[GROUPHELP]
                            if cmd=='mentionall':
                                group = ayam.getGroup(to)
                                midMembers = [contact.mid for contact in group.members]
                                midSelect = len(midMembers)//20
                                for mentionMembers in range(midSelect+1):
                                    no = 0
                                    ret_ = "[ Mention Members ]"
                                    dataMid = []
                                    for dataMention in group.members[mentionMembers*20 : (mentionMembers+1)*20]:
                                        dataMid.append(dataMention.mid)
                                        no += 1
                                        ret_ += "\n {}. @!".format(str(no))
                                    ayam.sendMentionV2(to, ret_, dataMid)
                                    print ("Respon MentionAll")
                            #[SETTINGS]
                            if cmd=='autolike on':settings["autolike"]=True;setback();ayam.sendMessage(to,"Autolike turned on!")
                            if cmd=='autolike off':settings["autolike"]=False;setback();ayam.sendMessage(to,"Autolike turned off!")
                            if cmd=='autoadd on':settings["autoadd"]=True;setback();ayam.sendMessage(to,'Autoadd Turned ON')
                            if cmd=='autoadd off':settings["autoadd"]=False;setback();ayam.sendMessage(to,'Autoadd Turned OFF')
                            if cmd=='autojoin on':settings["autojoin"] = True;setback();ayam.sendMessage(to,"Auto join turned on")
                            if cmd=='autojoin off':settings["autojoin"] = False;setback();ayam.sendMessage(to,"Auto join turned off")
                            if cmd=='sapa on':settings["sapa"] = True;setback();ayam.sendMessage(to,"Sapa turned on")
                            if cmd=='sapa off':settings["sapa"] = False;setback();ayam.sendMessage(to,"Sapa turned off")
                            if cmd=='respon off':settings["responMentionnya"]=False;ayam.sendFlex(to, plate["responMentionOff"])
                            if cmd=='respon on':settings["responMentionnya"]=True;ayam.sendFlex(to, plate["responMentionOn"])
                            if cmd=='restart':ayam.sendFlex(to, plate["restartnya"]);restartBot()
                            if cmd=='shutdown':ayam.sendFlex(to, plate["shutdownnya"]);sys.exit('bye')
                            if cmd == "changepicture":yam["changepicture"] = True;ayam.sendReplyMessage(msg_id,to,"Send a pict !")
#================================================================================================================================================================
                    elif msg.contentType == 1 or msg.contentType == 3: #foto / video
                        if yam["changepicture"] == True:
                            path = ayam.downloadObjectMsg(msg_id)
                            yam["changepicture"] = False
                            ayam.updateProfilePicture(path)
                            ayam.sendReplyMessage(msg_id,to, "Updated")
            except Exception as error:
                logError(error)
                traceback.print_tb(error.__traceback__)
        if op.type == 26:
            try:
                #print ("[ 26 ] RECIEVE MESSAGE")
                msg = op.message
                text = msg.text
                msg_id = msg.id
                receiver = msg.to
                sender = msg._from
                creatormid = "u95f5fcc0013c63589bd45685aeaeda24"
                if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
                    #if msg.contentType == 6:
                        #if msg.toType == 0:
                            #ayam.sendChatRemoved(0,sender,msg_id)
                            #ayam.removeMessage(msg_id)
                            
                    if msg.contentType == 16:
                        if settings["autolike"]==True:
                            url_post = msg.contentMetadata['postEndUrl']
                            pliter = url_post.replace('line://home/post?userMid=','')
                            pliter = pliter.split('&postId=')
                            ayam.likePost(mid=pliter[0],postId=pliter[1])
                            ayam.createComment(mid=pliter[0],postId=pliter[1],text=settings["comment"])
                            ayam.sendFlex(receiver, plate["likednya"])
                            print ("Post Liked")
                            
                    if msg.contentType == 0 and sender not in ayamMid and msg.toType == 2:
                        if "MENTION" in msg.contentMetadata.keys() != None and settings["responMentionnya"]==True:
                            contact = ayam.getContact(msg._from)
                            cName = contact.displayName
                            text = msg.text
                            balas = ["Apaan sih "+cName+" ?", "Berisik "+cName+" !!", "Ngetag mulu "+cName+" -_-"]
                            ret_ = "" + random.choice(balas)
                            mention = ast.literal_eval(msg.contentMetadata["MENTION"])
                            mentionees = mention["MENTIONEES"]
                            pesannya = {
                                    "type": "flex",
                                    "altText": "{} Mengirim Tanggapan Mention".format(str(ayam.getContact(ayamMid).displayName)),
                                    "contents": {
                                        "type": "bubble",
                                        "body": {
                                            "type": "box",
                                            "layout": "horizontal",
                                            "action": {
                                                "type": "uri",
                                                "uri": "line://ti/p/%40jix5504f"
                                            },
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "{}".format(str(text)),
                                                    "color": "#aaaaaa"
                                                }
                                            ]
                                        },
                                        "footer": {
                                            "type": "box",
                                            "layout": "horizontal",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "{}".format(str(ret_)),
                                                    "color": "#000000",
                                                    "align": "center",
                                                    "weight":"bold",
                                                    "wrap": True
                                                }
                                            ]
                                        },
                                        "styles": {
                                            "body": {
                                                "backgroundColor": "#ffda6b"
                                            },
                                            "footer": {
                                                "backgroundColor": "#f9bb00"
                                            }
                                        }
                                    }
                                }
                            for mention in mentionees:
                                if mention['M'] in ayamMid:
                                    ayam.sendFlex(msg.to,pesannya)
                                    ayam.sendMessage(msg._from,"Ada Perlu Apa Nge-Tag di Grup "+cName+" ?")
                                    print ("Respon Mention")
                                    break
                                
                        cmd = command(text)
                        if cmd=='mymid':
                            memyid = ayam.getContact(sender).mid
                            pesannya = {
                                    "type": "flex",
                                    "altText": "{} Menampilkan MID Pengirim".format(str(ayam.getContact(ayamMid).displayName)),
                                    "contents": {
                                        "type": "bubble",
                                        "body": {
                                            "type": "box",
                                            "layout": "horizontal",
                                            "action": {
                                                "type": "uri",
                                                "uri": "line://ti/p/%40jix5504f"
                                            },
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "MID Kamu : {}".format(str(memyid)),
                                                    "color": "#000000",
                                                    "align": "center",
                                                    "weight":"bold",
                                                    "wrap": True
                                                }
                                            ]
                                        },
                                        "styles": {
                                            "body": {
                                                "backgroundColor": "#ffda6b"
                                            }
                                        }
                                    }
                                }
                            ayam.sendFlex(msg.to,pesannya)
                            print ("Sender MID Showed")
                        
                        if cmd=='creator':
                            kontaknyo = ayam.getContact(ayamMid)
                            creatornye = {
                                "type": "flex",
                                "altText": "Creator",
                                "contents": {
                                    "type": "bubble",
                                    "header": {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "{}".format(str(kontaknyo.displayName)),
                                                "color": "#000000",
                                                "align":"center",
                                                "weight": "bold",
                                                "size": "xl"
                                            }
                                        ]
                                    },
                                    "hero": {
                                        "type": "image",
                                        "url": "https://os.line.naver.jp/os/p/{}".format(ayamMid),
                                        "size": "full",
                                        "aspectRatio": "40:31",
                                        "aspectMode": "cover",
                                        "action": {
                                            "type": "uri",
                                            "uri": "https://os.line.naver.jp/os/p/{}".format(ayamMid)
                                        }
                                    },
                                    "body": {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "{}".format(str(kontaknyo.statusMessage)),
                                                "color": "#000000",
                                                "align":"center",
                                                "wrap": True
                                            }
                                        ]
                                    },
                                    "footer": {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {
                                                "type": "spacer",
                                                "size": "sm"
                                            },
                                            {
                                                "type": "button",
                                                "style": "primary",
                                                "color": "#604800",
                                                "action": {
                                                    "type": "uri",
                                                    "label": "CONTACT",
                                                    "uri": "line://ti/p/~dev.line.me"
                                                }
                                            }
                                        ]
                                    },
                                    "styles": {
                                        "header": {
                                            "backgroundColor": "#f9bb00"
                                        },
                                        "hero": {
                                            "backgroundColor": "#ffda6b"
                                        },
                                        "body": {
                                            "backgroundColor": "#ffda6b"
                                        },
                                        "footer": {
                                            "backgroundColor": "#f9bb00"
                                        }
                                    }
                                }
                            }
                            ayam.sendFlex(msg.to,creatornye)
                            print ("Creator Showed")
                            
                        if cmd in ['cium','kiss',':*','mwah','muah']:  
                            pesannya = {
                                "type": "template",
                                "altText": "{} Mengirim Sticker".format(str(ayam.getContact(ayamMid).displayName)),
                                "baseSize": {
                                    "height": 1040,
                                    "width": 1040
                                },
                                "template": {
                                "type": "image_carousel",
                                "columns": [{
                                    "imageUrl": "https://stickershop.line-scdn.net/stickershop/v1/sticker/177796077/IOS/sticker.png",
                                    "action": {
                                        "type": "uri",
                                        "uri": "line://shop/detail/7384106",
                                        "area": {
                                            "x": 520,
                                            "y": 0,
                                            "width": 520,
                                            "height": 1040
                                        }
                                    }
                                }]
                                }
                            }
                            ayam.sendFlex(msg.to,pesannya)
                            print ("Kiss Sticker Showed")
                            
                        if cmd in ['hi','halo','hai','hy','hay','haii','helo','hello','hey']:  
                            pesannya = {
                                "type": "template",
                                "altText": "{} Mengirim Sticker".format(str(ayam.getContact(ayamMid).displayName)),
                                "baseSize": {
                                    "height": 1040,
                                    "width": 1040
                                },
                                "template": {
                                "type": "image_carousel",
                                "columns": [{
                                    "imageUrl": "https://stickershop.line-scdn.net/stickershop/v1/sticker/52002768/IOS/sticker_animation@2x.png",
                                    "action": {
                                        "type": "uri",
                                        "uri": "line://shop/detail/7384106",
                                        "area": {
                                            "x": 520,
                                            "y": 0,
                                            "width": 520,
                                            "height": 1040
                                        }
                                    }
                                }]
                                }
                            }
                            ayam.sendFlex(msg.to,pesannya)
                            print ("Hay Sticker Showed")    
                            
                        if cmd=='about':
                            ayam.sendFlex(msg.to,plate["aboutnya"])
                            print ("About Showed")
                        
                        if cmd=='help':
                            ayam.sendFlex(msg.to,plate["helpnya"])  
                            print ("Public Help Showed")
        				              
            except Exception as error:
                logError(error)
                traceback.print_tb(error.__traceback__)
    except Exception as error:
        logError(error)
        traceback.print_tb(error.__traceback__)
while True:
    try:
        delete_log()
        ops = ayamPoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                ayamBot(op)
                ayamPoll.setRevision(op.revision)
    except Exception as error:
        logError(error)
def atend():
    print("Saving")
    with open("Log_data.json","w",encoding='utf8') as f:
        json.dump(msg_dict, f, ensure_ascii=False, indent=4,separators=(',', ': '))
    print("BYE")
atexit.register(atend)
