import EntityDef
import random
import pygame

# costanti
probNoChild = 0.2
probVariation = 0.01
probTryToAcc = 0.01 # al giorno
probRandomDeath = 0.0000005 # ogni entità ogni giorno # da moltipliare con il num di entità
entitySpeed = 1 # px/day
initialEntity = 100
dayToXratio = 10 # ogni quanti giorni aggiornar i grafici
XtoPxRatio = 3.50

# variabili
myEntity = []
year = 0
day = 0
Xgraph = 0
contTotalEntity = 0
contDeadEntity = 0

def accoppiamento(p1,p2):
    randomNum = random.random()
    if randomNum < probNoChild:
        return
    DNA1 = p1.getDNA()
    DNA2 = p2.getDNA()
    if random.randint(0,1) == 0:
        DNAfiglio = [DNA1[0], DNA2[1], DNA1[2], DNA2[3], DNA1[4]]
    else:
        DNAfiglio = [DNA2[0], DNA1[1], DNA2[2], DNA1[3], DNA2[4]]
    if random.random() < probVariation:
        i = random.randint(0,4)
        if i <= 2:
            DNAfiglio[i] = random.randint(0,255)
        elif i == 3:
            DNAfiglio[3] = random.randint(1,3)
        elif i == 4:
            DNAfiglio[4] = random.randint(0,1)
    figlio = EntityDef.entity("id_"+str(len(myEntity)) , (p1.getName(),p2.getName()), DNAfiglio, 0, random.randint(450,1150), random.randint(565,1065))
    myEntity.append(figlio)
    global contTotalEntity
    contTotalEntity += 1

def ProbAccoppiamento(p1,p2):
    prob = 0
    if abs(p1.getAge() - p2.getAge()) > 8:
        return prob
    prob = random.randint(20, 70)
    if p1.getColor() == p2.getColor():
        prob += 10
    if p1.getSize() == 3 or p2.getSize() == 3:
        prob += 10
    if p1.getShape() != p2.getShape():
        prob -= 10
    return prob

def newDay():
    global year
    global day
    global contDeadEntity
    day += 1
    if day % dayToXratio == 0:
        global Xgraph
        Xgraph += 1 * XtoPxRatio
    if day % 365 == 0:
        year += 1
        day = 0
    for i in myEntity:
        if random.random() < probRandomDeath*len(myEntity):
            myEntity.remove(i)
            contDeadEntity += 1
            continue
        if i.getOlder() == False:
            myEntity.remove(i)
            contDeadEntity += 1
            continue

def selectCouple():
    HornyEntity = []
    for i in myEntity:
        if i.getAge() > 18 and i.getAge() < 55:
            if random.random() < probTryToAcc:
                HornyEntity.append(i)

    if len(HornyEntity) < 2:
        return
    for e in HornyEntity:
        e2 = random.choice(HornyEntity)
        if e == e2:
            continue
        if ProbAccoppiamento(e, e2) > random.randint(0,100):
            accoppiamento(e, e2)
        HornyEntity.remove(e)
        HornyEntity.remove(e2)

def updatePos(e):
    if e.x > 450 and e.x < 1150 and e.y > 565 and e.y < 1065:
        e.x += random.randint(-entitySpeed, entitySpeed)/2
        e.y += random.randint(-entitySpeed, entitySpeed)/2
    else:
        if e.x <= 450:
            e.x += entitySpeed
        elif e.x >= 1150:
            e.x -= entitySpeed
        if e.y <= 565:
            e.y += entitySpeed
        elif e.y >= 1065:
            e.y -= entitySpeed

# inizializza le entità
for i in range(initialEntity):
    DNA = [random.randint(0,255), random.randint(0,255), random.randint(0,255), random.randint(1,3), random.randint(0,1)]
    myEntity.append(EntityDef.entity("id_"+str(i), None, DNA, random.randint(0,100),random.randint(450,1150), random.randint(565,1065)))
contTotalEntity = len(myEntity)

pygame.init()
screen = pygame.display.set_mode((1600, 1200))
pygame.display.set_caption("Genetic Evolution")
font = pygame.font.Font(None, 36)

# creazione finestra
screen.fill((0, 0, 0))
# campo centrale
screen.fill((4, 90, 137), (395, 510, 810, 610)) # border
screen.fill((15, 96, 9), (400, 515, 800, 600)) # field
# scritte sotto il campo
screen.blit(font.render("Year: " + str(year), True, (255, 255, 255)), (600, 1135))
screen.blit(font.render("Day: " + str(day), True, (255, 255, 255)), (825, 1135))
# grafico TL
screen.fill((4, 90, 137), (20, 510, 350, 300))
screen.fill((0, 0, 0), (23, 513, 344, 294))
screen.blit(font.render("Num. Entity:", True, (255, 255, 255)), (80, 480))
# grafico TR
screen.fill((4, 90, 137), (1230, 510, 350, 300))
screen.fill((0, 0, 0), (1233, 513, 344, 294))
screen.blit(font.render("Born/year:", True, (255, 255, 255)), (1290, 480))
# grafico BL
screen.fill((4, 90, 137), (20, 820, 350, 300))
screen.fill((0, 0, 0), (23, 823, 344, 294))
screen.blit(font.render("Born/Death:", True, (255, 255, 255)), (80, 1125))
# grafico BR
screen.fill((4, 90, 137), (1230, 820, 350, 300))
screen.fill((0, 0, 0), (1233, 823, 344, 294))
screen.blit(font.render("Death/year:", True, (255, 255, 255)), (1290, 1125))
# pulsanti sopra il campo
pauseButton = pygame.Rect(415, 450, 130, 50)
speed1Button = pygame.Rect(570, 450, 50, 50)
speed2Button = pygame.Rect(645, 450, 50, 50)
speed4Button = pygame.Rect(720, 450, 50, 50)
speed10Button = pygame.Rect(795, 450, 50, 50)

pygame.display.flip()

# variabili per il controllo del tempo
clock = pygame.time.Clock()
FPS = 60
dt = 0

# variabili per il controllo del gioco
running = True
paused = False
speed = 1

# variabii per i grafici 
TLOldValues = [[0, 0]]
TLmoltY = 1
TLminusX = 0
TROldValues = [[0, 0]]
TRmoltY = 1
TRminusX = 0
BLOldValues = [[0, 0]]
BLmoltY = 1
BLminusX = 0
BROldValues = [[0, 0]]
BRmoltY = 1
BRminusX = 0

while running:
    
    # gestione degli eventi
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pauseButton.collidepoint(event.pos):
                paused = not paused
            if speed1Button.collidepoint(event.pos):
                speed = 1
            if speed2Button.collidepoint(event.pos):
                speed = 2
            if speed4Button.collidepoint(event.pos):
                speed = 4
            if speed10Button.collidepoint(event.pos):
                speed = 10
    if paused:
        pygame.draw.rect(screen, (60, 60, 60), pauseButton)
    else:
        pygame.draw.rect(screen, (100, 100, 100), pauseButton)
    if speed == 1:
        pygame.draw.rect(screen, (60, 60, 60), speed1Button)
        pygame.draw.rect(screen, (100, 100, 100), speed2Button)
        pygame.draw.rect(screen, (100, 100, 100), speed4Button)
        pygame.draw.rect(screen, (100, 100, 100), speed10Button)
    elif speed == 2:
        pygame.draw.rect(screen, (100, 100, 100), speed1Button)
        pygame.draw.rect(screen, (60, 60, 60), speed2Button)
        pygame.draw.rect(screen, (100, 100, 100), speed4Button)
        pygame.draw.rect(screen, (100, 100, 100), speed10Button)
    elif speed == 4:
        pygame.draw.rect(screen, (100, 100, 100), speed1Button)
        pygame.draw.rect(screen, (100, 100, 100), speed2Button)
        pygame.draw.rect(screen, (60, 60, 60), speed4Button)
        pygame.draw.rect(screen, (100, 100, 100), speed10Button)
    elif speed == 10:
        pygame.draw.rect(screen, (100, 100, 100), speed1Button)
        pygame.draw.rect(screen, (100, 100, 100), speed2Button)
        pygame.draw.rect(screen, (100, 100, 100), speed4Button)
        pygame.draw.rect(screen, (60, 60, 60), speed10Button)
    elif speed == 100:
        pygame.draw.rect(screen, (100, 100, 100), speed1Button)
        pygame.draw.rect(screen, (100, 100, 100), speed2Button)
        pygame.draw.rect(screen, (100, 100, 100), speed4Button)
        pygame.draw.rect(screen, (100, 100, 100), speed10Button)
    screen.blit(font.render("Pause", True, (255, 255, 255)), (445, 462))
    screen.blit(font.render("1x", True, (255, 255, 255)), (580, 462))
    screen.blit(font.render("2x", True, (255, 255, 255)), (655, 462))
    screen.blit(font.render("4x", True, (255, 255, 255)), (730, 462))
    screen.blit(font.render("10x", True, (255, 255, 255)), (800, 462))

    # aggiornamento del gioco
    if not paused:
        clock.tick(FPS*speed)
        dt += 1000
        if dt > 1000:
            dt -= 1000
            newDay()
            selectCouple()  

        # creazione scritte e dati
        screen.fill((0, 0, 0), (0, 1125, 1600, 100))
        screen.blit(font.render("Year: " + str(year), True, (255, 255, 255)), (600, 1135))
        screen.blit(font.render("Day: " + str(day), True, (255, 255, 255)), (825, 1135))
        # grafico TL
        screen.fill((0, 0, 0), (80, 480, 300, 30))
        numEntity = len(myEntity)
        screen.blit(font.render("Num. Entity:"+ str(numEntity), True, (255, 255, 255)), (80, 480))
        # grafico TR
        screen.fill((0, 0, 0), (1290, 480, 300, 30))
        if year!=0:
            Bratio = (contTotalEntity-initialEntity)/year
            Bratio = int(Bratio*1000)/1000
        else:
            Bratio = (contTotalEntity-initialEntity)
        screen.blit(font.render("Born/year:"+ str(Bratio), True, (255, 255, 255)), (1290, 480))
        # grafico BL
        if contDeadEntity!=0:
            BDratio = (contTotalEntity-initialEntity)/contDeadEntity
            BDratio = int(BDratio*1000)/1000
        else:
            BDratio = 1
        screen.blit(font.render("Born/Death:"+ str(BDratio), True, (255, 255, 255)), (80, 1125))
        # grafico BR
        if year!=0:
            Dratio = contDeadEntity/year
            Dratio = int(Dratio*1000)/1000
        else:
            Dratio = contDeadEntity
        screen.blit(font.render("Death/year:"+ str(Dratio), True, (255, 255, 255)), (1290, 1125))

        # disegno grafici
        if day % dayToXratio == 0:
            # grafico TL
            TLy = numEntity-initialEntity
            TLy = -1*TLy
            # salvo i valori 
            if len(TLOldValues) >= 100:
                TLOldValues.pop(0)
                TLminusX = 1
            TLOldValues.append([TLy, Xgraph])

            TLmaxV = TLOldValues[0][0]
            TLminV = TLOldValues[0][0]
            for pt in TLOldValues:
                if pt[0] > TLmaxV:
                    TLmaxV = pt[0]
                if pt[0] < TLminV:
                    TLminV = pt[0]
            TLdV = max(abs(TLmaxV), abs(TLminV))
            if TLdV > 147:
                TLmoltY = TLdV/147
            else:
                TLmoltY = 1
            screen.fill((4, 90, 137), (20, 510, 350, 300))
            screen.fill((0, 0, 0), (23, 513, 344, 294))
            for i in range(len(TLOldValues)):
                if i > 0:
                    pygame.draw.line(screen, (255, 255, 255), (25+TLOldValues[i-1][1]-(Xgraph-340)*TLminusX, 660+TLOldValues[i-1][0]/TLmoltY), (25+TLOldValues[i][1]-(Xgraph-340)*TLminusX, 660+TLOldValues[i][0]/TLmoltY), 2)

            # grafico TR
            TRy = (Bratio-1)*50
            TRy = -1*TRy
            # salvo i valori 
            if len(TROldValues) >= 100:
                TROldValues.pop(0)
                TRminusX = 1
            TROldValues.append([TRy, Xgraph])

            TRmaxV = TROldValues[0][0]
            TRminV = TROldValues[0][0]
            for pt in TROldValues:
                if pt[0] > TRmaxV:
                    TRmaxV = pt[0]
                if pt[0] < TRminV:
                    TRminV = pt[0]
            TRdV = max(abs(TRmaxV), abs(TRminV))
            if TRdV > 147:
                TRmoltY = TRdV/147
            else:
                TRmoltY = 1
            screen.fill((4, 90, 137), (1230, 510, 350, 300))
            screen.fill((0, 0, 0), (1233, 513, 344, 294))
            for i in range(len(TROldValues)):
                if i > 0:
                    pygame.draw.line(screen, (255, 255, 255), (1235+TROldValues[i-1][1]-(Xgraph-340)*TRminusX, 730+TROldValues[i-1][0]/TRmoltY), (1235+TROldValues[i][1]-(Xgraph-340)*TRminusX, 730+TROldValues[i][0]/TRmoltY), 2)

            # grafico BL
            BLy = (BDratio-1)*50
            BLy = -1*BLy
            # salvo i valori 
            if len(BLOldValues) >= 100:
                BLOldValues.pop(0)
                BLminusX = 1
            BLOldValues.append([BLy, Xgraph])

            BLmaxV = BLOldValues[0][0]
            BLminV = BLOldValues[0][0]
            for pt in BLOldValues:
                if pt[0] > BLmaxV:
                    BLmaxV = pt[0]
                if pt[0] < BLminV:
                    BLminV = pt[0]
            BLdV = max(abs(BLmaxV), abs(BLminV))
            if BLdV > 147:
                BLmoltY = BLdV/147
            else:
                BLmoltY = 1
            screen.fill((4, 90, 137), (20, 820, 350, 300))
            screen.fill((0, 0, 0), (23, 823, 344, 294))
            for i in range(len(BLOldValues)):
                if i > 0:
                    pygame.draw.line(screen, (255, 255, 255), (25+BLOldValues[i-1][1]-(Xgraph-340)*BLminusX, 970+BLOldValues[i-1][0]/BLmoltY), (25+BLOldValues[i][1]-(Xgraph-340)*BLminusX, 970+BLOldValues[i][0]/BLmoltY), 2)

            # grafico BR
            BRy = (Dratio-1)*50
            BRy = -1*BRy
            # salvo i valori 
            if len(BROldValues) >= 100:
                BROldValues.pop(0)
                BRminusX = 1
            BROldValues.append([BRy, Xgraph])

            BRmaxV = BROldValues[0][0]
            BRminV = BROldValues[0][0]
            for pt in BROldValues:
                if pt[0] > BRmaxV:
                    BRmaxV = pt[0]
                if pt[0] < BRminV:
                    BRminV = pt[0]
            BRdV = max(abs(BRmaxV), abs(BRminV))
            if BRdV > 147:
                BRmoltY = BRdV/147
            else:
                BRmoltY = 1
            screen.fill((4, 90, 137), (1230, 820, 350, 300))
            screen.fill((0, 0, 0), (1233, 823, 344, 294))
            for i in range(len(BROldValues)):
                if i > 0:
                    pygame.draw.line(screen, (255, 255, 255), (1235+BROldValues[i-1][1]-(Xgraph-340)*BRminusX, 1040+BROldValues[i-1][0]/BRmoltY), (1235+BROldValues[i][1]-(Xgraph-340)*BRminusX, 1040+BROldValues[i][0]/BRmoltY), 2)


        # disegno a schermo
        screen.fill((15, 96, 9), (400, 515, 800, 600))
        if len(myEntity) == 0:
            paused = True
            screen.blit(font.render("All entities are dead", True, (255, 255, 255)), (700, 600))
        for e in myEntity:
            c = e.getColor()
            color = (c[0], c[1], c[2])
            if e.getShape() == 0:
                pygame.draw.rect(screen, color, pygame.Rect(e.getPos()[0], e.getPos()[1], 10*e.getSize(), 10*e.getSize()))
            else:
                pygame.draw.circle(screen, color, e.getPos(), 5*e.getSize())
            updatePos(e)
        
    pygame.display.flip()

pygame.quit()