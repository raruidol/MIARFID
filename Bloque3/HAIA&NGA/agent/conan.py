import aiwolfpy
import aiwolfpy.contentbuilder as cb
import random
import optparse
import sys
import re
import json


class conan(object):

    def __init__(self, agent_name):
        self.myname = agent_name

    def initialize(self, base_info, diff_data, game_setting):
        self.id = base_info["agentIdx"]
        self.base_info = base_info
        self.game_setting = game_setting
        self.co_flag = False # control to comeout
        self.already_co = False
        self.game_history = {}  # dict to store the sentences stated each day
        self.player_map = {}  # dict with all the information inferred of each player
        self.revealed = {} # dict with comeout roles
        self.role_vector = [] # list of players most probable roles
        self.role = base_info["myRole"]
        self.current_target = None
        # dictionary of story of the game
        self.gameDict = {}
        # list of arguments (BECAUSE) stated
        self.arguments = []
        # Target agent of the day
        self.dayTarget = None
        # Target agent for werewolf attack
        self.nightTarget = None

        self.updatePlayerMap(base_info)

    def getName(self):
        return "VRAIN"

    def update(self, base_info, diff_data, request):
        #print("Executing update...")
        self.base_info = base_info

        self.processMessages(diff_data)
        self.updatePlayerMap(base_info)

    def dayStart(self):
        #print("Day start: ")
        # list of arguments (BECAUSE) stated
        self.arguments = []
        # Target agent of the day
        self.dayTarget = None
        # Target agent for werewolf attack
        self.nightTarget = None

    def talk(self):
        #print("Talking phase: ")
        # If someone has usurpated my role (seer, medium or bodyguard)
        if self.co_flag == True and self.already_co == False:
            talk = cb.comingout(self.id, self.role)
            self.already_co = True

        # If not a WW team player create arguments with other player num_lies
        elif self.role != "WEREWOLF" and self.role != "POSSESSED":
            lie = self.retrieveLies()
            if lie is not None:
                t = lie[0]
                m = lie[1]
                talk = cb.because(m, cb.vote(t))
                print('My argument: ', talk)
            else:
                talk = cb.skip()


        # If WW team player create arguments with correct accusations (fake_lies)
        elif self.role == "WEREWOLF" or self.role == "POSSESSED":
            lie = self.retrieveLies()
            if lie is not None:
                t = lie[0]
                m = lie[1]
                talk = cb.because(m, cb.vote(t))
                print('My argument: ', talk)
            else:
                talk = cb.skip()

        return talk

    def whisper(self):
        #print("Whispering: ")
        for agent, val in self.player_map.items():
            if (self.player_map[agent]["dangerous_agent"] == True) and (self.dayTarget != int(agent)) and (agent not in self.base_info["roleMap"].keys()):
                self.nightTarget = int(agent)
                break

        if self.nightTarget == None:
            ids = []
            for key,value in self.base_info["statusMap"].items():
        	       if value == "ALIVE" and int(key) != self.id:
        	              ids.append(int(key))

            self.nightTarget = random.choice(ids)

        return cb.request(cb.attack(self.nightTarget))

    def vote(self):
        #print("Voting: ")
        # For VLL team vote the high score argument with vote or estimate as claim
        if (self.role != "WEREWOLF") and len(self.arguments) > 0:
            if self.role != "POSSESSED":
                arg = self.scoreArgs(self.arguments)
                target = self.processArgument(arg)
                return target
            elif self.role == "POSSESSED":
                for agent, value in self.player_map.items():
                    if self.player_map[agent]["dangerous_agent"] == True:
                        return int(agent)

        # For WW team vote any agent tagged as dangerous
        else:
            for agent, value in self.player_map.items():
                if self.player_map[agent]["dangerous_agent"] == True:
                    return int(agent)

        # If there are no argument(VLL team) or there are no dangerous agents(WW team) pick random target
        ids = []
        for key,value in self.base_info["statusMap"].items():
            if value == "ALIVE" and int(key) != self.id and key not in self.base_info["roleMap"].keys():
                ids.append(int(key))

        target = random.choice(ids)
        return target

    def attack(self):
        #print("Attacking: ")
        if self.nightTarget != None:
            return self.nightTarget

        else:
            ids = []
            for key,value in self.base_info["statusMap"].items():
                if (value == "ALIVE") and (key not in self.base_info["roleMap"].keys()):
                    ids.append(int(key))

            return random.choice(ids)

    def divine(self):
        #print("Making a divination: ")
        for agent in self.player_map:
            if len(self.player_map[agent]["lies"]) > 0:
                return int(agent)

        ids = []
        for key,value in self.base_info["statusMap"].items():
            if (value == "ALIVE") and (key not in self.base_info["roleMap"].keys()):
                ids.append(int(key))

        return random.choice(ids)

    def guard(self):
        #print("Guarding: ")
        for agent in self.player_map:
            if len(self.player_map[agent]["lies"]) == 0:
                return int(agent)

        ids = []
        for key,value in self.base_info["statusMap"].items():
            if (value == "ALIVE") and (key not in self.base_info["roleMap"].keys()):
                ids.append(int(key))

        return random.choice(ids)

    def finish(self):
        print("Good game!")

    def updatePlayerMap(self, base_info):
        if self.player_map == None:
            self.player_map = {}

        for key, value in base_info["statusMap"].items():
            agent_id = int(key)
            if agent_id is not self.id:
                if agent_id not in self.player_map:
                    self.player_map[agent_id] = {}
                    self.player_map[agent_id]["lies"] = []
                    self.player_map[agent_id]["fake_lies"] = []
                    self.player_map[agent_id]["dangerous_agent"] = False
                self.player_map[agent_id]["status"] = value

    def processMessages(self, diff_data):
        for row in diff_data.itertuples():

            agent = getattr(row, "agent")
            text = getattr(row, "text")
            t = text.split()

            if agent == self.id:
                if "BECAUSE" in text:
                    self.arguments.append([agent, text])

            elif agent != self.id:
                # Add arguments to argument list
                if "BECAUSE" in text:
                    self.arguments.append([agent, text])

                # Analizar el texto buscando incongruencias
                # 15: 1 seer, medium, possessed, bodyguard, 8 villa, 3 ww
                # 5: 1 seer, possessed, ww, 2 villa

                # Comprobacion de los roles revelados
                if "COMINGOUT" in text:
                    if len(t) == 3:
                        # Si revela distintos roles en la misma partida almaceno la mentira
                        if "co_role" not in self.player_map[agent]:
                            self.player_map[agent]["co_role"] = t[2]
                        else:
                            self.player_map[agent]["lies"].append([agent, text])

                        # Si soy ROL_UNICO y alguien se revela como ROL_UNICO lo add a la lista de mentirosos
                        if self.role == "SEER":
                            if "SEER" in t[2]:
                                self.co_flag = True
                                self.player_map[agent]["lies"].append([agent, text])

                        elif self.role == "MEDIUM":
                            if "MEDIUM" in t[2]:
                                self.co_flag = True
                                self.player_map[agent]["lies"].append([agent, text])

                        elif self.role == "BODYGUARD":
                            if "BODYGUARD" in t[2]:
                                self.co_flag = True
                                self.player_map[agent]["lies"].append([agent, text])

                # Si estiman mi rol incorrectamente almaceno la mentira
                if "ESTIMATE" in text:
                    if len(t) == 3:
                        if ("{:02d}".format(self.id) in t[1]) and (self.role != t[2]):
                            self.player_map[agent]["lies"].append([agent, text])

                # Si soy del equipo WW y han acertado mi rol, me guardo el mensaje para construir argumentos en contra
                if self.role == "POSSESSED":
                    if ("{:02d}".format(self.id) in text) and ("POSSESSED" in text or "VOTE" in text):
                        self.player_map[agent]["dangerous_agent"] = True
                        if "ESTIMATE" in text and len(t) == 3:
                            self.player_map[agent]["fake_lies"].append([agent, text])

                elif self.role == "WEREWOLF":
                    if ("{:02d}".format(self.id) in text) and ("WEREWOLF" in text or "VOTE" in text):
                        self.player_map[agent]["dangerous_agent"] = True
                        if "ESTIMATE" in text and len(t) == 3:
                            self.player_map[agent]["fake_lies"].append([agent, text])

    def scoreArgs(self, argument_list):
        # an argument is a tuple (agent, text)

        max_score = 0
        bestArg = argument_list[0]
        for argument in argument_list:
            # norm. score based in the number of lies

            print(argument)

            if argument[0] == self.id:
                score = 1.5

            elif len(self.player_map[argument[0]]["lies"]) > 0:
                score = 1/(len(self.player_map[argument[0]]["lies"])+1)
            else:
                score = 1
            if score > max_score:
                max_score = score
                msg = argument[1].split()
                if "VOTE" in msg[2] or ("ESTIMATE" in msg[2] and "WEREWOLF" in msg[2]):
                    bestArg = argument


        print('Winning Argument:', bestArg)
        print('Score:', max_score)
        return bestArg

    def processArgument(self, argument):
        source_id = argument[0]
        text = argument[1]
        targets = re.findall("\[(.*?)\]", text)
        return targets[len(targets)-1]

    def retrieveLies(self):
        for agent, val in self.player_map.items():
            if self.role == "WEREWOLF" or self.role == "POSSESSED":
                list = self.player_map[agent]["fake_lies"]
            else:
                list = self.player_map[agent]["lies"]
            if len(list) > 0 and self.dayTarget == None:
                lie = list.pop(0)
                self.dayTarget = int(agent)
                break
            elif len(list) > 0 and self.dayTarget == int(agent):
                lie = list.pop(0)
                break
            else:
                lie = None

        return lie

def parseArgs(args):
    usage = "usage: %prog [options]"
    parser = optparse.OptionParser(usage=usage)

    # need this to ensure -h (for hostname) can be used as an option
    # in optparse before passing the arguments to aiwolfpy
    parser.set_conflict_handler("resolve")

    parser.add_option('-h', action="store", type="string", dest="hostname",
                      help="IP address of the AIWolf server", default=None)
    parser.add_option('-p', action="store", type="int", dest="port",
                      help="Port to connect in the server", default=None)
    parser.add_option('-r', action="store", type="string", dest="port",
                      help="Role request to the server", default=-1)

    (opt, args) = parser.parse_args()
    if opt.hostname == None or opt.port == -1:
        parser.print_help()
        sys.exit()

if __name__ == '__main__':
    parseArgs(sys.argv[1:])
    aiwolfpy.connect_parse(conan("DetectiveConan"))
