# Job finder
## Utilising BeautifulSoup to web scrape a list of companies' career pages

![image](https://github.com/user-attachments/assets/9468ec2d-c3ee-4b4d-b194-4f15512e8527)

This project:
- Pools together information from a list of hard-coded companies
- Pools together jobs already applied for at these certain companies
- Web scrape each companies' career site, and if a certain specified job comes up that hasn't been applied for before, append it to a string
- Once all companies have been cycled through and if there are jobs found, send out an email to my mailbox
- This system is setup on my local computer's task scheduler, to run once at midday every Monday, to keep track of all new jobs while respecting each companies' server as to not throttle them

![image](https://github.com/user-attachments/assets/bfa82ea4-64e2-45e1-ba8b-030ea782396d)
