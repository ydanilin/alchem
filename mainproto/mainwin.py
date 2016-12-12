#!/usr/bin/env python
import sys
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QStyle, QProxyStyle, QStyleOption, QWidget, QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QFontMetrics
#import platform
#platform.platform()
#>>> platform.system()
#'Windows'
#platform.release()
#'XP'
#platform.version()
#'5.1.2600'

# need to control paint visual widgets - subclass widget and catch PaintEvent

class MoyStil(QProxyStyle):
    def __init__(self):
        super(MoyStil, self).__init__()
        self.calledIDs = []

    def pixelMetric(self, metric, option=None, widget=None):
        size = super(MoyStil, self).pixelMetric(metric, option, widget)
        if metric == 46:  # HeaderMargin surrounding text in TableWidget header
            size = 5      # this value affects TableWidget column height if column height is small
        if metric == 92:  # default TableWidget column width
            size = 500
        if metric == 93:  # default TableWidget column height
            size = 50
        if not(metric in self.calledIDs) and widget:
            # print('pixel metric No {0} = {1}, called by {2}. Option: {3}').format(
            #     metric, size, widget, option)
            self.calledIDs.append(metric)
        return size

    def drawPrimitive(self, element, option, painter, widget):
        return super(MoyStil, self).drawPrimitive(element, option, painter, widget)

class MyApp(QApplication):
    def __init__(self, cmdLine):
        super(MyApp, self).__init__(cmdLine)
        self.upperTape = self.style().pixelMetric(QStyle.PM_TitleBarHeight)
        self.edge = self.style().pixelMetric(QStyle.PM_MdiSubWindowFrameWidth)
        self.myRectangle = self.getMarginalWindowSize(0.025)
        self.setStyle(MoyStil())

    def getMarginalWindowSize(self, marginRatio):
        rectangle = self.desktop().availableGeometry()
        margin = int(rectangle.height() * marginRatio)
        rectangle.adjust(margin + self.edge, self.upperTape,
                         -(margin + self.edge), -self.edge)
        return rectangle

class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('Basic Drawing')
        self.app = QCoreApplication.instance()
        self.setGeometry(self.app.myRectangle)
        st = self.app.style()
        self.params = (
            (str(QStyle.PM_ButtonMargin), 'ButtonMargin', st.pixelMetric(QStyle.PM_ButtonMargin)),
            (str(QStyle.PM_DockWidgetTitleBarButtonMargin), 'DockWidgetTitleBarButtonMargin', st.pixelMetric(QStyle.PM_DockWidgetTitleBarButtonMargin)),
            (str(QStyle.PM_ButtonDefaultIndicator), 'ButtonDefaultIndicator', st.pixelMetric(QStyle.PM_ButtonDefaultIndicator)),
            (str(QStyle.PM_MenuButtonIndicator), 'MenuButtonIndicator', st.pixelMetric(QStyle.PM_MenuButtonIndicator)),
            (str(QStyle.PM_ButtonShiftHorizontal), 'ButtonShiftHorizontal', st.pixelMetric(QStyle.PM_ButtonShiftHorizontal)),
            (str(QStyle.PM_ButtonShiftVertical), 'ButtonShiftVertical', st.pixelMetric(QStyle.PM_ButtonShiftVertical)),
            (str(QStyle.PM_DefaultFrameWidth), 'DefaultFrameWidth', st.pixelMetric(QStyle.PM_DefaultFrameWidth)),
            (str(QStyle.PM_SpinBoxFrameWidth), 'SpinBoxFrameWidth', st.pixelMetric(QStyle.PM_SpinBoxFrameWidth)),
            (str(QStyle.PM_ComboBoxFrameWidth), 'ComboBoxFrameWidth', st.pixelMetric(QStyle.PM_ComboBoxFrameWidth)),
            (str(QStyle.PM_MdiSubWindowFrameWidth), 'MdiSubWindowFrameWidth', st.pixelMetric(QStyle.PM_MdiSubWindowFrameWidth)),
            (str(QStyle.PM_MdiSubWindowMinimizedWidth), 'MdiSubWindowMinimizedWidth', st.pixelMetric(QStyle.PM_MdiSubWindowMinimizedWidth)),
            (str(QStyle.PM_LayoutLeftMargin), 'LayoutLeftMargin', st.pixelMetric(QStyle.PM_LayoutLeftMargin)),
            (str(QStyle.PM_LayoutTopMargin), 'LayoutTopMargin', st.pixelMetric(QStyle.PM_LayoutTopMargin)),
            (str(QStyle.PM_LayoutRightMargin), 'LayoutRightMargin', st.pixelMetric(QStyle.PM_LayoutRightMargin)),
            (str(QStyle.PM_LayoutBottomMargin), 'LayoutBottomMargin', st.pixelMetric(QStyle.PM_LayoutBottomMargin)),
            (str(QStyle.PM_LayoutHorizontalSpacing), 'LayoutHorizontalSpacing', st.pixelMetric(QStyle.PM_LayoutHorizontalSpacing)),
            (str(QStyle.PM_LayoutVerticalSpacing), 'LayoutVerticalSpacing', st.pixelMetric(QStyle.PM_LayoutVerticalSpacing)),
            (str(QStyle.PM_MaximumDragDistance), 'MaximumDragDistance', st.pixelMetric(QStyle.PM_MaximumDragDistance)),
            (str(QStyle.PM_ScrollBarExtent), 'ScrollBarExtent', st.pixelMetric(QStyle.PM_ScrollBarExtent)),
            (str(QStyle.PM_ScrollBarSliderMin), 'ScrollBarSliderMin', st.pixelMetric(QStyle.PM_ScrollBarSliderMin)),
            (str(QStyle.PM_SliderThickness), 'SliderThickness', st.pixelMetric(QStyle.PM_SliderThickness)),
            (str(QStyle.PM_SliderControlThickness), 'SliderControlThickness', st.pixelMetric(QStyle.PM_SliderControlThickness)),
            (str(QStyle.PM_SliderLength), 'SliderLength', st.pixelMetric(QStyle.PM_SliderLength)),
            (str(QStyle.PM_SliderTickmarkOffset), 'SliderTickmarkOffset', st.pixelMetric(QStyle.PM_SliderTickmarkOffset)),
            (str(QStyle.PM_SliderSpaceAvailable), 'SliderSpaceAvailable', st.pixelMetric(QStyle.PM_SliderSpaceAvailable)),
            (str(QStyle.PM_DockWidgetSeparatorExtent), 'DockWidgetSeparatorExtent', st.pixelMetric(QStyle.PM_DockWidgetSeparatorExtent)),
            (str(QStyle.PM_DockWidgetHandleExtent), 'DockWidgetHandleExtent', st.pixelMetric(QStyle.PM_DockWidgetHandleExtent)),
            (str(QStyle.PM_DockWidgetFrameWidth), 'DockWidgetFrameWidth', st.pixelMetric(QStyle.PM_DockWidgetFrameWidth)),
            (str(QStyle.PM_DockWidgetTitleMargin), 'DockWidgetTitleMargin', st.pixelMetric(QStyle.PM_DockWidgetTitleMargin)),
            (str(QStyle.PM_MenuBarPanelWidth), 'MenuBarPanelWidth', st.pixelMetric(QStyle.PM_MenuBarPanelWidth)),
            (str(QStyle.PM_MenuBarItemSpacing), 'MenuBarItemSpacing', st.pixelMetric(QStyle.PM_MenuBarItemSpacing)),
            (str(QStyle.PM_MenuBarHMargin), 'MenuBarHMargin', st.pixelMetric(QStyle.PM_MenuBarHMargin)),
            (str(QStyle.PM_MenuBarVMargin), 'MenuBarVMargin', st.pixelMetric(QStyle.PM_MenuBarVMargin)),
            (str(QStyle.PM_ToolBarFrameWidth), 'ToolBarFrameWidth', st.pixelMetric(QStyle.PM_ToolBarFrameWidth)),
            (str(QStyle.PM_ToolBarHandleExtent), 'ToolBarHandleExtent', st.pixelMetric(QStyle.PM_ToolBarHandleExtent)),
            (str(QStyle.PM_ToolBarItemMargin), 'ToolBarItemMargin', st.pixelMetric(QStyle.PM_ToolBarItemMargin)),
            (str(QStyle.PM_ToolBarItemSpacing), 'ToolBarItemSpacing', st.pixelMetric(QStyle.PM_ToolBarItemSpacing)),
            (str(QStyle.PM_ToolBarSeparatorExtent), 'ToolBarSeparatorExtent', st.pixelMetric(QStyle.PM_ToolBarSeparatorExtent)),
            (str(QStyle.PM_ToolBarExtensionExtent), 'ToolBarExtensionExtent', st.pixelMetric(QStyle.PM_ToolBarExtensionExtent)),
            (str(QStyle.PM_TabBarTabOverlap), 'TabBarTabOverlap', st.pixelMetric(QStyle.PM_TabBarTabOverlap)),
            (str(QStyle.PM_TabBarTabHSpace), 'TabBarTabHSpace', st.pixelMetric(QStyle.PM_TabBarTabHSpace)),
            (str(QStyle.PM_TabBarTabVSpace), 'TabBarTabVSpace', st.pixelMetric(QStyle.PM_TabBarTabVSpace)),
            (str(QStyle.PM_TabBarBaseHeight), 'TabBarBaseHeight', st.pixelMetric(QStyle.PM_TabBarBaseHeight)),
            (str(QStyle.PM_TabBarBaseOverlap), 'TabBarBaseOverlap', st.pixelMetric(QStyle.PM_TabBarBaseOverlap)),
            (str(QStyle.PM_TabBarScrollButtonWidth), 'TabBarScrollButtonWidth', st.pixelMetric(QStyle.PM_TabBarScrollButtonWidth)),
            (str(QStyle.PM_TabBarTabShiftHorizontal), 'TabBarTabShiftHorizontal', st.pixelMetric(QStyle.PM_TabBarTabShiftHorizontal)),
            (str(QStyle.PM_TabBarTabShiftVertical), 'TabBarTabShiftVertical', st.pixelMetric(QStyle.PM_TabBarTabShiftVertical)),
            (str(QStyle.PM_ProgressBarChunkWidth), 'ProgressBarChunkWidth', st.pixelMetric(QStyle.PM_ProgressBarChunkWidth)),
            (str(QStyle.PM_SplitterWidth), 'SplitterWidth', st.pixelMetric(QStyle.PM_SplitterWidth)),
            (str(QStyle.PM_TitleBarHeight), 'TitleBarHeight', st.pixelMetric(QStyle.PM_TitleBarHeight)),
            (str(QStyle.PM_IndicatorWidth), 'IndicatorWidth', st.pixelMetric(QStyle.PM_IndicatorWidth)),
            (str(QStyle.PM_IndicatorHeight), 'IndicatorHeight', st.pixelMetric(QStyle.PM_IndicatorHeight)),
            (str(QStyle.PM_ExclusiveIndicatorWidth), 'ExclusiveIndicatorWidth', st.pixelMetric(QStyle.PM_ExclusiveIndicatorWidth)),
            (str(QStyle.PM_ExclusiveIndicatorHeight), 'ExclusiveIndicatorHeight', st.pixelMetric(QStyle.PM_ExclusiveIndicatorHeight)),
            (str(QStyle.PM_MenuPanelWidth), 'MenuPanelWidth', st.pixelMetric(QStyle.PM_MenuPanelWidth)),
            (str(QStyle.PM_MenuHMargin), 'MenuHMargin', st.pixelMetric(QStyle.PM_MenuHMargin)),
            (str(QStyle.PM_MenuVMargin), 'MenuVMargin', st.pixelMetric(QStyle.PM_MenuVMargin)),
            (str(QStyle.PM_MenuScrollerHeight), 'MenuScrollerHeight', st.pixelMetric(QStyle.PM_MenuScrollerHeight)),
            (str(QStyle.PM_MenuTearoffHeight), 'MenuTearoffHeight', st.pixelMetric(QStyle.PM_MenuTearoffHeight)),
            (str(QStyle.PM_MenuDesktopFrameWidth), 'MenuDesktopFrameWidth', st.pixelMetric(QStyle.PM_MenuDesktopFrameWidth)),
            (str(QStyle.PM_HeaderMarkSize), 'HeaderMarkSize', st.pixelMetric(QStyle.PM_HeaderMarkSize)),
            (str(QStyle.PM_HeaderGripMargin), 'HeaderGripMargin', st.pixelMetric(QStyle.PM_HeaderGripMargin)),
            (str(QStyle.PM_HeaderMargin), 'HeaderMargin', st.pixelMetric(QStyle.PM_HeaderMargin)),
            (str(QStyle.PM_SpinBoxSliderHeight), 'SpinBoxSliderHeight', st.pixelMetric(QStyle.PM_SpinBoxSliderHeight)),
            (str(QStyle.PM_ToolBarIconSize), 'ToolBarIconSize', st.pixelMetric(QStyle.PM_ToolBarIconSize)),
            (str(QStyle.PM_SmallIconSize), 'SmallIconSize', st.pixelMetric(QStyle.PM_SmallIconSize)),
            (str(QStyle.PM_LargeIconSize), 'LargeIconSize', st.pixelMetric(QStyle.PM_LargeIconSize)),
            (str(QStyle.PM_FocusFrameHMargin), 'FocusFrameHMargin', st.pixelMetric(QStyle.PM_FocusFrameHMargin)),
            (str(QStyle.PM_FocusFrameVMargin), 'FocusFrameVMargin', st.pixelMetric(QStyle.PM_FocusFrameVMargin)),
            (str(QStyle.PM_IconViewIconSize), 'IconViewIconSize', st.pixelMetric(QStyle.PM_IconViewIconSize)),
            (str(QStyle.PM_ListViewIconSize), 'ListViewIconSize', st.pixelMetric(QStyle.PM_ListViewIconSize)),
            (str(QStyle.PM_ToolTipLabelFrameWidth), 'ToolTipLabelFrameWidth', st.pixelMetric(QStyle.PM_ToolTipLabelFrameWidth)),
            (str(QStyle.PM_CheckBoxLabelSpacing), 'CheckBoxLabelSpacing', st.pixelMetric(QStyle.PM_CheckBoxLabelSpacing)),
            (str(QStyle.PM_RadioButtonLabelSpacing), 'RadioButtonLabelSpacing', st.pixelMetric(QStyle.PM_RadioButtonLabelSpacing)),
            (str(QStyle.PM_TabBarIconSize), 'TabBarIconSize', st.pixelMetric(QStyle.PM_TabBarIconSize)),
            (str(QStyle.PM_SizeGripSize), 'SizeGripSize', st.pixelMetric(QStyle.PM_SizeGripSize)),
            (str(QStyle.PM_MessageBoxIconSize), 'MessageBoxIconSize', st.pixelMetric(QStyle.PM_MessageBoxIconSize)),
            (str(QStyle.PM_ButtonIconSize), 'ButtonIconSize', st.pixelMetric(QStyle.PM_ButtonIconSize)),
            (str(QStyle.PM_TextCursorWidth), 'TextCursorWidth', st.pixelMetric(QStyle.PM_TextCursorWidth)),
            (str(QStyle.PM_TabBar_ScrollButtonOverlap), 'TabBar_ScrollButtonOverlap', st.pixelMetric(QStyle.PM_TabBar_ScrollButtonOverlap)),
            (str(QStyle.PM_TabCloseIndicatorWidth), 'TabCloseIndicatorWidth', st.pixelMetric(QStyle.PM_TabCloseIndicatorWidth)),
            (str(QStyle.PM_TabCloseIndicatorHeight), 'TabCloseIndicatorHeight', st.pixelMetric(QStyle.PM_TabCloseIndicatorHeight)),
            (str(QStyle.PM_ScrollView_ScrollBarSpacing), 'ScrollView_ScrollBarSpacing', st.pixelMetric(QStyle.PM_ScrollView_ScrollBarSpacing)),
            (str(QStyle.PM_ScrollView_ScrollBarOverlap), 'ScrollView_ScrollBarOverlap', st.pixelMetric(QStyle.PM_ScrollView_ScrollBarOverlap)),
            (str(QStyle.PM_SubMenuOverlap), 'SubMenuOverlap', st.pixelMetric(QStyle.PM_SubMenuOverlap)),
            (str(QStyle.PM_TreeViewIndentation), 'TreeViewIndentation', st.pixelMetric(QStyle.PM_TreeViewIndentation)),
            (str(QStyle.PM_HeaderDefaultSectionSizeHorizontal), 'HeaderDefaultSectionSizeHorizontal', st.pixelMetric(QStyle.PM_HeaderDefaultSectionSizeHorizontal)),
            (str(QStyle.PM_HeaderDefaultSectionSizeVertical), 'HeaderDefaultSectionSizeVertical', st.pixelMetric(QStyle.PM_HeaderDefaultSectionSizeVertical)),
            (str(QStyle.PM_CustomBase), 'CustomBase', st.pixelMetric(QStyle.PM_CustomBase))
        )

        self.tw = QTableWidget(len(self.params), 3)
        vh = self.tw.verticalHeader()
        print(vh.sectionSize(0))
        # vh.setSectionResizeMode(QHeaderView.Fixed)
        # vh.setDefaultSectionSize(30)
        for i in range(len(self.params)):
            item1 = QTableWidgetItem (self.params[i][0])
            item2 = QTableWidgetItem (str(self.params[i][1]))
            item3 = QTableWidgetItem (str(self.params[i][2]))
            self.tw.setItem(i, 0, item1)
            self.tw.setItem(i, 1, item2)
            self.tw.setItem(i, 2, item3)
        self.setCentralWidget(self.tw)

        #fm = QFontMetrics(self.tw.font())
        fm = QFontMetrics(self.tw.item(1,1).font())
        #fm = self.tw.fontMetrics()
        strin = ''
        length = 0
        for param in self.params:
            l = fm.size(1, self.tr(param[1])).width()
            if l > length:
                length = l
                strin = self.tr(param[1])
        print 'MaxWidth: {0}, for string: {1}'.format(length, strin)
        self.tw.setColumnWidth(1, length)


        appFont = self.app.font()
        cellFont = self.tw.item(1,1).font()
        tableFont = self.tw.font()
        print appFont
        print cellFont
        print tableFont
        print fm
        #print 'TitleBarHeight: {0}'.format(app.upperTape)
        #print 'MdiSubWindowFrameWidth: {0}'.format(app.edge)

app = MyApp(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
