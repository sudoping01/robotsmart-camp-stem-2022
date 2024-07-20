from tkinter import *
import pdfkit
from os import system

client =""
date = ""
xtemps =""
idCaisiere =""
nbreProduit = int()

nomProduitEntry = None      # Champ du nom de Produit
prixEntry = None            # Champ du Prix du produit 
quantiteEntry = None        
produit = None 
infoProduit = []        # produits informations
coutTotalSansReduction = 0.0
coutTotalReduit  =0.0
fidelite = ""

def makeFile(nameFile,contenu) : 
    file = open(nameFile.replace(" ",""),"a")
    file.write(contenu)
    file.close()
    
def view(fileName):
    system(f"google-chrome {fileName.replace(' ','')}.html ")
    
    
#def makeHtmlToPdf(fileHtml):
   # global client 
    #pdfkit.from_file(fileHtml,f'{client}.pdf')

def coutProduit(quantite,prixUnitaire) : 
    return prixUnitaire*quantite

def calculReduction(prixOrigine):
    if  (prixOrigine > 0) and (prixOrigine < 10_000 ) :
        prix = (prixOrigine - (prixOrigine*0.02))
        
    elif (prixOrigine >= 10_000) and (prixOrigine < 100_000) : 
        prix = (prixOrigine - (prixOrigine*0.04))
        
    elif (prixOrigine >= 100_000) and (prixOrigine < 1_000_000):
        prix = (prixOrigine- (prixOrigine*0.08))
    else :
        prix = (prixOrigine - (prixOrigine*0.1))
    return prix 


def produceHtmlPage(soldInformation):     
    global  client 
    global date 
    global xtemps
    global idCaisiere 
    global coutTotalReduit
    global coutTotalSansReduction
    
    
    page = ""
    for article in soldInformation: 
        coutTotalReduit += coutProduit(article[1],article[-1])
        coutTotalSansReduction +=coutProduit(article[1],article[2])
        
         
        page += f"<tr>\n<td>{article[0]:.^25}</td>\n<td>{article[1]:.^25d}</td>\n<td>{str(article[2]):.>20s} FCFA</td>\n<td>{str(article[3]):.>20s} FCFA"
    ArgentEconomisé = coutTotalSansReduction - coutTotalReduit
    
    if (fidelite.lower()) == 'oui' or fidelite.lower() == 'yes': 
        total = coutTotalReduit
    else : 
        total = coutTotalSansReduction
        
    site_model = f"""<html>
        <head> </head>
        <body>
            <div>{'_'*200}</div>
            <h1 >**********************SUPERMARCHE ROBOTSMART****************************</h1>
             <div>{'_'*200}</div>
            <h3> Client :{client:.^30}</h3>         
            <table>
                <tr>
                    <td><b>ARTICLE</b></th>
                    <td><b>QUANTITE</b></th>
                    <td><b>PRIX UNITAIRE</b></th>
                    <td><b>PRIX FIDELITÉ</b></th>
                </tr>
                <tr>
                  <td>{'_' * 25}</td>
                  <td>{'_' * 25}</td>
                  <td>{'_' * 25}</td>
                  <td>{'_' * 25}</td>
                </tr>
                {page}
                 <tr>
                  <td>{'_' * 25}</td>
                  <td>{'_' * 25}</td>
                  <td>{'_' * 25}</td>
                  <td>{'_' * 25}</td>
                </tr>
                 <tr>
                 <tr> 
                  <td><b>SOMME A ECONOMISER VIA LA CARTE : </b></td>
                  <td></td>
                  <td>
                  <b>{'':25s}</b> 
                  <b>{int(ArgentEconomisé):.>20d} FCFA  </b>
                  </td>
                  </tr>
      <tr>
            <td>{'_' * 25}</td>
            <td>{'_' * 25}</td>
            <td>{'_' * 25}</td>
            <td>{'_' * 25}</td>
    </tr> 
     <div>{'_'*200}</div>
    <tr> 
                  <td><b>TOTAL: </b></td>
                  <td></td>
                  <td>
                  <b>{'':25s}</b> 
                  <b>{str(total):.>20s}FCFA </b>
                  </td>
     </tr>
     <tr>
    <table>
        <div>{'_'*200}</div>
        <div><i><b>BAMAKO {date}@{xtemps}</b></i></div>
        <div><i><b>CAISSE N°{idCaisiere:0>4s}</b></i></div> 
        <div><i><b>Merci Pour Votre Achat</b></i></div>
     </body>
    </html> 
    
"""
    makeFile(f"{client}.html",site_model)
    #makeHtmlToPdf(f"{client}.html")
    view(client)
    
          


def produitInfoEntry(number):
    global produit
    global nomProduitEntry
    global prixEntry
    global quantiteEntry
    
    produit = Tk()
    produit.title("PRODUIT INFO")
    produit.geometry("200x300")
    produit.configure(bg="white")
    produit.maxsize(width=300,height=300)
    entete = Label(text= f" ROBOTSMART \n INFORMATION DU PRODUIT N°{number}",bg="chocolate",fg="black",width=500,height=5)
    entete.pack()
    
    nomProduit = Label(produit,text="Nom du produit",fg='brown',bg="white")
    prix = Label(produit,text="Prix Unitaire",bg="white",fg="brown")
    quantite = Label(produit,text="Quantité",bg="white",fg="brown")

    nomProduit.place(x=15,y=100)
    prix.place(x=15,y=170)
    quantite.place(x=15,y=240)

    nomProduitEntry = Entry(produit,width=30)
    prixEntry = Entry(produit,width=30)
    quantiteEntry = Entry(produit,width=30)

    nomProduitEntry.place(x=15,y=120)
    prixEntry.place(x=15,y=190)
    quantiteEntry.place(x=15,y=260)
    
    def getProduitsInfo():
        global produit
        global nomProduitEntry
        global prixEntry
        global quantiteEntry
        global infoProduit
        infoProduit.append(list([nomProduitEntry.get(),int(quantiteEntry.get()),float(prixEntry.get()),calculReduction(float(prixEntry.get()))]))
        produit.destroy()   
        

    destroy = Button(produit,fg="black",width="27",height="1",text = "sumit",command = getProduitsInfo)
    destroy.place(x=15,y=300)
    produit.mainloop()
    
    

def produitWindowsManager(nbre) : 
    global achatinfo
    global infoProduit
    for i in range(1,nbre+1):
        produitInfoEntry(i)
    produceHtmlPage(infoProduit)

def getInfoAchat():
    global nameEntry
    global dateEntry  
    global timeEntry
    global idCaisseEntry
    global fidelityEntry
    global nbreProduitEntry
    global recu   
    global client 
    global date
    global xtemps 
    global idCaisiere 
    global nbreProduit
    global fidelite
    client = nameEntry.get()
    date = dateEntry.get()
    xtemps = timeEntry.get()
    idCaisiere = idCaisseEntry.get()
    fidelite = fidelityEntry.get()
    nbreProduit = int(nbreProduitEntry.get()) 
    recu.destroy()    
    produitWindowsManager(nbreProduit)
    
    
recu = Tk()  # fenetre pricipal 
recu.title("REÇU DU SUPER MARCHÉ ROBOTS-MART")
recu.geometry("300x500")
recu.configure(bg = "white")
recu.maxsize(width=300,height=530)

entete = Label(text= "ROBOTSMART",bg="chocolate",fg="black",width=500,height=5)
entete.pack()

clientName = Label(recu,text="Nom du Client : ",bg="white",fg="brown")
date = Label(recu,text="Date : ",bg="white",fg="brown")
time = Label(recu,text="heure : ",bg="white",fg="brown")
idCaisse = Label(recu,text="Caisse N° :",bg="white",fg="brown")
fidelity = Label(recu,text="Est-ce un client fidèle  ? : ",bg="white",fg="brown")
nbreProduits = Label(recu,text="Nombre de type  Produis acheté ",fg='brown',bg="white")

clientName.place(x=15,y=100)      
date.place(x=15,y=170)           
time.place(x=15,y=240)          
idCaisse.place(x=15,y=310)        
fidelity.place(x=15,y=380)
nbreProduits.place(x=15,y=450)

nameEntry = Entry(recu,width=30)
dateEntry = Entry(recu,width=30)
timeEntry = Entry(recu,width=30)
idCaisseEntry = Entry(recu,width=30)
fidelityEntry = Entry(recu,width=30)
nbreProduitEntry = Entry(recu,width=30)

nameEntry.place(x=15,y=120)         
dateEntry.place(x=15,y=190)         
timeEntry.place(x=15,y=260)           
idCaisseEntry.place(x=15,y=340)         
fidelityEntry.place(x=15,y=400) 
nbreProduitEntry.place(x=15,y=470)

continuous = Button(recu,fg="black",width="12",height = "1", text="Next",command= getInfoAchat)
detruire = Button(recu,fg="black",width="12",height="1",text = "exit",command = recu.destroy)

continuous.place(x = 15,y=530) 
detruire.place(x=135,y=530)

recu.mainloop()



