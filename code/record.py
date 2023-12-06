import csv
def writeCsv(result, kinds):
    names = ["kitchen","others","recycle","harmful"]
    if result == 0.0 or result == 1.0 or result == 3.0:
        key=2
        kinds[2] += 1
        name=names[2]
    elif result == 5.0 or result == 6.0 or result == 9.0:
        key=3
        kinds[3] += 1
        name=names[3]
    elif result == 4.0 or result == 10.0 or result == 11.0:
        key=0
        kinds[0] += 1
        name=names[0]
    elif result == 2.0 or result == 8.0 or result == 7.0:
        key=1
        kinds[1] += 1
        name=names[1]
    kinds[0] = kinds[0] + 1

    # 写入结果        
    with open("/home/mebius/workspace/yolov5/expression.csv", 'a', newline='') as csv_file:
        filenames=['Total','Kinds','Numbers','Success']
        writer=csv.DictWriter(csv_file,fieldnames=filenames)
        writer.writerow({'Total':f"{kinds[0]}",'Kinds':f"{name}",'Numbers':f"{kinds[key]}",'Success':" OK! "})
    
    return kinds