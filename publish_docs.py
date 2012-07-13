#!/usr/bin/env python
import subprocess

def call(args, shell=False):
    cmd = ' '.join(args)
    print("== attempting == %s =="%cmd)
    if subprocess.call(args, shell=shell):
        print("== !problem!  == %s ==" % cmd)
        exit(1)
    print("== done       == %s ==" % cmd)
    print

call(['git', 'checkout', 'master'])
call(['make', '-C', 'docs', 'html'])
call(['rm', '-rf', '/tmp/docs_html'])
call(['cp', '-R', 'docs/_build/html', '/tmp/docs_html'])
call(['git', 'checkout', 'gh-pages'])
call(['rm', '-rf', '/Users/prior/github/sanetime/*'], True)  # wtf!!  i can't do a rm -rf * for some reason
call(['cp', '-R', '/tmp/docs_html/*', '.'])
call(['git', 'add', '.'])
#call(['git', 'commit', '-a', '-v'])
#call(['git', 'push'])
#call(['git', 'checkout', 'master'])

