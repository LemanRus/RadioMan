# -*- coding: utf-8 -*-
"""Экраны справочника микросхем"""

import os

from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.uix.divider import MDDivider
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

from data_loader import load_chips_analogs
from misc import MDIconCard, ImageButton, MDShortenLabel

# Кэш для проверки существования файлов изображений
_image_cache = {}


class ChipsScreen(MDScreen):
    pass


class ChipsAnalogsSelectScreen(MDScreen):
    def on_enter(self):
        """Вызывается при входе на экран - динамически создаем карточки"""
        # Проверяем, нужно ли создавать карточки
        list_widget = self.ids.get('chips_analogs_list', None)
        if not list_widget:
            return
        
        # Если карточки уже созданы, не создаем заново
        if hasattr(self, '_cards_created') and self._cards_created:
            return
        
        # Используем Clock для асинхронной загрузки, чтобы не блокировать UI
        from kivy.clock import Clock
        # Загружаем данные сразу, но создаем карточки асинхронно
        self._chips_data = load_chips_analogs()
        self._prepare_series_data()
        # Начинаем создание карточек с небольшой задержкой
        Clock.schedule_once(lambda dt: self._start_creating_cards(), 0.05)
        self._cards_created = True

    def _prepare_series_data(self):
        """Подготавливает данные о сериях для создания карточек"""
        chips_data = self._chips_data
        series_names = {
            'series133': 'Серия 133',
            'series140': 'Серия 140',
            'series142': 'Серия 142',
            'series153': 'Серия 153',
            'series155': 'Серия 155',
            'series157': 'Серия 157',
            'series169': 'Серия 169',
            'series170': 'Серия 170',
            'series171': 'Серия 171',
            'series174': 'Серия 174',
            'series175': 'Серия 175',
            'series176': 'Серия 176',
            'series193': 'Серия 193',
            'series198': 'Серия 198',
            'series249': 'Серия 249',
            'series427': 'Серия 427',
            'series490': 'Серия 490',
            'series511': 'Серия 511',
            'series512': 'Серия 512',
            'series514': 'Серия 514',
            'series521': 'Серия 521',
            'series522': 'Серия 522',
            'series525': 'Серия 525',
            'series526': 'Серия 526',
            'series528': 'Серия 528',
            'series529': 'Серия 529',
            'series530': 'Серия 530',
            'series531': 'Серия 531',
            'series533': 'Серия 533',
            'series537': 'Серия 537',
            'series538': 'Серия 538',
            'series541': 'Серия 541',
            'series543': 'Серия 543',
            'series544': 'Серия 544',
            'series548': 'Серия 548',
            'series551': 'Серия 551',
            'series553': 'Серия 553',
            'series554': 'Серия 554',
            'series555': 'Серия 555',
            'series556': 'Серия 556',
            'series558': 'Серия 558',
            'series559': 'Серия 559',
            'series561': 'Серия 561',
            'series563': 'Серия 563',
            'series564': 'Серия 564',
            'series565': 'Серия 565',
            'series568': 'Серия 568',
            'series571': 'Серия 571',
            'series572': 'Серия 572',
            'series573': 'Серия 573',
            'series574': 'Серия 574',
            'series580': 'Серия 580',
            'series585': 'Серия 585',
            'series588': 'Серия 588',
            'series589': 'Серия 589',
            'series590': 'Серия 590',
            'series591': 'Серия 591',
            'series593': 'Серия 593',
            'series594': 'Серия 594',
            'series597': 'Серия 597',
            'series1002': 'Серия 1002',
            'series1004': 'Серия 1004',
            'series1005': 'Серия 1005',
            'series1006': 'Серия 1006',
            'series1008': 'Серия 1008',
            'series1009': 'Серия 1009',
            'series1014': 'Серия 1014',
            'series1015': 'Серия 1015',
            'series1016': 'Серия 1016',
            'series1017': 'Серия 1017',
            'series1019': 'Серия 1019',
            'series1021': 'Серия 1021',
            'series1022': 'Серия 1022',
            'series1023': 'Серия 1023',
            'series1025': 'Серия 1025',
            'series1026': 'Серия 1026',
            'series1027': 'Серия 1027',
            'series1031': 'Серия 1031',
            'series1032': 'Серия 1032',
            'series1033': 'Серия 1033',
            'series1038': 'Серия 1038',
            'series1039': 'Серия 1039',
            'series1040': 'Серия 1040',
            'series1043': 'Серия 1043',
            'series1051': 'Серия 1051',
            'series1053': 'Серия 1053',
            'series1054': 'Серия 1054',
            'series1055': 'Серия 1055',
            'series1056': 'Серия 1056',
            'series1057': 'Серия 1057',
            'series1058': 'Серия 1058',
            'series1064': 'Серия 1064',
            'series1066': 'Серия 1066',
            'series1071': 'Серия 1071',
            'series1072': 'Серия 1072',
            'series1075': 'Серия 1075',
            'series1082': 'Серия 1082',
            'series1084': 'Серия 1084',
            'series1086': 'Серия 1086',
            'series1087': 'Серия 1087',
            'series1091': 'Серия 1091',
            'series1100': 'Серия 1100',
            'series1102': 'Серия 1102',
            'series1103': 'Серия 1103',
            'series1107': 'Серия 1107',
            'series1108': 'Серия 1108',
            'series1109': 'Серия 1109',
            'series1113': 'Серия 1113',
            'series1114': 'Серия 1114',
            'series1116': 'Серия 1116',
            'series1118': 'Серия 1118',
            'series1121': 'Серия 1121',
            'series1125': 'Серия 1125',
            'series1128': 'Серия 1128',
            'series1146': 'Серия 1146',
            'series1152': 'Серия 1152',
            'series1156': 'Серия 1156',
            'series1157': 'Серия 1157',
            'series1162': 'Серия 1162',
            'series1167': 'Серия 1167',
            'series1183': 'Серия 1183',
            'series1401': 'Серия 1401',
            'series1407': 'Серия 1407',
            'series1408': 'Серия 1408',
            'series1409': 'Серия 1409',
            'series1413': 'Серия 1413',
            'series1420': 'Серия 1420',
            'series1422': 'Серия 1422',
            'series1423': 'Серия 1423',
            'series1426': 'Серия 1426',
            'series1433': 'Серия 1433',
            'series1435': 'Серия 1435',
            'series1436': 'Серия 1436',
            'series1500': 'Серия 1500',
            'series1506': 'Серия 1506',
            'series1507': 'Серия 1507',
            'series1520': 'Серия 1520',
            'series1521': 'Серия 1521',
            'series1526': 'Серия 1526',
            'series1531': 'Серия 1531',
            'series1533': 'Серия 1533',
            'series1540': 'Серия 1540',
            'series1554': 'Серия 1554',
            'series1556': 'Серия 1556',
            'series1561': 'Серия 1561',
            'series1564': 'Серия 1564',
            'series1566': 'Серия 1566',
            'series1568': 'Серия 1568',
            'series1590': 'Серия 1590',
            'series1601': 'Серия 1601',
            'series1603': 'Серия 1603',
            'series1617': 'Серия 1617',
            'series1623': 'Серия 1623',
            'series1625': 'Серия 1625',
            'series1628': 'Серия 1628',
            'series1630': 'Серия 1630',
            'series1656': 'Серия 1656',
            'series1800': 'Серия 1800',
            'series1802': 'Серия 1802',
            'series1809': 'Серия 1809',
            'series1810': 'Серия 1810',
            'series1816': 'Серия 1816',
            'series1818': 'Серия 1818',
            'series1820': 'Серия 1820',
            'series1821': 'Серия 1821',
            'series1823': 'Серия 1823',
            'series1827': 'Серия 1827',
            'series1830': 'Серия 1830',
            'series1834': 'Серия 1834',
            'series1835': 'Серия 1835',
            'series1843': 'Серия 1843',
            'series1850': 'Серия 1850',
            'series1852': 'Серия 1852',
            'series1853': 'Серия 1853',
            'series1858': 'Серия 1858',
            'series1873': 'Серия 1873',
            'series_ipv': 'Серия ИПВ',
        }
        
        # Сортируем серии для правильного отображения
        sorted_series = sorted(chips_data.keys(), key=lambda x: (
            # Сначала числовые серии
            (0, int(x.replace('series', '').replace('_ipv', '9999'))) if x.replace('series', '').replace('_ipv', '').isdigit() 
            else (1, x)
        ))
        
        # Сохраняем подготовленные данные для создания карточек
        self._series_list = []
        for series_key in sorted_series:
            if series_key not in chips_data:
                continue
            series_display_name = series_names.get(series_key, f'Серия {series_key.replace("series", "")}')
            self._series_list.append((series_key, series_display_name))
        
        # Индекс для порционной загрузки
        self._current_index = 0
        self._batch_size = 40  # Создаем по 40 карточек за раз (увеличено для оптимизации)

    def _start_creating_cards(self):
        """Начинает создание карточек порциями"""
        list_widget = self.ids.get('chips_analogs_list', None)
        content_view = self.ids.get('content_scroll_view', None)
        loading_overlay = self.ids.get('loading_overlay', None)
        
        if not list_widget:
            return
        
        # Показываем спиннер и скрываем контент
        if loading_overlay:
            loading_overlay.opacity = 1
        if content_view:
            content_view.opacity = 0
            content_view.disabled = True
        
        # Очищаем существующие виджеты
        from misc import MDIconCard
        for child in list_widget.children[:]:
            if isinstance(child, MDIconCard):
                list_widget.remove_widget(child)
        
        # Создаем первую порцию карточек
        self._create_batch_cards()

    def _create_batch_cards(self):
        """Создает порцию карточек (batch_size штук)"""
        list_widget = self.ids.get('chips_analogs_list', None)
        if not list_widget or not hasattr(self, '_series_list'):
            return
        
        from kivy.clock import Clock
        
        # Создаем карточки для текущей порции
        end_index = min(self._current_index + self._batch_size, len(self._series_list))
        
        for i in range(self._current_index, end_index):
            series_key, series_display_name = self._series_list[i]
            
            # Создаем карточку
            card = MDIconCard()
            
            # Создаем функцию-обработчик для этой серии
            def make_handler(series, name):
                def handler(*args):
                    self.manager.current = "chips_analogs_screen"
                    chips_analogs_screen = self.manager.get_screen("chips_analogs_screen")
                    chips_analogs_screen.ids.chips_analogs.build_table(
                        series,
                        chips_analogs_screen.ids.chips_analogs_scroll_view,
                        chips_analogs_screen
                    )
                    chips_analogs_screen.ids.chips_analogs_top_bar_title.text = name
                return handler
            
            card.bind(on_release=make_handler(series_key, series_display_name))
            
            # Создаем ImageButton
            img_btn = ImageButton()
            img_path = f"media/{series_key}.webp"
            # Проверяем существование файла с кэшированием, если нет - используем заглушку
            if img_path not in _image_cache:
                _image_cache[img_path] = os.path.exists(img_path)
            if not _image_cache[img_path]:
                img_path = "media/series_noname.webp"
            img_btn.source = img_path
            img_btn.bind(on_release=make_handler(series_key, series_display_name))
            card.add_widget(img_btn)
            
            # Создаем MDShortenLabel
            label = MDShortenLabel()
            label.text = series_display_name
            card.add_widget(label)
            
            # Добавляем карточку в список
            list_widget.add_widget(card)
        
        self._current_index = end_index
        
        # Если есть еще карточки для создания, планируем следующую порцию
        if self._current_index < len(self._series_list):
            Clock.schedule_once(lambda dt: self._create_batch_cards(), 0.01)
        else:
            # Загрузка завершена, скрываем спиннер и показываем контент
            from kivy.animation import Animation
            loading_overlay = self.ids.get('loading_overlay', None)
            content_view = self.ids.get('content_scroll_view', None)
            
            if loading_overlay:
                Animation(opacity=0, duration=0.3).start(loading_overlay)
            if content_view:
                content_view.disabled = False
                Animation(opacity=1, duration=0.3).start(content_view)


class ChipsAnalogsScreen(MDScreen):
    pass


class ChipsAnalogs(MDGridLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.adaptive_height = True
        self.padding = 10
        self.cols = 3
        self.spacing = [dp(4)]
        self.series = None
        # Загружаем данные о микросхемах из JSON
        self._chips_data = load_chips_analogs()

    def build_table(self, series, view, screen=None, *args):
        self.labels = []
        if not self.series == series:
            view.scroll_y = 1
            self.clear_widgets()
            
            # Получаем доступ к overlay и контенту через переданный экран
            if screen and hasattr(screen, 'ids'):
                loading_overlay = screen.ids.get('loading_overlay', None)
                content_view = screen.ids.get('chips_analogs_scroll_view', None)
                
                # Показываем спиннер и скрываем контент
                if loading_overlay:
                    loading_overlay.opacity = 1
                if content_view:
                    content_view.opacity = 0
                    content_view.disabled = True
            
            # Используем загруженные данные из JSON вместо getattr
            series_data = self._chips_data.get(series, {})
            
            # Подготавливаем данные для порционной загрузки
            self._table_items = list(series_data.items())
            self._table_current_index = 0
            self._table_batch_size = 30  # Создаем по 30 элементов за раз
            self.series = series
            self._view = view
            self._screen = screen
            
            # Начинаем порционную загрузку
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: self._create_table_batch(view), 0.01)
        else:
            self.series = series

        Window.bind(on_resize=self.update_width)
    
    def _create_table_batch(self, view):
        """Создает порцию элементов таблицы"""
        if not hasattr(self, '_table_items') or not hasattr(self, '_table_current_index'):
            return
        
        end_index = min(self._table_current_index + self._table_batch_size, len(self._table_items))
        
        for i in range(self._table_current_index, end_index):
            k, v = self._table_items[i]
            label_k = MDLabel(text=k, adaptive_height=True,
                              halign="right",
                              size_hint_x=None,
                              width=Window.width * 0.5 - 16)
            label_v = MDLabel(text=v, adaptive_height=True,
                              size_hint_x=None,
                              width=Window.width * 0.5 - 16)
            self.labels.append((label_k, label_v))

            self.add_widget(label_k)
            self.add_widget(MDDivider(orientation="vertical"))
            self.add_widget(label_v)
            self.add_widget(MDDivider())
            self.add_widget(MDDivider())
            self.add_widget(MDDivider())
        
        self._table_current_index = end_index
        
        # Если есть еще элементы, планируем следующую порцию
        if self._table_current_index < len(self._table_items):
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: self._create_table_batch(view), 0.01)
        else:
            # Загрузка завершена, скрываем спиннер и показываем контент
            from kivy.animation import Animation
            if hasattr(self, '_screen') and self._screen and hasattr(self._screen, 'ids'):
                loading_overlay = self._screen.ids.get('loading_overlay', None)
                content_view = self._screen.ids.get('chips_analogs_scroll_view', None)
                
                if loading_overlay:
                    Animation(opacity=0, duration=0.3).start(loading_overlay)
                if content_view:
                    content_view.disabled = False
                    Animation(opacity=1, duration=0.3).start(content_view)

    def update_width(self, *args):
        new_width = Window.width * 0.5 - 16
        for label_k, label_v in self.labels:
            label_k.width = new_width
            label_v.width = new_width
