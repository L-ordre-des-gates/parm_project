def lire_fichier_assembleur(nom_fichier):
    """
    Lit un fichier assembleur et affiche les lignes non vides
    et non commentées.

    :param nom_fichier: Le chemin vers le fichier assembleur.
    """
    try:
        with open(nom_fichier, 'r') as fichier:
            lignes = fichier.readlines()

        for ligne in lignes:
            ligne = ligne.strip()
            if not ligne or ligne.startswith(';') or ligne.startswith('#'):
                continue
            print(ligne)

    except FileNotFoundError:
        print(f"Erreur : Le fichier '{nom_fichier}' n'/opt/sonarqube-25.1.0.102122/bin/linux-x86-64/sonar.sh                                                                                                                            ✔  4s  
Java not found. Please make sure that the environmental variable SONAR_JAVA_PATH points to a Java executable
existe pas.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")


if __name__ == "__main__":
    nom_fichier = input("Entrez le chemin du fichier assembleur à lire : ")
    lire_fichier_assembleur(nom_fichier)
