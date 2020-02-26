Python下有许多款不同的 Web 框架。Django是重量级选手中最有代表性的一位。许多成功的网站和APP都基于Django。

Django是一个开放源代码的Web应用框架，由Python写成。

Django遵守BSD版权，初次发布于2005年7月, 并于2008年9月发布了第一个正式版本1.0 。

Django采用了MVC的软件设计模式，即模型M，视图V和控制器C。



Django 版本对应的 Python 版本：
Django版本 	Python 版本
1.8 	    2.7, 3.2 , 3.3, 3.4, 3.5
1.9,1.10 	2.7, 3.4, 3.5
1.11 	    2.7, 3.4, 3.5, 3.6
2.0 	    3.4, 3.5, 3.6, 3.7
2.1,2.2	    3.5, 3.6, 3.7




# Linux 上安装 Django

pip install Django
pip3 install django==1.8.2




# 创建第一个项目

使用 django-admin 来创建 HelloWorld 项目：

django-admin startproject HelloWorld

创建完成后我们可以查看下项目的目录结构：

$ cd HelloWorld/
$ tree
.
|-- HelloWorld
|   |-- __init__.py
|   |-- settings.py
|   |-- urls.py
|   `-- wsgi.py
`-- manage.py


目录说明：
    HelloWorld: 项目的容器。
    manage.py: 一个实用的命令行工具，可让你以各种方式与该 Django 项目进行交互。
    HelloWorld/__init__.py: 一个空文件，告诉 Python 该目录是一个 Python 包。
    HelloWorld/settings.py: 该 Django 项目的设置/配置。
    HelloWorld/urls.py: 该 Django 项目的 URL 声明; 一份由 Django 驱动的网站"目录"。
    HelloWorld/wsgi.py: 一个 WSGI 兼容的 Web 服务器的入口，以便运行你的项目。

接下来我们进入 HelloWorld 目录输入以下命令，启动服务器：

python3 manage.py runserver 0.0.0.0:8000

0.0.0.0 让其它电脑可连接到开发服务器，8000 为端口号。如果不说明，那么端口号默认为 8000。

在浏览器输入你服务器的 ip（这里我们输入本机 IP 地址： 127.0.0.1:8000） 及端口号，如果正常启动，输出结果如下：




# 常用命令
python manage.py <command> [options]  #Django Command python manange.py -h帮助文档
django-admin.py startproject my_blog  #创建项目
python manage.py startapp article  #创建app


#　出错处理
１、django.core.exceptions.DisallowedHost: Invalid HTTP_HOST header: '0.0.0.0:80
原因在于在项目目录下的settting.py有个字段：ALLOWED_HOSTS = []，表示允许访问的主机，对应的值为空，则表示不允许所有的主机访问该服务器。
需要修改该字段的值为：ALLOWED_HOSTS = ['*']，设置允许所有主机都可以访问


# 项目中如果代码有改动，服务器会自动监测代码的改动并自动重新载入，所以如果你已经启动了服务器则不需手动重启



# path() 函数

Django path() 可以接收四个参数，分别是两个必选参数：route、view 和两个可选参数：kwargs、name。
语法格式：

path(route, view, kwargs=None, name=None)

    route: 字符串，表示 URL 规则，与之匹配的 URL 会执行对应的第二个参数 view。
    view: 用于执行与正则表达式匹配的 URL 请求。
    kwargs: 视图使用的字典类型的参数。
    name: 用来反向获取 URL。

Django2. 0中可以使用 re_path() 方法来兼容 1.x 版本中的 url() 方法，一些正则表达式的规则也可以通过 re_path() 来实现 。

from django.urls import include, re_path

urlpatterns = [
    re_path(r'^index/$', views.index, name='index'),
    re_path(r'^bio/(?P<username>\w+)/$', views.bio, name='bio'),
    re_path(r'^weblog/', include('blog.urls')),
    ...
]










# Django 模板标签

## if/else 标签
基本语法格式如下：
{% if condition %}
     ... display
{% endif %}
或者：
{% if condition1 %}
   ... display 1
{% elif condition2 %}
   ... display 2
{% else %}
   ... display 3
{% endif %}

根据条件判断是否输出。if/else 支持嵌套。

{% if %} 标签接受 and ， or 或者 not 关键字来对多个变量做判断 ，或者对变量取反（ not )，例如：

{% if athlete_list and coach_list %}
     athletes 和 coaches 变量都是可用的。
{% endif %}


## for 标签
{% for %} 允许我们在一个序列上迭代。

与Python的 for 语句的情形类似，循环语法是 for X in Y ，Y是要迭代的序列而X是在每一个特定的循环中使用的变量名称。

每一次循环中，模板系统会渲染在 {% for %} 和 {% endfor %} 之间的所有内容。
例如，给定一个运动员列表 athlete_list 变量，我们可以使用下面的代码来显示这个列表：
<ul>
{% for athlete in athlete_list %}
    <li>{{ athlete.name }}</li>
{% endfor %}
</ul>

给标签增加一个 reversed 使得该列表被反向迭代：

{% for athlete in athlete_list reversed %}
...
{% endfor %}

可以嵌套使用 {% for %} 标签：

{% for athlete in athlete_list %}
    <h1>{{ athlete.name }}</h1>
    <ul>
    {% for sport in athlete.sports_played %}
        <li>{{ sport }}</li>
    {% endfor %}
    </ul>
{% endfor %}

ifequal/ifnotequal 标签

{% ifequal %} 标签比较两个值，当他们相等时，显示在 {% ifequal %} 和 {% endifequal %} 之中所有的值。

下面的例子比较两个模板变量 user 和 currentuser :

{% ifequal user currentuser %}
    <h1>Welcome!</h1>
{% endifequal %}

和 {% if %} 类似， {% ifequal %} 支持可选的 {% else%} 标签：8

{% ifequal section 'sitenews' %}
    <h1>Site News</h1>
{% else %}
    <h1>No News Here</h1>
{% endifequal %}


## 注释标签

Django 注释使用 {# #}。

{# 这是一个注释 #}

## 过滤器

模板过滤器可以在变量被显示前修改它，过滤器使用管道字符，如下所示：

{{ name|lower }}

{{ name }} 变量被过滤器 lower 处理后，文档大写转换文本为小写。

过滤管道可以被* 套接* ，既是说，一个过滤器管道的输出又可以作为下一个管道的输入：

{{ my_list|first|upper }}

以上实例将第一个元素并将其转化为大写。

有些过滤器有参数。 过滤器的参数跟随冒号之后并且总是以双引号包含。 例如：

{{ bio|truncatewords:"30" }}

这个将显示变量 bio 的前30个词。

其他过滤器：
    addslashes : 添加反斜杠到任何反斜杠、单引号或者双引号前面。
    date : 按指定的格式字符串参数格式化 date 或者 datetime 对象，实例：
    {{ pub_date|date:"F j, Y" }}
    length : 返回变量的长度。


# include 标签

{% include %} 标签允许在模板中包含其它的模板的内容。

下面这个例子都包含了 nav.html 模板：

{% include "nav.html" %}



