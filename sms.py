# import twilio.twiml
# from twilio.rest import TwilioRestClient
# from tokens import TWILIO_ID, TWILIO_TOKEN, TWILIO_NUM

# client = TwilioRestClient(TWILIO_ID, TWILIO_TOKEN)

# #---------------------------------------------
# # threading initialization
# # --------------------------------------------

# import Queue
# # import threading
# import time
# from multiprocessing import Pool

# queue = Queue.Queue()

# messages = []
# messages.append( { "phone": "+13038082955", "body" : "" } )
# messages.append( { "phone": "+15056909353", "body" : "" } )

# def sendMessage(message):

# 		print "send"
		
# 		current_time = str(time.time())
# 		message["body"] = current_time
		
# 		errors = client.sms.messages.create(to=message["phone"], from_=TWILIO_NUM, body=message["body"])
# 		print errors
# 		return current_time

# def addMessageTask(pool, message):

# 		result = pool.apply_async(sendMessage, [message])  

# 		print result.get()




# if __name__ == '__main__':
#     pool = Pool(processes=100)              # start 100 worker processes
    
#     addMessageTask(pool,messages[0])
#     # addMessageTask(pool,messages[1])

#     print "here"




# class ThreadMessage(threading.Thread):
# 		''' class to handle threaded SMS sending '''

# 		def __init__(self, queue):
# 				threading.Thread.__init__(self)
# 				self.queue = queue

# 		def run(self):
# 		    while True:
# 			      # grabs a message from queue
# 			      message = self.queue.get()

# 			      message["body"] = str(time.time())
			      
# 			      client.sms.messages.create(to=message["phone"], from_=TWILIO_NUM, body=message["body"])

# 			      #signals to queue job is done
# 			      self.queue.task_done()

# start = time.time()

# def main():

# 		# spawn a pool of threads, and pass them queue instance 
# 		for i in range(100):
# 				t = ThreadMessage(queue)
# 				t.setDaemon(True)
# 				t.start()

# 		# populate queue with data   
# 		for message in messages:
# 				queue.put(message)	

# 	  # wait on the queue until everything has been processed     
# 		# queue.join()

# main()

# print "Elapsed Time: %s" % (time.time() - start)
