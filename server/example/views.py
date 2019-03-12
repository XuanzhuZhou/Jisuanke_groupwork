# -*- coding: utf-8 -*-

'''
这个模块是接受 GET 和 POST 请求的样例。
可以用来给前端提供后台测试接口。
'''


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


@require_http_methods(['GET'])
def response_get_method(request) -> JsonResponse:
    '''
    本函数只接受 GET 请求，返回一个 json 格式的标准 Http 响应
    装饰器负责验证请求的方法，使用时记得从 django.views.decorators.http 引入
    -> 是 python3.5 引入的，提示函数返回的类型，不会影响代码执行
    '''
    response = {}
    # try:
    #     # 这里可以执行一些数据库操作
    #     response['msg'] = 'success'
    #     response['error_num'] = 0
    # except Exception as e:
    #     # 不建议直接用 Exception，根据 Django 数据库操作指定具体 Django 中的错误类型
    #     # 例如 DoesNotExist，具体错误类型以及用法请参考文档
    #     # 千万不要用 try except 语句进行逻辑判断
    #     # 尤其不要用 objects.get() 方法配合 DoesNotExist 判断数据库中是否存在要查询的数据
    #     # 可以使用 objects.filter().count() == 1 进行判断
    #     # 其他判断方法以及效率请参考文档
    #     # Django 错误类型参考文档如下
    #     # https://docs.djangoproject.com/zh-hans/2.1/ref/exceptions/
    #     print(e)
    #     # # 在服务端输出错误
    #     response['msg'] = str(e)
    #     response['error_num'] = 1
    response['msg'] = "success"
    response['error_num'] = 0
    return JsonResponse(response)
    # 返回 json 数据不要直接使用 json.dumps()
    # 要用 Django 自带的 JsonResponse 进行封装


@require_http_methods(['POST'])
def response_post_method_with_csrf_check(request) -> JsonResponse:
    '''
    本函数只接受 POST 请求，同样返回一个json 格式的标准 Http 响应
    装饰器负责验证请求的方法，使用时记得从 django.views.decorators.http 引入
    Django 默认对所有 POST 请求进行 csrf 验证
    如果是通过 axios 发送的请求想通过验证
    需要在请求头中加入从 cookie 中取出的 csrftoken 的值
    axios 用法请参考样例代码以及官方文档
    发送 POST 请求的具体操作同样参考样例代码
    '''
    print("*"*30)
    print(request.body)
    print("*"*30)
    print(request.user)
    response = {}
    # try:
    #     # books = Book.objects.filter()
    #     # response['list'] = json.loads(serialize("json", books))
    #     # 上面是从通过 Django 从数据库中取出信息的例子，直接运行无法执行
    #     # 因为数据库里还没有插入值，甚至连 model 还都没写
    #     # serialize 解释不清，贴出官方文档如下
    #     # https://docs.djangoproject.com/zh-hans/2.1/topics/serialization/
    #     # json.loads() 和 json.dumps() 参考 python 文档
    #     response['msg'] = "success"
    #     response['error_num'] = 0
    # except Exception as e:
    #     print(e)
    #     # 输出错误
    #     response['msg'] = str(e)
    #     response['erro_num'] = 1
    response['msg'] = "1"
    response['error_num'] = 0
    return JsonResponse(response)


@csrf_exempt
def response_post_method_without_csrf_check(request):
    '''
    本函数对 POST 请求不做 csrf 验证
    装饰器 csrf_exempt 可以达到上面的效果
    使用时不要忘记从 django.views.decorators.csrf 引入
    '''
    print("*"*30)
    print(request.body)
    response = {}
    response['msg'] = "0"
    response['error_num'] = 0
    return JsonResponse(response)
