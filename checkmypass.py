import requests
import hashlib
import sys

def request_api_data(query_char):
    url  = 'https://api.pwnedpasswords.com/range/' + query_char

    res= requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}')
    return res

def get_password_leaks_count(hashes, hash_to_check):
    hashes =  (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0
        #print(h, count)

def pwned_api_check(password):
    #check if password exists in api responsen 
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5 = sha1password[:5]
    tail= sha1password[5:]
    response = request_api_data(first5)
    return get_password_leaks_count(response, tail)


def main(args):
    for password in args:
      count = pwned_api_check(password)
      if count:
          print(f'{password} was found {count} times') 
      else: print(f'{password} was not found, carry on!') 
if __name__== '__main__':
    sys.exit(main(sys.argv[1:]))