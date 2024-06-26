"""Constants, links and functions that are used across multiple files."""
from os import environ

from bidict import bidict
from requests import Session

session = Session()
cookie = environ.get("JUEJIN_SESSION_ID")
data_filename = "juejin_articles.json"
config_filename = "juejin.ini"

api_tag_list = "https://api.juejin.cn/recommend_api/v1/tag/recommend_tag_list"
api_recommended_feed = "https://api.juejin.cn/recommend_api/v1/article/recommend_all_feed"
api_category_feed = "https://api.juejin.cn/recommend_api/v1/article/recommend_cate_feed"
api_tag_feed = "https://api.juejin.cn/recommend_api/v1/article/recommend_cate_tag_feed"
api_translate_manage_pending_list = "https://api.juejin.cn/study_api/v1/translate/pre_query_status"
api_check_in_status = "https://api.juejin.cn/growth_api/v1/get_today_status"
api_check_in_day_count = "https://api.juejin.cn/growth_api/v1/get_counts"
api_lottery_config = "https://api.juejin.cn/growth_api/v1/lottery_config/get"
api_lottery_history = "https://api.juejin.cn/growth_api/v1/lottery_history/global_small"
api_get_total_point = "https://api.juejin.cn/growth_api/v1/get_cur_point"
api_draw_lottery = "https://api.juejin.cn/growth_api/v1/lottery/draw"
api_profile_id = "https://api.juejin.cn/user_api/v1/user/profile_id"
api_user = "https://api.juejin.cn/user_api/v1/user/get"
api_user_articles = "https://api.juejin.cn/content_api/v1/article/query_list"
api_get_luck = "https://api.juejin.cn/growth_api/v1/lottery_lucky/my_lucky"
get_captcha_link = "https://verify.snssdk.com/captcha/get"
verify_captcha_link = "https://verify.snssdk.com/captcha/verify"
check_in_link = "https://api.juejin.cn/growth_api/v1/check_in"
login_link = "https://juejin.cn/passport/web/user/login/?account_sdk_source=web"
attract_luck_link = "https://api.juejin.cn/growth_api/v1/lottery_lucky/dip_lucky"

category_id_map = bidict({
    "后端": "6809637769959178254",
    "前端": "6809637767543259144",
    "Android": "6809635626879549454",
    "iOS": "6809635626661445640",
    "人工智能": "6809637773935378440",
    "开发工具": "6809637771511070734",
    "代码人生": "6809637776263217160",
    "阅读": "6809637772874219534",
})
tag_id_map = {
    "后端": bidict({
        "后端": "6809640408797167623",
        "Java": "6809640445233070094",
        "Python": "6809640448827588622",
        "算法": "6809640499062767624",
        "Go": "6809640364677267469",
        "数据库": "6809640600502009863",
        "MySQL": "6809640366896054286",
        "Linux": "6809640385980137480",
        "Spring Boot": "6809641037787561992",
        "Redis": "6809640371019055111",
        "Spring": "6809640703325372423",
        "架构": "6809640501776482317",
        "LeetCode": "6809641039037464589",
        "设计模式": "6809640467731316749",
        "数据结构": "6809641166313619470"
    }),
    "前端": bidict({
        "前端": "6809640407484334093",
        "JavaScript": "6809640398105870343",
        "Vue.js": "6809640369764958215",
        "CSS": "6809640394175971342",
        "React.js": "6809640357354012685",
        "算法": "6809640499062767624",
        "面试": "6809640404791590919",
        "TypeScript": "6809640543006490638",
        "Node.js": "6809640361531539470",
        "Webpack": "6809640528267706382",
        "Flutter": "6809641090145058824",
        "微信小程序": "6809640653266354190",
        "LeetCode": "6809641039037464589",
        "HTML": "6809640392770715656",
        "浏览器": "6809640625856577549"
    }),
    "Android": bidict({
        "Android": "6809640400832167949",
        "前端": "6809640407484334093",
        "Flutter": "6809641090145058824",
        "Kotlin": "6809640615584727053",
        "Android Jetpack": "6809641107346063368",
        "Java": "6809640445233070094",
        "架构": "6809640501776482317",
        "iOS": "6809640399544516616",
        "音视频开发": "6931165776812441614",
        "面试": "6809640404791590919",
        "源码": "6809640684354535432",
        "算法": "6809640499062767624",
        "鸿蒙OS": "6809641209204572174",
        "设计模式": "6809640467731316749",
        "后端": "6809640408797167623"
    }),
    "iOS": bidict({
        "iOS": "6809640399544516616",
        "前端": "6809640407484334093",
        "Swift": "6809640463633481741",
        "Objective-C": "6809640410084802573",
        "面试": "6809640404791590919",
        "Flutter": "6809641090145058824",
        "SwiftUI": "6809641204351926286",
        "Xcode": "6809640513700888584",
        "逆向": "6809640709902041101",
        "macOS": "6809640683003969543",
        "架构": "6809640501776482317",
        "RxSwift": "6809640648812003341",
        "音视频开发": "6931165776812441614",
        "算法": "6809640499062767624",
        "CocoaPods": "6809640966522142728"
    }),
    "人工智能": bidict({
        "人工智能": "6809640642101116936",
        "Python": "6809640448827588622",
        " 深度学习": "6809640679082295303",
        "MATLAB": "6809641002253418510",
        "机器学习": "6809640525595934734",
        "算法": "6809640499062767624",
        "后端": "6809640408797167623",
        "NLP": "6809640930740535303",
        "数据分析": "6809641053432315911",
        "计算机视觉": "6809640711177109517",
        "数据挖掘": "6809640526904557582",
        "机器人": "6809640586598055943",
        "大数据": "6809641131131797511",
        "神经网络": "6809641023665356814",
        "物联网": "6809640581501812743"
    }),
    "开发工具": bidict({
        "GitHub": "6809640375880253447",
        "前端": "6809640407484334093",
        "后端": "6809640408797167623",
        "Git": "6809640373774712840",
        "Unity3D": "6809640568071651336",
        "开源": "6809640419505209358",
        "Linux": "6809640385980137480",
        "Docker": "6809640396788858887",
        "Java": "6809640445233070094",
        "设计": "6809640406058270733",
        "Photoshop": "6809640552590639111",
        "动效": "6809640562514198535",
        "增强现实": "6809640606239981581",
        "程序员": "6809640482725953550",
        "爬虫": "6809640700968173576"
    }),
    "代码人生": bidict({
        "算法": "6809640499062767624",
        "Python": "6809640448827588622",
        "程序员": "6809640482725953550",
        "LeetCode": "6809641039037464589",
        "Java": "6809640445233070094",
        "后端": "6809640408797167623",
        "前端": "6809640407484334093",
        "测试": "6809640427465998350",
        "面试": "6809640404791590919",
        "Linux": "6809640385980137480",
        "设计模式": "6809640467731316749",
        "JavaScript": "6809640398105870343",
        "C++": "6809640447497994253",
        "GitHub": "6809640375880253447",
        "数据结构": "6809641166313619470"
    }),
    "阅读": bidict({
        "笔记": "6809641211075231751",
        "前端": "6809640407484334093",
        "云原生": "6809641127432421384",
        "Kubernetes": "6809640675944955918",
        "测试": "6809640427465998350",
        "算法": "6809640499062767624",
        "后端": "6809640408797167623",
        "JavaScript": "6809640398105870343",
        "程序员": "6809640482725953550",
        "黑客": "6809640516439769095",
        "云计算": "6809640508441231367",
        "大数据": "6809641131131797511",
        "音视频开发": "6931165776812441614",
        "C++": "6809640447497994253",
        "数据库": "6809640600502009863"
    })
}


class JuejinError(Exception):
    """JuejinError is raised when the response from Juejin is not 200 OK."""
    pass


def raise_error(err_code, err_msg=""):
    """Raise JuejinError with the given error code and error message."""
    if err_msg == "":
        err_msg = "<no message>"
    raise JuejinError(f"error {err_code}: {err_msg}")


def escape_markdown(text):
    """Escape all characters that bring special meanings in markdown."""
    to_escape = ["_", "*", "[", "]", "(", ")", "~", "`", ">", "#", "+", "-", "=", "|", "{", "}", ".", "!"]
    for char in to_escape:
        text = text.replace(char, "\\" + char)
    return text


def login_required(f):
    """Decorator, check if Juejin session ID is set."""

    def _wrapper(*args, **kwargs):
        if cookie is None:
            raise JuejinError("not authenticated")
        return f(*args, **kwargs)

    return _wrapper


def response_post_check(wrapped=None, return_keys=("data",)):
    """Decorator, check error code and extract data from response."""

    def _decorator(f):
        def _wrapper(*args, **kwargs):
            ret_json = f(*args, **kwargs)
            if ret_json["err_msg"] != "success":
                raise_error(ret_json["err_no"], ret_json["err_msg"])

            if len(return_keys) == 1:
                return ret_json[return_keys[0]]
            ret_list = []
            for key in return_keys:
                ret_list.append(ret_json[key])
            return ret_list

        return _wrapper

    if wrapped:
        return _decorator(wrapped)
    else:
        return _decorator
