#!/bin/bash
rm ui_*.py
rm ui_*.pyc
pyside-uic tracker_ui.ui > ui_tracker.py
