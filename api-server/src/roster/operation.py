dict1 = [
    {
        "id": 2,
        "time": "2021-06-06T18:16:24.600668-04:00",
        "count": 54,
        "munition": 4,
        "operation": 1,
        "squadron": 1
    },
    {
        "id": 3,
        "time": "2021-06-06T18:16:44.506231-04:00",
        "count": -2,
        "munition": 4,
        "operation": 1,
        "squadron": 1
    },
    {
        "id": 4,
        "time": "2021-06-06T18:16:55.564833-04:00",
        "count": -2,
        "munition": 4,
        "operation": 1,
        "squadron": 1
    }
]
dict2 = {}
for x in dict1:
    for key in dict2:
        if x['munition'] in dict1:
            dict2[key] = dict2[key] + dict1[key]
        else:
            pass

print(dict2)


