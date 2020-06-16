# cf tool

import random
import subprocess
import sys
import os
import time
import timeit
import requests
import urllib.request
from bs4 import BeautifulSoup
from termcolor import colored


templatefilepath = 'C:/Users/Anurag Shrivastava/PycharmProjects/cf-tool/temp.txt'

#function for parsing the problem
def problem_parse(problem_url,path):
    response = urllib.request.urlopen(problem_url)
    page = response.read()
    soup = BeautifulSoup(page,'html.parser')
    temp_in = soup.find_all('div',class_='input')
    temp_out = soup.find_all('div',class_='output')

    br_filter = lambda x: x.find('br') == -1
    get_raw = lambda x: '\n'.join(list(filter(br_filter, x)))

    err_msg = 'Error: Sample input/output not found.'
    io = soup.find("div", class_="sample-test")
    if io is None:
        print(colored(err_msg,"red"))
        return
    inputs = io.find_all("div", class_="input")
    outputs = io.find_all("div", class_="output")

    raw_inputs = [get_raw(e.pre.contents) + '\n' for e in inputs]
    raw_outputs = [get_raw(e.pre.contents) + '\n' for e in outputs]
    if os.path.exists(path):
        os.system('rm -r'+ path)
    path = path.replace(r'\\','/')
    os.mkdir(path)

    i = 1
    for x,y in zip(raw_inputs,raw_outputs):
        if_name = path + '/in'+ str(i) + '.txt'
        of_name = path + '/out' + str(i) + '.txt'
        with open(if_name,'w') as f:
            f.write(x)
        with open(of_name,'w') as f:
            f.write(y)
        i += 1

def create_code(path,problem_id):
    with open(templatefilepath, 'r') as temp:
        code = str(temp.read())
        create = False
        if os.path.exists(path):
            while True:
                print('file already exists... do you want to Remove' + path + '? (y/n)')
                res = input().lower()
                if res == 'y' or len(res.strip())==0:
                    print('Removing...')
                    os.system('rm '+ path)
                    create = True
                    break
                elif res == 'n':
                    break
        else:
           create = True
        if create:
            print("creating",problem_id.lower())
            with open(path,'w') as f:
                f.write(code)






def run():
    filename = args[1]
    full = filename
    if not filename.endswith('.cpp'):
        full = filename + '.cpp'

    compile_cmd = "g++ -std=c++14 " + str(full)
    print(colored('compiling  '+ str(full) + '...','cyan'))
    try:
        subprocess.run(
            compile_cmd,
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stdout,
            bufsize=1,
            universal_newlines=True
        )
    except:
        return



def test():
    run()
    filename = args[1].split(".")[0]
    fpath = cd + "/io"
    if not os.path.exists(fpath):
        print(colored("Error: No IO files found","red"))
        return

    count = int(len(os.listdir(fpath))/2)
    if count==0:
        print(colored("Error: No IO files found","red"))
        return
    for i in range(1,count+1):
        ifile = fpath + '/in'+ str(i) +".txt"
        ofile = fpath + '/out' + str(i)+".txt"

        if (not os.path.exists(ifile)) or (not os.path.exists(ofile)):
            print(colored("Error: I/O file doesn't exist.","red"))
            continue

        start = timeit.default_timer()
        exec_cmd = "a.exe"
        print(colored("Executing code...", "cyan"))
        ctest = subprocess.run(
            exec_cmd,
            stdin=open(ifile, 'r'),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=True
        )
        stop = timeit.default_timer()

        expected = ''
        output_ = ctest.stdout
        input_ = ''


        with open(ofile,'r') as f:
            expected = str(f.read())
        with open(ifile,'r') as f:
            input_ = str(f.read())


        s = output_.strip().split('\n')
        e = expected.strip().split('\n')

        verdict = True
        line = ''
        if len(s) != len(e):
            verdict = False
            line = 'Difference in number of lines'

        else:
            i=1
            for x,y in zip(s,e):
                if x.strip() != y.strip():
                    verdict = False
                    line = 'Line ' + str(i) + ': '
                    break
                i+=1

        if verdict:
            print(colored('PASSED','green'))
            print('({0:2f}s'.format(stop-start))
        else:
            print(colored("FAILED"))
            print(line)
            print(input_.strip())
            print("----------------------------------------------------------------")
            print(output_.strip())
            print("----------------------------------------------------------------")
            print(expected.strip())
            print("----------------------------------------------------------------")




def split_problem_id(problem_id):
    print(problem_id[:4])
    print(problem_id[4:])
    return [problem_id[0:4], problem_id[4:]]



def gen(code=True):
    if len(args) == 1:
        return
    print(colored("Hello this part is working fine","cyan"))
    contest_id,problem_id = split_problem_id(args[1])
    contest_url = 'https://codeforces.com/contest/' + contest_id

    path=cd + '/' +contest_id
    if os.path.exists(path):
        os.system('rm -r'+ path)
    os.mkdir(path)
    print(contest_url)
    if len(str(args[1]))!=4:
        print("hhhhh")
        problem_id = problem_id.upper()
        problem_url = contest_url + "/problem/" + problem_id.upper()
        problem_parse(problem_url,cd + '/' + str(contest_id) + '/' + problem_id.lower() + '/io')
        if code:
            create_code(problem_id)
        sys.exit(0)

    #parse the whole contest
    print('parsing the contest',contest_url)
    response = urllib.request.urlopen(contest_url)
    page = response.read()
    soup = BeautifulSoup(page, 'html.parser')
    # print(soup)
    table = soup.find_all('table',class_='problems')
    # print(table)
    trs = table[0].find_all('tr')

    for tr in trs:
        td = tr.find_all('td')
        if len(td)==0:
            continue
        td = td[0]
        problem_id = td.a.get_text().strip()
        problem_url = contest_url + "/problem/" + problem_id
        problem_path = path + '/' + problem_id.lower()

        if os.path.exists(problem_path):
            os.system('rm -r' + problem_path)
        os.mkdir(problem_path )

        problem_path = problem_path.replace(r'\\', '/')
        problem_parse(problem_url,problem_path + '/io')
        if code:
            create_code(problem_path+ '/' + problem_id.lower() + '.cpp',problem_id)




if __name__ == '__main__':
    os.system('color')
    print(colored("Hemlo","red"))
    args = sys.argv[1:]
    #getting the current working directory
    cd = os.getcwd()
    cd = cd.replace(r"\\","/")

    #taking careof any '/' at the end of the current dir name
    if cd[-1] == '/':
        cd = cd[:-1]
    if args[0] == 'run':
        run()
    elif args[0] == 'test':
        test()
    elif args[0] == 'parse':
        gen(code = False)
    elif args[0] == 'gen':
        gen()
    else:
        print(colored('Wrong Arguments','red'))

