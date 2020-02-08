from django.conf import settings

from linebot import LineBotApi
from linebot.models import *
from module import env
import requests
from linebot02 import viewsget
from django.conf.urls import url
from module import env
import time ,datetime

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)


def write_in_TextMessage(events):
    events_userid = str(events[0].source).split('"')[7]
    # print(type(events_userid))
    events_instantly_time = events[0].timestamp
    events_content = events[0].message.text

    # print("User獨立ID : ", events_userid)
    # print("傳送得當下時間 : ", events_instantly_time)
    # print("傳送當下文字內容 : ", events_content)

    events_file_message = str(events_instantly_time)[0:-3] + '////' + str(events_content)

    # print("把資訊合成一塊 : ", events_file_message, '\n')
    # print("-------------------------------------------------------------")
    events_file_path = "E:/db104_2_project/Message_Log/%s.txt" % (events_userid)

    with open(events_file_path, 'w', encoding="utf-8") as f:
        f.write(events_file_message)


def unix_time(timeArray):
    timestamp = time.mktime(timeArray)
    return timestamp





def sendCarousel_f(event ,events):  #我的推薦_轉盤樣板

    # print(events)
    local_events_time = str(events[0].timestamp)[:-3]
    # print("local_events_time : " ,local_events_time)
    events_userid = str(events[0].source).split('"')[7]
    events_file_path = "E:/db104_2_project/Message_Log/%s.txt" % (events_userid)

    with open(events_file_path ,'r' ,encoding='utf-8') as f:
        events_file_list = f.read()
    events_file_content = events_file_list.split('////')

    print(events_file_content[1] ,len(events_file_content[1]) ,type(events_file_content[1]) )
    events_file_content_text = events_file_content[1]

    print("------------------------------    到這邊讀取順利 --------------下面做 如果二次進來這個函數 ，需要退出---------------------")

    if events_file_content_text == "#請用一句話描述化妝的情境或想要強化的部位#" :
        line_bot_api.reply_message(event.reply_token ,TextSendMessage(text='不要在重複按了，輸入文字拉，無言餒'))
        return 0
    else:
        write_in_TextMessage(events)
        ## timeArray = time.localtime(time.time())
        ## unix_t = str(unix_time(timeArray)).split('.')[0]
        time.sleep(1)
        while True:
            time.sleep(0.5)
            with open(events_file_path, 'r', encoding='utf-8') as f:
                events_file_list2 = f.read()
            events_file_content2 = events_file_list2.split('////')
            events_file_content_time2 = events_file_content2[0]
            events_file_content_content2 = events_file_content2[1]
            # print("time2 要大於才可以 :" ,events_file_content_time2)
            # print("local_events_time : " ,local_events_time)
            if int(events_file_content_time2) > int(local_events_time):
                ###### 到這邊是成功得 ， 接著要判斷 USER 有沒有接著點其他功能 ######
                error_text_list = ["#我的推薦#" ,"#模擬上妝#" ,"#教學文章#" ,"#熱門排行#" ,"#聯絡我們#" ,"#我的推薦選單#" ,"#清除我的推薦資料#" ,"#眼妝_c#" ,"#臉部_c#" ,"#唇部_c#"]
                # print("第二次的內容: " + events_file_content_content2 ,type(events_file_content_content2))

                if events_file_content_content2 in error_text_list :
                    #line_bot_api.reply_message(event.reply_token, TextSendMessage(text='你點到其他功能了，去吧，我不留你在這功能了'))
                    print("點到其他功能了!")
                    return 0
                else:
                    ####### 這邊跑 env 檔案了 ######
                    print("這邊要開始跑推薦商品程式了 : 等吧")
                    hightest = env.env_search(events_file_content_content2)
                    if hightest == 0 :
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='無相關資料'))
                        return 0
                    else:
                        print("輸出文章長度" ,len(hightest))
                        break
            else:
                print("沒輸入")
                pass

    # print("hightest[0]" ,hightest[0] ,len(hightest[0]))
    # print("hightest[0][0]" ,hightest[0][0] ,type(hightest[0][0]))
    # print("hightest[0][1]" ,hightest[0][1] ,type(hightest[0][1]))
    # print("hightest[0][2]" ,hightest[0][2] ,type(hightest[0][2]),'\n')
    #
    # print("hightest[1]" ,hightest[1] ,type(hightest[1]))
    # print("hightest[1][0]" ,hightest[1][0])
    # print("hightest[1][1]" ,hightest[1][1])
    # print("hightest[1][2]" ,hightest[1][2] ,'\n')
    #
    # print("hightest[2]" ,hightest[2] ,len(hightest[2]))
    # print("hightest[2][0]" ,hightest[2][0])
    # print("hightest[2][1]" ,hightest[2][1])
    # print("hightest[2][2]" ,hightest[2][2] ,'\n')
    #
    # print("%s" %(hightest[0][0]) ,type(hightest[0][0]))
    #
    # print("到這一步就顯示推薦畫面了")

    imagessss = 'https://www.chanel.com/apac/img/q_auto,fl_lossy,dpr_2,f_jpg/w_1920/prd-emea/sys-master/content/h7f/h62/8856160862238-974x974_MUCollection.jpg'
    if len(hightest) >= 3 :
        try:
            message = TemplateSendMessage(
                alt_text='轉盤樣板',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url='https://scontent-hkg3-2.cdninstagram.com/v/t51.2885-15/e35/75238440_2384260238551183_1164111356821469319_n.jpg?_nc_ht=scontent-hkg3-2.cdninstagram.com&_nc_cat=107&_nc_ohc=OevIC5ccqokAX8LYWxb&oh=f2db2b87dc213e5e84ee7ae06f4a8b68&oe=5EB26880',
                            title='%s (一)' %(hightest[0][0]),
                            text='%s' %(hightest[0][1]),
                            actions=[
                                URITemplateAction(
                                    label='立即了解',
                                    uri='%s' %(hightest[0][2])
                                )
                                # PostbackTemplateAction(
                                #     label='重新查找',
                                #     data='action=refind'
                                # ),
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url='https://cdn2.ettoday.net/images/3400/d3400815.jpg',
                            title='%s (二)'%(hightest[1][0]),
                            text='%s' %(hightest[1][1]),
                            actions=[
                                URITemplateAction(
                                    label='立即了解',
                                    uri='%s'%(hightest[1][2])
                                )
                                # URITemplateAction(
                                #     label='產品說明/了解更多',
                                #     uri='http://www.e-happy.com.tw'
                                # ),
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url='https://i.imgur.com/fZ70mQs.jpg',
                            title='%s (三)'%(hightest[2][0]),
                            text='%s' %(hightest[2][1]),
                            actions=[
                                URITemplateAction(
                                    label='立即了解',
                                    uri='%s' %(hightest[2][2])
                                )
                                # URITemplateAction(
                                #     label='產品說明/了解更多',
                                #     uri='http://www.e-happy.com.tw'
                                # )
                            ]
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='無相關資料！'))

    elif len(hightest) == 2 :
        try:
            message = TemplateSendMessage(
                alt_text='轉盤樣板',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url='https://i.imgur.com/4QfKuz1.png',
                            title='%s (一)'%(hightest[0][0]),
                            text='文章標題_1',
                            actions=[
                                URITemplateAction(
                                    label='立即了解',
                                    uri='%s' %(hightest[0][2])
                                )
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url='https://i.imgur.com/4QfKuz1.png',
                            title='%s (二)'%(hightest[1][0]),
                            text='文章標題_2',
                            actions=[
                                URITemplateAction(
                                    label='立即了解',
                                    uri='%s' %(hightest[1][2])
                                )
                            ]
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='無相關資料！'))
    else:
        try:
            message = TemplateSendMessage(
                alt_text='轉盤樣板',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url='https://i.imgur.com/4QfKuz1.png',
                            title='%s (一)'%(hightest[0][0]),
                            text='文章標題_1',
                            actions=[
                                URITemplateAction(
                                    label='立即了解',
                                    uri='%s' %(hightest[0][2])
                                )
                            ]
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='無相關資料！'))




########################################################################################################

#     write_in_TextMessage(events)
#     #判斷是誰用這個功能
#     events_userid = str(events[0].source).split('"')[7]
#     events_file_path = "E:/db104_2_project/Message_Log/%s.txt" % (events_userid)
#     #抓取系統當下時間，等等會去用當下時間去判店
#     timeArray = time.localtime(time.time())
#     unix_t = str(unix_time(timeArray)).split('.')[0]
#     while True:
#         with open(events_file_path ,'r' ,encoding='utf-8') as f:
#             events_file_list = f.read()
#         events_file_time = events_file_list.split(',')[0][:-3]
#         events_file_text = events_file_list.split(',')[1]
#         #print(events_file_text)
#         error_text_list = ["#我的推薦#" ,"#模擬上妝#" ,"#教學文章#" ,"#請輸入情境#" ,"#熱門排行#" ,"#聯絡我們#"]
#         if int(events_file_time) > int(unix_t):
#             print("你成功進入拉!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#             if events_file_text in error_text_list:
#                 print("你點到其他功能了，強制跳出迴圈結束這回合，掰掰")
#                 break
#             else:
#                 print("很可以 沒有重複，繼續執行程式瞜")
#                 try:
#                     message = TemplateSendMessage(
#                         alt_text='轉盤樣板',
#                         template=CarouselTemplate(
#                             columns=[
#                                 CarouselColumn(
#                                     thumbnail_image_url='https://i.imgur.com/4QfKuz1.png',
#                                     title='推薦名單_1',
#                                     text='文章標題_1',
#                                     actions=[
#                                         URITemplateAction(
#                                             label='立即了解',
#                                             uri='http://www.e-happy.com.tw'
#                                         ),
#                                         PostbackTemplateAction(
#                                             label='重新查找',
#                                             data='action=refind'
#                                         ),
#                                     ]
#                                 ),
#                                 CarouselColumn(
#                                     thumbnail_image_url='https://i.imgur.com/4QfKuz1.png',
#                                     title='推薦名單_2',
#                                     text='文章標題_2',
#                                     actions=[
#                                         URITemplateAction(
#                                             label='立即了解',
#                                             uri='http://www.e-happy.com.tw'
#                                         ),
#                                         URITemplateAction(
#                                             label='產品說明/了解更多',
#                                             uri='http://www.e-happy.com.tw'
#                                         ),
#                                     ]
#                                 ),
#                                 CarouselColumn(
#                                     thumbnail_image_url='https://i.imgur.com/4QfKuz1.png',
#                                     title='推薦名單_3',
#                                     text='文章標題_3',
#                                     actions=[
#                                         URITemplateAction(
#                                             label='立即了解',
#                                             uri='http://www.e-happy.com.tw'
#                                         ),
#                                         URITemplateAction(
#                                             label='產品說明/了解更多',
#                                             uri='http://www.e-happy.com.tw'
#                                         ),
#                                     ]
#                                 )
#                             ]
#                         )
#                     )
#
#                     line_bot_api.reply_message(event.reply_token, message)
#                 except:
#                     line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

#                 print("最內圈 if 跳出")
#                 break
#         else:
#             #print("輸入時間晚了:請輸入文字")
#             continue



    #env.env_search()
    # b = input("二度卡住一下")


########################################################################################################

# def reFind(event,backdata):
#     try:
#         message = TemplateSendMessage(
#             alt_text='轉盤樣板',
#             template=CarouselTemplate(
#                 columns=[
#                     CarouselColumn(
#                         thumbnail_image_url='https://i.imgur.com/4QfKuz1.png',
#                         title='推薦名單_1',
#                         text='文章標題_1',
#                         actions=[
#                             URITemplateAction(
#                                 label='立即了解',
#                                 uri='http://www.e-happy.com.tw'
#                             ),
#                             PostbackTemplateAction(
#                                 label='重新查找',
#                                 data='action=refind'
#                             ),
#                         ]
#                     ),
#                     CarouselColumn(
#                         thumbnail_image_url='https://i.imgur.com/4QfKuz1.png',
#                         title='推薦名單_2',
#                         text='文章標題_2',
#                         actions=[
#                             URITemplateAction(
#                                 label='立即了解',
#                                 uri='http://www.e-happy.com.tw'
#                             ),
#                             URITemplateAction(
#                                 label='產品說明/了解更多',
#                                 uri='http://www.e-happy.com.tw'
#                             ),
#                         ]
#                     ),
#                     CarouselColumn(
#                         thumbnail_image_url='https://i.imgur.com/4QfKuz1.png',
#                         title='推薦名單_3',
#                         text='文章標題_3',
#                         actions=[
#                             URITemplateAction(
#                                 label='立即了解',
#                                 uri='http://www.e-happy.com.tw'
#                             ),
#                             URITemplateAction(
#                                 label='產品說明/了解更多',
#                                 uri='http://www.e-happy.com.tw'
#                             ),
#                         ]
#                     )
#                 ]
#             )
#         )
#
#         line_bot_api.reply_message(event.reply_token, message)
#     except:
#         line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

###########################################################################################################
    # try:
    #     message = TemplateSendMessage(
    #         alt_text='轉盤樣板',
    #         template=CarouselTemplate(
    #             columns=[
    #                 CarouselColumn(
    #                     thumbnail_image_url='https://i.imgur.com/4QfKuz1.png',
    #                     title='推薦名單_1',
    #                     text='文章標題_1',
    #                     actions=[
    #                         URITemplateAction(
    #                             label='立即了解',
    #                             uri='http://www.e-happy.com.tw'
    #                         ),
    #                         PostbackTemplateAction(
    #                             label='重新查找',
    #                             data='action=refind'
    #                         ),
    #                     ]
    #                 ),
    #                 CarouselColumn(
    #                     thumbnail_image_url='https://i.imgur.com/4QfKuz1.png',
    #                     title='推薦名單_2',
    #                     text='文章標題_2',
    #                     actions=[
    #                         URITemplateAction(
    #                             label='立即了解',
    #                             uri='http://www.e-happy.com.tw'
    #                         ),
    #                         URITemplateAction(
    #                             label='產品說明/了解更多',
    #                             uri='http://www.e-happy.com.tw'
    #                         ),
    #                     ]
    #                 ),
    #                 CarouselColumn(
    #                     thumbnail_image_url='https://i.imgur.com/4QfKuz1.png',
    #                     title='推薦名單_3',
    #                     text='文章標題_3',
    #                     actions=[
    #                         URITemplateAction(
    #                             label='立即了解',
    #                             uri='http://www.e-happy.com.tw'
    #                         ),
    #                         URITemplateAction(
    #                             label='產品說明/了解更多',
    #                             uri='http://www.e-happy.com.tw'
    #                         ),
    #                     ]
    #                 )
    #             ]
    #         )
    #     )
########################################################################################################



