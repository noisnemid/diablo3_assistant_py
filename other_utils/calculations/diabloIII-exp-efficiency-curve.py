def test(baseLvl, baseLvlTime, testLvl, testLvlTime, keyTimeCost=30):
    '''
    :args:  complete the BaseLvl GR during time of baseLvlTime, while complete the testLvl in testLvlTime, unit=second
            keyTimeCost: the time how much it costs you to gain a GR key stone
    :return: efficiency
    '''

    # 每层经验综合增益
    # 数据来源：http://bbs.d.163.com/forum.php?mod=viewthread&tid=173218346
    # 《暗黑三2.4.1版大秘境数据 150层基础奖励数据一览》
    
    factor = 1.05

    t = factor**(testLvl - baseLvl) / ((testLvlTime + keyTimeCost)/(baseLvlTime+keyTimeCost))
    t = float(f'{t:.2f}')

    return t


# 各层完成时间，单位：秒
data = [
    # [85, 90],
    [90, 90],
    [95, 120],
    [100, 120],
    [105, 150],
    [107, 155],
    [108, 134],
    [110, 180],
    [113, 250],
    [114, 270],
    [115, 330],
    [118, 400],
    [124, 900],
]

for d in data:
    r1 = test(data[0][0], data[0][1], d[0], d[1])
    r2 = test(data[0][0], data[0][1], d[0], d[1], keyTimeCost=0)
    d.append(r1)
    d.append(r2)
    print(d)

res = tuple(sorted(data, key=lambda x: x[2]))
bestLvl = res[-1][0]

print(f'最速层：{bestLvl}')

# 极值 即为 最有效率层
