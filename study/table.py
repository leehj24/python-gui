import os, sys, json
from collections import deque
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from functools import partial


class view(QWidget):

    def __init__(self, data):
        super(view, self).__init__()
        self.tree = QTreeView(self)
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.openMenu)
        layout = QVBoxLayout(self)
        layout.addWidget(self.tree)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Name', 'Height', 'Weight', 'unique_id', 'parent_id'])
        self.tree.header().setDefaultSectionSize(180)
        self.tree.setModel(self.model)
        self.importData(data)
        self.tree.expandAll()


    def iterItems(self, root):
        if root is not None:
            stack = [root]
            while stack:
                parent = stack.pop(0)
                for row in range(parent.rowCount()):
                    for column in range(parent.columnCount()):
                        child = parent.child(row, column)
                        yield child
                        if child.hasChildren():
                            stack.append(child)

    def transverse_tree(self):

        item_list = []

        root = self.model.invisibleRootItem()
        for item in self.iterItems(root):
            item_list.append(item.text())

       
        tree_list = []

        for idx in range(0, len(item_list), 5):

            dic = {}
            dic['unique_id'] = int(item_list[idx+3])
            dic['parent_id'] = int(item_list[idx+4])
            dic['short_name'] = item_list[idx]
            dic['height'] = item_list[idx+1]
            dic['weight'] = item_list[idx+2]
            tree_list.append(dic)

        return tree_list


    def importData(self, data, root=None):
        self.model.setRowCount(0)
        if root is None:
            root = self.model.invisibleRootItem()
        seen = {}   # List of  QStandardItem
        values = deque(data)
        while values:
            value = values.popleft()
            if value['unique_id'] == 1:
                parent = root
            else:
                pid = value['parent_id']
                if pid not in seen:
                    values.append(value)
                    continue
                parent = seen[pid]
            unique_id = value['unique_id']
            parent.appendRow([
                QStandardItem(value['short_name']),
                QStandardItem(value['height']),
                QStandardItem(value['weight']),
                QStandardItem(str(value['unique_id'])),
                QStandardItem(str(value['parent_id']))
            ])
            seen[unique_id] = parent.child(parent.rowCount() - 1)


    def openMenu(self, position):
            indexes = self.sender().selectedIndexes()
            mdlIdx = self.tree.indexAt(position)
            if not mdlIdx.isValid():
                return
            item = self.model.itemFromIndex(mdlIdx)
           
            if len(indexes) > 0:
                level = 0
                index = indexes[0]
                while index.parent().isValid():
                    index = index.parent()
                    level += 1
            else:
                level = 0

            right_click_menu = QMenu()

            if level < 2:
                act_add = right_click_menu.addAction(self.tr("자식 아이템 추가"))
                act_add.triggered.connect(partial(self.TreeItem_Add, level, mdlIdx))

            if level == 2:
                insert_up = right_click_menu.addAction(self.tr("바로 위에 아이템 추가"))
                insert_up.triggered.connect(partial(self.TreeItem_InsertUp, level, mdlIdx))

                insert_down = right_click_menu.addAction(self.tr("바로 아래에 아이템 추가"))
                insert_down.triggered.connect(partial(self.TreeItem_InsertDown, level, mdlIdx))

            if item.parent() != None:               
                act_del = right_click_menu.addAction(self.tr("아이템 삭제"))
                act_del.triggered.connect(partial(self.TreeItem_Delete, item))
           
            right_click_menu.exec_(self.sender().viewport().mapToGlobal(position))


    def TreeItem_Add(self, level, mdlIdx):
        global max_uniaue_id

        current_row = self.model.itemFromIndex(mdlIdx).row()

        if type(self.model.itemFromIndex(mdlIdx).parent()) == type(None):
            root = self.model.invisibleRootItem()

            parent_id = int(root.child(current_row, 3).text())

        else:
            parent_id = int(self.model.itemFromIndex(mdlIdx).parent().child(current_row, 3).text())

        max_uniaue_id = max_uniaue_id + 1
        unique_id = max_uniaue_id

        short_name = QStandardItem('xx')
        height = QStandardItem(' ')
        weight = QStandardItem(' ')
        unique_id = QStandardItem(str(unique_id))
        parent_id = QStandardItem(str(parent_id))

        self.model.itemFromIndex(mdlIdx).appendRow([short_name, height, weight, unique_id, parent_id ])

        self.tree.expandAll()


    def TreeItem_InsertUp(self, level, mdlIdx):
        global max_uniaue_id

        current_row = self.model.itemFromIndex(mdlIdx).row()
       
        first_child_unique_id = int(self.model.itemFromIndex(mdlIdx).parent().child(0, 3).text())

        parent_id = -1
        for i in range(self.model.itemFromIndex(mdlIdx).parent().parent().rowCount()):

            unique_id = int(self.model.itemFromIndex(mdlIdx).parent().parent().child(i, 0).child(0, 3).text())

            if first_child_unique_id == unique_id:
                parent_id = self.model.itemFromIndex(mdlIdx).parent().parent().child(i, 3).text()
                break

       
        max_uniaue_id = max_uniaue_id + 1
        unique_id = max_uniaue_id

        short_name = QStandardItem('xx')
        height = QStandardItem(' ')
        weight = QStandardItem(' ')
        unique_id = QStandardItem(str(unique_id))
        parent_id = QStandardItem(str(parent_id))


        level = level - 1

        self.model.itemFromIndex(mdlIdx).parent().insertRow(current_row, [short_name, height, weight, unique_id, parent_id ])

        self.tree.expandToDepth(1 + level)


    def TreeItem_InsertDown(self, level, mdlIdx):
        global max_uniaue_id

        current_row = self.model.itemFromIndex(mdlIdx).row()
       
        first_child_unique_id = int(self.model.itemFromIndex(mdlIdx).parent().child(0, 3).text())

        parent_id = -1
        for i in range(self.model.itemFromIndex(mdlIdx).parent().parent().rowCount()):

            unique_id = int(self.model.itemFromIndex(mdlIdx).parent().parent().child(i, 0).child(0, 3).text())

            if first_child_unique_id == unique_id:
                parent_id = self.model.itemFromIndex(mdlIdx).parent().parent().child(i, 3).text()
                break

       
        max_uniaue_id = max_uniaue_id + 1
        unique_id = max_uniaue_id

        short_name = QStandardItem('xx')
        height = QStandardItem(' ')
        weight = QStandardItem(' ')
        unique_id = QStandardItem(str(unique_id))
        parent_id = QStandardItem(str(parent_id))


        level = level - 1

        self.model.itemFromIndex(mdlIdx).parent().insertRow(current_row+1, [short_name, height, weight, unique_id, parent_id ])

        self.tree.expandToDepth(1 + level)


    def TreeItem_Delete(self, item):
        item.parent().removeRow(item.row())


    def closeEvent(self, event):

            close = QMessageBox.question(self,
                                        "QUIT",
                                        "Sure?",
                                        QMessageBox.Yes | QMessageBox.No)
            if close == QMessageBox.Yes:

                # 변경 사항 저장
                tree_list = self.transverse_tree()
               

                # JSON 출력
                for row in tree_list:
                    print(row)

                with open('test2.json', 'w') as outfile:
                    json.dump(tree_list, outfile, indent=4)

                event.accept()
                   
            else:
                event.ignore()

if __name__ == '__main__':

    filename = 'test2.json'


    if not os.path.exists(filename):
        json_data = [
            {'unique_id': 1, 'parent_id': 0, 'short_name': 'root', 'height': ' ', 'weight': ' '},
            {'unique_id': 2, 'parent_id': 1, 'short_name': 'Group 1', 'height': ' ', 'weight': ' '},
            {'unique_id': 3, 'parent_id': 2, 'short_name': 'Lucy', 'height': '162', 'weight': '50'},
            {'unique_id': 4, 'parent_id': 2, 'short_name': 'Joe', 'height': '175', 'weight': '65'},
            {'unique_id': 5, 'parent_id': 1, 'short_name': 'Group 2', 'height': ' ', 'weight': ' '},
            {'unique_id': 6, 'parent_id': 5, 'short_name': 'Lily', 'height': '170', 'weight': '55'},
            {'unique_id': 7, 'parent_id': 5, 'short_name': 'Tom', 'height': '180', 'weight': '75'},
            {'unique_id': 8, 'parent_id': 1, 'short_name': 'Group 3', 'height': ' ', 'weight': ' '},
            {'unique_id': 9, 'parent_id': 8, 'short_name': 'Jack', 'height': '178', 'weight': '80'},
            {'unique_id': 10, 'parent_id': 8, 'short_name': 'Tim', 'height': '172', 'weight': '60'}
        ]
    else:
        with open(filename, "r") as json_file:
            json_data = json.load(json_file)

    max_uniaue_id = -1
    for i in json_data:
        if max_uniaue_id < i['unique_id']:
            max_uniaue_id = i['unique_id']
   

    app = QApplication(sys.argv)
    view = view(json_data)
    view.setGeometry(300, 100, 600, 300)
    view.setWindowTitle('QTreeview Example')
    view.show()
    sys.exit(app.exec_())