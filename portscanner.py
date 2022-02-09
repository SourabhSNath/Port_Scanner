from PyQt6 import QtCore, QtGui, QtWidgets
import nmap


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.ip_box = QtWidgets.QFormLayout()
        self.ip_box.setObjectName("ip_box")
        self.ip_label = QtWidgets.QLabel(self.centralwidget)
        self.ip_label.setObjectName("ip_label")
        self.ip_box.setWidget(
            0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.ip_label
        )
        self.ip_input = QtWidgets.QLineEdit(self.centralwidget)
        self.ip_input.setText("")
        self.ip_input.setObjectName("ip_input")
        self.ip_box.setWidget(
            0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.ip_input
        )
        self.gridLayout.addLayout(self.ip_box, 0, 0, 1, 1)

        self.ports_box = QtWidgets.QFormLayout()
        self.ports_box.setObjectName("ports_box")
        self.ports_input = QtWidgets.QLineEdit(self.centralwidget)
        self.ports_input.setToolTip("")
        self.ports_input.setStatusTip("")
        self.ports_input.setWhatsThis("")
        self.ports_input.setObjectName("ports_input")
        self.ports_box.setWidget(
            0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.ports_input
        )
        self.ports_label = QtWidgets.QLabel(self.centralwidget)
        self.ports_label.setObjectName("ports_label")
        self.ports_box.setWidget(
            0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.ports_label
        )
        self.gridLayout.addLayout(self.ports_box, 0, 1, 1, 2)

        self.scan_button = QtWidgets.QPushButton(self.centralwidget)
        self.scan_button.setObjectName("scan_button")
        self.gridLayout.addWidget(self.scan_button, 0, 3, 1, 1)

        self.results_label = QtWidgets.QLabel(self.centralwidget)
        self.results_label.setObjectName("results_label")
        self.scan_result_view = QtWidgets.QTextEdit(self.centralwidget)
        self.scan_result_view.setObjectName("scan_result_view")
        self.gridLayout.addWidget(self.results_label, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.scan_result_view, 2, 0, 1, 2)

        self.ports_table = QtWidgets.QTableWidget(self.centralwidget)
        self.ports_table.setObjectName("ports_table")
        self.ports_table.setColumnCount(3)
        self.ports_table.setHorizontalHeaderLabels(["Host", "Port", "State"])
        hori_header = self.ports_table.horizontalHeader()
        hori_header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )
        hori_header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        hori_header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.ports_table.setRowCount(0)
        self.ports_table.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.ports_table, 2, 2, 1, 2)

        self.gridLayout.setColumnStretch(0, 3)
        self.gridLayout.setColumnStretch(1, 4)
        self.gridLayout.setColumnStretch(2, 2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.scan_button.clicked.connect(self.scanPorts)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.ip_label.setText(_translate("MainWindow", "IP Address"))
        self.ports_label.setText(_translate("MainWindow", "Ports"))
        self.scan_button.setText(_translate("MainWindow", "Scan"))
        self.results_label.setText(_translate("MainWindow", "Results"))

    def scanPorts(self):
        self.results_label.setText("Results: (Scanning, Please wait..)")
        self.scan_result_view.setText("")
        ip_address = self.ip_input.text()
        ports = self.ports_input.text()
        self.ports_table.setRowCount(0)

        print(f"Scan starting, IP = {ip_address}, ports = {ports}")

        if ip_address and ports:
            scanner = nmap.PortScanner()
            try:
                scanner.scan(ip_address, ports)
            except Exception as e:
                self.scan_result_view.setText(f"Please check your inputs, {e}")

            for host in scanner.all_hosts():
                host_address = host
                host_name = scanner[host].hostname()
                host_state = scanner[host].state()

                print(host_address, host_name, host_state)

                self.scan_result_view.append(
                    f"Host: {host_address} ({host_name if host_name else 'Unknown'})"
                )
                self.scan_result_view.append(f"State: {host_state}")

                for proto in scanner[host].all_protocols():
                    protocol = proto
                    print(f"Protocol = {protocol}")
                    ports = scanner[host][protocol].keys()
                    sorted(ports)

                    for p in ports:
                        port_number = p
                        port_state = scanner[host][protocol][p]["state"]

                        print(port_number, port_state)

                        current_row_pos = self.ports_table.rowCount()
                        self.ports_table.insertRow(current_row_pos)
                        self.ports_table.setItem(
                            current_row_pos, 0, QtWidgets.QTableWidgetItem(host_address)
                        )
                        self.ports_table.setItem(
                            current_row_pos,
                            1,
                            QtWidgets.QTableWidgetItem(f"{port_number}/{protocol}"),
                        )
                        self.ports_table.setItem(
                            current_row_pos,
                            2,
                            QtWidgets.QTableWidgetItem(port_state),
                        )

                if host_address:
                    self.results_label.setText("Results:")
        else:
            self.results_label.setText("Results")
            self.scan_result_view.setText("Please check your inputs")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
