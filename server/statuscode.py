STATUS_CODE = {
    'Success': 0,
    'Not Found': 1,

    'Identity Error': 901,
    # 身份错误

    'User Not Found': 902,
    # 未找到用户

    'Course Not Found': 903,
    # 课程未找到

    'Customer Not Found': 904,
    # 未找到客户

    'Customer Already Exists': 905,
    # 客户已存在

    'Seller Not Found': 906,
    # 未找到地推

    'Child Not Found': 907,
    # 未找到孩子

    'Old Not Found': 908,
    # 未找到老客户

    'User Already Exists': 909,
    # 用户已存在

    'Course Already Exists': 910,
    # 课程已存在

    'Teacher Not Found': 911,
    # 老师未找到

    'Refund Record Exception': 801,
    # 退款记录异常

    'Trade Record Exception': 802,
    # 收款记录异常

    'Alipay Error': 803,
    # 支付宝异常

    'Price Not Match': 804,
    # 金额不匹配

    'Course Not Paid': 805,
    # 有待支付的金额

    'Database Error': 700,
    # 数据库错误

    'Error File Type': 701,
    # 错误文件类型

    'Unable To Import File': 702,
    # 无法导入文件

    'File Data Error': 703,
    # 文件数据错误

    'Path Not Found': 704,
    # 路径未找到

    'Frontend Value Error': 705,
    # 前端参数异常

    'Error Time Range': 706,
    # 输入时间范围不正确

    'Verify Code Error': 707,
    # 验证码错误

    'Error Tel Number': 708,
    # 电话号码错误

    'Password Not Match': 709
    # 密码不正确
}

USER_TYPE = {
    'admin': 0,
    'customer': 1,
    'superuser': 2,
    'consultant': 3,
    'eduadmin': 4,
    'seller': 5
}

DATE_CODE = {
    'Monday': 1,
    'Tuesday': 2,
    'Wednesday': 3,
    'Thursday': 4,
    'Friday': 5,
    'Saturday': 6,
    'Sunday': 7,
}

DATE_DECODE = {
    1: '星期一',
    2: '星期二',
    3: '星期三',
    4: '星期四',
    5: '星期五',
    6: '星期六',
    7: '星期日'
}

REFUND_STATUS = {
   'No Refund Received': 0,
   'Under Review': 1,
   'Audit Passed': 2,
   'Already Paid': 3
}

LOG_TYPE = {
    'Refund': 0,
    'Delete User': 1,
    'Delete Customer': 2,
    'Add User': 3
}

TRADE_TYPE = {
    'wap_pay': 81,
    # 手机网页支付

    'page_pay': 82,
    # PC 网页支付

    'refund': 80,
    # 退款
}

