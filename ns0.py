
import json

def lim(dt, mn, mx):
    if dt < mn: dt = mn
    if dt > mx: dt = mx
    return dt

def layerPew(lr, nrDtIn, neyr):
    if lr == 0:
        for i in range(len(neyr)):
            neyr[i]["in"] = neyr[i]["out"] = nrDtIn[i]
    else:
        for nr in neyr: # перебор нейронов
            for i in range(len(nrDtIn)): # запись входов
                nr["in"][i] = nrDtIn[i]
                nr["out"] = sum([(nr["in"][i]-.5) * nr["weights"][i] for i in range(len(nr["weights"]))]) / len(nr["weights"])
                nr["out"] = lim(nr["out"], 0, 1)
                #print('O:', nr["out"])
        
def correct(lvl, ans, nr):
    learnK = 0.3
    if lvl > 0:
        nr["error"] = ans - nr["out"]
        nr["error"] = lim(nr["error"], -1, 1)
        if lvl == 2: print('E:', nr["error"], "[", ans, ":", nr["out"], "]")
        for i in range(len(nr["in"])):
            nr["weights"][i] += nr["error"]*learnK * ((nr["in"][i]-.5))
            nr["weights"][i] = lim(nr["weights"][i], -1, 1)
            nr["in"][i] -= nr["error"]*learnK * ((nr["in"][i]-.5)*-1)
            nr["in"][i] = lim(nr["in"][i], 0, 1)
            correct(lvl-1, nr["in"][i], neyro["neyrons"][lvl-1][i])
            
    

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

workMod = input("Режим работы (0-прервать, [1]-до прерывания, 2-количество итераций, 3-NOTSET): ")
if workMod != "": workMod = int(workMod)
else:
    workMod = 1
    i = 0
if workMod == 2:
    i = int(input("  количество итераций: "))

input("  [Нажмите Ввод для запуска обучения. CTRL+C - прервать]")

dataLearnNum = 0
while workMod > 0:
    try:
        print(i)
        layerPew(0,
            [data["learn"][dataLearnNum]["out"][i] for i in range(len(data["learn"][dataLearnNum]["out"]))],
            neyro["neyrons"][0])
        layerPew(1,
            [neyro["neyrons"][0][i]["out"] for i in range(len(neyro["neyrons"][0]))],
            neyro["neyrons"][1])
        layerPew(2,
            [neyro["neyrons"][1][i]["out"] for i in range(len(neyro["neyrons"][1]))],
            neyro["neyrons"][2])
        print("  Корректировка нейрона 1: ")
        correct(2, data["learn"][dataLearnNum]["ansver"][0], neyro["neyrons"][2][0])
        print("  Корректировка нейрона 2: ")
        correct(2, data["learn"][dataLearnNum]["ansver"][1], neyro["neyrons"][2][1])
        
        #print(neyro["neyrons"][2][0]["out"], neyro["neyrons"][2][1]["out"], "/", data["learn"][dataLearnNum]["ansver"][0], data["learn"][dataLearnNum]["ansver"][1])
        dataLearnNum += 1
        if dataLearnNum >= len(data["learn"]): dataLearnNum = 0
        if workMod == 1: i += 1
        elif workMod == 2:
            i -= 1
            if i <= 0: break
        
        
    except KeyboardInterrupt:
        workMod = input("Режим работы (0-прервать, [1]-до прерывания, 2-количество итераций, 3-NOTSET): ")
        if workMod != "": workMod = int(workMod)
        else:
            workMod = 1
        if workMod == 2:
            i = int(input("  количество итераций: "))
print("Сохранение состояния нейронки.")
neyroFile = open(fnameData, "w")
neyroFile.write(json.dumps(neyro))
neyroFile.close()
print("Выход.")
