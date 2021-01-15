# Coin scraper

Coin Scraper is a stock(KOSPI, KOSDAQ) traing program that automatically sells and buys stocks based on the 'Open Api' of KIWOOM Securities Co., Ltd. at Korea. The program uses TensorFlow-Keras time series analysis to predict stock prices for the next three days and automatically trade with trend-seeking techniques.

This program is built on Python 3.8.7, PyQt5, Tensorflow 2.3.0.
OpenAi installation of Kiwoom Securities is required for code use.
For more information, visit https://www3.kiwoom.com/nkw.templateFrameSet.do?m=m1408010600

File Configuration
============================
1. coinscraper.ui : PyQt5 ui file
2. main.py : Main Module
3. seriesPredict.ipynb : Tensorflow time-series analysis module 

How to use
============================
1. Download your target stock's daily candle chart from 'Yahoo finance'. You have to set period about 2 ~ 3 years. Downloaded file must be .csv file.
2. Remove dummy data in stock csv file. Due to error of Yahoo finance, There are some null cell in csv data. Please delete whole errored row (Even another cell in that row is normal)   
2. Import csv file to seriesPredict.ipynb. And click the interpret buttons in turn. Tensorflow-keras time-series analysis will be execute. (From Data preprocess to compile and build)
3. Please compile main.py in your IDE. (I suggest to use Pycharm 2020.3)
4. Click the "로그인" button and Login to Kiwoom open api. When main ui displayed, search your target stock's code in yahoo finance and Put the code beside of "추적" button, then click that "추적" button. and It will track stock's price trend in real-time. 
