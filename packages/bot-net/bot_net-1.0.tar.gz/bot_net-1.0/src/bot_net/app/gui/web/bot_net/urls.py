"""
*********************************************************************************
*                                                                               *
* input_arguments.py -- Methods to parse the user input arguments.              *
*                                                                               *
********************** IMPORTANT Bot-net LICENSE TERMS **************************
*                                                                               *
* This file is part of Bot-net.                                                 *
*                                                                               *
* Bot-net is free software: you can redistribute it and/or modify               *
* it under the terms of the GNU General Public License as published by          *
* the Free Software Foundation, either version 3 of the License, or             *
* (at your option) any later version.                                           *
*                                                                               *
* Bot-net is distributed in the hope that it will be useful,                    *
* but WITHOUT ANY WARRANTY; without even the implied warranty of                *
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                 *
* GNU General Public License for more details.                                  *
*                                                                               *
* You should have received a copy of the GNU General Public License             *
* along with Bot-net.  If not, see <http://www.gnu.org/licenses/>.              *
*                                                                               *
*********************************************************************************
"""

from django.urls import path, re_path

from bot_net
.app.gui.web.settings import STATIC_URL
from . import views

urlpatterns = [
    path('', views.index, name='black widow'),

    # --- SNIFFING --- #
    path('sniffing', views.Sniffing.SettingsView.as_view(), name='sniffing'),
    path('sniffing/capture', views.Sniffing.CaptureView.as_view(), name='sniffing'),

    # --- WEB PARSING --- #
    path('web/parsing', views.WebParsing.SettingsView.as_view(), name='web parsing'),
    path('web/parsing/parse', views.WebParsing.ParseView.as_view(), name='web parsing'),

    # --- SQL INJECTION --- #
    path('sql', views.Sql.SettingsView.as_view(), name='sql injection'),
    path('sql/inject', views.Sql.InjectView.as_view(), name='sql injection'),

    path('user', views.user, name='user'),
    path('tables', views.tables, name='tables'),
    path('typography', views.typography, name='typography'),
    path('icons', views.icons, name='icons'),
    path('notifications', views.notifications, name='notifications'),
    path('upgrade', views.upgrade, name='upgrade'),

    # static (non debug compatibility without web server)
    re_path(r'^' + STATIC_URL[1:] + '(?P<path>.*)$', views.static, name='static'),
]
