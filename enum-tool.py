import sublist3r
from datetime import datetime

# Define target domain
domain = input("Enter domain: ")

# Run sublist3r and store the results in a variable
subdomains = sublist3r.main(domain, enable_bruteforce=False, engines=None, threads=2, savefile=None, ports=None, silent=True, verbose=False)

if subdomains:

    filename = f"{domain}.txt"
    
    # Join subdomains into a single string
    body = "\n".join(subdomains)
    
    # Write the subdomains to the file
    with open(filename, "w") as file:
        file.write(body)
    
    print(f"Subdomains saved to {filename}")

    # Execute another script if needed
    with open('urllinks.py') as file:
        exec(file.read())

else:
    print('Scan failed')
