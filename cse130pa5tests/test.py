import misc
import crack
import sys

KEY="130>>"

def run_test(fun,args,chk,pts):
    try:
        rv=fun(*args)
        print("%s calling %s(%s)... " % \
              (KEY,fun.__name__,",".join([repr(x) for x in args])),rv)
    except Exception, e:
        print("Exception: "+str(e))
        return 0
    else:
        if chk(rv):
            print("Good")
            return pts
        else:
            print("Wrong")
            return 0

def chk_val(x):
    return lambda y: x==y

def chk_flt(x):
    return lambda y: abs(x-y)<1e-8

def chk_dict(qry,rslt,sz):
    return lambda d: len(d)==sz and qry in d and d[qry]==rslt

def chk_set(qry,sz):
    return lambda d: len(d)==sz and qry in d

def chk_file(fn):
    return lambda d: sys.stdout.write("\nSee file \"%s\"\n" % fn) or True

def run_tests(tests):
    score=0
    total=0
    for (fun,args,chk,pts) in tests:
        score+=run_test(fun,args,chk,pts)
        total+=pts
    return (score,total)

def run_all_tests():
    globals={}
    return run_tests([
        #problem 1
        (misc.closest_to,[[2,4,8,9],7],chk_val(8),1),
        (misc.closest_to,[[2,4,8,9],5],chk_val(4),1),
        (misc.closest_to,[[2,0,-21,8,9],-20],chk_val(-21),1), 
        (misc.closest_to,[[0,-21,8,9],0],chk_val(0),1), 
        (misc.closest_to,[[-999,999,-1200],0],chk_val(-999),1), 
        (misc.closest_to,[[1,-1,8,9],0],chk_val(1),1), 
        (misc.closest_to,[[],0],chk_val(None),1),
         
        (misc.make_dict,[["foo","baz"],["bar","blah"]],chk_val({'foo': 'bar', 'baz': 'blah'}),1),
        (misc.make_dict,[["key1","key2", "key3"],["val1","val2", "val3"]],chk_val({'key1': 'val1', 'key2': 'val2', 'key3': 'val3'}),1),
        (misc.make_dict,[["key1","key2", "key1"],["val1","val2", "val3"]],chk_val({'key1': 'val3', 'key2': 'val2'}),1),
        (misc.make_dict,[[1],[100]],chk_val({1:100}),1),
        (misc.make_dict,[[],[]],chk_val({}),1),

        (misc.word_count,["news.txt"],chk_dict("edu",2,407),1),
        (misc.word_count,["news.txt"],chk_dict("results",1,407),1),
        (misc.word_count,["news.txt"],chk_dict("four",1,407),1),
        (misc.word_count,["empty"],chk_val({}),1),

        #problem 2
        (crack.load_words,["words",r"^[A-Z].{2}$"],chk_set("Tim",3893),1),
        (crack.load_words,["words",r"^xYx.*$"],chk_val([]),1),
        # (crack.load_words,["words",r""],chk_val([]),1),


        (lambda x: set(crack.transform_reverse(x)),["Moose"],chk_val(set(['Moose','esooM'])),1),
        (lambda x: set(crack.transform_reverse(x)),["rAPHAEL"],chk_val(set(['rAPHAEL','LEAHPAr'])),1),
        (lambda x: set(crack.transform_reverse(x)),["hello world"],chk_val(set(['hello world','dlrow olleh'])),1),
     
        (lambda x: set(crack.transform_capitalize(x)),["foo"],chk_val(set(['foo', 'Foo', 'fOo', 'FOo', 'foO', 'FoO', 'fOO', 'FOO'])),1),
        (lambda x: set(crack.transform_capitalize(x)),["12aB"],chk_val(set(['12ab', '12aB', '12Ab', '12AB'])),1),
        (lambda x: set(crack.transform_capitalize(x)),["he1o"],chk_val(set(['he1o', 'he1O', 'hE1o', 'hE1O', 'He1o', 'He1O', 'HE1o', 'HE1O'])),1),
        
        (lambda x: set(crack.transform_digits(x)),["Bow"],chk_val(set(['Bow', 'B0w', '6ow', '60w', '8ow', '80w'])),1),
        (lambda x: set(crack.transform_digits(x)),["bow"],chk_val(set(['bow', 'b0w', '6ow', '60w', '8ow', '80w'])),1),
        (lambda x: set(crack.transform_digits(x)),["foo"],chk_val(set(['foo', 'fo0', 'f0o', 'f00'])),1),
        (lambda x: set(crack.transform_digits(x)),["greq"],chk_val(set(['greq', 'gre9', 'gr3q', 'gr39','9req', '9re9', '9r3q', '9r39'])),1),
        (lambda x: set(crack.transform_digits(x)),["la zo"],chk_val(set(['la zo', 'la z0', 'la 2o', 'la 20','l4 zo', 'l4 z0', 'l4 2o', 'l4 20',
            '1a zo', '1a z0', '1a 2o', '1a 20','14 zo', '14 z0', '14 2o', '14 20'])),1),

        (crack.check_pass,["asarta","IqAFDoIjL2cDs"],chk_val(True),1),
        (crack.check_pass,["foo","AAbcdbcdzyxzy"],chk_val(False),1),
        (lambda x: crack.load_passwd(x)[3],["passwd"],chk_dict("GECOS",'Forkland Maskins',7),1),
        (crack.crack_pass_file,["passwd","words","passwd-out.txt"],chk_file("passwd-out.txt"),1),
        
        ])

(s,t)=run_all_tests()
print("%s Results: (%d/%d)" % (KEY,s,t))
print("%s Compiled" % KEY)
    
