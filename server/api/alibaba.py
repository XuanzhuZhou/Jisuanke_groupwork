# -*- coding: utf-8 -*-

'''本模块用于处理和支付宝相关的'''

import logging
import random
import time

from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradePagePayModel import \
    AlipayTradePagePayModel
from alipay.aop.api.domain.AlipayTradeRefundModel import AlipayTradeRefundModel
from alipay.aop.api.domain.AlipayTradeWapPayModel import AlipayTradeWapPayModel
from alipay.aop.api.request.AlipayTradePagePayRequest import \
    AlipayTradePagePayRequest
from alipay.aop.api.request.AlipayTradeRefundRequest import \
    AlipayTradeRefundRequest
from alipay.aop.api.request.AlipayTradeWapPayRequest import \
    AlipayTradeWapPayRequest
from alipay.aop.api.util.SignatureUtils import verify_with_rsa
from django.http import HttpResponse
from rsa.pkcs1 import VerificationError

from statuscode import TRADE_TYPE


NOTIFY_URL = ''

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a',)
LOGGER = logging.getLogger('')

CLIENTCONFIG = AlipayClientConfig()
CLIENTCONFIG.server_url = 'https://openapi.alipaydev.com/gateway.do'
CLIENTCONFIG.app_id = '2016091700530462'
CLIENTCONFIG.charset = 'utf-8'
CLIENTCONFIG.sign_type = 'RSA2'
CLIENTCONFIG.notify_url = NOTIFY_URL
CLIENTCONFIG.app_private_key = (
    'MIIEogIBAAKCAQEAo9h9bEE9If52ENw4qp1VIfMTZ6vWldtbz/4XbXbYk+RAFhB+sTP7Y'
    '1OKryMpfkvcJwkRwF27zLSbpY8q78Udbpl+DiN1KtEeKIzqp6yaA+mwfoWytwAMyy73qX'
    'yL1WThmne88w+jixI/aNyRr7eWM41LbIuuRzZvgxBeLQjLaCoaYPOJI7dhcMcrq25cDKJ'
    'Z+i7afvin8/btT9gw8TZMTcRrRRCC9R2WpIkf/hgXrHaTczXmvoYLVwK1UQx41Z9jZfdg'
    'QEeerKuYhIYCnSmlDWbhkGJ3mhdkoUUOEdOCD89SMyUiSw/TgHsvEyh5wlhF8Z+9lE9PO'
    '6apIeQFi2b6LQIDAQABAoIBAFZugdt1ntYr8gR657m5PYunOvlZgN2U1h4moB0ysJVztw'
    'rssKiyD08aZvJ0zhK92ekNs7uSttsJ+4GewLuzdA9AEWtL8SchIZOqoq7JMoYV5PEZfml'
    'jMVyN7kAOX4W2rfxaZeaivVdDzQd4M7JKWoXfZ4ZfORR/9ttg6w0+sm7DzwGAGsxEVyDB'
    'tYER5UNjSPZeZIzS53FAUG40mhCDl+Ab/UWNSvAY44ITc6p29OdiLPwi8vpvdzL+AZtdw'
    '0B2dcsqq+H6tRyEuQwpH9SxrWCdiMWtiEsVyMl7PpI/FU0uDlSDTxFjwkesXhBXysh2rX'
    '0aHKcn1jiCljU/m1KxawECgYEA0IKUpuNZLgxIN3JYq/p6Tu15MMxLLzeoDw1m5n9qLGe'
    'QUqwkHMQbfbcN/9sT8UwgHTq4VdM0F2bIqNx5bFuT6Kz1zVWe5e7k6JC8Z9d9Xxi1lkFT'
    '+CyGFriJHT8eS/wPm4sV+WT3NuC+FDoi0tnHVBDpZYrjf9Z3GD+DtosO9X0CgYEAySmzA'
    'CJ1dNfbaKppq8RA5CWu+hc1sGOhKvwPMITy5LjT4dlx62ixn+GNVBrDOp5eEjz+PTRnDz'
    'MZKq/CLu/qyuPkOmjCUcpKoUEqsmUaSzYKd75g8YRjg4aLuFP0VVps5sTWSzFeGesC7za'
    'Taqkrg4SKMrUAm4d6oYCAHZRJdnECgYA4jWIiDYGPkrc3iqTwKCRqKdB34sD1koPbaUgi'
    'diZm2sPzGEtHHg1SwIZkgZfcF0iShO2gIYN8YV1FJ18re38XWWnlgjZxqKSfSzo+c9zGI'
    'R6HHTrYEcNggDZ4HzlpZHkbN9MC7FZ8pOII/GebhoOgkmGrL8taTeHJSti/duHcxQKBgB'
    'mGjQwrUzQsX878MMR29rT8gyOA5nMncT//E/5YIGodeeViri3s7v0WpdRSQQujJNSzoJ8'
    'rkxg+p6be/ojuMKDmIgO3X1D5lla36i8Q3TFF/jYLlkmPPwFlhT0yigJ6ou71cyu/a+1m'
    'AM1R44rZRIg/vTmJ9jXGDy2HHLqkIl5BAoGAZDA8mu0C3s8jFCsoEujIR9xXLbwe70gl8'
    'byTJOftMatTrLh8Dkmif3sWdJTUs5EcIjn8Nquo7CxJ62nCn+BrUYlqVPkguqkTVVjXsO'
    'R1TqtkcGOEtmsHFEOLc4tg5NfySIrNqUGJL6PwmdxgcaT//zXriLGHk3p6xqM+J+ZppbA'
    '=')
CLIENTCONFIG.alipay_public_key = (
    'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA1k6bzgJbJc92o4Z79UjspHjP6'
    'EzsiSjEnM69B8xvJdMtKrHbwGiO483gFxC1snVNHepaLmU7zowz8NvRkLLT/sE/ydXVeZ'
    '7H4ZOWU31eAsZiOjsh6h7X8c7qugabL4rXYhULtU6iQoay2fqdV7yQR0P60px/IX35G+l'
    'fLe++yptrlVaUq8zFAFH+BfmxLXP0Ni8hW065rXJoAH2/1NeU2XvOcWsGFgpGZicaZJzN'
    'HmPV0KlyGpLPqmD47KH1z7ZZoCh/n0rb7azvkqVaP2H3RZYOwX/Z/cQByx7hatOFXRjJ5'
    'Kkov0z9aSoqNSEcetJOcXI4BoKtiKQT+o4RDbSrkwIDAQAB')

CLIENT = DefaultAlipayClient(
    alipay_client_config=CLIENTCONFIG, logger=LOGGER)


def product_trade_no():
    """
    根据当前时间生成订单号

    :返回信息: 根据当前时间和随机数生成的订单号

    """
    trade_no = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    trade_no += ''.join([str(random.randint(0, 9)) for i in range(0, 5)])
    return trade_no


def response_page_pay(trade_no: str, price) -> str:
    '''
    处理电脑页面的支付请求，返回跳转到支付宝的页面地址

    :传入参数: trade_no: 字符串格式的订单号 price: 价格

    :返回: 字符串格式的支付地址
    '''
    model = AlipayTradePagePayModel()
    model.subject = "course"
    model.total_amount = price
    model.out_trade_no = trade_no
    model.body = "Courses"
    model.product_code = "FAST_INSTANT_TRADE_PAY"
    request = AlipayTradePagePayRequest(biz_model=model)
    return CLIENT.page_execute(request, http_method="GET")


def response_wap_page_pay(trade_no: str, price) -> str:
    '''
    处理手机页面的支付请求，返回拉起支付宝 App 的地址

    :传入参数: trade_no: 字符串格式的订单号 price: 价格

    :返回: 字符串格式的支付地址
    '''
    model = AlipayTradeWapPayModel()
    model.subject = "test"
    model.total_amount = price
    model.out_trade_no = trade_no
    model.body = "course"
    model.product_code = "QUICK_WAP_WAY"
    request = AlipayTradeWapPayRequest(biz_model=model)
    return CLIENT.page_execute(request, 'GET')


def check_notify(params):
    '''
    对从支付宝获取的 notify 信息进行处理，判断订单状态

    :传入参数: 支付宝发送的包含签名类型、签名等信息的字典参数

    :返回: bool 值

    '''
    sign = params.pop('sign', None)
    params.pop('sign_type')
    params = sorted(params.items(), key=lambda e: e[0], reverse=False)
    message = "&".join(u"{}={}".format(k, v) for k, v in params).encode()
    if 'sign_type' in params and 'sign' in params:
        sign = params['sign']
        del params['sign_type']
        del params['sign']
        try:
            status = verify_with_rsa(
                CLIENTCONFIG.alipay_public_key, message, sign)
            return status
        except VerificationError as error:
            print(error)
            return False
    return False


def pay_result(request):
    '''
    处理支付宝结果通知

    :前端传入参数: 支付宝发送的订单信息

    :返回: 代表是否成功的 http 相应

    '''
    if request.method == 'GET':
        params = request.GET.dict()
        if check_notify(params):
            return HttpResponse('success')
        return HttpResponse('')
    if request.method == 'POST':
        params = request.POST.dict()
        if check_notify(params):
            return HttpResponse('success')
        return HttpResponse('')
    return HttpResponse('')


def response_refund(trade_no: str, amount: float):
    '''
    接入支付宝处理退款

    :传入参数: trade_no: 字符串格式的订单号 amount: 价格

    :返回: 退款信息
    '''
    if len(trade_no) != 15:
        return -1
    model = AlipayTradeRefundModel()
    model.out_trade_no = trade_no
    model.refund_amount = amount
    request = AlipayTradeRefundRequest(biz_model=model)
    response = CLIENT.execute(request)
    print("response of refund: ", response)
    return response


def solve_trade(trade_type, *, trade_no="-1", amount=-1) -> str:
    '''
    处理与支付宝支付有关的入口

    :传入参数: trade_type: 交易类型, 含义请参考 statuscode.py 文件
             trade_no: 订单号, 可以为空
             amount: 订单价格, 可以为空

    :返回: 可能需要的支付地址

    '''
    if trade_type == TRADE_TYPE["refund"]:
        if trade_no == "-1" or amount == -1:
            return None
        response = response_refund(trade_no, amount)
        if response == -1:
            return None
        print(response)
    elif amount == -1 or trade_no == "-1":
        return None
    elif trade_type == TRADE_TYPE["wap_pay"]:
        url = response_wap_page_pay(trade_no=trade_no, price=amount)
        return url
    elif trade_type == TRADE_TYPE["page_pay"]:
        url = response_page_pay(trade_no=trade_no, price=amount)
        return url
    return ''
