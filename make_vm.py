import subprocess

def make_vm(name):
    
    # make directory    
    dir = '/var/kvm/disk/' + name + '/'
    command = 'mkdir ' + dir + ';'

    # make kickstart file
    # output = """
#"""
    # filename = 'kickstart.cfg'
    # f = open(dir + filename, 'w')
    # f.write(output)
    # f.close()

    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)    
    proc_stdout = process.communicate()[0].strip()
    print proc_stdout

make_vm('centos7_2')
