import random


class Noeud:
    """
    Class pour représenter un nœud
    """

    def __init__(self, id_noeud):
        """
        Constructeur pour créer un nœud
        """
        self.__id_noeud = id_noeud
        self.__connection = {}

    def ajouter_connection(self, noeud, temps_communication):
        """
        Méthode pour créer une connection entre de nœud
        """
        self.__connection[noeud] = temps_communication

    def set_connection(self, connection):
        """Mutateur de l'attribut connection"""
        self.__connection = connection

    def get_connection(self):
        """Accesseur de l'attribut connection """
        return self.__connection

    def set_id_noeud(self, id__noeud):
        """Mutateur de l'attribut id_noeud"""
        self.__id_noeud = id__noeud

    def get_id_noeud(self):
        """Accesseur de l'attribut id_noeud"""
        return self.__id_noeud

    # Propriété de la classe
    connection = property(get_connection, set_connection)
    id_noeud = property(get_id_noeud, set_id_noeud)


# Question 2.2 : Création de notre joli réseau
def créer_réseau():
    """
    Fonction pour créer le réseau
    """
    # Création des opérateurs pour les 3 niveaux
    tier_01 = [Noeud(i) for i in range(1, 11)]
    tier_02 = [Noeud(i) for i in range(11, 31)]
    tier_03 = [Noeud(i) for i in range(31, 101)]
    # Création du backbone
    for noeud_01 in tier_01:
        for noeud_02 in tier_01:
            if noeud_01 != noeud_02 and random.random() < 0.75:
                temps_communication = random.randint(5, 10)
                noeud_01.ajouter_connection(noeud_02, temps_communication)
                noeud_02.ajouter_connection(noeud_01, temps_communication)

    # Connection des opérateurs de niveau 2 avec niveau 1
    for noeud_02 in tier_02:
        connection_tier01 = random.choices(tier_01, k=random.randint(1, 2))
        temps_communication = [random.randint(10, 20) for i in range(len(connection_tier01))]
        for indice in range(len(connection_tier01)):
            noeud_02.ajouter_connection(connection_tier01[indice], temps_communication[indice])
            connection_tier01[indice].ajouter_connection(noeud_02, temps_communication[indice])

    # Connection des opérateurs de niveau 2 avec niveau 2
    for noeud in tier_02:
        for indice in range(random.randint(2, 3)):
            noeud_02 = random.choice(tier_02)
            while noeud_02 is noeud:
                noeud_02 = random.choice(tier_02)
            temps_communication = random.randint(10, 20)
            noeud.ajouter_connection(noeud_02, temps_communication)
            noeud_02.ajouter_connection(noeud, temps_communication)

    # Connection des opérateurs de niveau 2 avec niveau 3
    for noeud in tier_03:
        connection_tier02 = random.choices(tier_02, k=2)
        temps_communication = [random.randint(20, 50) for i in range(2)]
        for i in range(2):
            noeud.ajouter_connection(connection_tier02[i], temps_communication[i])
            connection_tier02[i].ajouter_connection(noeud, temps_communication[i])

    return tier_01 + tier_02 + tier_03


def est_connecté(réseau):
    # Choix d'un nœud de départ quelconque
    noeud_départ = réseau[0]

    # Liste pour suivre les nœuds visités
    visité = set()

    # Fonction récursive pour parcourir le graphe en profondeur
    def parcours_profondeur(noeud):
        visité.add(noeud)
        for voisin in noeud.connection:
            if voisin not in visité:
                parcours_profondeur(voisin)

    # Appliquer la recherche en profondeur pour marquer tous les nœuds accessibles
    parcours_profondeur(noeud_départ)

    # Si tous les nœuds ont été visités, le réseau est connexe
    return len(visité) == len(réseau)


def distance_minimale(liste_distance_noeud):
    """
    Fonction qui retourne le nœud avec la distance minimale pour l'atteindre
    """
    distance_min, noeud_min = liste_distance_noeud[0]
    indice = 1
    while indice < len(liste_distance_noeud):
        distance, noeud = liste_distance_noeud[indice]
        if distance < distance_min:
            distance_min = distance
            noeud_min = noeud
        indice += 1
    return distance_min, noeud_min


def ajouter_liste_priorité(distance_calculé, noeud, liste_priorité):
    """
    Fonction qui ajoute un nœud à la liste de priorité avec la distance exigé pour l'atteindre
    """
    indice = 0
    while indice < len(liste_priorité):
        distance, sommet = liste_priorité[indice]
        # Tester si le nœud existe déjà dans la liste
        if sommet == noeud:
            liste_priorité[indice] = distance_calculé, noeud
            return liste_priorité
        indice += 1
    # S'il n'existe pas, on l'ajoute directement
    return liste_priorité + [(distance_calculé, noeud)]


def dijkstra(graph, noeud_initial):
    """
    Fonction qui applique notre fameux algorithme de dijkstra vu en cours
    """
    # Dictionnaire qui stock pour chaque nœud, Sa distance entre lui et le nœud initial
    dictionnaire_noeud_distance = {}
    # Dictionnaire qui stock pour chaque nœud, Son prédécesseur (père)
    dictionnaire_fils_père = {}
    liste_priorité = [(0, noeud_initial)]
    # Initialisation de l'algorithme
    for noeud in graph:
        # les sommets atteignable
        if noeud in noeud_initial.get_connection():
            dictionnaire_noeud_distance[noeud] = noeud_initial.get_connection()[noeud]
            dictionnaire_fils_père[noeud] = noeud_initial
            liste_priorité.append((dictionnaire_noeud_distance[noeud], noeud))
        else:
            dictionnaire_noeud_distance[noeud] = "infini"
            dictionnaire_fils_père[noeud] = None

    dictionnaire_noeud_distance[noeud_initial] = 0

    while liste_priorité:
        # On récupère le nœud avec la distance minimale
        distance_courante, noeud_actuel = distance_minimale(liste_priorité)
        # Mettre à jour la liste de priorité en fonction des nœuds déjà traités
        liste_priorité.remove((distance_courante, noeud_actuel))
        # Traitement des sommets adjacents du nœud actuel
        for voisin, temps_communication in noeud_actuel.get_connection().items():
            distance = distance_courante + temps_communication
            # Si le nœud n'est pas encore traité ou sa distance peut être réduite , on effectue les modifications
            # nécessaires
            if dictionnaire_noeud_distance[voisin] == "infini" or distance < dictionnaire_noeud_distance[voisin]:
                dictionnaire_noeud_distance[voisin] = distance
                dictionnaire_fils_père[voisin] = noeud_actuel
                liste_priorité = ajouter_liste_priorité(distance, voisin, liste_priorité)
    # On retourne l'arborescence obtenue
    return dictionnaire_fils_père


def calcule_table_routage(réseau):
    tables_routage = {}

    # Pour chaque nœud dans le réseau
    for noeud in réseau:
        # Initialiser la table de routage pour ce nœud
        table_routage = {}
        # Calculer les distances les plus courtes à partir de ce nœud
        arborescence = dijkstra(réseau, noeud)
        # Extraction du premier nœud du plus court chemin
        for fils, père in arborescence.items():
            destination = fils
            if fils != noeud:
                while père != noeud:
                    fils = père
                    père = arborescence[père]
                table_routage[destination] = fils

        tables_routage[noeud] = table_routage
    # Retourner la table de routage pour chaque nœud
    return tables_routage


def saisie_noeud(message: str):
    """
    Fonction qui permet à l'utilisateur d'effectuer une saisie correct
    """
    saisie_incorrect = True
    while saisie_incorrect:
        saisie = input(message)
        try:
            saisie = int(saisie)
            assert 1 <= saisie < 101
            saisie_incorrect = False
        except ValueError:
            print("Veuillez saisir un entier")
        except AssertionError:
            print("Veuillez saisir un numéro compris entre 0 et 100")
    return saisie


if __name__ == "__main__":

    # Création du réseau
    print("Question 2.2 - La création aléatoire d’un réseau réaliste : ")
    réseau = créer_réseau()
    print("Le réseau est bien créé.\n")

    # Vérification de la connexité du réseau
    print("Question 2.3 - La vérification de la connexité du réseau: ")
    if est_connecté(réseau):
        print("Le réseau est connecté.\n")
    else:
        print("Le réseau n'est pas connecté. Création d'un nouveau réseau...")
        réseau = créer_réseau()
        while not est_connecté(réseau):
            réseau = créer_réseau()
        print("Nouveau réseau créé et connecté.\n")

    # Création de la table de routage de chaque nœud du réseau dans un fichier
    print("Question 2.4 - La détermination de la table de routage de chaque noeud : ")
    tables_routage = calcule_table_routage(réseau)
    # Affichage des tables de routage pour chaque nœud
    with open("tables_routage.txt", 'w') as fichier:
        for id_noeud, table_routage in tables_routage.items():
            fichier.write(f"Table de routage pour le noeud, {id_noeud.get_id_noeud()} \n")
            for destination, next_hop in table_routage.items():
                fichier.write(
                    f" Chemin vers:, {destination.get_id_noeud()}, Prochain sommet:, {next_hop.get_id_noeud()}\n")

    print('La table de routage est bien créé dans le fichier: tables_routage.txt\n')

    # Reconstitution du chemin entre deux nœuds
    print("Question 2.5 - La reconstitution du chemin entre 2 noeuds : ")
    noeud1 = réseau[saisie_noeud("Veuillez saisir le premier nœud : ") - 1]
    noeud2 = réseau[saisie_noeud("Veuillez saisir le deuxième nœud : ") - 1]
    print("Ordre de passage du message:")
    while noeud1 != noeud2:
        print(f"Le message est transmis par le noeud : {noeud1.get_id_noeud()}")
        table_routage = tables_routage[noeud1]
        noeud1 = table_routage[noeud2]
    print(f"Le message est bien arrivé au noeud {noeud2.get_id_noeud()}")
