import sys
import check
import datetime
from PyQt5 import QtCore, QtGui, QtWidgets

try:
    import cx_Oracle
except:
    print("Import Error")
    if cx_Oracle.version<'3.0':
        print("Very old version of cx_Oracle :",cx_Oracle.version)
        sys.exit()

connection = cx_Oracle.connect('MAINADMIN', 'einstein', 'XE')
cursor = connection.cursor()


class Ui_CreateConference(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("New Conference")
        self.resize(381, 246)
        self.setMaximumSize(QtCore.QSize(381, 246))
        self.setWindowIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DesktopIcon))

        label_Title = QtWidgets.QLabel(self)
        label_Title.setGeometry(QtCore.QRect(20, 20, 47, 21))
        label_Title.setText("Title*")

        self.Conf_Title = QtWidgets.QLineEdit(self)
        self.Conf_Title.setGeometry(QtCore.QRect(80, 20, 281, 20))
        self.Conf_Title.setMaxLength(70)
        self.Conf_Title.setText("")

        label_Theme = QtWidgets.QLabel(self)
        label_Theme.setGeometry(QtCore.QRect(20, 50, 47, 21))
        label_Theme.setText("Theme")

        self.Conf_Theme = QtWidgets.QLineEdit(self)
        self.Conf_Theme.setGeometry(QtCore.QRect(80, 50, 281, 20))
        self.Conf_Theme.setMaxLength(70)
        self.Conf_Theme.setText("")

        label_Place = QtWidgets.QLabel(self)
        label_Place.setGeometry(QtCore.QRect(20, 80, 47, 21))
        label_Place.setText("Place*")

        self.Conf_Place = QtWidgets.QLineEdit(self)
        self.Conf_Place.setGeometry(QtCore.QRect(80, 80, 281, 20))
        self.Conf_Place.setMaxLength(70)
        self.Conf_Place.setText("")

        label_Price = QtWidgets.QLabel(self)
        label_Price.setGeometry(QtCore.QRect(20, 110, 47, 21))
        label_Price.setText("Price*")

        self.Conf_Price = QtWidgets.QLineEdit(self)
        self.Conf_Price.setGeometry(QtCore.QRect(80, 110, 281, 20))
        self.Conf_Price.setMaxLength(7)
        self.Conf_Price.setText('')

        label_Place_Quantity = QtWidgets.QLabel(self)
        label_Place_Quantity.setGeometry(QtCore.QRect(20, 140, 90, 21))
        label_Place_Quantity.setText("Quantity of seats*")

        self.Conf_Place_Quantity = QtWidgets.QLineEdit(self)
        self.Conf_Place_Quantity.setGeometry(QtCore.QRect(120, 140, 241, 20))
        self.Conf_Place_Quantity.setMaxLength(4)
        self.Conf_Place_Quantity.setValidator(QtGui.QIntValidator(1,1000))

        label_DateTime = QtWidgets.QLabel(self)
        label_DateTime.setGeometry(QtCore.QRect(20, 170, 81, 21))
        label_DateTime.setText("Date and Time*")

        self.Conf_DateTime = QtWidgets.QDateTimeEdit(self)
        self.Conf_DateTime.setGeometry(QtCore.QRect(110, 170, 251, 22))
        self.Conf_DateTime.setCalendarPopup(True)
        self.Conf_DateTime.setDateTime(datetime.datetime.now())
        self.Conf_DateTime.setMinimumDateTime(datetime.datetime.now())
        self.Conf_DateTime.setDisplayFormat("yyyy-MM-dd HH:mm")

        Button_Ok = QtWidgets.QPushButton(self)
        Button_Ok.setGeometry(QtCore.QRect(210, 200, 75, 23))
        Button_Ok.setText("Ok")
        Button_Ok.clicked.connect(self.buttonClicked)

        Button_Close = QtWidgets.QDialogButtonBox(self)
        Button_Close.setGeometry(QtCore.QRect(290, 200, 75, 23))
        Button_Close.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel)

        Button_Close.rejected.connect(self.reject)

    def buttonClicked(self):
        sender = self.sender()


        if sender.text() == "Ok":
            if check.check_Title(self.Conf_Title.text()) == False:
                if self.Conf_Title.text() == "":
                     buttonReply = QtWidgets.QMessageBox.warning(self, 'Error', "Title field is empty!",
                                                                  QtWidgets.QMessageBox.Ok)
                else:
                     buttonReply = QtWidgets.QMessageBox.warning(self, 'Error', "Wrong format of title! "
                                                                                "Right: with a capital letter "
                                                                                "or number",
                                                                  QtWidgets.QMessageBox.Ok)

            elif check.check_Theme(self.Conf_Theme.text()) == False and self.Conf_Theme.text() != "":
                buttonReply = QtWidgets.QMessageBox.warning(self, 'Error', "Wrong format of theme! "
                                                                                "Right: with a capital letter "
                                                                                "or number",
                                                                  QtWidgets.QMessageBox.Ok)

            elif check.check_Theme(self.Conf_Place.text()) == False:
                if self.Conf_Place.text() == "":
                     buttonReply = QtWidgets.QMessageBox.warning(self, 'Error', "Place field is empty!",
                                                                  QtWidgets.QMessageBox.Ok)
                else:
                     buttonReply = QtWidgets.QMessageBox.warning(self, 'Error', "Wrong format of place! "
                                                                                "Right: with a capital letter "
                                                                                "or number",
                                                                  QtWidgets.QMessageBox.Ok)

            elif check.check_Price(str(self.Conf_Price.text())) == False:
                if self.Conf_Price.text() == "":
                     buttonReply = QtWidgets.QMessageBox.warning(self, 'Error', "Price field is empty!",
                                                                  QtWidgets.QMessageBox.Ok)
                else:
                     buttonReply = QtWidgets.QMessageBox.warning(self, 'Error', "Wrong format of price! "
                                                                                "Example:  1.00",
                                                                  QtWidgets.QMessageBox.Ok)

            elif check.check_Place_Quantity(str(self.Conf_Place_Quantity.text())) == False:
                if self.Conf_Place_Quantity.text() == "":
                     buttonReply = QtWidgets.QMessageBox.warning(self, 'Error', "Quantity field is empty!",
                                                                  QtWidgets.QMessageBox.Ok)
                else:
                     buttonReply = QtWidgets.QMessageBox.warning(self, 'Error', "Wrong format of quantity! ",
                                                                  QtWidgets.QMessageBox.Ok)

            else:
                cursor.execute('''SET TRANSACTION ISOLATION LEVEL READ COMMITTED''')
                cursor.execute(''' SELECT PLACE
                                   FROM CONFERENCE_ACTION
                                   WHERE TO_CHAR(DATETIME, 'YYYY-MM-DD HH24:MI')=:datetime AND RTRIM(PLACE)=:place''',
                               datetime = self.Conf_DateTime.text(), place = self.Conf_Place.text())

                result = cursor.fetchall()
                connection.commit()
                if len(result) != 0:
                     buttonReply = QtWidgets.QMessageBox.warning(self, 'Error', "The conference in this place and date"
                                                                                "is already exist! ",
                                                                  QtWidgets.QMessageBox.Ok)
                else:
                    cursor.execute('''SET TRANSACTION ISOLATION LEVEL SERIALIZABLE''')
                    Insert_Values = '''INSERT INTO CONFERENCE_ACTION(TITLE, THEME, DATETIME, PLACE, PRICE, QUANTITY)
                                    VALUES (:title,:theme, TO_DATE(:datetime, 'yyyy.mm.dd:hh24:mi'),
                                    :place, :price, :quantity)
                                  '''
                    cursor.execute(Insert_Values,title = self.Conf_Title.text(),
                                        theme = self.Conf_Theme.text(), datetime = self.Conf_DateTime.text(),
                                        place = self.Conf_Place.text(), price = float(self.Conf_Price.text()),
                                        quantity = int(self.Conf_Place_Quantity.text()))
                    connection.commit()

                    self.Conf_Title.clear()
                    self.Conf_Theme.clear()
                    self.Conf_Price.clear()
                    self.Conf_DateTime.clear()
                    self.Conf_Place.clear()
                    self.Conf_Place_Quantity.clear()
                    self.close()

        elif sender.text() == "Close":
            self.Conf_Title.clear()
            self.Conf_Theme.clear()
            self.Conf_Price.clear()
            self.Conf_DateTime.clear()
            self.Conf_Place.clear()
            self.Conf_Place_Quantity.clear()
            self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_CreateConference()
    ui.show()
    sys.exit(app.exec_())