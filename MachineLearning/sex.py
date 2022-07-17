import requests
import os
import json
import utils

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'

def get_user_information(users, driver=None, headless=True):
    """ get user information if the "from_account" argument is specified """

    driver = utils.init_driver(headless=headless)

    users_info = {}

    for i, user in enumerate(users) :

        log_user_page(user, driver)

        if user is not None:

            try:
                following = driver.find_element_by_xpath(
                    '//a[contains(@href,"/following")]/span[1]/span[1]').text
                followers = driver.find_element_by_xpath(
                    '//a[contains(@href,"/followers")]/span[1]/span[1]').text
            except Exception as e:
                #print(e)
                return

            try:
                element = driver.find_element_by_xpath('//div[contains(@data-testid,"UserProfileHeader_Items")]//a[1]')
                website = element.get_attribute("href")
            except Exception as e:
                #print(e)
                website = ""

            try:
                desc = driver.find_element_by_xpath('//div[contains(@data-testid,"UserDescription")]').text
            except Exception as e:
                #print(e)
                desc = ""
            a=0
            try:
                join_date = driver.find_element_by_xpath(
                    '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[3]').text
                birthday = driver.find_element_by_xpath(
                    '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[2]').text
                location = driver.find_element_by_xpath(
                    '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[1]').text
            except Exception as e: 
                #print(e)
                try :
                    join_date = driver.find_element_by_xpath(
                        '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[2]').text
                    span1 = driver.find_element_by_xpath(
                        '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[1]').text
                    if hasNumbers(span1):
                        birthday = span1
                        location = ""
                    else : 
                        location = span1
                        birthday = ""
                except Exception as e: 
                    #print(e)
                    try : 
                        join_date = driver.find_element_by_xpath(
                            '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[1]').text
                        birthday = ""
                        location = ""
                    except Exception as e: 
                        #print(e)
                        join_date = ""
                        birthday = ""
                        location = ""
            print("--------------- " + user + " information : ---------------")
            print("Following : ", following)
            print("Followers : ", followers)
            print("Location : ", location)
            print("Join date : ", join_date)
            print("Birth date : ", birthday)
            print("Description : ", desc)
            print("Website : ", website)
            users_info[user] = [following, followers, join_date, birthday, location, website, desc]

            if i == len(users)-1 :
                driver.close()   
                return users_info
        else:
            print("You must specify the user")
            continue

def auth():
    return os.environ.get("BEARER_TOKEN")

def create_url(ids):
    # Specify the usernames that you want to lookup below
    # You can enter up to 100 comma-separated values.
    usernames = "usernames=TwitterDev,TwitterAPI"
    user_fields = "user.fields=description,created_at"
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username, verified, and withheld
    url = "https://api.twitter.com/2/users?ids={}&{}".format(ids, user_fields)
    return url

def create_url3(names):
    # Specify the usernames that you want to lookup below
    # You can enter up to 100 comma-separated values.
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username, verified, and withheld
    url = "https://api.twitter.com/2/users/by?usernames={}".format(names)
    return url

def create_url2(ids):
    usernames = "usernames=TwitterDev,TwitterAPI"
    tweet_fields = "tweet.fields=public_metrics,text"
    url = "https://api.twitter.com/2/tweets?ids={}&{}".format(ids, tweet_fields)
    
    return url

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    #print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

bearer_token = "AAAAAAAAAAAAAAAAAAAAAJGvLAEAAAAAc3bclYbPxNXFLaY%2FKIsTBKjn3eg%3DvearLoCZU7bQSHKZ77rKas66UynuNR0mYM89BdUSda3CwqsJLb"

def main_test(ids):
    url = create_url(ids)
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(url, headers)
    json_array = json_response["data"]
    return json_array
    #print(json.dumps(json_response, indent=4, sort_keys=True))

def main_test2(ids):
    url = create_url3(ids)
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(url, headers)
    json_array = json_response["data"]
    
    return json_array
    #print(json.dumps(json_response, indent=4, sort_keys=True))

#if __name__ == "__main__":
#    main()

#lst = 'bolanascostas', 'esportenews', 'CBF_Futebol', 'revistasuper', 'CantadasCharlie', 'SporTV', 'renato_gaucho', 'multishow', 'BrazilWorldTV', 'loveletdie', 'sabrina_sato', 'daniredetv', 'geglobo', 'TO_DE_OLHO', 'sitevagalume', 'MixtapeOficial', 'hevo84', 'CassesOficial', 'jorgeiggor', 'vitorsergio', 'richstyles', 'espn', 'weboxygen', 'pcfromzero', 'marymagdalan', 'StarzUncut',  'SteveNash', 'yelyahwilliams', 'marca', 'ItsMoneybags', 'TextArtPrint', 'serenawilliams', 'justdemi', 'NBA', 'ashleytisdale', 'PerezHilton', 'ladygaga', 'jtimberlake', 'taylorswift13', 'MandyJiroux', 'mitchelmusso', 'billyraycyrus', 'EmilyOsment', 'BrandiCyrus', 'jonasbrothers', 'ddlovato', 'pamfoundation', 'bigeyeonsports', 'montanhadaniel', 'bixajacare', 'fabiannesangalo'
#main_test2(lst)
