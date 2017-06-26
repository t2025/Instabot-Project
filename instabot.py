#importing keys from keys.py
from keys import base_url,APP_ACCESS_TOKEN
#importing textblob
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
#importing requests
import requests
#importing urllib
import urllib
loc=[]
'''
Function declaration to get your own account information
'''
def self_info():
  request_url = (base_url + '/users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
  print 'Requesting info for:' + request_url
  my_info = requests.get(request_url).json()
  print 'My info is:\n', my_info
  print 'My Followers: %s\n' % (my_info['data']['counts']['followed_by'])
  print 'People I Follow: %s\n' % (my_info['data']['counts']['follows'])
  print 'No. of posts: %s\n' % (my_info['data']['counts']['media'])

'''
Method to get User Id by providing instagram username
'''
def get_user_id(insta_username):
    request_url = (base_url + '/users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print'Requesting info for:' + request_url
    search_results = requests.get(request_url).json()
    if search_results['meta']['code'] == 200:
        if len(search_results['data']):
            return search_results['data'][0]['id']
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 was received!'
        return None

'''
Method to get user information by providing username providing user_name
'''
def get_user_info(insta_username):
      user_id = get_user_id(insta_username)
      if user_id == None:
          print 'User does not exist!'
          exit()
      request_url = (base_url + '/users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
      print 'GET request url : %s' % (request_url)
      user_info = requests.get(request_url).json()

      if user_info['meta']['code'] == 200:
          if len(user_info['data']):
              print 'Username: %s' % (user_info['data']['username'])
              print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
              print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
              print 'No. of posts: %s' % (user_info['data']['counts']['media'])
          else:
              print 'There is no data for this user!'
      else:
          print 'Status code other than 200 received!'
'''
Function to download pictures of own post
'''
def get_own_post():
      request_url = (base_url + '/users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
      print 'GET request url : %s' % (request_url)
      own_media = requests.get(request_url).json()

      if own_media['meta']['code'] == 200:
          if len(own_media['data']):
              #Fetching the most recent media
              image_name = own_media['data'][0]['id'] + '.jpeg'
              image_url = own_media['data'][0]['images']['standard_resolution']['url']
              urllib.urlretrieve(image_url, image_name)
              print 'Your image has been downloaded!'
          else:
              print 'Post does not exist!'
      else:
          print 'Status code other than 200 received!'
'''
Function for downloading a user's posts
'''
def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (base_url + '/users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            # Fetching the most recent media
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'

'''
Method to get posts liked by user
'''
def get_user_liked_post():


    request_url= (base_url+'/users/self/media/liked?access_token=%s')%( APP_ACCESS_TOKEN)
    user_liked=requests.get(request_url).json()


    if user_liked['meta']['code']==200:
        if len (user_liked['data']):
            image_name = user_liked['data'][0]['id'] + '.jpeg'
            image_url = user_liked['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url,image_name)
            print "Liked media has been downloaded!"
        else:
            print "Could not find posts"
    else:
        print 'Status code other than 200 received'
'''
Method to get post Id of a user by providing username
'''
def get_post_id(insta_username):
    user_id=get_user_id(insta_username)
    request_url=(base_url +'/users/%s/media/recent/?access_token=%s') % (user_id,APP_ACCESS_TOKEN)
    print 'GET request url: %s'%(request_url)
    user_media=requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):

            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()


'''
Method to like a post of a user
 '''

def like_a_post(insta_username):
    media_id=get_post_id(insta_username)
    request_url=(base_url+'/media/%s/likes')%media_id
    payload={"access_token":APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like=requests.post(request_url,payload).json()
    if post_a_like['meta']['code']==200:
        print "You have successfully liked a post"
    else:
        print "Sorry ! the like was unsuccessful"
        exit()

'''
Function to get a comment list
'''
def get_comment_list(insta_username):
    media_id=get_post_id(insta_username)
    request_url=(base_url+'/media/%s/comments?access_token=%s')%(media_id,APP_ACCESS_TOKEN)
    print'GET %s'%request_url
    comment_list=requests.get(request_url).json()
    if comment_list['meta']['code']==200:
        for x in range(0, len(comment_list['data'])):

            print comment_list['data'][x]['text']
            print"\n Comments list successfully shown"
    else:
         print "No comments"


'''
Function to post a comment on a  user's post using username
'''
def post_a_comment(insta_username):
    media_id=get_post_id(insta_username)
    comment_text=raw_input("Your comment:")

    request_url=(base_url+"/media/%s/comments")%(media_id)
    payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_text}
    post_a_comment=requests.post(request_url,payload).json()
    print 'POST request url : %s' % (request_url)
    if post_a_comment['meta']['code']==200:
        print "Thanks! Your comment has been posted successfully"

    else:
        print "Failed! Comment has not been posted.Please try again"
        exit()


'''
Function to delete neagtive comment from a user's post
'''
def delete_negative_comment(insta_username):
     media_id=get_post_id(insta_username)
     request_url=(base_url+'/media/%s/comments/?access_token=%s')%(media_id,APP_ACCESS_TOKEN)
     print 'GET request url : %s' % (request_url)
     comment_info=requests.get(request_url).json()
     if comment_info['meta']['code']==200:
         for x in range(0, len(comment_info['data'])):
             comment_id = comment_info['data'][x]['id']
             comment_text = comment_info['data'][x]['text']
             #Naive implementation to delete negative comments
             blob=TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
             if(blob.sentiment.p_neg>blob.sentiment.p_pos):
                 print "It's a negative comment: %s"%comment_text
                 delete_url=(base_url+'media/%s/comments/%s/?access_token=%s')%APP_ACCESS_TOKEN
                 delete_info=requests.delete(delete_url).json()
                 if delete_info['meta']['code']==200:
                     print "Comment deleted successfully"

                 else:
                     print "Sorry we couldn't delete this comment! Try Again"
             else:
                 print "Positive comment"
     else:
      print "Status code other than 200 received"
'''
Method to get location
'''
def get_location():
    lat=raw_input("Enter latitude coordiante of the location")
    lat=float(lat)
    lon=raw_input("Enter longitude coordinate of the location")
    lon=float(lon)
    request_url=(base_url+'/locations/search?lat=%.2f&lng=%.2f&access_token=%s')%(lat,lon,APP_ACCESS_TOKEN)
    print 'GET %s'%request_url
    location=requests.get(request_url).json()
    if location['meta']['code']==200:
        if len(location['data']):
         for x in range(0,len(location['data'])):
            print location['data'][x]['id']+" "+location['data'][x]['name']
            id= location['data'][x]['id']
            id=int(id)
            loc.append(id)
         print loc

    else:
        print "Meta code other than 200 found"

'''
Method to get alerts about natural calamities
'''
def natural_calamities():
 location_id=get_location()
 tag_name=raw_input("Enter the tag for searching posts")
 if tag_name=="earthquake" or tag_name=="flood" or tag_name=="drought"or tag_name=="landslide" or tag_name=="drought"or tag_name=="cyclone" or tag_name=="tsunami":
        request_url=(base_url+'/tags/%s/media/recent?access_token=%s' )%(tag_name,APP_ACCESS_TOKEN)
        print 'GET %s'%request_url
        disaster=requests.get(request_url).json()
        #print disaster
        if disaster['meta']['code']==200:
         if len(disaster['data']):
            for x in range(0,len(disaster['data'])):
                print disaster['data'][x]['location']['id']
                print disaster['data'][x]['location']['name']
                loc_id=disaster['data'][x]['location']['id']
                for x in range(0,len(loc)):
                  if loc_id==loc[x]:
                      print "Matched!"
                      for x in range(0, len(disaster['data'])):
                          print disaster['data'][x]['link']
                          print "image found"
                      break

        else:
            "image not found"
 else:
        print "Tags inserted doesnot match "
'''
 Method to inialize bot
'''
def start_bot():
    while True:
        print "\n"
        print "Hello!Welcome to InstaBot"
        print "What would you like to do?"
        print "a.Get Your own details\n"
        print "b.Get details of another user by username\n"
        print "c.Get your own recent post\n"
        print "d.Get the recent post of a user by username\n"
        print "e.Get liked posts of user\n"
        print "f.Like the recent post of a user\n"
        print "g.Get a list of comments on the recent post of a user\n"
        print "h.Make a comment on the recent post of a user\n"
        print "i.Delete negative comments from the recent post of a user\n"
        print "j.Information about natural calamities\n"
        print "k.exit"

        choice = raw_input("Enter you choice: ")
        if choice == "a":
            self_info()
        elif choice == "b":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_id(insta_username)
            get_user_info(insta_username)
        elif choice == "c":
            get_own_post()
        elif choice == "d":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)
        elif choice == "e":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_liked_post()
        elif choice == "f":
            insta_username = raw_input("Enter the username of the user: ")
            like_a_post(insta_username)
        elif choice == "g":
            insta_username = raw_input("Enter the username of the user: ")
            get_comment_list(insta_username)
        elif choice == "h":
            insta_username = raw_input("Enter the username of the user: ")
            post_a_comment(insta_username)
        elif choice == "i":
            insta_username = raw_input("Enter the username of the user: ")
            delete_negative_comment(insta_username)
        elif choice=="j":
            natural_calamities()
        elif choice == "k":
            exit()
        else:
            print "wrong choice"


start_bot()






















