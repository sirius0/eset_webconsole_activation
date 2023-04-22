import ctypes
import sys
import base64
import os

if len(sys.argv) != 5:
    print("Usage: python3 eset_webconsole_activation.py <username> <password> <ERAServer port> <licence file>")
    sys.exit(1)

source_file = "/opt/eset/RemoteAdministrator/Server/Network.so"
link_path   = "/usr/libexec/Network.so"

try:
    if not os.path.exists(link_path):
        os.symlink(source_file, link_path)
        print(f"Symbolic link created: {link_path} -> {source_file}")
    else:
        print(f"The file or link {link_path} already exists.")

except PermissionError:
    print("Error: Insufficient permission to create the symbolic link. Try running the script as an administrator.")
    sys.exit(1)

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

server_api = ctypes.cdll.LoadLibrary("/opt/eset/RemoteAdministrator/Server/ServerApi.so")

era_init_lib = server_api.era_init_lib
era_init_lib.restype = ctypes.c_int

era_deinit_lib = server_api.era_deinit_lib
era_deinit_lib.restype = None

era_process_request = server_api.era_process_request
era_process_request.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p)]
era_process_request.restype = ctypes.c_int

era_free = server_api.era_free
era_free.argtypes = [ctypes.c_char_p]
era_free.restype = None

result = era_init_lib()

if result:
    print(f"Init lib result: {result}")
    sys.exit(1)

with open(sys.argv[4], 'rb') as file:
    licence_binary_content = file.read()

username = sys.argv[1]
password = sys.argv[2]
port     = sys.argv[3]
licence_base64_str = base64.b64encode(licence_binary_content).decode("utf-8")

api_calls = [
    '{"Era.ServerApi.StartRequest":{}}',
    f'{{"Era.ServerApi.CreateConnectionRequest":{{"host":"127.0.0.1","port":{port}}}}}',
    '{"Era.ServerApi.VerifyUserResponse":{"VerifyResult":true}}',
    f'{{"Era.Common.NetworkMessage.ConsoleApi.SessionManagement.RpcAuthLoginRequest" : {{"username":"{username}", "password":"{password}", "isDomainUser":false, "locale":"en-US"}}}}',
    f'{{"Era.Common.NetworkMessage.ConsoleApi.Licenses.RpcAddPoolByLicenseFileRequest":{{"licenseFile":"{licence_base64_str}"}}}}'
]

for request in api_calls:
    print(f"Executing json: {request}")
    response = ctypes.c_char_p()

    result = era_process_request(request.encode("utf-8"), ctypes.byref(response))

    if response.value:
        print(response.value.decode("utf-8"))

    era_free(response)

era_deinit_lib()
print("Exiting ...")
