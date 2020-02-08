from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from confluent_kafka import Producer
from linebot import LineBotApi, WebhookParser,WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, ImageMessage ,TextMessage, PostbackEvent,TextSendMessage ,ImageSendMessage
import main_gan
import argparse
from Dlib_faces_cut import face_cut
from urllib.parse import parse_qsl
import os
import sys
import random
import time
import requests
from hdfs import *
from linebot02 import viewsget

#新增的
# 跟店長同步

from module import my_recommend ,onekey_makeup ,learn_paper  ,func ,situation_helper
from django.shortcuts import render ,redirect
import MySQLdb

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)



def write_in_TextMessage(events):
    if events[0].type == "follow" or events[0].type == "unfollow":
        print("跑到這裡來")
        return 0
    else :
        pass
    events_userid = str(events[0].source).split('"')[7]
    print(type(events_userid))
    events_instantly_time = events[0].timestamp
    if events[0].message.type == "text":
        events_content = events[0].message.text
    else:
        events_content = "是照片"
    print("User獨立ID : ", events_userid)
    print("傳送得當下時間 : ", events_instantly_time)
    print("傳送當下文字內容 : ", events_content)

    events_file_message = str(events_instantly_time)[0:-3] + '////' + str(events_content)

    print("把資訊合成一塊 : ", events_file_message, '\n')
    print("-------------------------------------------------------------")
    events_file_path = "E:/db104_2_project/Message_Log/%s.txt" % (events_userid)

    with open(events_file_path, 'w', encoding="utf-8") as f:
        f.write(events_file_message)

def error_cb(err):
    print('Error: %s' % err)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            print("###################### events ################## : " ,event )
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    mtext = event.message.text
                    if mtext == '#我的推薦#':
                        write_in_TextMessage(events)
                        # 先抓取 UserId 號碼，看看資料庫有沒有存在
                        # 如果 count = 1 代表存在
                        user_Data = my_recommend.search_db(event)
                        if user_Data[6] == 1 and user_Data[1] != None :
                            my_recommend.sendCarousel(event ,user_Data)  #轉盤樣板
                        elif user_Data[6] == 0 or user_Data[1] == None :
                            my_recommend.fill_in_the_form(event)
                        else:
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='系統維護，請稍等!'))
                        return HttpResponse()

                    elif mtext == "#清除我的推薦資料#":
                        write_in_TextMessage(events)
                        my_recommend.delete_commend_form(event)
                        return HttpResponse()

                    elif mtext == "#我的推薦選單#" :
                        write_in_TextMessage(events)
                        my_recommend.send_commend_Quickreply(event)
                        return HttpResponse()


                    elif mtext == '#模擬上妝#':
                        write_in_TextMessage(events)
                        onekey_makeup.openCameraRoll(event) #多元按鈕樣板
                        return HttpResponse()


                    elif mtext == '#教學文章#':
                        write_in_TextMessage(events)
                        learn_paper.sendQuickreply(event) #快速按鈕
                        return HttpResponse()


                    elif mtext == '#請用一句話描述化妝的情境或想要強化的部位#':
                        ## 還沒寫 write 進去函式在寫
                        situation_helper.sendCarousel_f(event ,events)
                        return HttpResponse()


                    elif mtext == '#熱門排行#':
                        write_in_TextMessage(events)
                        func.Top_Ranking_Position(event)
                        return HttpResponse()

                    elif mtext == '#眉睫#' or mtext == '#眼影#' or mtext == '#眼線#' or mtext == '#面頰#' or mtext == '#唇彩#' :
                        write_in_TextMessage(events)
                        func.Top_Ranking_List(event)
                        return HttpResponse()

                    elif mtext == '#人氣最高#' or mtext == '#推薦指數最高#' :
                        write_in_TextMessage(events)
                        # 查詢 userid 有沒有先點選過 部位
                        user_Data = func.Top_Ranking_search_user(event)
                        print("sear_user的user_Data : " ,user_Data)
                        # 查詢 function 在這邊寫
                        if user_Data[2] == 1 :
                            func.Top_Ranking_fetch(event ,user_Data)
                        elif user_Data[2] == 0 :
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='您沒點選部位，請重新點選功能。'))
                        else:
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='有錯誤，請重新點選功能'))
                        return HttpResponse()

                    elif mtext == '#聯絡我們#': #位置提供
                        write_in_TextMessage(events)
                        func.sendPosition(event)
                        return HttpResponse()

                    elif mtext == '#眼妝_c#' or mtext == '#臉部_c#' or mtext == '#唇部_c#':
                        write_in_TextMessage(events)
                        learn_paper.sendLearn_paper(event , mtext)
                        return HttpResponse()


                elif isinstance(event.message,ImageMessage):
                    #PostbackEvent
                    # line_bot_api.reply_message(event.reply_token,TextSendMessage(text='spark沒開，先不給你照片，哈哈'))
                    # return HttpResponse()
                    message_content = line_bot_api.get_message_content(event.message.id)
                    print(message_content)
                    # with open('C:/Users/Big data/Desktop/db104_2_project/templates/' + event.message.id + '.jpg','wb')as fd:

                    user_id = event.message.id
                    user_id = str(user_id) + str(random.randrange(10 ,99))
                    print(user_id)
                    with open('E:/db104_2_project/static/{}.jpg' .format(user_id),'wb')as fd:
                        for chunk in message_content.iter_content():
                            fd.write(chunk)

                    temp_pic = 'E:/db104_2_project/static/{}.jpg'.format(user_id)
                    # parser1 = argparse.ArgumentParser()
                    # parser1.add_argument('--static', type=str,default=os.path.join(path=temp_pic_1),help='path to the no_makeup image')
                    # args = parser1.parse_args()

                    content = face_cut.detect_face_landmarks(temp_pic)
                    #main_gan.make_upup(temp_pic_1)
                    print(type(content) ,content)

                    # 步驟1. 設定要連線到Kafka集群的相關設定
                    props = {
                        # Kafka集群在那裡?
                        'bootstrap.servers': '10.120.38.7:9092',  # <-- 置換成要連接的Kafka集群
                        'error_cb': error_cb  # 設定接收error訊息的callback函數
                    }

                    # 步驟2. 產生一個Kafka的Producer的實例
                    producer = Producer(props)
                    # 步驟3. 指定想要發佈訊息的topic名稱
                    topicName = 'test'
                    msgCounter = 0
                    try:
                        # produce(topic, [value], [key], [partition], [on_delivery], [timestamp], [headers])
                        producer.produce(topicName, content )

                        msgCounter += 4
                        print('Send ' + str(msgCounter) + ' messages to Kafka')
                    except BufferError as e:
                        # 錯誤處理
                        sys.stderr.write('%% Local producer queue is full ({} messages awaiting delivery): try again\n'
                                         .format(len(producer)))
                    except Exception as e:
                        print(e)
                    # 步驟5. 確認所在Buffer的訊息都己經送出去給Kafka了
                    producer.flush()


                    onekey_makeup.sendMulti_send_image(event ,content)

                    
                    # time.sleep(8)
                    # send_res = send_image()
                    # print(send_res)
                else:
                    print("到這呢???")
                    return HttpResponse()
            elif events[0].type == "follow":
                my_recommend.follow_in_the_form(event)
                return HttpResponse()
            print("到文字func後會，跑到這，如果拿掉下面那行，會跑到 儲存輸入文字")
            # return HttpResponse()

        #viewsget.get_resquest(events)
        print("儲存輸入文字")
        # if events[0].message.type == "text":
        #     write_in_TextMessage(events)
        # else:
        #     print(events[0].message.type)
        #     print("不能存")
        #     pass
        write_in_TextMessage(events)
        return HttpResponse()

    else:
        print("不是POST")
        return HttpResponseBadRequest()


def set_cookie(request,key=None,value=None):   #定義set_cookie函式，key為名稱，value為內容
    # response = HttpResponse('Cookie 儲存完畢')
    print(key ,value)
    response = HttpResponse('Cookie 儲存完畢')
    response.set_cookie(key,value)
    # request.session[key] = value
    Poseidon = value
    # print(request.session["key"])
    # print(request.session)
    # cstf = request.COOKIES["csrftoken"]
    # print(request.COOKIES["csrftoken"])


    db = MySQLdb.connect(host="localhost", user="min", passwd="1234", db="db104_testdb", port=3306, charset="utf8")
    corsor = db.cursor()  # 建立游標
    db.autocommit(True)  # 自動確認
    sql_str = "select * from footprint where UserId = \"{}\" ; " .format(Poseidon)
    corsor.execute(sql_str)
    data1 = corsor.fetchone()
    print(data1)


    if data1 == None:
        # 先儲存 UserId 、csrttoken 欄位 以便等等回傳資料辨識
        insert_Poseidon = "insert into footprint (UserId) values(\"{}\") ;".format(Poseidon)
        corsor.execute(insert_Poseidon)
        data2 = corsor.fetchone()
        db.close()
        print(data2)
    # elif data1[0] == Poseidon :
    #     update_Posedon = "update footprint set Poseidon = \"{}\" ;" .format(Poseidon)
    #     db.close()

    return render(request, 'get_cookie.html', locals())


def get_cookie(request,key=None):
    # csrf_token = str(request.COOKIES["csrftoken"])
    # print(csrf_token ,request.POST)
    print("HAHAHAH : " ,request.META["HTTP_REFERER"])
    referer = str(request.META["HTTP_REFERER"]).split("/")[5]
    print("I'm referer : " ,referer )
    likes = request.GET["like"] ; unlike = request.GET["unlike"] ; money = request.GET["money"] ; channel = request.GET["channel"] ; func = request.GET["func"]
    print(likes ,unlike ,money ,channel ,func)

    db = MySQLdb.connect(host="localhost", user="min", passwd="1234", db="db104_testdb", port=3306, charset="utf8")
    corsor = db.cursor()  # 建立游標
    db.autocommit(True)  # 自動確認

    # 儲存其他欄位
    update_foorprint = "update footprint set likes = \"{}\" ,unlike = \"{}\" ,price_range = \"{}\" ,channels = \"{}\" ,functions = \"{}\"  where UserId = \"{}\" ;" \
        .format(likes ,unlike ,money ,channel ,func ,referer)
    corsor.execute(update_foorprint)
    db.close()
    return HttpResponse("輸入成功!!")

####################################################################


# def form_db(request):
#     # request.session['luckey_number'] = 8
#     # print("0000 : " ,request.session)
#     # print(request.session['lucky_number'])
#     # if 'lucky_number' in request.session:
#     #     lucky_number = request.session['lucky_number']  # 讀取lucky_number
#     #     response = HttpResponse('Your lucky_number is ' + str(lucky_number))
#     # return response
#
#     Poseidon = request.GET["Poseidon"]
#     csrf_token = str(request.COOKIES).split("'")[3]
#     # csrf_token = str(request.COOKIES["csrftoken"])
#     # csrf_token = request.META['HTTP_X_CSRFTOKEN']
#     # print(Poseidon ,'|' ,csrf_token)
#     print(request.POST)
#     # print("=========================================")
#     print(request.META)
#     # print("=========================================")
#     #
#     db = MySQLdb.connect(host="localhost", user="min", passwd="1234", db="db104_testdb", port=3306, charset="utf8")
#     corsor = db.cursor()  # 建立游標
#     db.autocommit(True)  # 自動確認
#     sql_str = "select * from footprint where UserId = \"{}\" ; " .format(Poseidon)
#     corsor.execute(sql_str)
#     data1 = corsor.fetchone()
#     print(data1)
#     if data1 == None:
#         # 先儲存 UserId 、csrttoken 欄位 以便等等回傳資料辨識
#         insert_Poseidon = "insert into footprint (UserId ,csrftoken) values(\"{}\" ,\"{}\") ;".format(Poseidon, csrf_token)
#         corsor.execute(insert_Poseidon)
#         data2 = corsor.fetchone()
#         db.close()
#         print(data2)
#     elif data1[0] == Poseidon :
#         update_Posedon = "update footprint set csrftoken = \"{}\" ;" .format(csrf_token)
#         db.close()
#     return render(request, "get_form.html" ,locals())
#
# def post(request):
#     csrf_token = str(request.COOKIES["csrftoken"])
#     print(csrf_token ,request.POST)
#     likes = request.POST["like"] ; unlike = request.POST["unlike"] ; money = request.POST["money"] ; channel = request.POST["channel"] ; func = request.POST["func"]
#     print(likes ,unlike ,money ,channel ,func)
#
#     db = MySQLdb.connect(host="localhost", user="min", passwd="1234", db="db104_testdb", port=3306, charset="utf8")
#     corsor = db.cursor()  # 建立游標
#     db.autocommit(True)  # 自動確認
#
#     # 儲存其他欄位
#     update_foorprint = "update footprint set likes = \"{}\" ,unlike = \"{}\" ,price_range = \"{}\" ,channels = \"{}\" ,functions = \"{}\"  where csrftoken = \"{}\" ;" \
#         .format(likes ,unlike ,money ,channel ,func ,csrf_token)
#     corsor.execute(update_foorprint)
#     db.close()
#     return HttpResponse("輸入成功!!")
#


####################################################################



#
#
# if isinstance(event ,PostbackEvent):
#     ## 觸發事件，不回傳訊息
#     backdata = dict(parse_qsl(event.postback.data))
#     ## 取得Postback資料
#     if backdata.get("action") == 'refind':
#         situation_helper.reFind(event.backdata)