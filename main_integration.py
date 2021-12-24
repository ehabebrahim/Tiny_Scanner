import matplotlib.pyplot as plt
import sys
from PyQt5 import QtWidgets
#from PyQt5.QtWidgets import QApplication, QPushButton, QGridLayout, QLabel, QTextEdit, QWidget
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import *
from Scanner import scanner
from parser import parser
import networkx as nx
import matplotlib
from PyQt5.uic import loadUi
matplotlib.use("TkAgg")

class TINYParserWidget(QMainWindow):
    def __init__(self):

        super(TINYParserWidget, self).__init__()
        loadUi("/media/ehab/Data 2/faculty of engineering ain shams/4th CSE/System Software/project/parser.ui", self)
        pixmap = QPixmap("/media/ehab/Data 2/faculty of engineering ain shams/4th CSE/System Software/project/Logo.png")
        self.label.setPixmap(pixmap)
        #self.label.resize(pixmap.width(), pixmap.height())
        self.textEdit.setTextColor(QColor(255, 0, 0))
        self.pushButton_2.clicked.connect(self.submitted)
        self.pushButton.clicked.connect(self.scanner_phase1)
        self.add_initial_code()
        #self.textEdit.setPlainText()
        self.show()
        #super().__init__()
        #self.initUI()

    def initUI(self):

        print("fj")

        """
        lbl = QLabel('Enter TINY Language Code', self)
        self.textEdit = QTextEdit()
        self.add_initial_code()
        submit_button = QPushButton('Parse')
        submit_button.clicked.connect(self.submitted)
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(lbl, 1, 0)
        grid.addWidget(self.textEdit, 1, 1)
        grid.addWidget(submit_button, 2, 1)
        self.setLayout(grid)
        self.setGeometry(40, 40, 500, 900)
        self.setWindowTitle('TINY Parser')
        self.show()
        """

    def add_initial_code(self):
        self.textEdit.append("read x;")
        self.textEdit.append("if 0<x then")
        self.textEdit.append("    fact:=1;")
        self.textEdit.append("    repeat")
        self.textEdit.append("        fact:=fact*x;")
        self.textEdit.append("        x:=x-1")
        self.textEdit.append("    until x=0;")
        self.textEdit.append("    write fact")
        self.textEdit.append("end")

    def pygraphviz_layout_with_rank(self, G, prog="dot", root=None, sameRank=[], args=""):
        try:
            import pygraphviz
        except ImportError:
            raise ImportError('requires pygraphviz ',
                              'http://networkx.lanl.gov/pygraphviz ',
                              '(not available for Python3)')
        if root is not None:
            args += "-Groot=%s" % root
        A = nx.nx_agraph.to_agraph(G)
        for sameNodeHeight in sameRank:
            if type(sameNodeHeight) == str:
                print("node \"%s\" has no peers in its rank group" %
                      sameNodeHeight)
            A.add_subgraph(sameNodeHeight, rank="same")
        A.layout(prog=prog, args=args)
        node_pos = {}
        for n in G:
            node = pygraphviz.Node(A, n)
            try:
                xx, yy = node.attr["pos"].split(',')
                node_pos[n] = (float(xx), float(yy))
            except:
                print("no position for node", n)
                node_pos[n] = (0.0, 0.0)
        return node_pos

    def draw(self, same_rank_nodes):
        graph = self.G
        # pos = nx.get_node_attributes(graph, 'pos')
        pos = self.pygraphviz_layout_with_rank(
            graph, prog='dot', sameRank=same_rank_nodes)
        # pos = nx.nx_pydot.graphviz_layout(graph, prog='dot')
        labels = dict((n, d['value']) for n, d in graph.nodes(data=True))
        f = plt.figure(1, figsize=(13, 8.65))
        for shape in ['s', 'o']:
            nx.draw_networkx_nodes(graph, pos, node_color='g', node_size=2500, node_shape=shape, labels=labels, nodelist=[
                sNode[0] for sNode in filter(lambda x: x[1]["shape"] == shape, graph.nodes(data=True))])
        nx.draw_networkx_edges(graph, pos, arrows=False)
        nx.draw_networkx_labels(graph, pos, labels=labels, font_size=8)
        f.canvas.manager.window.wm_geometry("+%d+%d" % (600, 0))
        plt.show()

    def submitted(self):
        
        scanned_code = scanner(self.textEdit.toPlainText())
        
        
        scanned_code.scan()
        parse_code = parser()
        parse_code.set_tokens_list_and_code_list(
            scanned_code.token_list, scanned_code.code_list)
        parse_code.run()
        nodes_list = parse_code.nodes_table
        edges_list = parse_code.edges_table
        self.G = nx.DiGraph()
        for node_number, node in nodes_list.items():
            self.G.add_node(
                node_number, value=node[0] + '\n' + node[1], shape=node[2])
        self.G.add_edges_from(edges_list)
        parse_code.clear_tables()
        self.draw(parse_code.same_rank_nodes)

    def scanner_phase1(self):
        scanned_code = scanner(self.textEdit.toPlainText())
        scanned_code.scan()
        scanned_out = scanned_code.scan_out
        widget2.addWidget(scann_pahase1(scanned_out))
        widget2.setCurrentIndex(widget.currentIndex() + 1)
        widget2.show()

        

class scann_pahase1(QMainWindow):
    def __init__(self, scanned_out):
        super(scann_pahase1, self).__init__()
        loadUi("/media/ehab/Data 2/faculty of engineering ain shams/4th CSE/System Software/project/Scanner output.ui", self)
        pixmap = QPixmap("/media/ehab/Data 2/faculty of engineering ain shams/4th CSE/System Software/project/new.png")
        self.label.setPixmap(pixmap)
        #self.label.resize(pixmap.width(), pixmap.height())
        self.textEdit.setTextColor(QColor(255, 0, 0))
        for i in scanned_out:
            self.textEdit.append(i)



app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
widget2 = QtWidgets.QStackedWidget()
widget.addWidget(TINYParserWidget())
widget.setFixedWidth(1050)
widget.setFixedHeight(1000)
widget2.setFixedWidth(1050)
widget2.setFixedHeight(1000)
widget.show()
app.exec_()

