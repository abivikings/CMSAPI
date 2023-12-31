## Sullivan Elections Installation Process
  ### Python Version
      Python 3.6 to 3.9
  ### Create Environment
      python -m venv sullivan_election_venv
  ### Activate Environment
   #### For windows
        .\sullivan_election_venv\Script\activate
   #### For Linux
        source /sullivan_election_venv/bin/activate
  ### Clone Project
      git clone https://github.com/harmonysheets/sullivan-elections.git
  ### Install Requirments
      cd sullivan-elections
      pip install - requirements.txt
  ### Run Project
      python manage.py runserver
      
   ![sullivan_login](https://user-images.githubusercontent.com/9355195/190843749-f1c2d98a-471c-427a-b545-f236adbd4df7.jpg)
## projects structure 
   #### Projects has three part
    1. Main application 
    2. Socket server for support real time session user changes
    3. Stand alone time trigger script
  ### Main application
   #### Backend
    Main application is developed by Django(MVT architecture).Mainly projects is used function based view because of frequently requirements change and correction.View and REST framework both is used here based on purpose.
   #### Frontend 
    HTML 5, Bootstrap 5, Jquey. Jquery is used here to call API and make frontend interactive. 
  ### Socket Server
    Socket server is supporting real time changes for session users.Here can be used channel but for broadcasting socket io is supporting good for this project. In future if need channel can be used here. 
  ### Time trigger Script
   Time trigger script will help us to trigger for all absentee voter if date is over autometically set In person voting.
   
## Deployment 
  Initially project is deploed in namecheap server(shared hosting). For running multiple server need to move VPS hosting in future.
