from django.conf import settings
from pymongo import MongoClient
from linebot import LineBotApi
from linebot.models import *
import random

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)



def sendQuickreply(event):  # 快速選單

    ## 點擊後，以用戶身份發送文字消息
    ## MessageAction
    eyeButton = QuickReplyButton(
        action=MessageAction(
            label="眼妝",
            text="#眼妝_c#",
        )
    )

    faceButton = QuickReplyButton(
        action=MessageAction(
            label="臉部",
            text="#臉部_c#"
        )
    )
    lipButton = QuickReplyButton(
        action=MessageAction(
            label="唇部",
            text="#唇部_c#"
        )
    )
    quickReplyList = QuickReply(
        items=[eyeButton, faceButton, lipButton]
    )

    try:

        message = TextSendMessage(
            text='選擇您想要學習的區域?', quick_reply=quickReplyList)

        line_bot_api.reply_message(event.reply_token, message)

        # line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))


def sendLearn_paper(event, mtext):
    try:
        conn = MongoClient('mongodb://10.120.38.27:15000/')
        db = conn.teach_data

        if mtext == "#唇部_c#":
            collection = db.lips
        elif mtext == "#臉部_c#":
            collection = db.face
        else:
            collection = db.eyes

        # conn = MongoClient('mongodb://10.120.38.27:15000/')
        # db = conn.teach_data)
        # test if connection success
        # collection.stats
        mongo_fetch_content = []
        count = 1
        while count <= 6:
            j = random.randint(1, 150)
            coursor = collection.find_one({'_id': j})
            mongo_fetch_content.append(coursor['標題'])
            mongo_fetch_content.append(coursor['網址'])
            count += 1
        learn_url = ''.join(x + '\n' for x in mongo_fetch_content)

        message = TextSendMessage(text=learn_url)

        line_bot_api.reply_message(event.reply_token, message)

    except:

        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))


##########################################################################################################
# from django.conf import settings
# from pymongo import MongoClient
# from linebot import LineBotApi
# from linebot.models import *
#
# line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
#
# # 創建QuickReplyButton
#
# ## 點擊後，以用戶身份發送文字消息
# ## MessageAction
# eyeButton = QuickReplyButton(
#     action=MessageAction(
#         label="眼妝",
#         text="#眼妝_c#",
#     )
# )
# faceButton = QuickReplyButton(
#     action=MessageAction(
#         label="臉部",
#         text="#臉部_c#"
#     )
# )
# lipButton = QuickReplyButton(
#     action=MessageAction(
#         label="唇部",
#         text="#唇部_c#"
#     )
# )
# quickReplyList = QuickReply(
#     items = [eyeButton, faceButton, lipButton]
# )
#
# def sendQuickreply(event):  #快速選單
#     try:
#
#
#         message = TextSendMessage(
#             text='選擇您想要學習的區域?', quick_reply=quickReplyList)
#
#         line_bot_api.reply_message(event.reply_token,message)
#         ########################  return 0 是多放的 ，為了環境測試用 #########################
#         return 0
#         conn = MongoClient('mongodb://10.120.38.7:15000/')
#         db = conn.teach_data
#         collection = db.eyes
#
#         ###### test if connection success
#         collection.stats
#
#         coursor = collection.find_one({})
#
#         message = TextSendMessage(text=str(coursor))
#
#     except:
#         line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
