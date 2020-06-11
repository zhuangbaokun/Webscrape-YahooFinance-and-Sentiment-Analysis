# -*- coding: utf-8 -*-
"""
Created on Tue May 26 15:12:26 2020

@author: User
"""
##############Scrape#########################################
import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd
import numpy as np


# Create the Spider class
class YourSpider(scrapy.Spider):
    name = 'yourspider'
    headline_lst = []
    topic_lst = []
    url_lst = []
    date_lst = []
    test = None
  # start_requests method
    def start_requests(self):
        urls = ["https://sg.finance.yahoo.com/topic/stocks"]
        for url_ in urls:
            yield scrapy.Request(url = url_, callback = self.parse_stocks)
        urls = ["https://sg.finance.yahoo.com/topic/economy"]
        for url_ in urls:
            yield scrapy.Request(url = url_, callback = self.parse_economy)
        urls = ["https://sg.finance.yahoo.com/topic/technology"]
        for url_ in urls:
            yield scrapy.Request(url = url_, callback = self.parse_technology)  

        urls = ["https://www.businessinsider.sg/finance"]
        for url_ in urls:
            yield scrapy.Request(url = url_, callback = self.parse_bi)  

#########################Biz insider##############################################
    def parse_bi(self, response):
        length = 5
        root_url = ""
        urls = response.xpath('//div[@class="td_block_inner"]//h3/a/@href').getall()[0:length]
        headlines = response.xpath('//div[@class="td_block_inner"]//h3/a/@title').getall()[0:length]
        dates = response.xpath('//div[@class="td_block_inner"]//time/text()').getall()[0:length]
        
        YourSpider.topic_lst += ["Business Insider Finance"]*length
        YourSpider.headline_lst += headlines
        YourSpider.url_lst += pd.Series(urls).apply(lambda x: root_url + x).tolist()
        YourSpider.date_lst += dates


########################Stocks Parse#####################################################
    def parse_stocks(self, response):
        length = 5
        root_url = "https://sg.finance.yahoo.com"
        urls = response.xpath('//div[@id="Fin-Stream"]//a/@href').getall()[0:length]
        headlines = response.xpath('//div[@id="Fin-Stream"]//a/text()').getall()[0:length]
#        dates = response.xpath('//div[@id="Fin-Stream"]//div[@class="C(#959595) Fz(11px) D(ib) Mb(6px)"]/span/text()').getall()[0:length]

        YourSpider.topic_lst += ["Yahoo Fianance Stock"]*length
        YourSpider.headline_lst += headlines
        YourSpider.url_lst += pd.Series(urls).apply(lambda x: root_url + x).tolist()
        YourSpider.date_lst += [""]*length


########################Economy Parse#####################################################
    def parse_economy(self, response):
        length = 5
        root_url = "https://sg.finance.yahoo.com"
        urls = response.xpath('//div[@id="Fin-Stream"]//a/@href').getall()[0:length]
        headlines = response.xpath('//div[@id="Fin-Stream"]//a/text()').getall()[0:length]
#        dates = response.xpath('//div[@id="Fin-Stream"]//div[@class="C(#959595) Fz(11px) D(ib) Mb(6px)"]/span/text()').getall()[0:length]

        YourSpider.topic_lst += ["Yahoo Fianance Economy"]*length
        YourSpider.headline_lst += headlines
        YourSpider.url_lst += pd.Series(urls).apply(lambda x: root_url + x).tolist()
        YourSpider.date_lst += [""]*length

########################Techonology Parse#####################################################
    def parse_technology(self, response):
        length = 5
        root_url = "https://sg.finance.yahoo.com"
        urls = response.xpath('//div[@id="Fin-Stream"]//a/@href').getall()[0:length]
        headlines = response.xpath('//div[@id="Fin-Stream"]//a/text()').getall()[0:length]
#        dates = response.xpath('//div[@id="Fin-Stream"]//div[@class="C(#959595) Fz(11px) D(ib) Mb(6px)"]/span/text()').getall()[0:length]

        YourSpider.topic_lst += ["Yahoo Fianance Technology"]*length
        YourSpider.headline_lst += headlines
        YourSpider.url_lst += pd.Series(urls).apply(lambda x: root_url + x).tolist()
        YourSpider.date_lst += [""]*length

################### Run Spider#########################################################
process = CrawlerProcess()
process.crawl(YourSpider)
process.start()

df = pd.DataFrame({"Date":YourSpider.date_lst,"Topic":YourSpider.topic_lst,"url":YourSpider.url_lst,"title":YourSpider.headline_lst})
#######################Sentiment Analysis#####################################################

from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()
df["Sentiment_title"] = df.title.apply(sid.polarity_scores).apply(lambda x : "negative" if x["compound"]<=0 else "positive")
df["Sentiment_title_score"] = df.title.apply(sid.polarity_scores).apply(lambda x: str(x["compound"]))
################################Telegram Bot############################################
import matplotlib.pyplot as plt
df1 = df.groupby(["Sentiment_title"]).count().reset_index()
df1["overall"] = df1["Date"]/np.sum(df1["Date"])
fig = plt.figure()
plt.bar(df1["Sentiment_title"], df1["Date"]/np.sum(df1["Date"]))
plt.xlabel("Sentiment_title")
plt.ylabel("Value")
plt.title("Title Sentiment")
fig.savefig('Title Sentiment Breakdown.png')


from telegram.ext import Updater, InlineQueryHandler, CommandHandler,MessageHandler, Filters
import requests
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

token = '1263733111:AAEneGfvNNGN8ZoIOrGrHKcKg7AcpGPIgno'

def get_url():
    contents = requests.get('https://random.dog/woof.json').json()    
    url = contents['url']
    return url

#def bop(bot, update):
def bop(update, context):
#    url = get_url()
#    chat_id = update.message.chat_id
#    bot.send_photo(chat_id=chat_id, photo=url)
#    bot.send
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=get_url())

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry can speakerh Engrish?")

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me! \n Available Functions are: \n \n Main Functions: \n\n  \n 1) /sentimentscoreonly or /sentimentscoreplot \n 2) /headlineandsentiment \n 3) /headline \n \n Other Functions(Possibly Random): \n\n 1) /start \n 2) /bop \n 3) /caps <msg to apply higher case> ")

def ssplot(update, context):
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Title Sentiment Breakdown.png', 'rb'))

def ss(update, context):
    df2 = df.copy()
    df2 = df2[df2.Topic != "Yahoo Finance Technology"]
    df2 = df.groupby(["Sentiment_title"]).count().reset_index()
    df2["overall"] = df2["Date"]/np.sum(df2["Date"])
    content = "Overall Sentiment: \n" + df2.Sentiment_title.iloc[0]+"=" + str(df2.overall.iloc[0]) +"\n" +df2.Sentiment_title.iloc[1]+"=" + str(df2.overall.iloc[1]) 
    context.bot.send_message(chat_id=update.effective_chat.id, text=content)   

def hls(update, context):

    content = "Overall Sentiment:" + df1.Sentiment_title.iloc[0]+"=" + str(df1.overall.iloc[0]) +","+df1.Sentiment_title.iloc[1]+"=" + str(df1.overall.iloc[1]) 
    df2 = df[df.Topic != "Yahoo Finance Technology"]
    for i in range(len(df2)):
        content = content + "\n" +str(i + 1)+ ")"+ df2.title.iloc[i]  + " : " + df2.Sentiment_title.iloc[i]+" , " + df2.Sentiment_title_score.iloc[i] 
    context.bot.send_message(chat_id=update.effective_chat.id, text=content)

    
def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


def hl(update, context):
    content = ""
    topic = df.Topic.unique().tolist()
    for t in topic:
        df2 = df[df.Topic == t]
        content = content + "\n" +"**"+ t +"**"
        for i in range(len(df2)):
            content = content + " \n "+str(i + 1)+ ")"  + df2.title.iloc[i] + " : " + df2.url.iloc[i] 
    context.bot.send_message(chat_id=update.effective_chat.id, text=content )
#        context.bot.send_message(chat_id=update.effective_chat.id, text=)
#        context.bot.send_message(chat_id=update.effective_chat.id, text='<b>bold</b> <i>italic</i> <a href="{}">link</a>.'.format(df.url.iloc[i]), parse_mode=telegram.ParseMode.HTML)     

def main():
    updater = Updater(token, use_context = True)
    dp = updater.dispatcher
    ########Start
    dp.add_handler(CommandHandler('start', start))
    ########BOP    
    dp.add_handler(CommandHandler('bop',bop))
    #######Caps
    dp.add_handler(CommandHandler('caps', caps))
    ########HeadLines
    dp.add_handler(CommandHandler('headline',hl))
    ########HeadLines and Sentiment
    dp.add_handler(CommandHandler('headlineandsentiment',hls))
    ########Sentiment Score Only
    dp.add_handler(CommandHandler('sentimentscoreonly',ss))
    ########Sentiment Score Plot Only
    dp.add_handler(CommandHandler('sentimentscoreplot',ssplot))
    ##########Unknown
    unknown_handler = MessageHandler(Filters.command, unknown)
    dp.add_handler(unknown_handler)
#    dispatcher.add_handler(unknown_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()



#from telegram.ext import CommandHandler
#
#dispatcher.add_handler(start_handler)
#https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot
#updater.stop()
#Note: This handler must be added last. If you added it sooner, it would be triggered before the CommandHandlers had a chance to look at the update. Once an update is handled, all further handlers are ignored. To circumvent this, you can pass the keyword argument group (int) to add_handler with a value other than 0.




#location_keyboard = telegram.KeyboardButton(text="send_location", request_location=True)
#contact_keyboard = telegram.KeyboardButton(text="send_contact", request_contact=True)
#custom_keyboard = [[ location_keyboard, contact_keyboard ]]
#reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
#bot.send_message(chat_id=chat_id, 
#...                  text="Would you mind sharing your location and contact with me?", 
#...                  reply_markup=reply_markup)
    
    
    