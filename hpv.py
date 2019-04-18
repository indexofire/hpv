#!/usr/bin/env python
################################################################################
# 使用方法：
# python hpv.py -e 400 -p 200 -s 10000
#
# <indexofire@gmail.com>
################################################################################
import time
import random
import argparse
from scipy import stats


parser = argparse.ArgumentParser()
parser.add_argument('-e', '--extract', type=int, default=400,
    help='How many id numbers extracted')
parser.add_argument('-p', '--pick', type=int, default=200,
    help='How many id numbers picked')
parser.add_argument('-s', '--sim', type=int, default=10000,
    help='How many id numbers simulated')
parser.add_argument('-i', '--input', help="input file")
args = parser.parse_args()

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

def digit_7to10(a=2, b=5, min=6, max=50):
    """
    生成年龄beta分布
    """
    return str(2019 - int(stats.beta.rvs(a, b, min, max)))

def digit_11to14(start=(1948, 1, 1, 0, 0, 0, 0, 0, 0),
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
    return time.strftime("%m%d", rand_t)

def digit_15to17():
    """
    生成身份证15到17位数字
    """
    # 后面序号低于相应位数，前面加上0填充
    # 身份证号17位必须是偶数
    num = random.randrange(0, 999, 2)
    if num < 10:
        num = '00' + str(num)
    elif 9 < num < 100:
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
		    id_raw = digit_1to6() + digit_7to10() + digit_11to14() + digit_15to17()
		    id = id_raw + digit_18(id_raw)
		    ids.append(id)
    else:
	    return False
    return ids

def check_id_for_hpv(id):
    """
    检测身份证号是否符合要求
    """
    # 检测性别, 17位数字应为偶数
    id = str(id)
    if int(id[16]) % 2 != 0:
        print("Only Femail available")
        return False
    # 检测年龄，9价HPV疫苗只适合9～26岁
    # 身份证年份设置为1993~2010
    # 考虑到疫苗有3针，要打半年，具体时间范围参考疾控中心解释。
    birth = int(id[6:10])
    if birth > 1992 and birth < 2010:
        return True
    else:
        return False

def main():
    """
    调用函数
    """
    # 生成--sim个身份证号，保存到文件 ids.txt 中
    if args.sim:
        ids = simulate_ids(args.sim)
        if ids:
	        with open("ids.txt", "w") as f:
	            f.write("\n".join(ids))
    elif args.input:
        with open(args.input, "r") as f:
            ids = f.readlines()
    else:
	    print("please type correct simulate id number")

    # 打乱列表
    for i in range(100):
        random.shuffle(ids)

    # 抽选一定个数量的身份证
    result_ids = random.sample(ids, args.extract)
    check = 0
    last_ids = []
    for id in result_ids:
        if check == args.pick:
            break
        if check_id_for_hpv(id):
            check += 1
            print(id+"\n")
            last_ids.append(id)

    print("total right id number is %d" % len(last_ids))

    with open("last_ids.txt", "w") as f:
	       f.write("\n".join(last_ids))


if __name__ == "__main__":
    main()
