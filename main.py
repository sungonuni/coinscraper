import sys
import threading
import time
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QAxContainer import *
app = None

form_class = uic.loadUiType("coinscraper.ui")[0]


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Coinscraper v0.4 / Made by Seonggon Michael Kim")
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

        self.upjongMenu.setDisabled(True)
        self.gwanjongMenu.setDisabled(True)
        self.tmoneyBtn.setDisabled(True)
        self.tmoneyOutput.setDisabled(True)
        self.codeInput.setDisabled(True)
        self.watchBtn.setDisabled(True)
        self.stopBtn.setDisabled(True)
        self.autoCheck.setDisabled(True)
        self.watchOutput.setDisabled(True)
        self.bidaskLog.setDisabled(True)
        self.compareLog.setDisabled(True)

        # 로그인 부
        self.loginBtn.clicked.connect(self.login)
        self.kiwoom.OnEventConnect.connect(self.event_connect)
        # 실시간 감시 부
        self.watchBtn.clicked.connect(self.getName)
        # self.watchBtn.clicked.connect(self.watchDogs)
        self.tmoneyBtn.clicked.connect(self.getTopmoney)
        self.kiwoom.OnReceiveTrData.connect(self.getData)
        # self.kiwoom.OnReceiveRealData.connect(self.getRealdata) # 실시간 체결가분석
        self.stopBtn.clicked.connect(self.stopSearch)
        # 주문 및 TS5T 부
        self.orderBtn.clicked.connect(self.sendOrder)
        self.kiwoom.OnReceiveChejanData.connect(self.getChejan)
        # 실시간 호가 부
        self.rHogaSearch.clicked.connect(self.sendrHoga)
        self.kiwoom.OnReceiveRealData.connect(self.getRealdata)
        self.rstopBtn.clicked.connect(self.rstopSearch)

        self.stopCheck = 0
        self.check0 = 0
        self.check1 = 0
        self.check2 = 0
        '''
        self.status = 0  # 실시간 틱 이평 작동지표

        self.list200 = []
        self.count200 = 0

        self.list400 = []
        self.count400 = 0
        '''

    def login(self):
        ret = self.kiwoom.dynamicCall("CommConnect()")

    def event_connect(self, err_code):
        if err_code == 0:
            self.loginStatus.setText("로그인\n 성공")

            self.upjongMenu.setDisabled(False)
            self.gwanjongMenu.setDisabled(False)
            self.tmoneyBtn.setDisabled(False)
            self.tmoneyOutput.setDisabled(False)
            self.codeInput.setDisabled(False)
            self.watchBtn.setDisabled(False)
            self.autoCheck.setDisabled(False)
            self.watchOutput.setDisabled(False)
            self.bidaskLog.setDisabled(False)
            self.compareLog.setDisabled(False)

            # 계좌 자동추가
            accounts = self.kiwoom.dynamicCall("GetLoginInfo(QString)", "ACCNO")
            accounts_num = int(self.kiwoom.dynamicCall("GetLoginInfo(QString)", "ACCOUNT_CNT"))
            account_list = accounts.split(';')[0:accounts_num]
            self.accList.addItems(account_list)

        else:
            self.loginStatus.setText("로그인\n 실패")

    def getTopmoney(self):
        upjongMenu_look_up = {'전체': '000', '코스피': '001', '코스닥': '101'}
        gwanjongMenu_look_up = {'관리종목 포함': 1, '관리종목 미포함': 0}

        upjong = self.upjongMenu.currentText()
        gwanjong = self.gwanjongMenu.currentText()

        self.kiwoom.dynamicCall("SetInputValue(Qstring, Qstring)", "시장구분", upjongMenu_look_up[upjong])
        self.kiwoom.dynamicCall("SetInputValue(Qstring, Qstring)", "관리종목포함", gwanjongMenu_look_up[gwanjong])
        self.kiwoom.dynamicCall("CommRqData(Qstring, Qstring, int, Qstring)", "opt10032_req", "opt10032", 0, "0101")

    def getName(self):
        while True:
            self.watchDogs()
            time.sleep(10)

    def watchDogs(self):
        code = self.codeInput.text()
        # 이름 요청
        self.kiwoom.dynamicCall("SetInputValue(Qstring, Qstring)", "종목코드", code)
        self.kiwoom.dynamicCall("CommRqData(Qstring, Qstring, int, Qstring)", "opt10001_req", "opt10001", 0, "0101")
        time.sleep(1)
        # 틱 이평 요청
        print("틱이평 요청시작")
        self.kiwoom.dynamicCall("SetInputValue(Qstring, Qstring)", "종목코드", code)
        self.kiwoom.dynamicCall("SetInputValue(Qstring, Qstring)", "틱범위", 10)
        self.kiwoom.dynamicCall("SetInputValue(Qstring, Qstring)", "수정주가구분", 0)
        self.kiwoom.dynamicCall("CommRqData(Qstring, Qstring, int, Qstring)", "opt10079_req", "opt10079", 0, "0101")
        print("틱이평 요청완료, i = " + str(0))
        time.sleep(1)
        # 지수 이평 요청
        print("지수이평 요청시작")
        self.kiwoom.dynamicCall("SetInputValue(Qstring, Qstring)", "업종코드", "101")
        self.kiwoom.dynamicCall("SetInputValue(Qstring, Qstring)", "틱범위", 1)
        self.kiwoom.dynamicCall("CommRqData(Qstring, Qstring, int, Qstring)", "opt20005_req", "opt20005", 0, "0101")
        print("지수이평 요청완료, i = " + str(0))
        time.sleep(1)
        # 체결강도 요청
        print("체결강도 요청시작")
        self.kiwoom.dynamicCall("SetInputValue(Qstring, Qstring)", "종목코드", code)
        self.kiwoom.dynamicCall("CommRqData(Qstring, Qstring, int, Qstring)", "opt10003_req", "opt10003", 0, "0101")
        print("체결강도 요청완료, i = " + str(0))

        if self.stopCheck == -1:  # -1 == 정지명령
            self.compareLog.appendPlainText("2번 감시 종료")
            self.stopCheck = 0

    def stopSearch(self):
        self.stopCheck = -1
        self.compareLog.appendPlainText("1번 감시 종료")

    def getData(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
        # self.kiwoom.dynamicCall("DisconnectRealData(Qstring)", "0101") # 과부하 방지를 위한 실시간 검색 중지

        if rqname == "opt10001_req":
            name1 = self.kiwoom.dynamicCall("GetCommData(Qstring, Qstring, int, Qstring)", trcode, "주식기본정보요청", 0,
                                            "종목명")
            self.compareLog.appendPlainText(" ")
            self.compareLog.appendPlainText(name1.strip())
            self.watchOutput.setItem(0, 0, QTableWidgetItem(name1.strip()))

        if rqname == "opt10079_req":
            # 200틱 이동평균
            num2 = 0
            sum2 = 0
            for i in range(20):
                tsma2 = self.kiwoom.dynamicCall("GetCommData(Qstring, Qstring, int, Qstring)", trcode, "주식틱차트요청", i,
                                                "현재가")
                if tsma2 == '':  # 오류 방지를 위한 예외처리
                    tsma2 = '0'
                print('200틱 : ' + tsma2)  # 디버깅용

                num2 = int(tsma2.strip())
                # self.list200.append(num)
                # self.count200 = self.count200 + 1
                sum2 = sum2 + num2
            tsma200 = sum2 / 20
            self.compareLog.appendPlainText(" ")
            self.compareLog.appendPlainText("최초 200틱 이동평균 :" + str(tsma200))

            # 400틱 이동평균
            num3 = 0
            sum3 = 0
            for i in range(40):
                tsma3 = self.kiwoom.dynamicCall("GetCommData(Qstring, Qstring, int, Qstring)", trcode, "주식틱차트요청", i,
                                                "현재가")
                if tsma3 == '':  # 오류 방지를 위한 예외처리
                    tsma3 = '0'
                print('400틱 :' + tsma3)  # 디버깅용

                num3 = int(tsma3.strip())
                # self.list400.append(num)
                # self.count400 = self.count400 + 1
                sum3 = sum3 + num3
            tsma400 = sum3 / 40
            self.compareLog.appendPlainText("최초 400틱 이동평균 :" + str(tsma400))

            if tsma200 > tsma400:
                self.watchOutput.setItem(0, 1, QTableWidgetItem("만족"))
                self.compareLog.appendPlainText("만족")
                self.check0 = 1
            else:
                self.watchOutput.setItem(0, 1, QTableWidgetItem("불만족"))
                self.compareLog.appendPlainText("불만족")
                self.check0 = 0

            # self.status = 1 # 실시간 틱 데이터 취합시작

        if rqname == "opt20005_req":
            # 2분 이동평균
            num4 = 0
            sum4 = 0
            for i in range(0, 2):
                kospi4 = self.kiwoom.dynamicCall("GetCommData(Qstring, Qstring, int, Qstring)", trcode, "업종분봉조회요청",
                                                 i, "현재가")
                if kospi4 == '':  # 오류 방지를 위한 예외처리
                    kospi4 = '0'
                print('코스피 2분 :' + kospi4)  # 디버깅용

                num4 = int(kospi4.strip()[1:7])
                sum4 = sum4 + num4
            kospi2m = sum4 / 2
            # self.tsmaOutput.appendPlainText("코스피 2분 이동평균 : " + str(kospi2m))
            self.compareLog.appendPlainText(str(kospi2m))

            # 4분 이동평균
            num5 = 0
            sum5 = 0
            for i in range(0, 4):
                kospi5 = self.kiwoom.dynamicCall("GetCommData(Qstring, Qstring, int, Qstring)", trcode, "업종분봉조회요청",
                                                 i, "현재가")
                if kospi5 == '':  # 오류 방지를 위한 예외처리
                    kospi5 = '0'
                print('코스피 4분 :' + kospi5)  # 디버깅용

                num5 = int(kospi5.strip()[1:7])
                sum5 = sum5 + num5
            kospi4m = sum5 / 4
            # self.tsmaOutput.appendPlainText("코스피 4분 이동평균 : " + str(kospi4m))
            self.compareLog.appendPlainText(str(kospi4m))

            if kospi2m > kospi4m:
                self.watchOutput.setItem(0, 2, QTableWidgetItem("만족"))
                self.compareLog.appendPlainText("만족")
                self.check1 = 1
            else:
                self.watchOutput.setItem(0, 2, QTableWidgetItem("불만족"))
                self.compareLog.appendPlainText("불만족")
                self.check1 = 0

        if rqname == "opt10003_req":
            num6 = 0
            sum6 = 0
            for i in range(0, 3):
                vola = self.kiwoom.dynamicCall("GetCommData(Qstring, Qstring, int, Qstring)", trcode, "체결정보요청", i,
                                               "체결강도")
                if vola == '':  # 오류 방지를 위한 예외처리
                    vola = '0'
                print('체결강도 :' + vola)  # 디버깅용

                num6 = float(vola.strip())
                sum6 = sum6 + num6
            vola4ea = sum6 / 3
            self.compareLog.appendPlainText(str(vola4ea))

            if vola4ea > 70:
                self.watchOutput.setItem(0, 3, QTableWidgetItem("만족"))
                self.compareLog.appendPlainText("만족")
                self.check2 = 1
            else:
                self.watchOutput.setItem(0, 3, QTableWidgetItem("불만족"))
                self.compareLog.appendPlainText("불만족")
                self.check2 = 0

            if self.check0 == 1 and self.check1 == 1 and self.check2 == 1:
                self.watchOutput.setItem(0, 4, QTableWidgetItem("가능"))
                self.stopSearch()
                QMessageBox.about(self, "알림", "진입가능시점입니다. 진입하시겠습니까?")

            else:
                self.watchOutput.setItem(0, 4, QTableWidgetItem("불가능"))

        if rqname == "opt10032_req":
            self.tmoneyOutput.clear()
            for i in range(0, 5):
                tmoneyCode = self.kiwoom.dynamicCall("GetCommData(Qstring, Qstring, int, Qstring)", trcode,
                                                     "거래대금상위요청", i, "종목코드")
                tmoneyName = self.kiwoom.dynamicCall("GetCommData(Qstring, Qstring, int, Qstring)", trcode,
                                                     "거래대금상위요청", i, "종목명")
                tmoneyVol = self.kiwoom.dynamicCall("GetCommData(Qstring, Qstring, int, Qstring)", trcode,
                                                    "거래대금상위요청", i, "거래대금")
                self.tmoneyOutput.appendPlainText(" ")
                self.tmoneyOutput.appendPlainText("종목코드 : " + tmoneyCode.strip())
                self.tmoneyOutput.appendPlainText("종목명 : " + tmoneyName.strip())
                self.tmoneyOutput.appendPlainText("거래대금 : " + tmoneyVol.strip())

    # 디버깅 필요!!
    def sendOrder(self):
        orderType_look_up = {'신규매수': 1, '신규매도': 2, '매수취소': 3, '매도취소': 4}
        hoga_lookup = {'지정가': "00", '시장가': "03"}

        soAccount = self.accList.currentText()
        soOrderType = self.orderType.currentText()
        soCode = self.orderCode.text()
        soHoga = self.hoga.currentText()
        soNum = self.orderNum.value()
        soPrice = self.orderPrice.value()

        self.kiwoom.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                                ["RQ_1", "0101", str(soAccount), int(orderType_look_up[soOrderType]), str(soCode),
                                 int(soNum), int(soPrice), str(hoga_lookup[soHoga]), ""])
        self.bidaskLog.appendPlainText("주문을 전송했습니다.")

    def getChejan(self, gubun, item_cnt, fid_list):
        self.bidaskLog.appendPlainText(" ")
        self.bidaskLog.appendPlainText("구분 : " + gubun)
        gcOrderNum = self.kiwoom.dynamicCall("GetChejanData(int)", 9203)  # 9203 = 주문번호
        gcStockName = self.kiwoom.dynamicCall("GetChejanData(int)", 302)  # 302 = 종목명
        gcOrderAmt = self.kiwoom.dynamicCall("GetChejanData(int)", 900)  # 900 = 주문수량
        gcOrderPirce = self.kiwoom.dynamicCall("GetChejanData(int)", 901)  # 901 = 주문가격
        self.bidaskLog.appendPlainText("주문번호 : " + gcOrderNum)
        self.bidaskLog.appendPlainText("이름 : " + gcStockName)
        self.bidaskLog.appendPlainText("주문수량 : " + gcOrderAmt)
        self.bidaskLog.appendPlainText("주문가격 : " + gcOrderPirce)

    def sendrHoga(self):
        rHogaCode = self.rHogaCode.text()
        self.kiwoom.dynamicCall("SetInputValue(Qstring, Qstring)", "종목코드", rHogaCode)
        self.kiwoom.dynamicCall("CommRqData(Qstring, Qstring, int, Qstring)", "opt10004_req", "opt10004", 0, "0101")

    def getRealdata(self, sCode, sRealType, sRealData):  # bid : 매수, ask : 매도
        if sRealType == "주식호가잔량":
            '''
            ask5 = self.kiwoom.dynamicCall("GetCommRealData(Qstring, int)", sCode, 45)
            ask4 = self.kiwoom.dynamicCall("GetCommRealData(Qstring, int)", sCode, 44)
            ask3 = self.kiwoom.dynamicCall("GetCommRealData(Qstring, int)", sCode, 43)
            ask2 = self.kiwoom.dynamicCall("GetCommRealData(Qstring, int)", sCode, 42)
            ask1 = self.kiwoom.dynamicCall("GetCommRealData(Qstring, int)", sCode, 41)
            '''
            self.bidaskTable.setItem(0, 0, QTableWidgetItem(
                self.kiwoom.dynamicCall("GetCommRealData(Qstring, int)", sCode, 45)))
            self.bidaskTable.setItem(1, 0, QTableWidgetItem(
                self.kiwoom.dynamicCall("GetCommRealData(Qstring, int)", sCode, 44)))
            self.bidaskTable.setItem(2, 0, QTableWidgetItem(
                self.kiwoom.dynamicCall("GetCommRealData(Qstring, int)", sCode, 43)))
            self.bidaskTable.setItem(3, 0, QTableWidgetItem(
                self.kiwoom.dynamicCall("GetCommRealData(Qstring, int)", sCode, 42)))
            self.bidaskTable.setItem(4, 0, QTableWidgetItem(
                self.kiwoom.dynamicCall("GetCommRealData(Qstring, int)", sCode, 41)))
            self.bidaskTable.setItem(6, 1, QTableWidgetItem(
                self.kiwoom.dynamicCall("GetCommRealData(Qstring, int)", sCode, 51)))
            self.bidaskTable.setItem(7, 1, QTableWidgetItem(
                self.kiwoom.dynamicCall("GetCommRealData(Qstring, int)", sCode, 52)))
            self.bidaskTable.setItem(8, 1, QTableWidgetItem(
                self.kiwoom.dynamicCall("GetCommRealData(Qstring, int)", sCode, 53)))
            self.bidaskTable.setItem(9, 1, QTableWidgetItem(
                self.kiwoom.dynamicCall("GetCommRealData(Qstring, int)", sCode, 54)))
            self.bidaskTable.setItem(10, 1, QTableWidgetItem(
                self.kiwoom.dynamicCall("GetCommRealData(Qstring, int)", sCode, 55)))
        '''
        if sRealType == "주식체결":
            self.bidaskTable.setItem(5, 0, QTableWidgetItem(
                self.kiwoom.dynamicCall("GetCommRealData(Qstring, int)", sCode, 10)))
        '''

    def rstopSearch(self):
        self.kiwoom.dynamicCall("DisconnectRealData(Qstring)", "0101")
        self.bidaskTable.setItem(0, 0, QTableWidgetItem(" "))
        self.bidaskTable.setItem(1, 0, QTableWidgetItem(" "))
        self.bidaskTable.setItem(2, 0, QTableWidgetItem(" "))
        self.bidaskTable.setItem(3, 0, QTableWidgetItem(" "))
        self.bidaskTable.setItem(4, 0, QTableWidgetItem(" "))
        self.bidaskTable.setItem(5, 0, QTableWidgetItem(" "))
        self.bidaskTable.setItem(6, 1, QTableWidgetItem(" "))
        self.bidaskTable.setItem(7, 1, QTableWidgetItem(" "))
        self.bidaskTable.setItem(8, 1, QTableWidgetItem(" "))
        self.bidaskTable.setItem(9, 1, QTableWidgetItem(" "))
        self.bidaskTable.setItem(10, 1, QTableWidgetItem(" "))

    ''' 실시간 감시기
    def getRealdata(self, sCode, sRealType, sRealData):
        if self.status == 1:
            priceStr = self.kiwoom.dynamicCall("GetCommRealData(Qstring, int)", sCode, 10)  # 실시간 현재가 받아오기
            price = int(priceStr.strip()[1:])

            # 실시간 200틱 평균 구하기
            sum = 0
            self.list200.append(price)
            self.count200 = self.count200 + 1
            if self.count200 > 200:
                del self.list200[0]
                self.count200 = self.count200 - 1
            for i in range(0, self.count200):
                sum = sum + self.list200[i]
            tsma200 = sum / self.count200

            # 실시간 400틱 평균 구하기
            sum = 0
            self.list400.append(price)
            self.count400 = self.count400 + 1
            if self.count400 > 400:
                del self.list400[0]
                self.count400 = self.count400 - 1
            for i in range(0, self.count400):
                sum = sum + self.list400[i]
            tsma400 = sum / self.count400

            self.compareLog.appendPlainText("실시간 200틱: " + str(tsma200) + ", 실시간 400틱: " + str(tsma400))

            if tsma200 > tsma400:
                self.watchOutput.setItem(0, 1, QTableWidgetItem("만족"))
            else:
                self.watchOutput.setItem(0, 1, QTableWidgetItem("불만족"))
    '''


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
