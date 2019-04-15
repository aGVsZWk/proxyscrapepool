# -*- coding: utf-8 -*-
# author: Luke
from flask import request, jsonify
from flask.views import MethodView
from proxyscrapepool import app
from proxyscrapepool.models import Proxy


class ProxyListView(MethodView):

    def get(self):
        proxies = Proxy.objects.all()
        type = request.args.get('type')
        if type:
            proxies = proxies.filter(type=type)
        data = [proxy.to_dict() for proxy in proxies]
        return jsonify(proxies=data)

    def post(self):
        data = request.get_json()
        proxy = Proxy()
        proxy.figer = data.get('figer')
        proxy.ip = data.get('ip')
        proxy.port = data.get('port')
        proxy.type = data.get('type')
        proxy.is_outwall = data.get('is_outwall')
        proxy.delay_time = data.get('delay_time')
        proxy.loss_packet_percent = data.get('loss_packet_percent')
        proxy.source = data.get('source')
        proxy.is_ok = data.get('is_ok')
        proxy.save()
        return jsonify(proxy.to_dict())



class ProxyDetailView(MethodView):
    def get(self, figer):
        try:
            proxy = Proxy.objects.get(figer=figer)
        except Proxy.DoesNotExist:
            return jsonify({'error': 'proxy does not exist'}), 404
        return jsonify(proxy.to_dict())


    def delete(self, figer):
        try:
            proxy = Proxy.objects.get(figer=figer)
        except Proxy.DoesNotExist:
            return jsonify({'error': 'proxy does not exist'}), 404
        proxy.delete()
        return 'Succed to delete post', 204



app.add_url_rule('/proxies/', view_func=ProxyListView.as_view('proxies'))
app.add_url_rule('/proxy/<figer>/', view_func=ProxyDetailView.as_view('proxy'))