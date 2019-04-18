# 通过九价HPV疫苗摇号练习程序学习 Python 编程

最近9价HPV疫苗一直是热门的稀缺资源，很多地区都通过预约摇号的方式开展接种。称这个机会通过尝试用Python实现功能，比如身份证号的生成与验证，随机数的分配等。学习语言最好的方式是实践，从小项目开始可以快速完成，Python编程的快感就在与此。

利用 Python 的一些网络开发框架比如 Django 很快就建立信息录入的前台界面和后台管理；通过注册的身份证信息，随机选取很容易实现；当然前提我们要测试程序的话，最好以一部分身份证数据来模拟程序。9价疫苗是有年龄限制的，另外有一些地区也有区域接种限制。加入200个接种名额，我们计划抽取400个，按照顺序判断身份证是否正确，年龄是否符合，性别是否为女性等。

## 1. 生成一定数量的随机身份证号

### 1.1 检测身份证最后一位是否正确

**身份证的规则**
1. 将身份证号码前17位数分别乘以不同的系数，从第1位到第17位的系数分别为：`7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2`
2. 将得到的17个乘积相加。
3. 将相加后的和除以11并得到余数。
4. 余数为其对应的身份证最后一位校验码，按照0-10顺序为`1, 0, X, 9, 8, 7, 6, 5, 4, 3, 2`

身份证规则也可以参考[这里](https://github.com/jayknoxqu/id-number-util)

```python
def check_last_num(id):
    """
    检测身份证最后一位数字是否正确，如果正确返回True，错误则返回False
    """
    # id 是一个数字，要以列表操作先将其转换成字符串
    a = str(id)
    b = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    c = [1, 0, "X", 9, 8, 7, 6, 5, 4, 3, 2]
    # 最后一位的计算规则
    # 通过lambda表达式一行获得计算结果，不过语义不明确，也可以用for循环实现，比较易读。
    # 总想着减少行数写python是一种病
    r = list(map(lambda x, y: int(x) * y, list(a), b))
    if str(c[sum(r) % 11]) == a[17]:
        return True
    return False
```

### 1.2 批量生成身份证

```python
import random
import time

def digit_1to6():
    """身份证前六位"""
    # 假设报名的都是杭州地区的身份证，前六位号码：
    first_list = [
        '330102', # 上城区
        '330103', # 下城区
        '330104', # 江干区
        '330105', # 拱墅区
        '330106', # 西湖区
        '330108', # 滨江区
        '330109', # 萧山区
        '330110', # 余杭区
        '330122', # 桐庐县
        '330127', # 淳安县
        '330181', # 萧山区
        '330182', # 建德市
        '330183', # 富阳市
        '330184', # 余杭区
        '330185'  # 临安市
    ]
    return random.choice(first_list)

def digit_7to14(start=(1948, 1, 1, 0, 0, 0, 0, 0, 0), 
    end=(2018, 12, 31, 23, 59, 59, 0, 0, 0)):
    """
    随机生成8位日期
    """
    # 生成开始时间戳，首批身份证从1948年开始。
    start = time.mktime(start)
    # 生成结束时间戳，设置为2018-12-31截至	
    end = time.mktime(end)
    rand_t = time.localtime((end - start) * random.random() + start)
    # 将时间元组转成格式化字符串
    return time.strftime("%Y%m%d", rand_t)

def digit_15to17():
    """
    生成身份证15到17位数字
    """
    # 后面序号低于相应位数，前面加上0填充
    # 身份证号17位必须是偶数
    num = random.randrange(0, 999, 2)
    if num < 10:
        num = '00' + str(num)
    elif 9 < five < 100:
        num = '0' + str(num)
    else:
        num = str(num)
    return num

def digit_18(id):
    """
    根据前17位数字计算获得身份证最后一位数字
    """
    a = list(id)
    b = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    c = [1, 0, "X", 9, 8, 7, 6, 5, 4, 3, 2]
    r = list(map(lambda x, y: int(x) * y, a, b))
    return str(c[sum(r)%11])

def simulate_ids(num):
    """
    模拟生成一定数量的身份证号
    """
    ids = []
    if num > 0:
	    for i in range(1, num+1):
		    id_raw = digit_1to6() + digit_7to14() + digit_15to17()
		    id = id_raw + digit_18(id_raw)
		    ids.append(id)
	else:
	    return False
	return ids

# 生成10000个身份证号，保存到文件 ids.txt 中
ids = simulate_ids(10000)
#
if ids:
	with open("sim_ids.txt", w) as f:
	    f.write("\n".join(ids))
else:
	print("please type correct simulate id number")	    
```

## 2. 随机抽取一定数量的身份证

第一部分的代码获得了10000个身份证号，我们打算从中间抽取一定数量的身份证。

```python
# 先随机将身份证进行随机排序
# 这一步不是必须，主要目的是学习一下shuffle函数还是
for i in range(100):
    random.shuffle(ids)

# 抽选200个数量的身份证
result_ids = random.sample(id_list, 200)
```

## 3. 验证身份证的年龄是否符合

```python
def check_id_for_hpv(id):
    """
    检测身份证号是否符合要求
    """
    # 检测性别, 17位数字应为偶数
    id = str(id)
    if int(id[17]) % 2 != 0:
        print("Only Femail available")
        return False
    # 检测年龄，9价HPV疫苗只适合9～26岁
    # 身份证年份设置为1993~2010
    # 考虑到疫苗有3针，要打半年，具体时间范围参考疾控中心解释。
    birth = int(id[6:9])
    if birth > 1992 and birth < 2010:
        status = 1
    else:
        status = 0
    return status
```

## 4. 完成脚本

最后引入 argparse 模块，使脚本接受参数。完成的脚本放在[这里]()，接下来要租用阿里云，建立web server，支持python后端，采用django开发框架实现前端和后端的网站功能对于数量的 pythoner 来说基本上一天就能完成。

最终我们模拟生成10000个身份证，随机选取400个，符合规定的有大约110个左右。这主要因为年龄是随机分布的，而26-9=17,大约是2018-1948=70的1/4，因此才会有这个结果。如果考虑到真实情况，注册时年龄不应是随机分布，可以考虑引入 numpy, scipy 等模块，使用 beta 分布，alpha=2, beta=5，起始年龄为6，最大年龄50，生成一个模拟年龄分布。

```python
from scipy import stats

def digit_7to10(a=2, b=5, min=6, max=50):
    """
    生成年龄beta分布
    """
    return str(2019 - int(stats.beta.rvs(a, b, min, max)))
```

按照顺序公布结果，其中包含的一些文本文件操作，在 shell 下利用 awk, sort 等工具即可。

```bash
# 脚本运行方式
$ python hpv.py -e 400 -p 200 -s 10000
$ python hpv.py --help
usage: hpy.py [-h] [-e EXTRACT] [-p PICK] [-s SIM] [-i INPUT]

optional arguments:
  -h, --help            show this help message and exit
  -e EXTRACT, --extract EXTRACT
                        How many id numbers extracted
  -p PICK, --pick PICK  How many id numbers picked
  -s SIM, --sim SIM     How many id numbers simulated
  -i INPUT, --input INPUT
                        input file
```
