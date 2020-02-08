from django.conf import settings

from linebot import LineBotApi
from linebot.models import *

## 新增的 ##
from hdfs import *

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

def openCameraRoll(event):  #按鈕樣版
    try:
        message = TemplateSendMessage(
            alt_text='按鈕樣板',
            template=ButtonsTemplate(
                thumbnail_image_url='https://a20514ab.ngrok.io/static/Schneewittchen.jpg',  #顯示的圖片
                title='智能上妝程式',  #主標題
                text='上傳一張照片,馬上模擬上妝',  #副標題
                actions=[
                    URITemplateAction(  #開啟相機
                        label='開啟相機',
                        uri='line://nv/camera/'
                    ),
                    URITemplateAction(  #開啟相簿
                        label='開啟相簿',
                        uri='line://nv/cameraRoll/single'
                    )
                ]
            )
        )

        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))



def sendMulti_send_image(event ,content):  #我要傳一張化妝圖片
    ########### 每次都要更改 ##########
    ngrok_name = "f7aabb5f"
    client = Client("http://10.120.38.7:50070")
    content_name = content.split('/')[3].split('.')[0]
    download_images_name = content_name + "_makeup.jpg"
    print("download_images_name :" , download_images_name)
    print("download to : " ,"E:/db104_2_project/static/%s" %(download_images_name))
    print("hdfs_path : " ,"/user/cloudera/makeup_images/%s" %(download_images_name))

    #這裡是重點
    while True:
        if client.status("/user/cloudera/makeup_images/%s" %(download_images_name) ,strict=False) != None :
            print("資料存在")
            break

    client.download("/user/cloudera/makeup_images/%s" %(download_images_name) ,"E:/db104_2_project/static/%s" %(download_images_name))
    print("從 圖片 hdfs 下載到本機了 準備上傳到 linebot ! ")



    try:
        message =[TextSendMessage(text="請打開") ,
                  ImageSendMessage(  #傳送圖片
                original_content_url = "https://%s.ngrok.io/static/%s" %(ngrok_name ,download_images_name),
                preview_image_url = "https://%s.ngrok.io/static/gift.jpg" %(ngrok_name)
            )]

        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))







###################### 下面舊版本的 ################################ 不用理會 ######################
#
# def sendMulti_send_image(event ,content):  #我要傳一張化妝圖片
#
#     #每次都要改
#     ngrok_name = "4af9da3e"
#
#     #跟hdfs 建立連結
#     client = Client("http://10.120.38.7:50070")
#
#     #print(client.list("/user/"))
#     #print(client.list("/user/cloudera/"))
#     #print(client.list("/user/cloudera/makeup_images/"))
#     content_name = content.split('/')[3].split('.')[0]
#     print(content_name)
#     download_images_name = content_name + "_makeup.jpg"
#     print("download_images_name :" , download_images_name)
#     print("download to : " ,"E:/db104_2_project/static/%s" %(download_images_name))
#     print("hdfs_path : " ,"/user/cloudera/makeup_images/%s" %(download_images_name))
#
#     count = 0
#     while True:
#         if client.status("/user/cloudera/makeup_images/%s" %(download_images_name) ,strict=False) != None :
#             print("資料存在")
#             break
#
#     #time.sleep(10)
#     client.download("/user/cloudera/makeup_images/%s" %(download_images_name) ,"E:/db104_2_project/static/%s" %(download_images_name))
#     print("從 圖片 hdfs 下載到本機了 準備上傳到 linebot : " ,count)
#
#     # 架構也可以變這樣 都可以
#     #client.download("/user/cloudera/makeup_images/%s_makeup.jpg" %(content_name) ,"E:/db104_2_project/static/%s_makeup.jpg" %(content_name) )
#
#     try:
#         message =[TextSendMessage(text="請打開") ,
#                   ImageSendMessage(  #傳送圖片
#                 original_content_url = "https://%s.ngrok.io/static/%s" %(ngrok_name ,download_images_name),
#                 preview_image_url = "https://%s.ngrok.io/static/gift.jpg" %(ngrok_name)
#             )]
#
#         line_bot_api.reply_message(event.reply_token,message)
#     except:
#         line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
