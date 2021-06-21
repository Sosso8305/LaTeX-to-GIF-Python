# coding: utf-8

user = "olivier2"

def mon_decorateur(fonction):

    def autre_fonction():
        print ("Action refusée")

    if (user != "olivier"):  
        return autre_fonction

    return fonction 


@mon_decorateur
def do_that():
    print ("Execution des instructions")





