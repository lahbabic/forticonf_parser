.. forticonf parser documentation master file, created by
   sphinx-quickstart on Wed Jul 18 11:37:19 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Documentation Forticonf Parser 0.0.1
====================================

Bienvenue sur la documentation de Forticonf Parser 0.0.1.

Introduction
++++++++++++

**Forticonf Parser** a été developé dans le but de faciliter la lecture des fichiers de configuration des firewalls FortiGate du constructeur `Fortinet`_.

.. _Fortinet: https://www.fortinet.com

Dans certaines circonstances, il est possible qu'on ait besoin de savoir les différents objets que contient un fichier de configuration; comme par exemple les machines, les réseaux, les groupes de réseaux, les services ou groupes de services ou encore les politiques de sécurité appliqués à ces objets.

Généralement un fichier de configuration Fortigate contient environ 6000 lignes, avec une syntaxe que l'on ne comprend pas forcement.

Dans d'autres cas, même en connaissant la syntaxe, il s'avère difficile de repérer un objet spécifique. Par exemple un groupe de services peut contenir d'autres groupes de services qui eux-mêmes peuvent contenir d'autres groupes de services. Il est donc possible de perdre facilement le fil au milieu de tous ces objets.

*Forticonf parser* facilite la lecture de ces fichiers de configuration en exportant ces objets dans un format plus lisible qui est le *format excel*.

Table des matières
+++++++++++++++++++



.. toctree::
   :maxdepth: 2

   prerequis
   utilisation
   specifications 


Index et tables des matières :
==============================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`



