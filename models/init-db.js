// mongo --username root --password example --authenticationDatabase admin /tmp/init-db.js
db = db.getSiblingDB('jobs')
try {
    var ides = [{
        "name": "Jupyter",
        "title": "Jupyter (Python, R)",
        "start": "/bin/bash /var/opt/workspaces/jupyter/start",
        "middlewares": [],
        "has_relative_path": true
        },
        {
        "name": "JupyterLab",
        "title": "JupyterLab (Python, R)",
        "start": "/bin/bash /var/opt/workspaces/Jupyterlab/start.sh",
        "middlewares": [],
        "has_relative_path": true
        },
        {
        "name": "Vscode",
        "title": "Visual Studio Code",
        "start": "/bin/bash /var/opt/workspaces/vscode/start",
        "middlewares": ["ilyde-workspace-replacepathregex"],
        "has_relative_path": true
        }
   ]
   db.ide.insertMany( ides );
   var envs = [
        {
            "name": "Minimal py37",
            "image": "gitlab.hopenly.com:4567/ilyde/base-images/minimal-py37:1.4",
            "deployment": false
        },
        {
            "name": "Deployment py37",
            "image": "gitlab.hopenly.com:4567/ilyde/base-images/deployment-py37:1.0",
            "deployment": true
        }
   ]
   db.environment.insertMany( envs );
} catch (e) {
   print(e);
}