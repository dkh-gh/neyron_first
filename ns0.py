
import json

def layerPew(nrDtIn, nr):
    for i in range(len(nr)):
        for j in range(len(nr[i]["in"])):
            nr[i]["in"][j] = nrDtIn[j]
        nr[i]["out"] = sum([nr[i]["in"][q]*nr[i]["weights"][q] for q in range(len(nr[i]["in"]))])

def correct(lvl, ans, nr):
    learnK = 0.3
    if lvl > 0:
        nr["error"] = ans - nr["out"]
        print('E:',lvl, nr["error"])
        for i in range(len(nr["in"])):
            nr["in"][i]
    

fnameDataIn = input("файл для обучения [dataIn.db]: ")
if fnameDataIn == "": fnameDataIn = "dataIn.db"
fnameData = input("файл нейросети [data.db]: ")
if fnameData == "": fnameData = "data.db"
fnameDataLogs = input("файл для логов [dataLogs.db]: ")
if fnameDataLogs == "": fnameDataLogs = "dataLogs.db"

print("Загрузка данных...")
data = json.loads(open(fnameDataIn).read())
print("  данных обучения:", len(data["learn"]))
neyro = json.loads(open(fnameData).read())
print("  слоёв:", len(neyro["neyrons"]))

workMod = input("Режим работы (0-прервать, [1]-до прерывания, 2-NOTSET, 3-NOTSET): ")
if workMod != "": workMod = int(workMod)
else: workMod = 1

input("  [Нажмите Ввод для запуска обучения. CTRL+C - прервать]")

dataLearnNum = 0
while workMod > 0:
    try:
        layerPew(
            [data["learn"][dataLearnNum]["out"][i] for i in range(len(data["learn"][dataLearnNum]["out"]))],
            neyro["neyrons"][0])
        layerPew(
            [neyro["neyrons"][0][i]["out"] for i in range(len(neyro["neyrons"][0]))],
            neyro["neyrons"][1])
        layerPew(
            [neyro["neyrons"][1][i]["out"] for i in range(len(neyro["neyrons"][1]))],
            neyro["neyrons"][2])
        correct(2, data["learn"][dataLearnNum]["ansver"][0], neyro["neyrons"][2][0])
        correct(2, data["learn"][dataLearnNum]["ansver"][1], neyro["neyrons"][2][1])
        
        print(neyro["neyrons"][2][0]["out"], neyro["neyrons"][2][1]["out"], "/", data["learn"][dataLearnNum]["ansver"][0], data["learn"][dataLearnNum]["ansver"][1])
        dataLearnNum += 1
        if dataLearnNum >= len(data["learn"]): dataLearnNum = 0
        
        
    except KeyboardInterrupt:
        workMod = input("Режим работы (0-прервать, [1]-до прерывания, 2-NOTSET, 3-NOTSET): ")
        if workMod != "": workMod = int(workMod)
        else: workMod = 1
print("Сохранение состояния нейронки.")
neyroFile = open(fnameData, "w")
neyroFile.write(json.dumps(neyro))
print("Выход.")
