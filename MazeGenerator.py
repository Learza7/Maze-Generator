"""
MAZE GENERATOR
"""
import keyboard
# Modules
from matplotlib.pyplot import *
from random import randint
import operator

# Dimensions
#m=int(input("nombre de lignes ? "))
#n=int(input("nombre de colonnes ? "))

m=30
n=30

width=3 # épaisseur des murs

# Fonctions
def Laby(m,n):
    """renvoie deux tableaux Sud et Est modélisant un labyrinthe de taille m*n"""
    Sud=[n*[True] for k in range(m)]
    Est=[n*[True] for k in range(m)]

    compt=0
    
    Numeros=[list(range(k*n+1, (k+1)*n+1)) for k in range(m)] # Liste numérotant chaque case de 1 à m*n
    
    while compt<m*n-1:
        
        i=randint(0,m-1)
        j=randint(0,n-1)
        
       # Liste contenant les cases adjacentes à la case (i,j) ayant une valeur différente 
        Cases=Adjacente(Numeros,i,j,operator.ne,Numeros[i][j]) 
        
        k=len(Cases)
        if k>0: # Si la liste Cases est non nulle, je tire au sort une case de la liste et la traite en fonction de son emplacement par rapport à la case (i,j)   
            p=Cases[randint(0,k-1)]
            
            if p[2]==2:
                Sud[i][j]=False
            elif p[2]==1:
                Est[i][j]=False
            elif p[2]==0:
                Sud[p[0]][p[1]]=False
            else:
                Est[p[0]][p[1]]=False

            # Je récupères les valeurs des deux cases
            a=Numeros[i][j]
            b=Numeros[p[0]][p[1]]

            # Je prends a comme le plus petit et b comme le plus grand des deux nombres
            if not a<b: 
               a,b=b,a

            # Et à chaque case ayant la valeur b, je lui assigne la valeur a
            for y in range(m):
                for z in range(n):
                    if Numeros[y][z]==b:
                        Numeros[y][z]=a
                        if a==1:
                            compt+=1
                            
    # Entrée et Sortie du Labyrinthe
    Sud[m-1][0]=False
    Est[0][n-1]=False
    
    return Sud,Est

def Resolution(S,E):
    """résout le labytinthe modélisé par les tableaux S et E en renvoyant la liste contenant la solution"""
    Table=[n*[0] for k in range(m)]
    Table[m-1][0]=1
    k=1

    while Table[0][n-1]==0:
        for y in range(m):
            for z in range(n):
                if Table[y][z]==0:
                    Cases=Adjacente(Table,y,z,operator.eq,k) #renvoie la liste des cases adjacentes ayant pour valeur k
                    if VoisinSansMur(Cases,y,z,S,E):
                        Table[y][z]=k+1
        k+=1

    Solution=[]
    Solution.append([0,n-1])
    
    while k>1:
        y=Solution[0][0]
        z=Solution[0][1]
        
        Cases=Adjacente(Table,y,z,operator.eq,k-1) #renvoie la liste des cases adjacentes ayant pour valeur k-1

        for Alpha in Cases:
            if VoisinSansMur([Alpha],y,z,S,E):
                Solution.insert(0,[Alpha[0],Alpha[1]])
        k-=1
    return Solution


def VoisinSansMur(Cases,y,z,S,E):
    """Détermine si la case y,z n'a pas de mur avec au moins une des cases de la liste Cases"""
    Condition=False
    i=0
    
    while not Condition and i<len(Cases):
        elem=Cases[i]
        if elem[2]==1:
            if not E[y][z]:
                Condition=True
        elif elem[2]==2:
            if not S[y][z]:
                Condition=True
        elif elem[2]==3:
            if not E[elem[0]][elem[1]]:
                Condition=True
        else:
            if not S[elem[0]][elem[1]]:
                Condition=True
        i+=1
        
    return Condition
                

def Adjacente(Table,i,j,operateur,k):
    """renvoie une liste contenant les cases adjacentes à la case (i,j) respectant la condition operateur (soit une égalité soit une inégalité avec k)"""
    Cases=[]
    
    for h in range(-1,2,2):
        
        if 0<=i+h<m and operateur(Table[i+h][j],k):
                if h==-1:
                    Cases.append([i+h,j,0])
                else:
                    Cases.append([i+h,j,2])
                
        if 0<=j+h<n and operateur(Table[i][j+h],k):
                if h==-1:
                    Cases.append([i,j+h,3])
                else:
                    Cases.append([i,j+h,1])
                    
         # je les enregistre sous le format [coordonnée verticale, coordonnée horizontale, 0 (si la case est au dessus) ou 1 (si à droite) ou 2 (si en dessous) ou 3 (si à gauche)

    return Cases

def DepPoss(i,j):
    Dep=[False for k in range(4)]

    for h in (-1,1):
        if 0<=i+h<m:
                if h==-1 and VoisinSansMur([[i+h,j,0]],i,j,Sud,Est):
                    Dep[0]=True
                elif h==1 and VoisinSansMur([[i+h,j,2]],i,j,Sud,Est):
                    Dep[2]=True
        if 0<=j+h<n:
                if h==-1 and VoisinSansMur([[i,j+h,3]],i,j,Sud,Est):
                    Dep[3]=True
                elif h==1 and VoisinSansMur([[i,j+h,1]],i,j,Sud,Est):
                    Dep[1]=True
    return Dep
                    
    


def AffLaby(S,E):
    """affiche le labyrinthe modélisé pat les tableaux S et E"""
    plot([0,0,n],[0,m,m],color="k",linewidth=width)
    for i in range(m):
        for j in range(n):
            if S[i][j]:
                plot([j,j+1],[m-i-1,m-i-1],color="k",linewidth=width)
            if E[i][j]:
                plot([j+1,j+1],[m-i-1,m-i],color="k",linewidth=width)
                
def AffSol(Sol):
    """affiche le chemin, qui relie l'entrée à la sortie du labyrinthe, contenu dans le tableau Sol"""
    x=[0.5]
    y=[0]
    for e in Sol:
        x.append(e[1]+0.5)
        y.append(m-e[0]-0.5)
    x.append(n)
    y.append(m-0.5)
    plot(x,y,color="r",linewidth=width/2)




""" This part of the script does not work anymore. It allowed the user to move
a cursor through the maze
"""

def AffChem(Chem):
    
    x=[]
    y=[]
    for e in Chem:
        x.append(e[1]+0.5)
        y.append(m-e[0]-0.5)
    plot(x,y,color="b",linewidth=width/2,linestyle="--")

def Effacer(route):
    x,y=[],[]
    print(route)
    for e in route:
        x.append(e[1]+0.5)
        y.append(m-e[0]-0.5)
    plot(x,y,color="w",linewidth=width)
    
def press(event):
    print(event)
    if not CHEM[-1]==[0,m]:
        maj=False
        i,j=CHEM[-1]
        Dep=DepPoss(i,j)
        print(event.key)
        if event.key=="up" and Dep[0]:
            CHEM.append([i-1,j])
            maj=True
        elif event.key=="right" and (Dep[1] or i==0 and j==n-1):
            CHEM.append([i,j+1])
            maj=True
        elif event.key=="down" and Dep[2]:
            CHEM.append([i+1,j])
            maj=True
        elif event.key=="left" and Dep[3]:
            CHEM.append([i,j-1])
            maj=True
        print(CHEM)
        if maj:
            Effacer(CHEM[:])
            if len(CHEM)>2 and CHEM[-1]==CHEM[-3]:
                Effacer(CHEM[:])
                del CHEM[-1]
                del CHEM[-1]
            AffChem(CHEM)
        event.canvas.draw()


def release(event):
    if event.key=="r":
        print("lol")
        CHEM,Sol,Sud,Est=Init()


# création et affichage du labyrinthe
Sud,Est=Laby(m,n)
Sol=Resolution(Sud,Est)
CHEM=[[m-1,0]]
    
fig, laby = subplots()
fig.canvas.mpl_connect('key_press_event', press)
fig.canvas.mpl_connect('key_release_event', release)

AffLaby(Sud,Est)
#AffChem([[m,0]]+CHEM)
plot([n-0.5,n+0.5],[m-0.5,m-0.5],"w")

axis("equal")



show()


