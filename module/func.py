from django.conf import settings

from linebot import LineBotApi
from linebot.models import *
from module.my_recommend import check_end

import MySQLdb

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

def Top_Ranking_search_user(event):
    event_userID = str(event.source).split('"')[7]
    #print(event_userID , ":" ,type(event_userID))

    db = MySQLdb.connect(host="localhost", user="min", passwd="1234", db="db104_testdb", port=3306, charset="utf8")
    corsor = db.cursor()  # 建立游標
    db.autocommit(True)  # 自動確認
    sql_str = "select * ,count(UserId) from top_ranking_footprint where UserId = \"{}\" ; " .format(event_userID)
    corsor.execute(sql_str)
    user_Data = corsor.fetchone()
    db.close()
    return user_Data

def Top_Ranking_Position(event):  #多項傳送

    eyebrow_Button = QuickReplyButton(
        action=MessageAction(
            label="眉睫",
            text="#眉睫#",
        )
    )

    eyeshadow_Button = QuickReplyButton(
        action=MessageAction(
            label="眼影",
            text="#眼影#",
        )
    )

    eyeliner_Button = QuickReplyButton(
        action=MessageAction(
            label="眼線",
            text="#眼線#",
        )
    )

    cheek_Button = QuickReplyButton(
        action=MessageAction(
            label="面頰",
            text="#面頰#",
        )
    )

    lip_Button = QuickReplyButton(
        action=MessageAction(
            label="唇彩",
            text="#唇彩#"
        )
    )

    quickReplyList = QuickReply(
        items=[eyebrow_Button ,eyeshadow_Button ,eyeliner_Button ,cheek_Button ,lip_Button ]
    )

    try:

        message = TextSendMessage(
            text='選擇部位', quick_reply=quickReplyList)

        line_bot_api.reply_message(event.reply_token, message)

    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤，請重新點選功能'))



def Top_Ranking_List(event):  #多項傳送

    event_userID = str(event.source).split('"')[7]
    print(event_userID , ":" ,type(event_userID))
    message_content = str(event.message.text).strip().strip("#")
    print("message : " ,message_content ,":" ,type(message_content))

    #測試用 存在
    # event_userID = "Uac87c5da0501e3c35e05b0aeae7b733f"
    #測試用 不存在
    # event_userID = "Uac87c5da0501e3c35e05b0aeae7b7322"

    # 建立連線
    db = MySQLdb.connect(host="localhost", user="min", passwd="1234", db="db104_testdb", port=3306, charset="utf8")
    corsor = db.cursor()  # 建立游標
    db.autocommit(True)  # 自動確認

    sql_str = "select count(UserId) from top_ranking_footprint where UserId = \"{}\" ".format(event_userID)
    corsor.execute(sql_str)
    exist_user = corsor.fetchone()
    print(exist_user)
    #把 message.text 寫入資料庫
    if exist_user[0] == 0 :
        insert_top_ranking_str = "insert into top_ranking_footprint values(\"{}\" ,\"{}\") ;" .format(event_userID ,message_content)
        corsor.execute(insert_top_ranking_str)
        db.close()
    elif exist_user[0] == 1 :
        update_top_ranking_str = "update top_ranking_footprint set part = \"{}\" where UserId = \"{}\" ; " .format(message_content ,event_userID)
        corsor.execute(update_top_ranking_str)
        db.close()
    else:
        print("沒新增到，也沒更新到")
        pass

    popular_Button = QuickReplyButton(
        action=MessageAction(
            label="人氣最高",
            text="#人氣最高#",
        )
    )

    index_Button = QuickReplyButton(
        action=MessageAction(
            label="推薦指數最高",
            text="#推薦指數最高#"
        )
    )

    quickReplyList = QuickReply(
        items=[popular_Button ,index_Button]
    )

    try:

        message = TextSendMessage(
            text='選擇推薦指標', quick_reply=quickReplyList)

        line_bot_api.reply_message(event.reply_token, message)

    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤，請重新點選功能'))


def Top_Ranking_fetch(event ,user_Data):
    print(user_Data[1])
    if event.message.text == "#人氣最高#" :
        fetch_cloumn_name = "popularity"
    else :
        fetch_cloumn_name = "recommend"
    print(fetch_cloumn_name)
    print("Top_ranking_fetch_message : " ,event.message.text)
    db = MySQLdb.connect(host="localhost", user="min", passwd="1234", db="db104_testdb", port=3306, charset="utf8")
    corsor = db.cursor()  # 建立游標
    db.autocommit(True)  # 自動確認

    top_ranking_str = "select * from my_recommend where product_type = \"{}\"  order by {} desc limit 5 ; " .format(user_Data[1] ,fetch_cloumn_name)
    corsor.execute(top_ranking_str)
    product_Data = corsor.fetchall()
    db.close()
    product_name = []
    images = []
    images_html = "https://i.imgur.com/S1tEKgE.png"
    images_html2 = "https://dg9ugnb21lig7.cloudfront.net/uploads/images/product_default_250x250.png"
    check_end(product_Data ,product_name ,images ,images_html2)

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


def sendMulti(event):  #多項傳送
    try:
        message = [  #串列
            StickerSendMessage(  #傳送貼圖
                package_id='1',
                sticker_id='2'
            ),
            TextSendMessage(  #傳送y文字
                text = "這是 Pizza 圖片！"
            ),
            ImageSendMessage(  #傳送圖片
                original_content_url = "https://i.imgur.com/4QfKuz1.png",
                preview_image_url = "https://i.imgur.com/4QfKuz1.png"
            )
        ]
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))



def sendStick(event):  #傳送貼圖
    try:
        message = StickerSendMessage(  #貼圖兩個id需查表
            package_id='1',
            sticker_id='2'
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))



def sendPosition(event):  #傳送位置
    try:
        message = LocationSendMessage(
            title='TibaMe x 資策會中壢中心',
            address='320桃園市中壢區中大路300號',
            latitude=24.967775,  #緯度
            longitude=121.191621  #經度
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))



