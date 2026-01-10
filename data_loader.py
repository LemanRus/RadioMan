#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Модуль для загрузки данных из JSON файлов с кэшированием"""

import json
import os

# Кэш для загруженных данных
_cache = {}


def _load_json(filepath):
    """Загружает JSON файл с кэшированием"""
    if filepath in _cache:
        return _cache[filepath]
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Файл не найден: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    _cache[filepath] = data
    return data


def load_chips_analogs():
    """
    Загружает все серии микросхем из JSON файла.
    
    Returns:
        dict: Словарь, где ключи - имена серий (series133, series140, etc.),
              значения - словари с аналогами микросхем
    """
    filepath = os.path.join('data', 'chips_analogs.json')
    return _load_json(filepath)


def load_resistor_markings():
    """
    Загружает словари для маркировки резисторов (TH).
    
    Returns:
        dict: Словарь с ключами: nominal, multiplier, tolerance, thermal
    """
    filepath = os.path.join('data', 'resistor_markings.json')
    return _load_json(filepath)


def load_smd_resistor_markings():
    """
    Загружает словари для маркировки SMD резисторов.
    
    Returns:
        dict: Словарь с ключами: eia96, eia96_multiplier
    """
    filepath = os.path.join('data', 'smd_resistor_markings.json')
    return _load_json(filepath)


def load_capacitor_markings():
    """
    Загружает словари для маркировки конденсаторов.
    
    Returns:
        dict: Словарь с ключами: decimal_point, voltage, smd_capacity
    """
    filepath = os.path.join('data', 'capacitor_markings.json')
    return _load_json(filepath)


def clear_cache():
    """Очищает кэш загруженных данных"""
    _cache.clear()
