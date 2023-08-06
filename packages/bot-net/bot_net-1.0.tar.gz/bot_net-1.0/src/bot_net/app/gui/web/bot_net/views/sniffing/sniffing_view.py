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

from django.http import JsonResponse
from django.shortcuts import render, redirect

from bot_net.app.gui.web.bot_net.models import SniffingJobModel
from bot_net.app.helpers import network, util
from bot_net.app.managers.sniffer import PcapSniffer

from .abstract_sniffing_view import AbstractSniffingView


class Sniffing:
    """
    Sniffing Container View
    """
    class SettingsView(AbstractSniffingView):
        """
        Sniffing Settings View
        """
        name = 'sniffing'
        template_name = 'sniffing/settings.html'

        def get(self, request, *args, **kwargs):
            """
            :type request: django.core.handlers.wsgi.WSGIRequest
            :return: django.http.HttpResponse
            """
            if not PcapSniffer.is_executable():
                return render(request, self.error_templates.get('root_required'))
            view_params = {
                'interfaces': network.get_interfaces(),
                'jobs': SniffingJobModel.all()
            }
            return render(request, self.template_name, view_params)

        def post(self, request):
            """
            :type request: django.core.handlers.wsgi.WSGIRequest
            :return: django.http.HttpResponseRedirect
            """
            if not PcapSniffer.is_executable():
                return JsonResponse({
                    'message': 'You are not #root'
                }, status=401)
            request_params: dict = request.POST.dict()
            if request_params.get('interfaces') is not None:
                request_params['interfaces'] = request.POST.getlist('interfaces')
            pcap_file = request.FILES.get('pcap')
            if pcap_file is not None:
                request_params['pcap'] = self.upload_file(pcap_file)
            else:
                request_params['pcap'] = None

            job = self._new_job(
                request_params.get('filters'),
                request_params.get('pcap'),
                request_params.get('interfaces'),
            )

            return redirect('/sniffing/capture?id=' + str(job.id))

    class CaptureView(AbstractSniffingView):
        """
        Sniffing Capture View
        """
        name = 'sniffing'
        template_name = 'sniffing/capture.html'

        def get(self, request, *args, **kwargs):
            """
            :type request: django.core.handlers.wsgi.WSGIRequest
            :return: django.http.HttpResponse
            """
            if not PcapSniffer.is_executable():
                return render(request, self.error_templates.get('root_required'))

            return self._get_job(request, redirect_url='/sniffing')

        def post(self, request) -> JsonResponse:
            """
            :type request: django.core.handlers.wsgi.WSGIRequest
            :return: django.http.JsonResponse
            """
            return self._post_job(request)
