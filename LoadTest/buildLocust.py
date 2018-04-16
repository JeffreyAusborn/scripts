#!/usr/bin/python
from optparse import OptionParser
import os
import commands
import getpass


def buildHead(builder):
    builder.write("\tdef getHead(self):\n\t\treturn {'Content-Type': 'application/json', 'Accept': 'application/json','Preferred-Auth': 'APP'}\n\n")


def buildTaskFunctions(builder, endpoints):
    count = 0
    while count < endpoints:
        builder.write(''.join(["def endPoint{0}(self):\n\tmerchant_uuid = self.Merchants.getMerchant()\n\tself.client.get(url=''.join([self.Endpoints.getEndpoint({0}).format(merchant_uuid), ".format(count), "'?access_token={}'", ".format(self.Merchants.getToken(merchant_uuid))]), headers=self.getHead(), name=self.Endpoints.getEndpoint({0}))\n\n".format(count)]))
        count += 1


def buildTasks(builder, endpoints):
    count = 0
    if endpoints == 1:
        builder.write('\ttasks = {endPoint0:Endpoints.getOPS(0)}\n\n')
    else:
        builder.write('\ttasks = {endPoint0:Endpoints.getOPS(0), ')
        count += 1
        while count < endpoints-1:
            if count % 5 == 0:
                builder.write('endPoint{0}:Endpoints.getOPS({0}),\n\t'.format(count))
            else:
                builder.write('endPoint{0}:Endpoints.getOPS({0}),'.format(count))
            count += 1
        builder.write(''.join(['endPoint{0}:Endpoints.getOPS({0})'.format(count), '}\n\n']))


def buildUserClass(builder, min_wait, max_wait, stop_timeout):
    builder.write('class WebsiteUser(HttpLocust):\n')
    builder.write('\ttask_set = ApiRequests\n\tmin_wait = {}\n\tmax_wait = {}\n\tstop_timeout = {}\n\n'.format(min_wait, max_wait, stop_timeout))


def parse_options():
    parser = OptionParser(usage="python buildPy.py [options]")
    parser.add_option('-E', '--end-points', dest="end_points", default=1, help="The number of end-points you want to test,")
    parser.add_option('--min-wait', dest="min_wait", default=1000, help="In milliseconds, the minimum time that a simulated user will wait between executing each task,")
    parser.add_option('--max-wait', dest="max_wait", default=1000, help="In milliseconds, the maximum time that a simulated user will wait between executing each task,")
    parser.add_option('-T', '--stop-timeout', dest="stop_timeout", default=60, help="In milliseconds, how long you want locust to run for.")
    parser.add_option('--no-web', dest='no_web', default=False, help="Disable the web interface, and instead start running the test immediately. Requires -c and -r to be specified.")
    parser.add_option('-H', '--host', dest="host", default='ss1.dev. clover.com', help="Host to load test in the following format: ss1.dev.clover.com")
    parser.add_option('-K', '--kibana', dest="kibana", default=False, help="Kibana Raw CSV of API Get Requests")
    parser.add_option('-F', '--file', dest="file", default=False, help="CSV file containing the list of endpoints and rps")
    opts, args = parser.parse_args()
    return parser, opts, args


def checkForEnv():
    envStatus = commands.getoutput('pip -V')
    if getpass.getuser() in envStatus:
        print "\tvirtualenv is established"
    else:
        exit('Please activate your virtualenv\n\tvirtualenv <env_name>\n\tsource <env_name>/bin/activate')


def checkForModules():
    pipMods = commands.getoutput('pip list')
    if "locustio" not in pipMods:
        os.system("pip install locustio")
    if "pyzmq" not in pipMods:
        os.system("pip install pyzmq")


def buildMerchantClass(builder):
    builder.write("class Merchants:\n\tdef __init__(self):\n\t\tself.merchant_and_accessToken = {}\n\t\twith open('access.csv', 'rb') as infile:\n\t\t\treader = csv.DictReader(infile)\n\t\t\tfor rows in reader:\n\t\t\t\tif rows['mId']:\n\t\t\t\t\tmids = rows['mId']\n\t\t\t\tif rows['access']:\n\t\t\t\t\tself.merchant_and_accessToken[mids] = rows['access']\n\n\tdef getMerchant(self):\n\t\treturn random.choice(self.merchant_and_accessToken.keys())\n\n\tdef getToken(self, merchant):\n\t\treturn self.merchant_and_accessToken[merchant]\n")


def buildEndpointClass(builder):
    builder.write("\nclass Endpoints:\n\tdef __init__(self):\n\t\tself.endPoints = []\n\t\tself.OPS = []\n\t\twith open('endpoints.csv', 'rb') as csvfile:\n\t\t\tapiReader = csv.DictReader(csvfile)\n\t\t\tfor row in apiReader:\n\t\t\t\tif row['Type'] == 'GET':\n\t\t\t\t\tgetReq = row['Request'].replace('{mId}', '{}')\n\t\t\t\t\tif (getReq.count('{}') == 1 and getReq.count('{') == 1):\n\t\t\t\t\t\tself.endPoints.append(getReq)\n\t\t\t\t\t\tself.OPS.append(int(row['Avg OPS']))\n\n\tdef getEndpoint(self, loc):\n\t\treturn self.endPoints[loc]\n\n\tdef getOPS(self, loc):\n\t\treturn self.OPS[loc]\n\n")


def main():
    parser, options, arguments = parse_options()
    if options.kibana:
        print "Parsing Kibana csv file"
        apiCount = commands.getoutput('python apiParser.py {0} {1}'.format(options.kibana, 1))
        if int(apiCount) < int(options.end_points):
            exit("Please choose a smaller endpoint count. Kibana csv only had {} endpoints".format(apiCount))
    elif options.file:
        print "Parsing endpoint csv file"
        apiCount = commands.getoutput('python apiParser.py {0} {1}'.format(options.file, 0))
        print apiCount
        if int(apiCount) < int(options.end_points):
            exit("Please choose a smaller endpoint count. The csv only had {} endpoints".format(apiCount))
    print "Getting data from {}".format(options.host)
    if 'ss1' in options.host:
        os.system('python getData.py ssdb1.dev.clover.com ')
    else:
        os.system('python getData.py {}'.format(options.host))
    print "Building your locust.py"
    with open('locustLoadTest.py', 'w') as builder:
        builder.write('from locust import HttpLocust, TaskSet, task\nimport csv\nimport random\n\n')
        buildMerchantClass(builder)
        buildEndpointClass(builder)
        buildTaskFunctions(builder, int(options.end_points))
        builder.write('class ApiRequests(TaskSet):\n\tMerchants = Merchants()\n\tEndpoints = Endpoints()\n\n')
        buildHead(builder)
        buildTasks(builder, int(options.end_points))
        buildUserClass(builder, int(options.min_wait), int(options.max_wait), int(options.stop_timeout))
    print "Checking locustLoadTest.py for compile errors"
    exitStatus = commands.getoutput('python locustLoadTest.py | echo $? ')
    if exitStatus == "0":
        checkForEnv()
        checkForModules()
        print "\tLocust file build complete.\n"
        print "\tIf you're in your virtualenv, you can now run:\n"
        print "\t\tlocust -f locustLoadTest.py --host=https://{}\n".format(options.host)
        print "\t\tlocust --no-web --clients=50 --hatch-rate=25 -f locustLoadTest.py --host=https://{}\n".format(options.host)
    else:
        print "Compile Error on locustLoadTest.py"


main()
