from django.conf import settings

from linebot import LineBotApi
from linebot.models import *

import MySQLdb
import pandas as pd

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)


def check_end(product_Data ,product_name ,images ,images_html2):
    for i in product_Data:
        if len(i[5]) >= 30 :
            temp = str(i[5])[0:30]+"..."
            product_name.append(temp)
        else :
            product_name.append(i[5])

        if i[15] == "無商品圖片":
            images.append(images_html2)
        else:
            images.append(i[15])


def check_money(user_money):
    if user_money == 300:
        return  "price < 300"
    elif user_money >= 300 and user_money < 750:
        return "price >= 300 and price < 750"
    else:
        return "price >= 750"


def check_channel(user_channel):
    if user_channel == "專櫃":
        return "( channel = \"專櫃\"  or  channel = \"專賣店\")"
    elif user_channel == "網路":
        return "( channel = \"網路\"  or  channel = \"網站\")"
    elif user_channel == "開架" :
        return "channel = \"開架\" "
    else:
        return "( channel = \"其他\"  or channel = \"醫療通路\")"


def sendCarousel(event ,user_Data):  #我的推薦_轉盤樣板

    # data_id[1] -> "喜歡" ,data_id[2] -> "不喜歡" ,data_id[3] -> "價格範圍" ,data_id[4] -> "喜歡的行銷通路"
    db = MySQLdb.connect(host="localhost", user="min", passwd="1234", db="db104_testdb", port=3306, charset="utf8")
    corsor = db.cursor()  # 建立游標
    db.autocommit(True)  # 自動確認
    price = check_money(user_Data[3])
    channel = check_channel(user_Data[4])
    product_type = ["眉睫" ,"面頰" ,"唇彩"  ,"眼影" ,"眼線"]
    product_Data = []
    for i in product_type:
        sql_str = "select * from my_recommend where class_label = \"{}\" and {} and {}  and product_type = \"{}\" order by rand() limit 1 ; " .format(user_Data[1] ,price  ,channel , i)
        corsor.execute(sql_str)
        product_Data_temp = corsor.fetchone()
        product_Data.append(product_Data_temp)
        print(product_Data_temp)
    db.close()

    images_html = "https://i.imgur.com/S1tEKgE.png"
    images_html2 = "https://dg9ugnb21lig7.cloudfront.net/uploads/images/product_default_250x250.png"
    product_name = []
    images = []
    check_end(product_Data ,product_name ,images ,images_html2)

    print(product_name)
    print(images)
    try:
        message = TemplateSendMessage(
            alt_text='轉盤樣板',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='%s' %(images[0]),
                        title='%s' %(product_name[0]),
                        text='%s' %(product_Data[0][3]),
                        actions=[
                            URITemplateAction(
                                label='產品詳情',
                                uri='%s' %(product_Data[0][16])
                            ),
                            URITemplateAction(
                                label='文章介紹',
                                uri='%s' %(product_Data[0][18])
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='%s' %(images[1]),
                        title='%s'%(product_name[1]),
                        text='%s' %(product_Data[1][3]),
                        actions=[
                            URITemplateAction(
                                label='產品詳情',
                                uri='%s' %(product_Data[1][16])
                            ),
                            URITemplateAction(
                                label='文章介紹',
                                uri='%s' %(product_Data[1][18])
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='%s' %(images[2]),
                        title='%s' %(product_name[2]),
                        text='%s' %(product_Data[2][3]),
                        actions=[
                            URITemplateAction(
                                label='產品詳情',
                                uri='%s' %(product_Data[2][16])
                            ),
                            URITemplateAction(
                                label='文章介紹',
                                uri='%s' %(product_Data[2][18])
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='%s' %(images[3]),
                        title='%s' %(product_name[3]),
                        text='%s' %(product_Data[3][3]),
                        actions=[
                            URITemplateAction(
                                label='產品詳情',
                                uri='%s' %(product_Data[3][16])
                            ),
                            URITemplateAction(
                                label='文章介紹',
                                uri='%s' %(product_Data[3][18])
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='%s' %(images[4]),
                        title='%s' %(product_name[4]),
                        text='%s' %(product_Data[4][3]),
                        actions=[
                            URITemplateAction(
                                label='產品詳情',
                                uri='%s' %(product_Data[4][16])
                            ),
                            URITemplateAction(
                                label='文章介紹',
                                uri='%s' %(product_Data[4][18])
                            ),
                        ]
                    )
                ]
            )
        )

        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))



def fill_in_the_form(event):
    event_userID = str(event.source).split('"')[7]
    ngrok_http = "f7aabb5f"
    print(event_userID)

    # poseidon_url = "http://%s.ngrok.io/form_db/?Poseidon=%s"%(ngrok_http ,event_userID)
    poseidon_url = "https://%s.ngrok.io/set_cookie/name/%s"%(ngrok_http ,event_userID)
    # poseidon_url = "https://forms.gle/PZmWWXcBn6M5uEJt5"

    # 這邊給網址 ， 導入到 views.post 的 func 網頁
    # message = [TextSendMessage(text="https://7d8cbda6.ngrok.io/form_db/?Poseidon=%s"%(event_userID))]
    bubble = BubbleContainer(
        body=BoxComponent(
            layout='horizontal' ,
            contents=[
                ButtonComponent(
                    style="primary",
                    height="sm",
                    action=URIAction(label="♥    推薦表單    ♥" ,
                                     uri=poseidon_url),
                    color="#e899c5"
                    # color="#eba2ca"

                )
            ],
        )
    )
    message = FlexSendMessage(alt_text="推薦表單" ,contents=bubble)

    line_bot_api.reply_message(event.reply_token, message)
    # line_bot_api.reply_message(event.reply_token, TextSendMessage(text='line://app/1653665371-Ow2DqxB6'))
    # line_bot_api.reply_message(event.reply_token, TextSendMessage(text='你沒填過資料，但是表單還沒好，還沒辦法填喔，哈哈哈哈哈!!!!!'))
    return 0



def search_db(event):
    event_userID = str(event.source).split('"')[7]
    #print(event_userID , ":" ,type(event_userID))

    #測試用 存在
    # event_userID = "Uac87c5da0501e3c35e05b0aeae7b733f"
    #測試用 不存在
    # event_userID = "Uac87c5da0501e3c35e05b0aeae7b7322"

    db = MySQLdb.connect(host="localhost", user="min", passwd="1234", db="db104_testdb", port=3306, charset="utf8")
    corsor = db.cursor()  # 建立游標
    db.autocommit(True)  # 自動確認
    sql_str = "select * ,count(UserId) from footprint where UserId = \"{}\" ; " .format(event_userID)
    corsor.execute(sql_str)
    user_Data = corsor.fetchone()
    db.close()
    return user_Data


def send_commend_Quickreply(event):  # 快速選單

    mycommendButton = QuickReplyButton(
        action=MessageAction(
            label="我的推薦",
            text="#我的推薦#",
        )
    )

    deleteButton = QuickReplyButton(
        action=MessageAction(
            label="清除推薦資訊",
            text="#清除我的推薦資料#"
        )
    )

    quickReplyList = QuickReply(
        items=[mycommendButton, deleteButton]
    )

    try:

        message = TextSendMessage(
            text='選擇您的功能', quick_reply=quickReplyList)

        line_bot_api.reply_message(event.reply_token, message)

    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤，請重新點選功能'))


def delete_commend_form(event):
    # line_bot_api.reply_message(event.reply_token, TextSendMessage(text='功能完成，暫時不開放使用'))
    # return 0

    event_userID = str(event.source).split('"')[7]
    db = MySQLdb.connect(host="localhost", user="min", passwd="1234", db="db104_testdb", port=3306, charset="utf8")
    corsor = db.cursor()  # 建立游標
    db.autocommit(True)  # 自動確認

    delete_sql_str = "delete from footprint where UserId = \"{}\" ;" .format(event_userID)
    corsor.execute(delete_sql_str)
    db.close()

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text='刪除完成，請重新填選表單'))

    return 0



def follow_in_the_form(event):
    event_userID = str(event.source).split('"')[7]
    print(event_userID)
    ngrok_http = "f7aabb5f"
    poseidon_url = "https://%s.ngrok.io/set_cookie/name/%s"%(ngrok_http ,event_userID)
    # poseidon_url = "https://forms.gle/PZmWWXcBn6M5uEJt5"
    bubble = BubbleContainer(
        body=BoxComponent(
            layout='horizontal' ,
            contents=[
                ButtonComponent(
                    style="primary",
                    height="sm",
                    action=URIAction(label="♥    推薦表單    ♥" ,
                                     uri=poseidon_url),
                    color="#e899c5"
                    # color="#eba2ca"

                )
            ],
        )
    )
    message = FlexSendMessage(alt_text="推薦表單" ,contents=bubble)

    line_bot_api.reply_message(event.reply_token, message)
    return 0

#####################################################################################################################
    #
    #
    # try:
    #     message = TemplateSendMessage(
    #         alt_text='轉盤樣板',
    #         template=CarouselTemplate(
    #             columns=[
    #                 CarouselColumn(
    #                     thumbnail_image_url='https://i.imgur.com/4QfKuz1.png',
    #                     title='商品名稱,品牌_1',
    #                     text='產品種類',
    #                     actions=[
    #                         URITemplateAction(
    #                             label='推薦原因/使用心得',
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
    #                     title='商品名稱,品牌_2',
    #                     text='產品種類',
    #                     actions=[
    #                         URITemplateAction(
    #                             label='推薦原因/使用心得',
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
    #                     title='商品名稱,品牌_3',
    #                     text='產品種類',
    #                     actions=[
    #                         URITemplateAction(
    #                             label='推薦原因/使用心得',
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
    #                     title='商品名稱,品牌_4',
    #                     text='產品種類',
    #                     actions=[
    #                         URITemplateAction(
    #                             label='推薦原因/使用心得',
    #                             uri='http://www.e-happy.com.tw'
    #                         ),
    #                         URITemplateAction(
    #                             label='產品說明/了解更多',
    #                             uri='http://www.e-happy.com.tw'
    #                         ),
    #                     ]
    #                 ),
    #                 CarouselColumn(
    #                     thumbnail_image_url='https://i.imgur.com/qaAdBkR.png',
    #                     title='商品名稱,品牌_5',
    #                     text='產品種類',
    #                     actions=[
    #                         URITemplateAction(
    #                             label='推薦原因/使用心得',
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
    #
    #     line_bot_api.reply_message(event.reply_token, message)
    # except:
    #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))
    #



