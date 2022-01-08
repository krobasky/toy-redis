def stdout_queue_item(outitem):
    print( "[ {0} ] *** executed stdout_queueble_item ***".format(str(outitem)) )
    return 100;

#def file_queueble_item(i:int):
#    with open("redis_data/f.txt","w+") as f:
#        f.write("executed f")
