# GPTWorker

gptWorker.py est un script Python qui automatise l'interaction avec le modèle GPT-4 d'OpenAI pour appliquer des modifications à une base de code existante.

## Fonctionnalités
Concaténation du code : Rassemble le contenu de tous les fichiers texte du répertoire courant, en respectant les règles de .gitignore.
Interaction avec GPT-4 : Envoie le code concaténé au modèle GPT-4 avec une tâche spécifiée par l'utilisateur.
Mise à jour automatique : Met à jour les fichiers modifiés ou créés par GPT-4 directement dans le système de fichiers.
Boucle interactive : Permet d'enchaîner plusieurs tâches sans redémarrer le script.

## Utilisation

### Installer les dépendances
```bash
pip install openai dotenv pathspec
```

### Configurer la clé API OpenAI :
Créez un fichier .env dans le répertoire du script.
Ajoutez votre clé API sous la forme API_KEY=sk-...

### Exécuter le script :
```bash
python gptWorker.py
```

### Entrer une tâche :
Lorsque le script vous invite avec Enter your task:, saisissez la description de la tâche à effectuer sur la base de code.

### Vérifier les modifications :
Après l'exécution, le script met à jour les fichiers concernés.
Consultez les fichiers modifiés pour valider les changements.

## Remarques
Limites du modèle : Assurez-vous que la taille de votre codebase n'excède pas la limite de contexte de GPT-4 (environ 8 000 tokens).
Exclusions : Les fichiers spécifiés dans .gitignore et ceux listés dans other_ignore ne seront pas inclus.
Sécurité : Vérifiez toujours les modifications apportées par le modèle pour éviter les erreurs ou les comportements indésirables.

## Licence
Ce projet est distribué sous la licence MIT.

![image](https://github.com/user-attachments/assets/11c19a85-c4c5-416d-84c1-0831cf04a278)
*Exemple d'un simple Mario Bross minimaliste générer avec gpt4 de OpenAI*