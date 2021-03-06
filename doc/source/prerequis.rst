Prérequis
**********

Afin d'utiliser ce script vous aurez besoin d'utiliser une version de python supérieur ou égale à la version 3.0

Installer Python
================

Il est très probable que la version 2.7 de python soit déjà installé sur votre machine.
Pour utiliser ce script il nous faudra une version supérieure ou égale à la version 3.0.

Linux (debian)
---------------

Afin de savoir si la version 3 de python est installé sur votre machine, ouvrez une console et tapez la commande suivante:

.. code-block:: console
        
        $ python3 --version
        Python 3.5.3

Si cette commande renvoie une erreur, vous aurez besoin d'installer Python3 et pip3. Sur votre console tapez la commande suivante:

.. code-block:: console

        $ sudo aptitude install python3 python3-pip


Windows
-------

Vous pouvez télécharger Python pour Windows sur le site web `python.org`_ ou télécharger la version 3.5.3 en cliquant sur le lien `python-3.5.3`_ .

Après avoir téléchargé le fichier .exe, lancez-le et suivez les instructions pour l'installer.

.. _python.org: https://www.python.org/downloads/windows/

.. _python-3.5.3: https://www.python.org/ftp/python/3.5.3/python-3.5.3.exe

.. note::
        Cochez la case "Ajouter Python 3.5 au chemin", en anglais "Add Python 3.5 to PATH".

        Notez le chemin où il va être installé. Vous en aurez besoin plutard afin de lancer le script.
      

Installer les modules requis
============================

Le lien *github* pour récupérer le script se trouve à l'adresse suivante: `forticonf_parser`_

.. _forticonf_parser: https://github.com/lahbabic/forticonf_parser.git

Les modules requis pour le bon fonctionnement du script sont dans le fichier **requirements.txt** qui se trouve dans le répertoire du script.

Télécharger le script et installer les dépendances
--------------------------------------------------

Linux (debian)
++++++++++++++

**Télécharger le script**

Vous pouvez télécharger le script soit manuellement, dans ce cas vous aurez un fichier .zip que vous devrez décompresser.

La deuxième méthode consiste a utilisé la commande **git**.

Si vous n'avez pas git d'installé, ouvrez une console puis taper la commande suivante:

.. code-block:: console
        
        $ sudo aptitude install git

Après avoir installé git, vous pouvez à présent télécharger le script à l'aide de la commande suivante:

.. code-block:: console

        $ git clone https://github.com/lahbabic/forticonf_parser.git

Une fois cela effectué, naviguez dans le dossier *forticonf_parser*:

.. code-block:: console

        $ cd forticonf_parser


**Installer les dépendances**


Ouvrez une console et tapez la commande suivante pour installer les dépendances:

.. code-block:: console

        $ pip3 install -r requirements.txt


Windows
+++++++

**Télécharger le script**

Sur Windows vous pouvez télécharger le script sur la page:

`github.com/lahbabic/forticonf_parser.git`

Une fois le script téléchargé, décompressez le fichier .zip.

Ouvrez une console "cmd.exe" et naviguez au dossier *forticonf_parser-master*:

.. code-block:: console

        C:\Users\username\>cd Downloads\forticonf_parser-master

**Installer les dépendances**


Premièrement vous aurez besoin de mettre à jour *pip*. Utilisez la commande suivante:

.. code-block:: console     
        
        C:\Users\username\Downloads\forticonf_parser-master>python -m pip install --upgrade pip

Puis installez les dépendances en utilisant la commande suivante:

.. code-block:: console

        C:\Users\username\Downloads\forticonf_parser-master>pip install -r requirements.txt


Vous pouvez à présent utiliser le script.




