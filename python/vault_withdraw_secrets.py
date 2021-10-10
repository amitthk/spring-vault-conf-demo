import sys, os, json, time
import requests

PATH = os.path.dirname(os.path.abspath(__file__))
VALUE_FILE = os.path.join(PATH,'.env')
CONST_RETRY_COUNT = 5

def ParseBoolean (b):
    # ...
    if len(b) < 1:
        raise ValueError ('Cannot parse empty string into boolean.')
    b = b[0].lower()
    if b == 't' or b == 'true' or b == 'y' or b == 'yes' or b == '1':
        return True
    if b == 'f' or b == 'alse' or b == 'n' or b == 'no' or b == '0':
        return False
    raise ValueError ('Cannot parse string into boolean.')

def write_to_file(file_name,f_output):
    with open(file_name,'w') as f:
        f.write(f_output)

def vault_read_secret(request_url,should_decode=False,token=None):
    if token is not None:
        headers = {'content-type':'application/json', 'X-Vault-Token': token}
    retry_count = CONST_RETRY_COUNT
    response = requests.get(request_url,headers=headers)
    while retry_count >= 0:
        time.sleep(3) # wait 3 seconds then try again
        try:
            #print('response: '+str(response.json()))
            foutput = ''
            for field_name in response.json()['data']['data']:
                value = str(response.json()['data']['data'][field_name])
                if should_decode is True:
                    value = value.decode('base64')
                foutput = foutput + field_name + "=" + value + "\n"

                write_to_file(file_name=VALUE_FILE,f_output=foutput)
            break
        except Exception as exc:
            retry_count-=1
            print ("File {} not ready, trying again. Retry count: {}".format(VALUE_FILE, retry_count))
            if(retry_count<0):
                print("Failed to process your request. Error: " + exc)

def main():
    if len(sys.argv)<5:
        print('Usage vault_withdraw_secret.py <vault_addr> <vault_token> <key_name> <base64decode? true/false>')
        sys.exit()
    vault_addr = sys.argv[1]
    vault_token = sys.argv[2]
    secret_key_name = sys.argv[3]
    should_decode = ParseBoolean(sys.argv[4])
    read_secret_url = '{}/v1/{}'.format(vault_addr,secret_key_name)
    vault_read_secret(request_url=read_secret_url,should_decode=should_decode, token=vault_token)

if __name__=="__main__":
    main()
