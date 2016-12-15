xml-archive-to-pdf
==================

Transformation d'un fichier xml de type *unistra:archive* en fichier pdf

Installation
------------

.. code-block:: bash

    pip install xml-archive-to-pdf

Usage
-----

.. code-block:: bash

    cat tests/data/pathfinder_1.xml | xargs -0 xml-archive-to-pdf

Documentation
-------------

Structuration d'un fichier xml de type *unistra:archive*
********************************************************

L'objectif est de pouvoir générer simplement un fichier pdf en se basant sur un fichier xml conforme à la norme *unistra:archive*.
En amont, il faudra s'assurer que le fichier xml soit validé par un schéma xsd et qu'il contient toutes les informations nécessaires à la fabrication du pdf.

On aura principalement :

* Des blocs séparés par des titres
* Des clés avec un intitulé parlant
* Des valeurs
* Quelques types de mise en formes simples (tableau par exemple)


Exemple d'un fichier xml
************************

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!-- Racine du fichier, id et source sont optionnels, le name correspond au titre -->
    <personnage xmlns="fr:unistra:di:archive:pathfinder:v1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="fr:unistra:di:archive:pathfinder:v1 pathfinder_v1.xsd"
        id="1" source="pathfinder" name="document récapitulatif du personnage 1 de pathfinder">
        <!-- Affiche le sous-titre de l'état civil -->
        <etat-civil name="son état civil">
            <!-- Affichage de clés/valeurs -->
            <nom>Sombre-crâne</nom>
            <age name="son âge">20</age>
            <!-- Nouveau bloc avec un sous-titre -->
            <classes name="classes et niveaux">
                <!-- Ici on affiche le sous-titre de name -->
                <classe name="Première classe">
                    <nom>Barbare</nom>
                    <niveau>3</niveau>
                </classe>
                <!-- Ici name est vide, donc ça affiche un titre vide -->
                <classe name="">
                    <nom>Voleur</nom>
                    <niveau>1</niveau>
                </classe>
                <!-- Lorsqu'il n'y a pas d'attribut name, on affiche le nom du tag. Ici classe -->
                <classe>
                    <nom>Moine</nom>
                    <niveau>2</niveau>
                </classe>
            </classes>
        </etat-civil>
    </personnage>



Légende de l'exemple
********************

TODO

attributs
#########

name : intitulé parlant
type : title|table (default title), utilisé pour
